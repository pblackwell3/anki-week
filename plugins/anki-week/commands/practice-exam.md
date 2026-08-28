---
description: Build, resume, or report on an interactive source-grounded practice exam from your lecture materials — faculty blueprint enforced, every question traced to a slide.
---

Run the **practice-exam-builder** skill (`${CLAUDE_PLUGIN_ROOT}/skills/practice-exam-builder/SKILL.md`).
Read it and follow its eight steps — this command is the entry point, not a shortcut past them.

First work out which of these the user is asking for, and say which one you picked:

- **New exam** → step 1. Collect exam name, date, total question count, the **current** faculty
  distribution, and the lecture slides / review slides / professor-posted review questions. Never
  reuse a prior exam's distribution or sources.
- **Resume** → read `session.json` from the exam directory and reopen at `current_index` with
  `question_order` **unchanged**. Never reshuffle a session in progress.
- **Report / remediate** → step 8, from the existing `exam.json` + `session.json`.
- **Weakness drill or review-marked** → a *new* session file; leave the original attempt's history intact.

Three things this command must not let slide:

1. **The blueprint gate (step 2).** Sum the faculty counts and compare with the requested total
   *before* mapping sources or writing anything. Mismatch → stop, report expected vs. actual vs.
   difference, ask for a corrected distribution. Do not redistribute counts yourself.
2. **Validation before launch (step 5).**

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/practice-exam-builder/scripts/validate_exam.py" <exam.json> --complete
   ```

   Exit `0` = clean · `1` = errors, fix every one and rerun · `2` = the file couldn't be parsed.
   A pass covers structure and blueprint arithmetic only — the source-grounding and clinical-quality
   audit in step 5 is still yours to do by hand.
3. **Source grounding.** Every question traces to a slide or posted material. An unsupported fact is
   either cut or explicitly flagged — never quietly filled in from general knowledge.

Build the exam UI as an **Artifact**: one self-contained HTML page, one question at a time, five
choices, Mark + strikeout, Submit → Next. Load the `artifact-design` skill before you write it. The
page can't write files and the sandbox blocks downloads, so give it an **Export session** panel with
copy-to-clipboard JSON, and write `session.json` yourself when the run pauses or finishes.

Anki is **read-only** here: matches are suggestions for the report. Never unsuspend, edit, or create
a card without the user explicitly approving that specific action.
