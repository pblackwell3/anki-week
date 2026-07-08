---
name: study-week
description: >-
  Build your weekly medical-school study plan. Reads the coming week's IM lectures from the
  class calendar (config `class_calendar_id`), maps each lecture to its Boards & Beyond video(s) with runtimes, reserves
  a daily Anki-review block from your recent review volume, and packs pre-lecture study blocks into your
  2–8 PM weekday window (wider on weekends). Emits BOTH a written weekly plan doc AND `🟡 Proposed —`
  calendar events on your personal calendar for you to accept or delete. Reads data/config.md for
  calendars, the study window, caps, and Anki settings. Does NOT build Anki decks — that's the separate
  anki-week skill; this plans time around whatever decks exist. Requires the Google Calendar MCP
  (and, for the rolling-average Anki reserve, the Anki MCP).
---

# study-week

## Overview

Turn the coming week's lectures into a concrete study plan: **what B&B to watch, when, plus reserved
Anki time**, placed into the real open time in your 2–8 PM study window — delivered as a plan doc
and proposed calendar events you approve. Sibling to `anki-week` (which builds the cards) and
`daily-schedule-assistant` (whose calendar conventions this matches). **Pre-lecture prep:** a lecture's
B&B videos are scheduled before that lecture.

## When to use

- Start of a study week / "plan my week", "what should I study", "build this week's study blocks".
- After the week's lectures are on the Class calendar. Decoupled from deck-building — accuracy assumes
  the matching Anki cards exist, but this skill never unsuspends or creates cards.

## Prerequisites

- **Google Calendar MCP** connected: reads the class calendar (config `class_calendar_id`) for lectures + Personal (busy time), writes
  Personal (proposed events). IDs in `data/config.md`.
- **Anki MCP** only if `anki_reserve_mode = rolling-avg` — else it uses the fixed fallback. If Anki is
  down, the skill still runs and flags the estimate as unavailable.
- `data/bb-videos.json` present (rebuild with `data/build-bb-videos.py <checklist.pdf>` when B&B changes).

## The procedure

Run the detailed steps in **reference/playbook.md**. Summary:

| Stage | What | Key tools |
|---|---|---|
| 0 · Week | Resolve the target week (default: coming Mon–Sun) from `config.md`. | — |
| 1 · Lectures | Read the week's `IM (NN)` sessions from the Class calendar → ordered lecture list. | `list_events` |
| 2 · Busy | Read Personal calendar; per day, subtract window events → free intervals in the 2–8 PM window. | `list_events` |
| 3 · Anki | Reserve a daily review block from recent review volume (`find_notes deck:… rated:N`), or the fixed fallback. Reviews go first. | `find_notes` |
| 4 · Map | Map each lecture → B&B leaf video(s) by subject (reuse `data/lecture-map.md`); flag no-match lectures as attend-only. | Read `bb-videos.json` |
| 5 · Pack | Greedy earliest-fit: place each video before its lecture, front-loading light days, honoring caps; flag anything that won't fit. | — |
| 6 · Emit | Write the plan doc → stage `🟡 Proposed —` events (Banana, FREE, 120+15 reminders) → log run + event ids → append new mappings. | `create_event`, Write |

## Key rules

- **Window:** blocks only inside 2–8 PM weekdays (wider weekends). Never mornings — you handle
  morning lecture overlaps and occasional afternoon meetings yourself. Work isn't on the calendar; ignore it.
- **Pre-lecture:** every mapped video lands before its lecture, or is flagged "couldn't fit" — never
  pushed past the lecture, never over a cap.
- **Propose, never commit:** everything staged is `🟡 Proposed —` and FREE, on the personal calendar
  only; never touch events with other attendees. You accept or delete.
- **B&B primary lens:** map by subject via `bb-videos.json`; dedupe shared videos.

## Common mistakes

- Placing study in the morning or over an existing block — blocks go only in computed free window intervals.
- Mapping by lecture title keyword instead of subject (e.g. a "Cell Signaling" lecture → the right B&B
  leaf, not any video with "cell" in it). Verify subject; record the confirmed mapping.
- Forecasting exact Anki due counts (they change on the weekly rebuild) — use the rolling-average estimate.
- Writing hard commitments — always proposed/FREE until you accept.
- Duplicating on re-run — check for existing proposed blocks / offer replace via run-log ids.

## Artifacts

- `data/config.md` — calendars, window, caps, Anki knobs. **Edit first.**
- `data/bb-videos.json` — B&B video library (subject → sections → videos). Rebuilt via `build-bb-videos.py`.
- `data/lecture-map.md` — confirmed lecture→B&B mappings; grows each run.
- `data/run-log.md` — per-week audit trail + created event ids (undo/replace).
- `reference/playbook.md` — the full procedure.
- `study-plans/<week>-week.md` — the weekly plan doc output.
