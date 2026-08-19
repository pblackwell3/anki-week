# study-week — Watched videos (the memory)

Which study videos you have **already watched** — Boards & Beyond or Med School Bootcamp, whichever
library you run (`video_library` in `config.md`). `study-week` reads this every run and
**does not re-schedule** a video that's already here — that frees window capacity for what you haven't
seen yet. Grows over time; edit it by hand from GitHub mobile whenever you like.

Companion to `bb-videos.json` / `bootcamp-videos.json` (what *exists*). This file is what's been
*consumed*.

## Matching rule

The key depends on the library, because only one of them has unique titles:

| Library | Key | Why |
|---|---|---|
| `bb` | **`Video title`** | Re-verified 2026-08-18 against schema v2: all **502** titles in `bb-videos.json` are **globally unique**, so the title alone is unambiguous — `Subject` / `Section` are for your reading. |
| `bootcamp` | **`Subject › Section › Title`** | Bootcamp titles repeat by design — `Board-style Question Breakdown` appears **166 times**, `Case Progression I` 25 times, 83 titles are non-unique. **Fill in `Subject` and `Section` on every Bootcamp row**; a bare title matches many videos and study-week will flag it as ambiguous rather than skip them all. |

- Everything is matched **case-insensitively with whitespace collapsed**.
- Leave `Library` blank and the row is read as `bb` (that's what rows written before Bootcamp support
  meant).
- A title here that matches no video **must be checked against that library's `title_aliases`
  before it's called a miss** — B&B renamed 20 videos (`Trisomies` → `Trisomy Disorders`,
  `Cushing's Syndrome` → `Cushing Syndrome`, `Beta Thalassemias` → `Beta Thalassemia`, …), and an
  alias hit is a **match**, not an error. Update the row to the current title as you go.
- A title that matches neither a video nor an alias is a **typo or a retired video** →
  study-week flags it in the plan doc rather than silently ignoring it. Fix the spelling, or drop the
  row if the library retired the video.
- Two Bootcamp `Subject › Section › Title` triples still collide
  (`Gross Anatomy › Anterior & Medial Thigh, Knee › Knee Joint`,
  `Histology › Blood & Blood Formation › Bone Marrow - Overview`). Note the video's `route` in `Notes`
  if you ever log one of them.
- `Status`: `watched` (done) · `partial` (started, not finished — treated as **NOT watched**, it still
  gets scheduled) · `skip` (deliberately never watching this one — treated as watched, never scheduled).

## ⚠️ Watched ≠ uncovered

Skipping an already-watched video **must never** turn its lecture concepts into a `coverage_gap`. The
concept is still covered — it was covered by watching it. In the plan doc a watched video appears under
its lecture's mapping as `✓ watched <date>` so the coverage tally stays honest; it just gets no calendar
block. **Only a concept that no video covers at all is a real gap.**

## Format

| Video title | Library | Subject | Section | Status | Date | For lecture | Notes |
|---|---|---|---|---|---|---|---|

<!-- Example rows — delete or keep as reference:
| Inhaled Anesthetics | bb | Anesthesia | General Topics | watched | 2026-07-14 | — | |
| Cell Cycle | bb | Cell Biology | | watched | 2026-06-30 | IM06 | rewatched before the midterm |
| Enzyme Kinetics | bb | Basic Pharmacology | | partial | 2026-07-20 | IM39 | stopped ~halfway, finish it |
| Cell Trafficking | bootcamp | Biochemistry | Cell Biology | watched | 2026-08-19 | IM06 | |
| Board-style Question Breakdown | bootcamp | Cardiology | Heart Failure | watched | 2026-08-19 | IM41 | Section is REQUIRED — this title exists 166× |
-->

<!-- Watched videos appended below this line -->

| Video title | Library | Subject | Section | Status | Date | For lecture | Notes |
|---|---|---|---|---|---|---|---|

*(empty — nothing recorded yet. The first `study-week` run that confirms watched videos will fill this
in, or add rows yourself.)*

## How this gets filled

1. **You tell Claude** — "mark Cell Cycle and DNA Replication watched" → rows get appended.
2. **End-of-run confirmation** — when `study-week` runs, it lists the **previous** run's scheduled
   videos and asks which you actually watched, then appends those. Scheduling a video never marks it
   watched on its own — a block you didn't get to shouldn't silently count as done.
3. **By hand** — add a row. `Video title` and `Status` are always required; on a Bootcamp row
   `Subject` and `Section` are required too (they're part of the key). The rest is for your records.

## Undo / correction

Delete the row (or set `Status` to `partial`) and the video becomes schedulable again on the next run.
