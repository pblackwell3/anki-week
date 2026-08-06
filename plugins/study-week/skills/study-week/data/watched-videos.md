# study-week — Watched B&B videos (the memory)

Which Boards & Beyond videos you have **already watched**. `study-week` reads this every run and
**does not re-schedule** a video that's already here — that frees window capacity for what you haven't
seen yet. Grows over time; edit it by hand from GitHub mobile whenever you like.

Companion to `bb-videos.json` (what *exists*). This file is what's been *consumed*.

## Matching rule

- **Key = the video title**, matched case-insensitively with whitespace collapsed.
  Verified 2026-07-31: all **496** titles in `bb-videos.json` are **globally unique**, so the title
  alone is unambiguous — the `Subject` column is for your reading, not for matching.
- A title here that matches **no** video in `bb-videos.json` is a **typo or a renamed video** →
  study-week flags it in the plan doc rather than silently ignoring it. Fix the spelling, or drop the
  row if B&B retired the video.
- `Status`: `watched` (done) · `partial` (started, not finished — treated as **NOT watched**, it still
  gets scheduled) · `skip` (deliberately never watching this one — treated as watched, never scheduled).

## ⚠️ Watched ≠ uncovered

Skipping an already-watched video **must never** turn its lecture concepts into a `coverage_gap`. The
concept is still covered — it was covered by watching it. In the plan doc a watched video appears under
its lecture's mapping as `✓ watched <date>` so the coverage tally stays honest; it just gets no calendar
block. **Only a concept that no video covers at all is a real gap.**

## Format

| Video title | Subject | Status | Date | For lecture | Notes |
|---|---|---|---|---|---|

<!-- Example rows — delete or keep as reference:
| Inhaled Anesthetics | Anesthesia | watched | 2026-07-14 | — | |
| Cell Cycle | Cell Biology | watched | 2026-06-30 | IM06 | rewatched before the midterm |
| Enzyme Kinetics | Basic Pharmacology | partial | 2026-07-20 | IM39 | stopped ~halfway, finish it |
-->

<!-- Watched videos appended below this line -->

| Video title | Subject | Status | Date | For lecture | Notes |
|---|---|---|---|---|---|

*(empty — nothing recorded yet. The first `study-week` run that confirms watched videos will fill this
in, or add rows yourself.)*

## How this gets filled

1. **You tell Claude** — "mark Cell Cycle and DNA Replication watched" → rows get appended.
2. **End-of-run confirmation** — when `study-week` runs, it lists the **previous** run's scheduled
   videos and asks which you actually watched, then appends those. Scheduling a video never marks it
   watched on its own — a block you didn't get to shouldn't silently count as done.
3. **By hand** — add a row. Only `Video title` and `Status` are required; the rest is for your records.

## Undo / correction

Delete the row (or set `Status` to `partial`) and the video becomes schedulable again on the next run.
