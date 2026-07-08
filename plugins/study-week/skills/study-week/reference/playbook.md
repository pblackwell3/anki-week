# study-week — Playbook

The full procedure. SKILL.md is the summary; this is what to actually do each run. All times
**America/Chicago**. Read `data/config.md` first — every knob below comes from it.

## Prerequisites (check first)

- **Google Calendar MCP** connected (read Class + Personal, write Personal).
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
- Result: an ordered list of the week's lectures.

## Stage 2 · Read window busy-time

- `list_events(personal_calendar_id, week_start, week_end)`.
- For each day, start from the day's window (`weekday_window` or `weekend_window`; treat US holidays
  and school-holiday days as weekend windows). Subtract everything that occupies the window:
  1. **In-window class events from Stage 1** — most lectures are mornings (outside the window), but
     afternoon lectures and review sessions DO fall inside it (e.g. a 1–3 PM lecture, a 1–5 PM midterm
     review). These block time; never place a study block over them.
  2. **Personal-calendar events** in the window — workouts, chores, meetings, existing `🟡 Proposed —`
     blocks.
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
- The reserve is one `🟡 Proposed — Anki review (~<reserve_min> min)` block per study day, placed at
  the **start** of that day's first free interval (reviews first), before B&B packing.

## Stage 4 · Map lectures → B&B

For each lecture, in order:
1. Check `data/lecture-map.md` for a confirmed mapping of this lecture title → B&B video(s). Reuse it.
2. Else search `bb-videos.json` for the leaf video(s) whose subject/topic matches the lecture's
   subject (not just a title keyword). One lecture may map to several videos; several lectures may
   share one (dedupe — schedule the shared video once, before the earliest of them).
3. No clean match → mark `attend_only` (no block).
4. Record new confirmed mappings to append to `lecture-map.md` in Stage 6.

Produce a mapping table: `lecture → [videos w/ minutes] | total_min | attend_only?`.

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
   `couldnt_fit` — do NOT push it past its lecture and do NOT overrun a cap.
5. On light early days with spare capacity, pull **later-week** videos (and, if the week's lectures
   are all placed, next-block/exam-prep videos) forward to fill — never exceeding caps.

Each resulting block → an event spec: `{day, start, end, title, video_list, preps:[lectures]}`.

## Stage 6 · Emit — doc, then events, then log

**A. Plan doc** → `<plans_dir>/<week_start>-week.md`:
- Header: week range; # lectures; total B&B minutes; Anki reserve/day used (+ how derived);
  any "Anki estimate unavailable" flag.
- Per-day schedule table: `start–end | activity | min | preps`.
- Lecture → B&B mapping table (incl. `attend only — no B&B` rows).
- Flags: unmatched lectures, `couldnt_fit` videos (with the lecture they were for), days over/under target.

**B. Proposed calendar events** (personal calendar) — one per block + the per-day Anki block:
- Use the proposed-item convention from config (prefix, `colorId 5`, FREE, 120+15 reminders, description).
- Idempotency: before creating, check an identical `🟡 Proposed —` block isn't already on that day/time
  (re-run safety). If this week was already run (see run-log), offer to **replace**: delete this week's
  previously-created study-week events (ids in run-log) first, then re-create.
- **Never modify or overlap** an event with other attendees, or any existing block; blocks only land in
  the free intervals computed in Stage 2.

**C. Log** → append to `data/run-log.md`: date run, week, # lectures, # blocks, total minutes, Anki
reserve used, and the **created event ids** (for undo/replace). Append newly-confirmed mappings to
`data/lecture-map.md`.

## Guardrails

- Write only to the personal calendar; everything staged is `🟡 Proposed —` (FREE) for you to
  accept or delete. Never touch events with other attendees.
- Respect caps and the window absolutely — if prep won't fit before a lecture, flag it, don't overrun.
- If a calendar can't be read, do nothing destructive; write the doc with what you have and say what
  was missing.
- Mornings and work are out of scope by design — never place a block before the window starts.

## Undo a run

Delete the events whose ids are listed under this week's entry in `data/run-log.md` (or delete every
`🟡 Proposed — B&B:` / `🟡 Proposed — Anki review` event in the week range).
