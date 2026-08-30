---
name: practice-exam-builder
description: >-
  Build reusable, interactive, source-grounded medical-school practice exams from your own course
  materials. Use when creating, resuming, or reporting on an NBME/USMLE-style practice exam built
  from lecture slides, review slides, professor-posted review questions, missed topics, Anki
  tags/decks, and optional Bootcamp or Boards & Beyond mappings; when validating a faculty question
  distribution against the requested total; or when producing exam performance and remediation
  reports. Runs on BOTH surfaces — on Claude (Claude Code, Cowork, Desktop) the exam UI is an
  Artifact; on ChatGPT/Codex it is the in-app app surface. Ships with anki-week: anki-week builds the
  cards, study-week schedules the time, this skill tests what actually stuck. Do not use for an
  ordinary chat-only quiz when an interactive surface is available.
---

# Practice Exam Builder

Build an exam-specific interactive app from the user's current materials. Keep every question traceable to those materials, preserve the current faculty blueprint exactly, and persist exam and session state locally.

## Where this fits

Third skill in the same weekly loop: **`anki-week`** builds the cards, **`study-week`** schedules the
time around them, **this skill tests what stuck** and routes what didn't back into the other two.

It **reads** `anki-week`'s config at `../anki-week/data/config.md` when present — `course_folder`
(where the slides live and where exams get written), `deck_name` / `tag_namespace` /
`backbone_resource` (how to name an Anki match), `current_block` (which system this exam belongs to).
Nothing here writes to that config, and **nothing here modifies Anki** — see step 8.

When the user hasn't supplied a video map, the catalogs shipped in the sibling plugin are the
searchable source list — from this skill's folder,
`../../../study-week/skills/study-week/data/bootcamp-videos.json` (Med School Bootcamp, incl. Anatomy
Bootcamp) and `../../../study-week/skills/study-week/data/bb-videos.json` (Boards & Beyond). Both
carry each site's own keyword index for substring matching. Follow `backbone_resource` to pick one;
they are catalogs — titles, runtimes, keywords — so a match is a **pointer to a video the user owns**,
never content.

## Follow the workflow

### 1. Collect the current exam configuration

Require:

- exam name and date
- total question count
- the current faculty/question distribution
- lecture slides, review slides, and professor-posted review questions

Accept optional missed topics, Anki tags/decks, and a Bootcamp video map or searchable source list. Treat every exam as new configuration: never reuse a prior faculty distribution or silently carry forward sources.

### 2. Enforce the blueprint gate

Sum the faculty counts and compare the result with the requested total before mapping sources or writing questions.

- If the totals differ, stop and report the expected total, actual total, and difference.
- Ask for a corrected distribution.
- Do not add topics, remove faculty, or redistribute counts without explicit approval.
- If required inputs are missing, request them rather than guessing.

### 3. Build the source map

Read the supplied materials with the appropriate document, PDF, or presentation tools. Create this hierarchy before question generation:

`faculty -> lecture -> objectives -> topics -> source pages/slides`

For each mapped topic, record direct Bootcamp and Anki matches when supplied or reliably searchable. Prefer exact organ system, disease, drug class, anatomy region, or mechanism matches. Flag unsupported blueprint areas as source gaps; do not fill them with outside facts.

Use professor-posted questions to infer emphasis and style, not as text to copy. Keep the source map in the exam package described in [references/data-contract.md](references/data-contract.md).

### 4. Generate the questions

Generate the exact number assigned to each faculty member. Randomize the question sequence across faculty and topics while preserving the blueprint.

Unless the user specifies another mix, target the whole exam at approximately:

- 20% first-order or free-standing questions
- 50% second-order questions
- 30% third-order questions

Keep at least 80% of the bank second- or third-order. Treat first-order items as a deliberate supplement for source facts that do not benefit from a vignette; do not use them as the default.

Classify cognitive order by the reasoning required, not stem length:

- **First order:** recall one fact or direct association.
- **Second order:** infer the diagnosis, localization, or process, then select its mechanism, structure, mutation, drug effect, or expected finding.
- **Third order:** combine at least two inferential steps, such as diagnosis plus a downstream mechanism, complication, physiologic consequence, or treatment response.

For every item:

- Prefer an original, patient-centered NBME/USMLE Step 1-style vignette that tests integrated reasoning rather than recognition of a memorized phrase.
- Integrate relevant demographics, time course, risks, examination findings, labs, imaging, procedures, anatomy, histology, pathophysiology, microbiology, genetics, or pharmacology when supported. Include only details that contribute to the reasoning or realistic presentation.
- Use free-standing recall only when it best matches the source and the tested fact cannot be assessed naturally through a clinical vignette.
- Provide exactly five plausible choices labeled A through E with one best answer.
- Randomize choice order independently for each item.
- Avoid making the answer predictably longest, shortest, most specific, or most technical.
- Avoid consecutive repetition of the same diagnosis, drug, mechanism, or tested concept.
- Exclude or explicitly flag facts not supported by the provided sources.

Attach faculty, lecture, source, page/slide when identifiable, topic, subtopic, tested concept, cognitive order, difficulty, answer, direct Bootcamp match, and direct Anki match.

Write explanations that teach the reasoning:

- Identify the decisive stem clues and walk through the reasoning chain to the correct answer.
- For every distractor, state what diagnosis, mechanism, structure, drug effect, or finding it would fit and name the specific clue or missing feature that rules it out here.
- Explain why a tempting near-neighbor is wrong when applicable.
- Never use generic dismissals such as `not source-supported`, `does not match`, or `is incorrect` without a concrete contrast.
- End with the key concept and an identifiable source citation.

### 5. Audit before launch

Write the generated exam to the data contract, then run:

```text
python scripts/validate_exam.py <exam.json> --complete
```

Resolve every reported error and inspect warnings. The script checks structural and blueprint invariants; it does not replace a source-grounding and clinical-quality review.

Manually audit every item for:

- one unambiguous best answer and exactly five A-E choices
- relevant details and no unsupported outside facts
- original wording rather than copied posted questions
- balanced answer-choice construction without pattern clues
- complete correct-answer and distractor explanations
- at least 80% second- or third-order items across the complete bank
- integrated clinical vignettes that require the claimed reasoning order
- specific distractor explanations that identify both the alternative represented and the vignette clue that excludes it
- identifiable source citation when available
- no consecutive duplicate diagnosis, drug, mechanism, or concept
- exact faculty allocation and appropriate topic coverage

Fix violations and rerun validation before opening the exam.

### 6. Build the interactive exam surface

Use the most capable interactive surface this host supports, and build the same exam either way — the
UI contract below does not change with the surface.

| Host | Surface to build | Notes |
|---|---|---|
| **Claude** (Code, Cowork, Desktop) | An **Artifact** — one self-contained HTML page, published private to the user | Load the `artifact-design` skill before writing it. Keep it one file: inline CSS/JS, no external fetches. If the artifact runtime offers this user a persistence capability, use it; otherwise `localStorage`, keyed by `exam_id`. |
| **ChatGPT / Codex** | The in-app app / embedded UI surface | Same one-question-at-a-time contract; persist to the exam directory plus the surface's own local storage. |
| **No interactive surface available** | Chat, one question per turn | State the limitation in one line first, then run it — and still write the same `exam.json` / `session.json` / `report.json`. |

Do not fall back to a normal chat-only quiz while an interactive surface is available. If a true side panel is unavailable, briefly state that limitation before implementation and use the closest functional in-app experience.

Show only one question at a time with:

- progress, question number, and section/topic tag
- five selectable choices
- Mark Question and optional strikeout controls
- Submit, then a clear Next Question action

Never reveal future questions early or add broad summaries unless requested.

Support these modes:

- **Timed Exam:** enforce exam-like timing and withhold all explanations until completion.
- **Tutor:** reveal correctness and the full explanation after submission.
- **Weakness Drill:** filter or generate source-grounded items for recorded missed topics.
- **Review Marked:** redo marked and incorrect items without losing the original history.

After a Tutor submission, show correctness, the correct answer, why it is correct, why each distractor is wrong, the key concept, and the source. Capture answer, marked state, strikeouts, and confidence when available.

### 7. Persist progress safely

Store the generated exam, session state, and reports in an exam-specific local directory: `<course_folder>/_practice-exams/<exam_id>/` when `anki-week`'s `course_folder` is set, otherwise the current workspace or a user-selected path. Also use the in-app surface's local persistence when available. Save after each answer or navigation change and use stable exam and question IDs so the session can resume without changing question order.

Maintain `exam.json`, `session.json`, and `report.json` according to [references/data-contract.md](references/data-contract.md). Keep cross-exam weakness history in a separate local history file; never merge exams or overwrite unrelated data.

**Getting state back out of a hosted page.** An Artifact (and most embedded app surfaces) cannot write
to the filesystem, and page-initiated downloads are blocked in the artifact sandbox — so never offer
progress as a download link. Give the page an **Export session** panel that renders `session.json` as
selectable, copy-to-clipboard text; write the copied JSON to disk yourself whenever the run pauses or
completes. On resume, read `session.json` and seed the page with it.

### 8. Report and remediate

At completion, report overall score; scores by faculty, content area, topic, and subtopic; marked and incorrect questions; concise remediation; ranked weak topics; and priorities for the remaining study time.

Classify misses only when supported by response or confidence evidence: knowledge gap, misread question, confused similar concepts, forgot mechanism, wrong association, low confidence but correct, or high confidence but incorrect. Leave the reason unclassified rather than inventing one.

Route remediation as follows:

- knowledge gap -> source slide plus a direct Bootcamp match
- forgot mechanism -> mechanism-focused Anki cards and Bootcamp segment
- confused similar concepts -> comparison table or contrast drill
- misread question -> test-taking review rather than extra content
- wrong association -> targeted recall drill
- low confidence but correct -> light review

Recommend Bootcamp videos and Anki tags/decks only for direct conceptual matches. Put the most targeted match first. Say `No direct Bootcamp match found.` when appropriate. Identify low-yield or poorly aligned Anki matches. Never modify Anki unless access is available and the user explicitly approves the specific action.

## Resources

- Read [references/data-contract.md](references/data-contract.md) when creating, resuming, or reporting an exam.
- Run `scripts/validate_exam.py` before launching a complete exam and after any question-set revision.
