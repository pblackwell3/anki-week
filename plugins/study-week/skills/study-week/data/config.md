# study-week — Config  (EDIT THIS FIRST)

Single source of truth for the `study-week` skill. The skill reads this at the start of every run.
Rows marked **← SET THIS** are yours.

## Calendars

| Key | Value | Notes |
|---|---|---|
| `class_calendar_id` | `← SET THIS` | Your class calendar — holds the numbered IM lectures (`IM (NN) Title`). READ only. |
| `personal_calendar_id` | `← SET THIS` (your primary calendar) | The ONLY calendar the skill writes to. Also read to carve around existing events. |

Mornings are left alone; the skill only proposes blocks inside the study window below.

## Lecture materials (Stage 1.5 — read these BEFORE mapping videos)

| Key | Value | Notes |
|---|---|---|
| `course_folder` | `← SET THIS` (e.g. `~/Lecture Materials`) | Local archive, **same path as `anki-week`'s config**. Layout: `<course_folder>/<Course>/Week <n>/` with materials directly inside. A week can span multiple `<Course>` folders — gather all `*/Week <n>/`. **"Materials" = these slide FILES (PPTX/PDF) only** — an Anki deck named `Meharry Slides` is not materials, never satisfies this check, and is never read for scope. |
| `blackboard_url` | `← SET THIS` (e.g. `https://blackboard.yourschool.edu/`) | Your school's LMS login / course-list page. When a lecture's materials are missing from `course_folder`, Stage 1.5 fetches them from here rather than guessing from the title. Same value as `anki-week`'s. **No credentials are stored** — if you're not logged in, the skill stops and asks you to log in. |

## Study window & caps

| Key | Value | Notes |
|---|---|---|
| `weekday_window` | `14:00–20:00` | Where blocks go on class days (2–8 PM). |
| `weekend_window` | `12:00–20:00` | Wider on Sat/Sun & holidays. |
| `weekday_cap_hours` | `6` | Ceiling of study/day on class days. |
| `weekend_cap_hours` | `8` | Ceiling on weekends/holidays. |
| `min_block_min` | `20` | Don't stage a block shorter than this. |
| `max_block_min` | `120` | Split longer runs into separate events with a break. |

## Video library (which resource the plan maps to)

Two libraries ship with the skill. **Pick the one you actually study from** — the plan is only as
useful as the videos it points you at.

| Key | Value | Notes |
|---|---|---|
| `video_library` | `auto` | `auto` \| `bb` \| `bootcamp` \| `both`. `auto` = follow anki-week's `backbone_resource`: `#Bootcamp` → `bootcamp`, anything else → `bb`. Set it explicitly if you don't run anki-week. |

| Value | File | What it is |
|---|---|---|
| `bb` | `data/bb-videos.json` | **Boards & Beyond** — Step 1 Preclinical. 22 subjects / 502 videos / 9,003 min. Per-video `video_index` (the site's own keyword index), `description`, First Aid page refs, `quiz_count`. |
| `bootcamp` | `data/bootcamp-videos.json` | **Med School Bootcamp** — Step 1 Preclinical + Step 2 Clinical (Preview) + Anatomy Bootcamp (Gross Anatomy, Neuroanatomy, Histology, OMM). 26 subjects / 2,724 catalog entries (2,705 unique videos) / 26,175 min. Per-video `source_keywords` (Bootcamp's own keyword string), exact `duration`, `subject_tags` / `concept_tags`, `route`. `description` is `null` — Bootcamp doesn't publish per-video prose. |
| `both` | both files | Map against both and take the better cover per concept. Label every video with its library in the plan doc and the lecture map — **titles are not unique across the two libraries.** |

**Video identity (matters for the watched log and the lecture map):**

| Library | Key | Why |
|---|---|---|
| `bb` | `title` | Globally unique across all 502 videos. |
| `bootcamp` | `Subject › Section › Title` | Titles repeat by design — `Board-style Question Breakdown` appears **166 times**, `Case Progression I` 25 times. A bare title is ambiguous; always qualify it. Two `Subject › Section › Title` pairs still collide (`Gross Anatomy › Anterior & Medial Thigh, Knee › Knee Joint`, `Histology › Blood & Blood Formation › Bone Marrow - Overview`) — use the video's `route` there. |

## Resource timing & mapping

- **Pre-lecture prep:** a lecture's mapped video(s) must be scheduled before that lecture starts; pull forward onto earlier light days rather than leaving window capacity idle.
- **Primary lens = your `video_library`** (resolved from `backbone_resource` when it's `auto`). Map each lecture to its video(s) by subject, not title keywords. Dedupe a video shared by two lectures — in `bootcamp` that includes the 19 cross-listed entries, which are one underlying video published under two sections (`cross_listed_under` records the alternates; schedule it once).
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
