# study-week — Config  (EDIT THIS FIRST)

Single source of truth for the `study-week` skill. The skill reads this at the start of every run.
Rows marked **← SET THIS** are yours.

## Calendars

| Key | Value | Notes |
|---|---|---|
| `class_calendar_id` | `← SET THIS` | Your class calendar — holds the numbered IM lectures (`IM (NN) Title`). READ only. |
| `personal_calendar_id` | `← SET THIS` (your primary calendar) | The ONLY calendar the skill writes to. Also read to carve around existing events. |

Mornings are left alone; the skill only proposes blocks inside the study window below.

## Study window & caps

| Key | Value | Notes |
|---|---|---|
| `weekday_window` | `14:00–20:00` | Where blocks go on class days (2–8 PM). |
| `weekend_window` | `12:00–20:00` | Wider on Sat/Sun & holidays. |
| `weekday_cap_hours` | `6` | Ceiling of study/day on class days. |
| `weekend_cap_hours` | `8` | Ceiling on weekends/holidays. |
| `min_block_min` | `20` | Don't stage a block shorter than this. |
| `max_block_min` | `120` | Split longer runs into separate events with a break. |

## Resource timing & mapping

- **Pre-lecture prep:** a lecture's mapped video(s) must be scheduled before that lecture starts; pull forward onto earlier light days rather than leaving window capacity idle.
- **Primary lens = your `backbone_resource`** from anki-week's config (`bb-videos.json` holds a Boards & Beyond index; swap or extend for another resource). Map each lecture to its video(s) by subject, not title keywords. Dedupe a video shared by two lectures.
- Non-content sessions (Formative, Peer Instruction, communication, library training, exam/review) get **no block** — list them under "attend only".

## Anki review reserve

Reserve a daily Anki block from a stable estimate:

| Key | Value | Notes |
|---|---|---|
| `anki_reserve_mode` | `rolling-avg` | `rolling-avg` \| `fixed` \| `off`. |
| `anki_deck` | `AnKing Step Deck` | Deck to scope the review-volume query to. |
| `anki_window_days` | `7` | Look-back for the rolling average. |
| `anki_sec_per_card` | `10` | Seconds/card to convert review count → minutes. |
| `anki_reserve_fallback_min` | `60` | Used if Anki is unreachable, or if `mode = fixed`. |
| `anki_reserve_cap_min` | `120` | Never reserve more than this per day. |

## Outputs

| Key | Value | Notes |
|---|---|---|
| `plans_dir` | `study-plans/` | Where weekly plan docs are written (`YYYY-MM-DD-week.md`). |
| `current_week` | `upcoming` | `upcoming` = the coming Mon–Sun; or set an explicit `YYYY-MM-DD`. |

## Proposed-item convention

- Title prefix: **`🟡 Proposed — `**; color Banana (`colorId 5`); availability FREE.
- Accepting = remove the prefix. The skill won't restage an identical block.
