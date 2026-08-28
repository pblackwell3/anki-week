# practice-exam-builder — Data Contract

Everything this skill persists is plain JSON, UTF-8, one exam per directory. The layout is the same
on every host — Claude Artifact, ChatGPT/Codex app surface, or plain chat — so a session started on
one can be resumed on another.

```
<course_folder>/_practice-exams/          ← or the workspace, or a path the user picks
├── weakness-history.json                 ← ONE file, spans every exam
└── <exam_id>/
    ├── exam.json                         ← the question bank + blueprint + source map
    ├── session.json                      ← one attempt's live state (rewritten as you go)
    └── report.json                       ← scoring + remediation, written at completion
```

**Rules that hold for every file.** `schema_version` is `"1.0"`. IDs are stable and never renumbered
(`exam_id` is the directory name; `question_id` survives every revision so a resumed session keeps
its order). Timestamps are ISO-8601 UTC (`2026-03-14T15:04:05Z`). Unknown keys are preserved on
rewrite — never drop a field you did not write. **Never merge two exams into one file**, and never
overwrite `weakness-history.json` wholesale; append to it.

---

## `exam.json`

The exam package. Written once at generation, rewritten only on a deliberate revision.

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_version` | string | ✅ | `"1.0"` |
| `exam_id` | string | ✅ | Slug, matches the directory name. e.g. `cardio-block-2-2026-03-14` |
| `exam_name` | string | ✅ | As the user says it: `"Cardiology Block Exam 2"` |
| `exam_date` | string | ✅ | `YYYY-MM-DD` |
| `created_at` | string | ✅ | ISO-8601 UTC |
| `total_questions` | integer | ✅ | The requested total. **The blueprint must sum to this** (step 2). |
| `block` | string | — | `current_block` from anki-week, when known |
| `blueprint` | array | ✅ | The faculty distribution, verbatim as given. See below. |
| `sources` | array | ✅ | Every material read. See below. |
| `source_map` | array | ✅ | `faculty → lecture → objectives → topics → pages`. See below. |
| `source_gaps` | array | — | Blueprint areas with no supporting source. Never silently filled. |
| `questions` | array | ✅ | The bank. See below. |

### `blueprint[]`

```json
{ "faculty": "Dr. Nguyen", "count": 20, "topics": ["Heart failure", "Valvular disease"] }
```

`faculty` unique across the array; `count` a non-negative integer; `topics` optional. **`sum(count)`
must equal `total_questions`** — the validator treats any difference as an error, which is the
blueprint gate in machine-readable form.

### `sources[]`

```json
{
  "source_id": "src-001",
  "type": "lecture_slides",
  "title": "Heart Failure — Pathophysiology",
  "path": "~/Lecture Materials/Cardio/Week 3/HF-patho.pptx",
  "faculty": "Dr. Nguyen"
}
```

`type` is one of `lecture_slides`, `review_slides`, `faculty_questions`, `syllabus`, `notes`, `other`.
`source_id` is unique and is what every question and topic points back to.

### `source_map[]`

```json
{
  "faculty": "Dr. Nguyen",
  "lecture": "Heart Failure — Pathophysiology",
  "objectives": ["Explain the Frank-Starling relationship in systolic dysfunction"],
  "topics": [
    {
      "topic": "Systolic heart failure",
      "subtopics": ["Frank-Starling", "Neurohormonal compensation"],
      "source_id": "src-001",
      "pages": [12, 13, 14],
      "bootcamp_match": "Cardiology → Heart Failure I",
      "anki_match": "#AK_Step1_v12::#B&B::05_Cardio::Heart_Failure",
      "gap": false
    }
  ]
}
```

`bootcamp_match` / `anki_match` are `null` when there is no **direct** conceptual match — an
approximate match is worse than none. `gap: true` marks a topic the blueprint demands and the sources
do not support; mirror it into `source_gaps` with a reason.

### `questions[]`

```json
{
  "question_id": "q-001",
  "sequence": 1,
  "faculty": "Dr. Nguyen",
  "lecture": "Heart Failure — Pathophysiology",
  "source_id": "src-001",
  "source_page": 13,
  "topic": "Systolic heart failure",
  "subtopic": "Neurohormonal compensation",
  "tested_concept": "RAAS activation drives afterload in decompensated HFrEF",
  "cognitive_order": 3,
  "difficulty": "hard",
  "stem": "A 64-year-old man is brought to the emergency department because of …",
  "choices": {
    "A": "Decreased renal sympathetic tone",
    "B": "Increased angiotensin II-mediated efferent arteriolar constriction",
    "C": "Increased atrial natriuretic peptide clearance",
    "D": "Decreased aldosterone-mediated sodium reabsorption",
    "E": "Increased nitric-oxide-mediated vasodilation"
  },
  "answer": "B",
  "explanation": {
    "reasoning": "The 3-week weight gain, JVD and S3 place this in decompensated HFrEF; …",
    "distractors": {
      "A": "Renal sympathetic tone is *increased*, not decreased, in low-output states — …",
      "C": "ANP clearance would fit a … , but this patient's rising BNP argues the opposite.",
      "D": "Aldosterone-mediated reabsorption rises here, which is why the patient is …",
      "E": "NO-mediated vasodilation would lower afterload; the cool extremities show …"
    },
    "key_concept": "RAAS activation raises afterload and worsens forward failure in HFrEF.",
    "citation": "HF-patho.pptx, slide 13"
  },
  "bootcamp_match": "Cardiology → Heart Failure I",
  "anki_match": "#AK_Step1_v12::#B&B::05_Cardio::Heart_Failure",
  "unsupported_flag": false
}
```

| Field | Required | Rule |
|---|---|---|
| `question_id` | ✅ | Unique, stable across revisions |
| `sequence` | ✅ | `1..N`, contiguous, **randomized across faculty and topic** — never blocked by faculty |
| `faculty` | ✅ | Must name a `blueprint[].faculty` |
| `source_id` | — | Must name a `sources[].source_id` when present |
| `topic`, `tested_concept` | ✅ | `tested_concept` must not repeat in adjacent `sequence` positions |
| `cognitive_order` | ✅ | `1`, `2`, or `3`. **≥80% of the bank must be 2 or 3.** |
| `difficulty` | — | `easy`, `moderate`, `hard` |
| `choices` | ✅ | Exactly keys `A`–`E`, all non-empty and mutually distinct |
| `answer` | ✅ | One of `A`–`E` |
| `explanation.reasoning` | ✅ | Decisive clues → reasoning chain → answer |
| `explanation.distractors` | ✅ | Exactly the four non-answer letters; each names what it *would* fit and the clue that excludes it. Generic dismissals (`does not match`, `is incorrect`, `not source-supported`) are rejected. |
| `explanation.key_concept` | ✅ | One sentence |
| `explanation.citation` | — | Source + page/slide when identifiable |
| `unsupported_flag` | — | `true` = contains a fact the sources do not support, deliberately surfaced |

---

## `session.json`

One attempt. Rewritten after every answer or navigation change — a crash or a closed tab costs at
most the current question.

```json
{
  "schema_version": "1.0",
  "exam_id": "cardio-block-2-2026-03-14",
  "session_id": "sess-2026-03-10-a",
  "mode": "tutor",
  "started_at": "2026-03-10T18:02:11Z",
  "updated_at": "2026-03-10T18:44:57Z",
  "completed_at": null,
  "time_limit_seconds": 3600,
  "elapsed_seconds": 2566,
  "current_index": 23,
  "question_order": ["q-001", "q-002", "q-003"],
  "responses": {
    "q-001": {
      "selected": "B",
      "marked": false,
      "struck": ["A", "E"],
      "confidence": "high",
      "answered_at": "2026-03-10T18:03:40Z",
      "time_spent_seconds": 89,
      "changed_answer": false
    }
  }
}
```

`mode` is `timed`, `tutor`, `weakness_drill`, or `review_marked`. `question_order` is the frozen
order for this attempt — **resuming never reshuffles it**. `selected` is `null` for a seen-but-unanswered
question and the key is absent for a question not yet reached. `confidence` (`low`/`medium`/`high`)
is optional and is the only evidence that licenses the confidence-based miss reasons in step 8.

A **Review Marked** or **Weakness Drill** run is a *new* `session_id` with its own file
(`session-<id>.json` alongside `session.json`); it never overwrites the original attempt's history.

---

## `report.json`

Written at completion, from `exam.json` + `session.json`.

```json
{
  "schema_version": "1.0",
  "exam_id": "cardio-block-2-2026-03-14",
  "session_id": "sess-2026-03-10-a",
  "generated_at": "2026-03-10T19:05:00Z",
  "score": { "correct": 44, "answered": 60, "total": 60, "percent": 73.3 },
  "by_faculty": [{ "key": "Dr. Nguyen", "correct": 14, "total": 20, "percent": 70.0 }],
  "by_topic": [{ "key": "Systolic heart failure", "correct": 3, "total": 6, "percent": 50.0 }],
  "by_subtopic": [],
  "by_cognitive_order": [{ "key": "3", "correct": 9, "total": 18, "percent": 50.0 }],
  "marked": ["q-004", "q-017"],
  "incorrect": ["q-002", "q-009"],
  "misses": [
    {
      "question_id": "q-002",
      "topic": "Systolic heart failure",
      "reason": "forgot_mechanism",
      "evidence": "answered high-confidence, correct on the diagnosis stem q-011",
      "remediation": {
        "route": "mechanism-focused Anki + Bootcamp segment",
        "bootcamp": "Cardiology → Heart Failure I",
        "anki": "#AK_Step1_v12::#B&B::05_Cardio::Heart_Failure",
        "source": "HF-patho.pptx, slide 13"
      }
    }
  ],
  "weak_topics": [{ "topic": "Systolic heart failure", "missed": 3, "seen": 6, "rank": 1 }],
  "priorities": ["Re-watch Heart Failure I, then drill the RAAS cards before Thursday"]
}
```

`reason` is one of `knowledge_gap`, `misread_question`, `confused_similar_concepts`,
`forgot_mechanism`, `wrong_association`, `low_confidence_correct`, `high_confidence_incorrect`, or
**`unclassified`** — which is the honest default. Do not infer a reason the response data does not
support. `bootcamp` / `anki` are `null` when there is no direct match; the report text then says
`No direct Bootcamp match found.`

---

## `weakness-history.json`

Cross-exam, one file above all the exam directories. **Append-only**: a new exam adds an entry to each
topic it touched; it never rewrites another exam's numbers.

```json
{
  "schema_version": "1.0",
  "updated_at": "2026-03-10T19:05:00Z",
  "topics": [
    {
      "topic": "Systolic heart failure",
      "missed_total": 5,
      "seen_total": 11,
      "exams": [
        { "exam_id": "cardio-block-1-2026-02-07", "date": "2026-02-07", "missed": 2, "seen": 5 },
        { "exam_id": "cardio-block-2-2026-03-14", "date": "2026-03-14", "missed": 3, "seen": 6 }
      ]
    }
  ]
}
```

This is what **Weakness Drill** filters on, and what makes "still weak three exams later" visible.

---

## Validation

```text
python scripts/validate_exam.py <exam.json>            # partial bank, mid-generation
python scripts/validate_exam.py <exam.json> --complete # full-bank invariants, before launch
python scripts/validate_exam.py <exam.json> --json     # machine-readable
```

Use `python3` where `python` is unversioned. Exit `0` = no errors, `1` = errors found, `2` = the file
could not be read or parsed. Warnings never
fail the run — read them anyway; they are where pattern clues and answer-key bias show up. The script
is stdlib-only Python 3.8+ and checks structure and blueprint arithmetic. **It cannot check whether a
question is clinically sound or actually supported by the slide it cites** — that is the manual audit
in step 5.
