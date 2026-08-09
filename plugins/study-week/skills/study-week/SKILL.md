---
name: study-week
description: >-
  Build your weekly medical-school study plan. Reads the coming week's lectures from your class
  calendar (config `class_calendar_id`) to know which lecture materials to pull, then READS THOSE
  MATERIALS (slides/PDF) to build each lecture's concept inventory and maps that inventory — not the
  lecture title — to its Boards & Beyond video(s) with runtimes, choosing a video set that covers
  everything the lecture teaches. Reserves a daily Anki-review block from your recent review volume and
  packs pre-lecture study blocks into your 2–8 PM weekday window (wider on weekends). Emits BOTH a
  written weekly plan doc AND committed calendar events on your personal calendar — real blocks you can
  move or delete yourself, not proposals awaiting approval.
  Reads data/config.md for calendars, the course-materials folder, the study window, caps, and
  Anki settings. Does NOT build Anki decks — that's the separate anki-week skill; this plans time
  around whatever decks exist. Requires the Google Calendar MCP (and, for the rolling-average Anki
  reserve, the Anki MCP).
---

# study-week

## Overview

Turn the coming week's lectures into a concrete study plan: **what B&B to watch, when, plus reserved
Anki time**, placed into the real open time in your 2–8 PM study window — delivered as a plan doc
and **committed calendar events**. Sibling to `anki-week` (which builds the cards) and
`daily-schedule-assistant`. **Pre-lecture prep:** a lecture's B&B videos are scheduled before that
lecture.

**Committed, not proposed (2026-07-31).** Study blocks go on the calendar as real BUSY events with no
`🟡 Proposed — ` prefix and no accept step. If a block needs to move, **you move it** — and a
re-run leaves moved blocks exactly where you put them. This intentionally diverges from
`daily-schedule-assistant`, which still stages its obligations as proposals.

**Materials-driven (same rule as `anki-week`).** The calendar is an **index** — it tells you which
lectures exist so you know **which materials to go read**. Then you **read those materials** and map
the lecture's **concept inventory** to B&B videos. You are picking videos to cover *what the professor
will actually teach*, not what the lecture title sounds like.

**📄 "Materials" = the professor's slide FILES only — never an Anki deck.** Same definition as
`anki-week`: `.pptx` / `.ppt` / `.pdf` in `<course_folder>/<Course>/Week <n>/`, or fetched from
`blackboard_url`. **An Anki deck named `Meharry Slides`** (or any slides-named deck) is pre-made cards,
**not** the lecture — never read it for the concept inventory, and never let it count as "materials
found." Checking for materials is a **file check**; no PPTX/PDF → the lecture has no materials → the
fetch ladder → Blackboard. This skill touches Anki only to size your **review load**, never for scope.

**⬆️ The floor rule: never plan LESS video than the materials require.** If a lecture's concepts span
three B&B videos, schedule all three — a single title-matched video that covers half the lecture is a
planning failure. Going **bigger** (an extra adjacent video, a deeper section) is fine; going smaller
is not. When the week's video load genuinely won't fit the window, **flag it** — never silently drop
coverage to make the calendar look tidy.

## When to use

- Start of a study week / "plan my week", "what should I study", "build this week's study blocks".
- After the week's lectures are on the Class calendar. Decoupled from deck-building — accuracy assumes
  the matching Anki cards exist, but this skill never unsuspends or creates cards.

## Prerequisites

- **Google Calendar MCP** connected: reads your class calendar (config `class_calendar_id`) for lectures
  + Personal (busy time), writes Personal (committed study blocks). IDs in `data/config.md`.
- **Read access to the course-materials folder** (`course_folder` in `data/config.md`) — Stage 1.5 reads
  the week's slides/PDFs. Without it the skill still runs, but every mapping is `low-confidence`
  (title/objective-derived) and the plan doc must say so.
- **Anki MCP** only if `anki_reserve_mode = rolling-avg` — else it uses the fixed fallback. If Anki is
  down, the skill still runs and flags the estimate as unavailable.
- `data/bb-videos.json` present — the B&B library (22 subjects / **496 videos**). Rebuild when B&B
  changes: `python3 data/build-bb-videos.py <checklist.pdf>` (PyMuPDF, falling back to macOS PDFKit).
- `data/watched-videos.md` — what you have already watched. Read every run; empty is fine.

## The procedure

Run the detailed steps in **reference/playbook.md**. Summary:

| Stage | What | Key tools |
|---|---|---|
| 0 · Week | Resolve the target week (default: coming Mon–Sun) from `config.md`. | — |
| 1 · Lectures | Read the week's `IM (NN)` sessions from the Class calendar → ordered lecture list. **This is the index of what to read next, not the scope.** | `list_events` |
| **1.4 · Fetch** | Any lecture with no **PPTX/PDF on disk** in `<course_folder>/<Course>/Week <n>/` → **fetch before mapping** (an Anki `Meharry Slides` deck does not count as having materials). See *Materials missing → FETCH* below. | browser |
| **1.5 · Materials** | **READ each lecture's materials** from `<course_folder>/<Course>/Week <n>/` (PPTX→`pptx`, PDF→`pdf`) → a **concept inventory** per lecture. Still no materials after Stage 1.4 → fall back to syllabus objectives/title and mark the mapping `low-confidence`. | Read, `pptx`/`pdf` |
| 2 · Busy | Read Personal calendar; per day, subtract window events → free intervals in the 2–8 PM window. | `list_events` |
| 3 · Anki | Reserve a daily review block from recent review volume (`find_notes deck:… rated:N`), or the fixed fallback. Reviews go first. | `find_notes` |
| 4 · Map | Map each lecture's **concept inventory** → the B&B leaf video(s) that **cover all of it** (reuse `data/lecture-map.md`); several videos per lecture is normal and correct. Then drop anything already in `watched-videos.md` (still counts as covered). Flag no-match lectures as attend-only, and flag concepts no video covers. | Read `bb-videos.json`, `watched-videos.md` |
| 5 · Pack | Greedy earliest-fit: place each video before its lecture, front-loading light days, honoring caps; flag anything that won't fit. | — |
| 6 · Emit | Write the plan doc → create **committed** events (no prefix, Banana, **BUSY**, 120+15 reminders, `[study-week:<week>]` in the description) → log run + event ids → append new mappings → confirm which of *last* run's videos were watched and record them. | `create_event`, Write |

## Key rules

- **Window:** blocks only inside 2–8 PM weekdays (wider weekends). Never mornings — you handle
  morning lecture overlaps and occasional afternoon meetings yourself. Work isn't on the calendar; ignore it.
- **Pre-lecture:** every mapped video lands before its lecture, or is flagged "couldn't fit" — never
  pushed past the lecture, never over a cap.
- **Commit, don't propose:** blocks are real BUSY events on the personal calendar only — no prefix, no
  approval step. Never touch events with other attendees. **You move or delete them yourself, and
  a re-run respects that** (a still-existing block is left where you put it, never recreated or
  re-timed).
- **B&B primary lens:** map by subject via `bb-videos.json`; dedupe shared videos.
- **Cover the materials:** the mapped video set must cover the lecture's whole concept inventory.
  Under-covering is a defect; over-covering is fine. Surface uncovered concepts in the plan doc.

### Materials missing → FETCH, never silently degrade

Same rule as `anki-week` — a missing file must not quietly become a title-derived guess. For any
lecture with **no PPTX/PDF** in `<course_folder>/<Course>/Week <n>/` — a `Meharry Slides` deck in Anki
is not a substitute and does not skip this ladder — work it and stop at the first rung that succeeds:

1. **Browser available → fetch it.** Open `blackboard_url`, find that course's materials area, and
   download the missing files into that lecture's week folder. Not logged in → **STOP and ask the user
   to log in**, then continue.
2. **No browser on this surface → hand it back.** Say so plainly, name the exact folder the files
   belong in, and suggest re-running in **Claude Cowork**. **Then wait.**
3. **Only if both fail** → fall back to objectives/title, mark the mapping `low-confidence`, and flag
   the lecture **🚧 materials pending** in the plan doc.

Mapping a video off a lecture *title* is the failure mode this prevents: the title says what the
lecture is called, the materials say what it teaches, and only the second one picks the right video.
- **Don't re-schedule watched videos.** Skip anything in `data/watched-videos.md` — but it still
  **counts as covering** its concepts (`✓ watched`), so skipping never creates a coverage gap.
  Scheduling a video never marks it watched; only an explicit confirmation does.

## Common mistakes

- Placing study in the morning or over an existing block — blocks go only in computed free window intervals.
- **Mapping videos without reading the materials.** The calendar title is a pointer to the lecture, not
  the lecture. Read the slides, then map.
- **Treating an Anki deck as the lecture materials.** A deck named **`Meharry Slides`** is someone's
  pre-made cards — mapping videos off it means covering *their* card selection instead of the
  professor's slides. Materials are **files**; no file → fetch from Blackboard.
- **Stopping at one video per lecture.** A lecture routinely spans several B&B leaves; one title-matched
  video that covers a third of the slides leaves you unprepared. Map the whole inventory.
- Mapping by lecture title keyword instead of subject (e.g. a "Cell Signaling" lecture → the right B&B
  leaf, not any video with "cell" in it). Verify subject; record the confirmed mapping.
- **Silently dropping coverage to fit the window.** If the week's videos won't fit, flag the overflow —
  don't quietly plan less than the lectures require.
- **Counting a watched video as a coverage gap.** Skipping it frees time; the concept is still covered
  (it was covered by watching it). Only a concept *no* video teaches is a real gap.
- **Marking a video watched because it was scheduled.** A block you never got to isn't done — only
  an explicit confirmation or a hand-edited row writes a `watched` status.
- Forecasting exact Anki due counts (they change on the weekly rebuild) — use the rolling-average estimate.
- **Moving a block you already moved.** If a logged event still exists, that placement is your
  decision — leave it. Only a deleted block gets re-created.
- Duplicating on re-run — match by run-log event ids (or the `[study-week:<week>]` description
  signature), never by title; offer replace rather than restage.
- Undoing by title match — `B&B:` / `Anki review` are not reliable identifiers now that the prefix is
  gone and could catch your own events. Use the ids/signature.

## Artifacts

- `data/config.md` — calendars, window, caps, Anki knobs. **Edit first.**
- `data/bb-videos.json` — B&B video library (subject → sections → videos). Rebuilt via `build-bb-videos.py`.
- `data/lecture-map.md` — confirmed lecture→B&B mappings; grows each run.
- `data/watched-videos.md` — **the watched memory**: videos already consumed, so they aren't re-staged.
- `data/run-log.md` — per-week audit trail + created event ids (undo/replace).
- `reference/playbook.md` — the full procedure.
- `study-plans/<week>-week.md` — the weekly plan doc output.
