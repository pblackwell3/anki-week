#!/usr/bin/env python3
"""Validate a practice-exam-builder exam.json against the data contract.

Checks structure and blueprint arithmetic — the invariants a machine can settle.
It cannot tell you whether a question is clinically sound or actually supported by
the slide it cites; that is the manual audit in step 5 of the skill.

    python validate_exam.py exam.json              # partial bank, mid-generation
    python validate_exam.py exam.json --complete   # full-bank invariants, before launch
    python validate_exam.py exam.json --json       # machine-readable

Exit codes: 0 = clean, 1 = errors found, 2 = file unreadable or unparseable.
Stdlib only, Python 3.8+.
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict

SCHEMA_VERSION = "1.0"
LETTERS = ["A", "B", "C", "D", "E"]
REQUIRED_TOP = [
    "schema_version", "exam_id", "exam_name", "exam_date",
    "total_questions", "blueprint", "sources", "source_map", "questions",
]
SOURCE_TYPES = {
    "lecture_slides", "review_slides", "faculty_questions",
    "syllabus", "notes", "other",
}
DIFFICULTIES = {"easy", "moderate", "hard"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WS_RE = re.compile(r"\s+")
DISMISSAL_RE = re.compile(
    r"\b(not\s+source[-\s]?supported"
    r"|does\s+not\s+match"
    r"|is\s+(?:simply\s+)?incorrect"
    r"|is\s+wrong"
    r"|not\s+supported\s+by\s+the\s+sources?"
    r"|not\s+the\s+best\s+answer"
    r"|unrelated\s+to\s+(?:the\s+)?(?:vignette|stem|question))\b",
    re.IGNORECASE,
)

# Target cognitive mix (step 4), and how far off it may drift before a warning.
TARGET_MIX = {1: 0.20, 2: 0.50, 3: 0.30}
MIX_TOLERANCE = 0.10
MIN_HIGHER_ORDER = 0.80


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, message):
        self.errors.append({"where": where, "message": message})

    def warn(self, where, message):
        self.warnings.append({"where": where, "message": message})


def norm(value):
    """Lowercase, collapse whitespace, drop a trailing period — for comparing text."""
    if not isinstance(value, str):
        return ""
    return WS_RE.sub(" ", value).strip().lower().rstrip(".")


def is_text(value):
    return isinstance(value, str) and value.strip() != ""


def check_top_level(exam, rep):
    for key in REQUIRED_TOP:
        if key not in exam:
            rep.error("exam", "missing required key `%s`" % key)

    if exam.get("schema_version") != SCHEMA_VERSION:
        rep.warn("exam", "schema_version is %r; this validator targets %r"
                 % (exam.get("schema_version"), SCHEMA_VERSION))

    for key in ("exam_id", "exam_name"):
        if key in exam and not is_text(exam.get(key)):
            rep.error("exam", "`%s` must be a non-empty string" % key)

    date = exam.get("exam_date")
    if date is not None and not (isinstance(date, str) and DATE_RE.match(date)):
        rep.error("exam", "`exam_date` must be YYYY-MM-DD, got %r" % (date,))

    total = exam.get("total_questions")
    if not isinstance(total, int) or isinstance(total, bool) or total <= 0:
        rep.error("exam", "`total_questions` must be a positive integer, got %r" % (total,))


def check_blueprint(exam, rep):
    """The blueprint gate (step 2), in machine-readable form."""
    blueprint = exam.get("blueprint")
    counts = {}
    if not isinstance(blueprint, list) or not blueprint:
        rep.error("blueprint", "`blueprint` must be a non-empty array")
        return counts

    seen = set()
    for i, entry in enumerate(blueprint):
        where = "blueprint[%d]" % i
        if not isinstance(entry, dict):
            rep.error(where, "entry must be an object")
            continue
        faculty = entry.get("faculty")
        if not is_text(faculty):
            rep.error(where, "`faculty` must be a non-empty string")
            continue
        if faculty in seen:
            rep.error(where, "duplicate faculty %r" % faculty)
            continue
        seen.add(faculty)

        count = entry.get("count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            rep.error(where, "`count` for %r must be a non-negative integer, got %r"
                      % (faculty, count))
            continue
        if count == 0:
            rep.warn(where, "%r is allocated 0 questions" % faculty)
        counts[faculty] = count

    total = exam.get("total_questions")
    if counts and isinstance(total, int) and not isinstance(total, bool):
        actual = sum(counts.values())
        if actual != total:
            rep.error(
                "blueprint",
                "BLUEPRINT GATE: faculty counts sum to %d, requested total is %d "
                "(difference %+d). Stop and ask for a corrected distribution — do not "
                "redistribute counts yourself." % (actual, total, actual - total),
            )
    return counts


def check_sources(exam, rep):
    sources = exam.get("sources")
    ids = set()
    if not isinstance(sources, list):
        rep.error("sources", "`sources` must be an array")
        return ids
    if not sources:
        rep.warn("sources", "no sources recorded — every question should trace to a material")

    for i, src in enumerate(sources):
        where = "sources[%d]" % i
        if not isinstance(src, dict):
            rep.error(where, "entry must be an object")
            continue
        sid = src.get("source_id")
        if not is_text(sid):
            rep.error(where, "`source_id` must be a non-empty string")
            continue
        if sid in ids:
            rep.error(where, "duplicate source_id %r" % sid)
        ids.add(sid)
        if not is_text(src.get("title")):
            rep.error(where, "`title` must be a non-empty string (source_id %r)" % sid)
        stype = src.get("type")
        if stype is not None and stype not in SOURCE_TYPES:
            rep.warn(where, "unknown source type %r (expected one of %s)"
                     % (stype, ", ".join(sorted(SOURCE_TYPES))))
    return ids


def check_source_map(exam, rep, faculty_counts, source_ids):
    source_map = exam.get("source_map")
    if not isinstance(source_map, list):
        rep.error("source_map", "`source_map` must be an array")
        return
    if not source_map:
        rep.warn("source_map", "empty — build faculty → lecture → objectives → topics → pages "
                               "before generating questions")

    flagged_gaps = set()
    for i, entry in enumerate(source_map):
        where = "source_map[%d]" % i
        if not isinstance(entry, dict):
            rep.error(where, "entry must be an object")
            continue
        faculty = entry.get("faculty")
        if faculty_counts and is_text(faculty) and faculty not in faculty_counts:
            rep.error(where, "faculty %r is not in the blueprint" % faculty)

        topics = entry.get("topics")
        if topics is None:
            continue
        if not isinstance(topics, list):
            rep.error(where, "`topics` must be an array")
            continue
        for j, topic in enumerate(topics):
            twhere = "%s.topics[%d]" % (where, j)
            if not isinstance(topic, dict):
                rep.error(twhere, "entry must be an object")
                continue
            if not is_text(topic.get("topic")):
                rep.error(twhere, "`topic` must be a non-empty string")
            sid = topic.get("source_id")
            if sid is not None and source_ids and sid not in source_ids:
                rep.error(twhere, "unknown source_id %r" % sid)
            if topic.get("gap") is True:
                flagged_gaps.add(norm(topic.get("topic")))

    gaps = exam.get("source_gaps") or []
    if not isinstance(gaps, list):
        rep.error("source_gaps", "`source_gaps` must be an array")
        gaps = []
    declared = {norm(g.get("blueprint_area")) for g in gaps if isinstance(g, dict)}
    for gap in sorted(flagged_gaps - declared):
        if gap:
            rep.warn("source_gaps", "topic %r is flagged `gap: true` but is not listed in "
                                    "`source_gaps`" % gap)
    for gap in gaps:
        if isinstance(gap, dict) and is_text(gap.get("blueprint_area")):
            rep.warn("source_gaps", "unsupported blueprint area %r — do not fill it with outside "
                                    "facts" % gap["blueprint_area"])


def check_question(q, where, rep, faculty_counts, source_ids):
    if not is_text(q.get("question_id")):
        rep.error(where, "`question_id` must be a non-empty string")

    faculty = q.get("faculty")
    if not is_text(faculty):
        rep.error(where, "`faculty` must be a non-empty string")
    elif faculty_counts and faculty not in faculty_counts:
        rep.error(where, "faculty %r is not in the blueprint" % faculty)

    sid = q.get("source_id")
    if sid is not None and source_ids and sid not in source_ids:
        rep.error(where, "unknown source_id %r" % sid)

    for key in ("topic", "tested_concept", "stem"):
        if not is_text(q.get(key)):
            rep.error(where, "`%s` must be a non-empty string" % key)

    order = q.get("cognitive_order")
    if order not in (1, 2, 3) or isinstance(order, bool):
        rep.error(where, "`cognitive_order` must be 1, 2, or 3, got %r" % (order,))

    difficulty = q.get("difficulty")
    if difficulty is not None and difficulty not in DIFFICULTIES:
        rep.warn(where, "unknown difficulty %r (expected easy, moderate, or hard)" % (difficulty,))

    # --- choices: exactly A-E, non-empty, mutually distinct -------------------
    choices = q.get("choices")
    if not isinstance(choices, dict):
        rep.error(where, "`choices` must be an object keyed A-E")
        choices = {}
    else:
        keys = sorted(choices.keys())
        if keys != LETTERS:
            rep.error(where, "`choices` must have exactly the keys A-E, got %s"
                      % (", ".join(keys) if keys else "none"))
        seen_text = {}
        for letter in LETTERS:
            if letter not in choices:
                continue
            if not is_text(choices[letter]):
                rep.error(where, "choice %s is empty" % letter)
                continue
            key = norm(choices[letter])
            if key in seen_text:
                rep.error(where, "choices %s and %s are the same option"
                          % (seen_text[key], letter))
            else:
                seen_text[key] = letter

    answer = q.get("answer")
    if answer not in LETTERS:
        rep.error(where, "`answer` must be one of A-E, got %r" % (answer,))
        return

    # --- explanation ----------------------------------------------------------
    exp = q.get("explanation")
    if not isinstance(exp, dict):
        rep.error(where, "`explanation` must be an object")
        return

    for key in ("reasoning", "key_concept"):
        if not is_text(exp.get(key)):
            rep.error(where, "`explanation.%s` must be a non-empty string" % key)

    if not is_text(exp.get("citation")):
        rep.warn(where, "no `explanation.citation` — cite the source and page/slide when identifiable")

    distractors = exp.get("distractors")
    expected = [l for l in LETTERS if l != answer]
    if not isinstance(distractors, dict):
        rep.error(where, "`explanation.distractors` must be an object keyed by the four "
                         "non-answer letters (%s)" % ", ".join(expected))
        return

    got = sorted(distractors.keys())
    if got != sorted(expected):
        rep.error(where, "`explanation.distractors` must cover exactly %s, got %s"
                  % (", ".join(expected), ", ".join(got) if got else "none"))

    for letter in expected:
        if letter not in distractors:
            continue
        text = distractors[letter]
        if not is_text(text):
            rep.error(where, "distractor explanation %s is empty" % letter)
            continue
        stripped = text.strip()
        if len(stripped) < 25:
            rep.error(where, "distractor explanation %s is too short to name both the "
                             "alternative it represents and the clue that excludes it" % letter)
        elif DISMISSAL_RE.search(stripped):
            if len(stripped) < 120:
                rep.error(where, "distractor explanation %s is a generic dismissal — say what "
                                 "diagnosis, mechanism, or finding it would fit and which clue "
                                 "rules it out here" % letter)
            else:
                rep.warn(where, "distractor explanation %s contains a generic dismissal phrase; "
                                "confirm it draws a concrete contrast" % letter)

    if q.get("unsupported_flag") is True:
        rep.warn(where, "flagged as containing a fact the sources do not support")


def check_questions(exam, rep, faculty_counts, source_ids, complete):
    questions = exam.get("questions")
    if not isinstance(questions, list):
        rep.error("questions", "`questions` must be an array")
        return
    if not questions:
        rep.warn("questions", "no questions generated yet")
        return

    total = exam.get("total_questions")
    n = len(questions)
    if isinstance(total, int) and not isinstance(total, bool):
        if n > total:
            rep.error("questions", "%d questions exceed the requested total of %d" % (n, total))
        elif complete and n < total:
            rep.error("questions", "only %d of %d questions are present" % (n, total))
        elif not complete and n < total:
            rep.warn("questions", "partial bank: %d of %d questions" % (n, total))

    ids = set()
    sequences = {}
    per_faculty = Counter()

    for i, q in enumerate(questions):
        where = "questions[%d]" % i
        if not isinstance(q, dict):
            rep.error(where, "entry must be an object")
            continue
        qid = q.get("question_id")
        if is_text(qid):
            where = "question %s" % qid
            if qid in ids:
                rep.error(where, "duplicate question_id")
            ids.add(qid)

        seq = q.get("sequence")
        if isinstance(seq, int) and not isinstance(seq, bool):
            if seq in sequences:
                rep.error(where, "duplicate sequence %d (also %s)" % (seq, sequences[seq]))
            else:
                sequences[seq] = where
        elif complete:
            rep.error(where, "`sequence` must be an integer")
        else:
            rep.warn(where, "no `sequence` — the exam order is not pinned yet")

        if is_text(q.get("faculty")):
            per_faculty[q["faculty"]] += 1

        check_question(q, where, rep, faculty_counts, source_ids)

    if complete and sequences:
        expected = set(range(1, n + 1))
        if set(sequences.keys()) != expected:
            missing = sorted(expected - set(sequences.keys()))
            extra = sorted(set(sequences.keys()) - expected)
            detail = []
            if missing:
                detail.append("missing %s" % ", ".join(str(m) for m in missing[:10]))
            if extra:
                detail.append("out of range %s" % ", ".join(str(e) for e in extra[:10]))
            rep.error("questions", "`sequence` must be contiguous 1..%d (%s)"
                      % (n, "; ".join(detail)))

    for faculty, allocated in sorted(faculty_counts.items()):
        actual = per_faculty.get(faculty, 0)
        if actual > allocated:
            rep.error("blueprint", "%r has %d questions but is allocated %d"
                      % (faculty, actual, allocated))
        elif complete and actual < allocated:
            rep.error("blueprint", "%r has %d questions but is allocated %d"
                      % (faculty, actual, allocated))

    ordered = sorted(
        [q for q in questions if isinstance(q, dict)],
        key=lambda q: q.get("sequence") if isinstance(q.get("sequence"), int) else 1 << 30,
    )
    check_mix(ordered, rep, complete)
    check_adjacency(ordered, rep)
    check_answer_key(ordered, rep)
    check_randomization(ordered, rep, faculty_counts)


def check_mix(questions, rep, complete):
    orders = [q.get("cognitive_order") for q in questions
              if q.get("cognitive_order") in (1, 2, 3)]
    n = len(orders)
    if n == 0:
        return
    counts = Counter(orders)
    higher = (counts[2] + counts[3]) / n
    if higher < MIN_HIGHER_ORDER:
        msg = ("only %.0f%% of the bank is second- or third-order (%d of %d); at least %.0f%% "
               "must be" % (higher * 100, counts[2] + counts[3], n, MIN_HIGHER_ORDER * 100))
        if complete:
            rep.error("questions", msg)
        else:
            rep.warn("questions", msg + " once complete")

    if n >= 10:
        for order, target in sorted(TARGET_MIX.items()):
            share = counts[order] / n
            if abs(share - target) > MIX_TOLERANCE:
                rep.warn("questions", "cognitive order %d is %.0f%% of the bank; the target is "
                                      "%.0f%%" % (order, share * 100, target * 100))


def check_adjacency(questions, rep):
    """Step 4: no consecutive repetition of the same tested concept."""
    prev_concept = None
    prev_where = None
    topic_run = []
    answer_run = []

    for q in questions:
        where = "question %s" % q.get("question_id", "?")

        concept = norm(q.get("tested_concept"))
        if concept and concept == prev_concept:
            rep.error(where, "repeats the tested concept of the preceding question (%s) — "
                             "reorder or rewrite one of them" % prev_where)
        prev_concept, prev_where = concept, where

        topic = norm(q.get("topic"))
        if topic_run and topic_run[-1][0] == topic:
            topic_run.append((topic, where))
        else:
            _flush_topic_run(topic_run, rep)
            topic_run = [(topic, where)]

        letter = q.get("answer")
        if answer_run and answer_run[-1][0] == letter:
            answer_run.append((letter, where))
        else:
            _flush_answer_run(answer_run, rep)
            answer_run = [(letter, where)]

    _flush_topic_run(topic_run, rep)
    _flush_answer_run(answer_run, rep)


def _flush_topic_run(run, rep):
    if len(run) >= 3 and run[0][0]:
        rep.warn(run[0][1], "%d consecutive questions on topic %r — randomize the sequence "
                            "across topics" % (len(run), run[0][0]))


def _flush_answer_run(run, rep):
    if len(run) >= 4 and run[0][0] in LETTERS:
        rep.warn(run[0][1], "%d consecutive questions answer %s — a visible pattern clue"
                 % (len(run), run[0][0]))


def check_answer_key(questions, rep):
    answers = [q.get("answer") for q in questions if q.get("answer") in LETTERS]
    n = len(answers)
    if n >= 20:
        counts = Counter(answers)
        for letter in LETTERS:
            share = counts[letter] / n
            if share > 0.35:
                rep.warn("questions", "answer %s is correct on %.0f%% of items — rebalance the key"
                         % (letter, share * 100))
            elif share < 0.10:
                rep.warn("questions", "answer %s is correct on only %.0f%% of items — rebalance "
                                      "the key" % (letter, share * 100))

    # "Avoid making the answer predictably longest" (step 4).
    longest = 0
    scored = 0
    for q in questions:
        choices = q.get("choices")
        answer = q.get("answer")
        if not isinstance(choices, dict) or answer not in choices:
            continue
        texts = {k: v for k, v in choices.items() if isinstance(v, str)}
        if len(texts) < 2 or answer not in texts:
            continue
        scored += 1
        best = max(len(v) for v in texts.values())
        if len(texts[answer]) == best and list(
                len(v) for v in texts.values()).count(best) == 1:
            longest += 1
    if scored >= 10 and longest / scored > 0.40:
        rep.warn("questions", "the correct choice is the longest option on %.0f%% of items — "
                              "length is acting as a clue" % (longest / scored * 100))


def check_randomization(questions, rep, faculty_counts):
    """Step 4: randomize across faculty while preserving the blueprint."""
    faculties = [q.get("faculty") for q in questions if is_text(q.get("faculty"))]
    distinct = len(set(faculties))
    if distinct < 2 or len(faculties) <= distinct:
        return
    runs = 1
    for a, b in zip(faculties, faculties[1:]):
        if a != b:
            runs += 1
    if runs == distinct:
        rep.warn("questions", "the sequence is blocked by faculty (%d faculty, %d runs) — "
                              "randomize across faculty and topics while keeping the blueprint "
                              "counts" % (distinct, runs))


def render(rep, path, complete, as_json, quiet):
    if as_json:
        json.dump({
            "file": path,
            "mode": "complete" if complete else "partial",
            "ok": not rep.errors,
            "errors": rep.errors,
            "warnings": rep.warnings,
            "summary": {"errors": len(rep.errors), "warnings": len(rep.warnings)},
        }, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    if not quiet:
        for label, items in (("ERROR", rep.errors), ("WARN", rep.warnings)):
            for item in items:
                print("%-5s %s: %s" % (label, item["where"], item["message"]))
        if rep.errors or rep.warnings:
            print("")

    mode = "complete" if complete else "partial"
    if rep.errors:
        print("FAIL (%s): %d error(s), %d warning(s) — fix every error and rerun before launch."
              % (mode, len(rep.errors), len(rep.warnings)))
    else:
        print("PASS (%s): 0 errors, %d warning(s). Structure and blueprint check out — the "
              "source-grounding and clinical-quality audit is still yours."
              % (mode, len(rep.warnings)))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate a practice-exam-builder exam.json against the data contract.")
    parser.add_argument("exam", help="path to exam.json")
    parser.add_argument("--complete", action="store_true",
                        help="apply full-bank invariants (run this before launching an exam)")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="emit machine-readable results")
    parser.add_argument("--quiet", action="store_true",
                        help="print only the summary line")
    args = parser.parse_args(argv)

    try:
        with open(args.exam, "r", encoding="utf-8") as handle:
            exam = json.load(handle)
    except OSError as exc:
        print("cannot read %s: %s" % (args.exam, exc), file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print("%s is not valid JSON: %s" % (args.exam, exc), file=sys.stderr)
        return 2

    rep = Report()
    if not isinstance(exam, dict):
        rep.error("exam", "top level must be a JSON object")
        render(rep, args.exam, args.complete, args.as_json, args.quiet)
        return 1

    check_top_level(exam, rep)
    faculty_counts = check_blueprint(exam, rep)
    source_ids = check_sources(exam, rep)
    check_source_map(exam, rep, faculty_counts, source_ids)
    check_questions(exam, rep, faculty_counts, source_ids, args.complete)

    render(rep, args.exam, args.complete, args.as_json, args.quiet)
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
