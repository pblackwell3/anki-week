# anki-week — Config

Edit these to match **your** setup. The skill reads this at Stage 0. Most values are a shared
Meharry M1 preset; the rows marked **← SET THIS** are yours.

| Key | Value | Notes |
|---|---|---|
| `course_folder` | `← SET THIS` (e.g. `~/Lecture Materials`) | Your local folder of lecture slides. Layout: `<course_folder>/<Course>/Week <n>/` with the PPTX/PDF directly inside. |
| `syllabus` | `← SET THIS` (path to your syllabus `.docx`/`.pdf`) | **Read in Stage 0.** Its Course Outline table gives each lecture's Learning Objectives = the authoritative card scope. You already have this as an enrolled student — point the skill at your own copy. |
| `current_week` | `1` | Curriculum week to build. Bump each week. |
| `class_calendar_id` | `← SET THIS` | The class calendar that lists the numbered IM lectures (`IM (n) Title`). Subscribe to the shared class calendar and paste its id (a long string ending in `calendar.google.com`), or leave blank and feed lectures manually. |
| `deck_name` | `AnKing Step Deck` | The card-source library. |
| `tag_namespace` | `#AK_Step1_v12` | Step-deck tag root. Setup detects your actual version and writes it here. |
| `backbone_resource` | `#B&B` | **Your primary study resource = the deck's backbone + naming lens.** Options that live under `tag_namespace`: `#B&B` (Boards & Beyond), `#Pathoma`, `#FirstAid`, `#Physeo`, `#Bootcamp`, `#SketchyMicro` / `#SketchyPharm` / `#SketchyPhysiology`, `#DirtyMedicine`, or `^Systems` (body-system tree). Map each lecture's objectives to leaves under THIS tree first; fall back to other trees only where your backbone has no clean leaf. Setup writes this from what it finds in your deck. |
| `yield_filter` | `1+2` | AnKing high-yield tiers to include: `1` = High-Yield only · `1+2` = + Relatively-High-Yield (recommended) · `1+2+3` = + High-Yield-temporary · `off` = all tiers. Foundational/intro/definitional lectures auto-include all tiers regardless. |
| `new_per_day_cap` | `25` | Runaway ceiling for new cards/day. The MCP can't set New/day — set it in Anki ▸ deck ▸ Options ▸ New cards/day. |
| `leaf_size_hint` | `60` | A tag subtree bigger than this (notes) is "too high" — descend to leaves. |

## Method (backbone + coverage supplement)

1. **Your `backbone_resource` IS the deck + naming lens.** Map each lecture's objectives to its leaf tags; deck names follow that resource's chapter topics.
2. **Supplement from other trees ONLY to fill specific coverage gaps** — pull the individual card that closes a gap, never a whole other chapter (that over-pulls). Author a custom card only for genuine framework gaps AnKing has no card for at any tag.
3. **Tier = `yield_filter`** (default `1+2`); foundational/intro/definitional lectures go all-tier.
4. **Verify every build with a coverage audit** — map the finished deck against the slides' concepts; confirm every concept has ≥1 card. Then a card-by-card keep-vs-cut pass against the slides to drop off-lecture ride-alongs.
5. **One deck per lecture**, tagged `Sched::<Class>::M<n>-W<nn>::<lecture>`; merge only when two lectures map to one unsplittable leaf.
