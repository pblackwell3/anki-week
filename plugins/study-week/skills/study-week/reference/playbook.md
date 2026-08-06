# study-week — Playbook

The full procedure. SKILL.md is the summary; this is what to actually do each run. All times
**America/Chicago**. Read `data/config.md` first — every knob below comes from it.

## Prerequisites (check first)

- **Google Calendar MCP** connected (read Class + Personal, write Personal).
- **`course_folder` readable** (path in `config.md`) — Stage 1.5 reads the week's slides/PDFs. If it's
  unreachable, don't fail: fall back to objectives/title and mark every mapping `low-confidence`.
- **Anki MCP** reachable **only if** `anki_reserve_mode = rolling-avg` — Anki desktop open with the
  add-on. If it's not reachable, don't fail: use `anki_reserve_fallback_min` and flag it in the doc.
- `data/bb-videos.json` present. If B&B has changed, rebuild it: `python3 data/build-bb-videos.py <pdf>`.

## Stage 0 · Resolve the week

- `current_week = upcoming` → the coming Mon–Sun (if today is mid-week, still the NEXT Monday's week
  unless you say "this week"). An explicit `YYYY-MM-DD` overrides. Compute `week_start` (Mon 00:00)
  and `week_end` (Sun 23:59).

## Stage 1 · Read lectures

- `list_events(class_calendar_id, week_start, week_end, orderBy=startTime)`.
- Keep timed sessions whose title matches `IM (NN)` or `IM:` (and any other course codes present).
  Parse `{session_no, title, date, start, end}`. Note all-day banners (week themes) as context, not
  lectures.
- Result: an ordered list of the week's lectures — **the index of which materials to go read in Stage
  1.5.** The title is a pointer, never the scope; nothing maps to a video from this list alone.

## Stage 1.5 · Read the lecture materials  (MATERIALS-FIRST)

The step that makes the mapping real. For **each lecture** from Stage 1, find and read its materials in
`<course_folder>/<Course>/Week <n>/` (path in `config.md`; materials sit **directly inside**):

- `*.pptx` / `*.ppt` → full slide text via the **pptx** skill (legacy `.ppt` binary → PowerPoint-atom parser).
- `*.pdf` → full text via the **pdf** skill / **PyMuPDF** (the old pure-zlib method mangles CID PDFs).
- Skip non-lecture files (orientation/how-to docs, Anatomage links, sample-question decks).

Produce a **concept inventory** per lecture — every distinct thing the slides teach (mechanisms,
named frameworks/lists, definitions, diagrams, drugs/diseases named). This inventory, not the title,
is what Stage 4 maps to videos, and it is the **coverage floor**: the chosen video set must span it.

**Fallback ladder** (record which rung you used; it drives the confidence flag):
1. **Materials read** → `confidence: high`.
2. **No materials posted** → derive the inventory from the **syllabus objectives**, scope it
   generously, mark `confidence: low` and the lecture `🚧 materials pending` in the plan doc.
3. **No objectives either** → title only, `confidence: low`, and say so explicitly in the doc.

A lecture whose materials you can't find is **never silently skipped** — it appears in the plan with
its confidence flag so you know the prep is a guess.

> Mirrors `anki-week` Stage 0. If both skills run for the same week, reuse the inventory rather than
> re-reading the slides twice.

## Stage 2 · Read window busy-time

- `list_events(personal_calendar_id, week_start, week_end)`.
- For each day, start from the day's window (`weekday_window` or `weekend_window`; treat US holidays
  and school-holiday days as weekend windows). Subtract everything that occupies the window:
  1. **In-window class events from Stage 1** — most lectures are mornings (outside the window), but
     afternoon lectures and review sessions DO fall inside it (e.g. a 1–3 PM lecture, a 1–5 PM midterm
     review). These block time; never place a study block over them.
  2. **Personal-calendar events** in the window — workouts, chores, meetings, `🟡 Proposed —` blocks
     staged by `daily-schedule-assistant`, and **study-week's own committed blocks from a previous run**
     (they're ordinary BUSY events now, so they carve out time like anything else — including after
     you have moved one).
  What remains = that day's **free intervals** inside the window.
- **Optional class sessions** (title contains `Optional`/`voluntary`, e.g. "Optional Supplemental
  Session") are treated as non-blocking — you may skip them; don't reserve around them, but note the
  overlap in the doc so you can decide.
- Ignore free/transparent all-day items and reminder nudges (same rules as daily-schedule-assistant).

## Stage 3 · Anki reserve (per day)

- If `mode = off`: reserve 0.
- If `mode = fixed`: reserve = `anki_reserve_fallback_min`.
- If `mode = rolling-avg`:
  1. `find_notes("deck:<anki_deck> rated:<anki_window_days>")` → count of cards reviewed in the
     look-back window. (If the MCP query errors or returns empty, fall back to
     `anki_reserve_fallback_min` and flag "Anki estimate unavailable".)
  2. `per_day_cards = count / anki_window_days`.
  3. `reserve_min = round(per_day_cards * anki_sec_per_card / 60)`, clamped to
     `[0, anki_reserve_cap_min]`.
- The reserve is one `Anki review (~<reserve_min> min)` block per study day, placed at the **start** of
  that day's first free interval (reviews first), before B&B packing.

## Stage 4 · Map concepts → B&B  (cover the inventory)

Map from the **Stage-1.5 concept inventory**, not the lecture title. The goal is a video set that
**covers everything the lecture teaches** — "bigger than the materials is fine, smaller is not."

For each lecture, in order:
1. Check `data/lecture-map.md` for a confirmed mapping. Reuse it — **then verify it still covers the
   current inventory** (professors revise decks; a mapping confirmed in June can under-cover in July).
2. Else search `bb-videos.json` for the leaf video(s) whose subject matches — **working concept by
   concept, not lecture by lecture.** Walk the inventory and ask "which video teaches this?" A lecture
   spanning cell signaling + second messengers + receptor classes maps to **all three** videos.
   **Several videos per lecture is the normal case**, not an exception.
3. **Coverage check (the floor):** lay the chosen video set against the inventory and mark any concept
   no video covers. Try a wider/adjacent leaf to close it. If nothing covers it, record it as a
   **`coverage_gap`** for the plan doc — you need to know that part of the lecture has no video
   and you'll be meeting it cold (or via Anki only).
4. **Prefer over- to under-coverage.** When torn between a narrow video that covers most of a concept
   and a broader one that covers all of it plus adjacent material, take the broader one. Only drop to
   the narrow one when the window genuinely can't hold the runtime — and say so.
5. Several lectures may share a video → **dedupe**: schedule it once, before the earliest of them.
6. **Filter against the watched memory** (`data/watched-videos.md`, per `config.md`):
   - Match by **title**, case-insensitive with whitespace collapsed (titles are globally unique).
   - `watched` / `skip` → **don't schedule it.** Keep it in the mapping table marked
     `✓ watched <date>`; **its concepts stay covered** — this is not a `coverage_gap`.
   - `partial` → treat as **not** watched; schedule it normally.
   - `rewatch_after_days` set and the watch date is older than that → back into the schedulable pool.
   - A row in the watched log matching **no** library video → **flag it** in the plan doc
     ("watched-log entry `<title>` matches no B&B video — typo or retired?"). Never ignore it silently.
7. No clean match for the whole lecture → mark `attend_only` (no block).
8. Record new confirmed mappings to append to `lecture-map.md` in Stage 6, with the concepts each
   video was chosen to cover (so the next run can re-verify coverage, not just re-use a title match).

Produce a mapping table:
`lecture → [videos w/ minutes, ✓watched?] | total_min to schedule | concepts_covered / concepts_total | coverage_gaps | confidence | attend_only?`

## Stage 5 · Pack the window (pre-lecture, front-loaded)

Goal: every mapped video sits in a free interval **before its lecture**, days packed earliest-first so
capacity isn't wasted, honoring caps.

Algorithm (greedy, earliest-fit, deadline-aware):
1. Build a worklist of `{video, deadline = lecture.start}`; sort by deadline asc, then subject to keep
   a lecture's videos together.
2. Walk study days from `week_start` forward. For each day: available = free intervals minus the
   day's Anki reserve; remaining-cap = `cap_hours*60 − minutes_already_placed_that_day`.
3. Place the next not-yet-placed video whose `deadline` is after this day's end, into the earliest
   free interval that fits, respecting `remaining-cap`, `min_block_min`, `max_block_min`. Group
   consecutive same-lecture/adjacent videos into one contiguous block (split at `max_block_min` with a
   short gap).
4. If a video's `deadline` arrives with the video unplaced (no capacity before it), mark it
   `couldnt_fit` — do NOT push it past its lecture and do NOT overrun a cap. **A `couldnt_fit` is a
   coverage shortfall, not a scheduling detail:** name the lecture AND the concepts that go unprepped,
   and surface it at the top of the plan doc. Capacity limits may shrink the *schedule*; they never
   justify quietly shrinking the *mapping* in Stage 4.
5. On light early days with spare capacity, pull **later-week** videos (and, if the week's lectures
   are all placed, next-block/exam-prep videos) forward to fill — never exceeding caps.

Each resulting block → an event spec: `{day, start, end, title, video_list, preps:[lectures]}`.

## Stage 6 · Emit — doc, then events, then log

**A. Plan doc** → `<plans_dir>/<week_start>-week.md`:
- Header: week range; # lectures; total B&B minutes; Anki reserve/day used (+ how derived);
  any "Anki estimate unavailable" flag; **how many lectures had materials read vs. objective-derived**.
- **Coverage summary up top** — the floor report: `concepts covered / total` for the week, plus any
  `coverage_gap` (no video teaches it) and any `couldnt_fit` (video exists, no room before the
  lecture). If coverage is complete, say so plainly ("all 47 concepts covered"). Note separately how
  many videos were **skipped as already watched** (with the time that freed) — covered, not missing.
- Any **unmatched watched-log rows** (a title matching no B&B video — typo or retired video).
- Per-day schedule table: `start–end | activity | min | preps`.
- Lecture → B&B mapping table: `lecture | videos (min) | concepts covered/total | gaps | confidence`
  (incl. `attend only — no B&B` rows and `🚧 materials pending` rows).
- Flags: unmatched lectures, `couldnt_fit` videos (with the lecture **and concepts** they were for),
  low-confidence mappings, days over/under target.

**B. Committed calendar events** (personal calendar) — one per block + the per-day Anki block:
- Use the **committed-event convention** from config: **no `🟡 Proposed —` prefix**, `colorId 5`,
  **BUSY**, 120+15 reminders, and a description ending in the `[study-week:<week_start>]` signature.
  These are real commitments you can move or delete yourself — there is no accept/reject step.
- **Idempotency (titles no longer carry a marker, so use the ids):**
  1. Look up this week's previously-created event ids in the run-log; fall back to matching the
     `[study-week:<week_start>]` description signature over the week range.
  2. **A logged event that still exists counts as satisfied — even if its start/end no longer match the
     plan.** You moved it deliberately: **leave it alone, don't recreate it, don't move it back.**
  3. Only create events that are genuinely missing (deleted, or never made).
  4. If the week materially changed (lectures added/removed, concept inventory changed), offer to
     **replace**: delete this week's logged events, then re-create. Never silently duplicate.
- **Never modify or overlap** an event with other attendees, or any existing block; blocks only land in
  the free intervals computed in Stage 2.
- Because these are BUSY, they now **participate in `daily-schedule-assistant`'s conflict scan** — that
  is intentional (it's what protects the time), but it means a later meeting booked over a study block
  will surface as a real conflict.

**C. Log** → append to `data/run-log.md`: date run, week, # lectures, # blocks, total minutes, Anki
reserve used, and the **created event ids** (for undo/replace). Append newly-confirmed mappings to
`data/lecture-map.md`.

**D. Update the watched memory** → `data/watched-videos.md`:
- List the **previous** run's scheduled videos (from the run-log) and ask which ones you actually
  watched. Append a row per confirmation: `| <title> | <subject> | watched | <date> | <IM##> | |`.
- **Never auto-mark this run's videos as watched** — scheduling is not watching, and a block he didn't
  get to must not silently count as done. Only an explicit confirmation (or his own hand-edit) writes
  a `watched` row.
- If he says "I got halfway through X" → `partial` (it stays schedulable).
- Skip the question entirely on a first run, or when the previous run staged nothing.

## Guardrails

- Write only to the personal calendar. Blocks are **committed** (BUSY, no prefix) — you move or
  delete them yourself; there's no accept step to wait on. Never touch events with other attendees.
- **Respect a moved block.** If a previously-created event still exists, that's your decision —
  never "correct" its time back to the plan, and never duplicate it.
- Respect caps and the window absolutely — if prep won't fit before a lecture, flag it, don't overrun.
- **Coverage is a floor, capacity is a ceiling — report the collision, never hide it.** Map what the
  materials require (Stage 4), then schedule what fits (Stage 5); when they disagree, the plan doc says
  so. Never resolve the conflict by mapping fewer videos.
- If a calendar can't be read, do nothing destructive; write the doc with what you have and say what
  was missing. Same for unreadable materials — fall back down the ladder and flag the confidence.
- Mornings and work are out of scope by design — never place a block before the window starts.

## Undo a run

Delete the events whose ids are listed under this week's entry in `data/run-log.md` — or, if the log is
unavailable, every event in the week range whose description carries the `[study-week:<week_start>]`
signature. (Titles no longer carry a marker, so **don't** try to undo by title match — `B&B:` /
`Anki review` prefixes are not reliable identifiers and could catch your own events.)
