---
name: anki-week
description: Use when building or refreshing a week's AnKing Step Deck study set from medical-school lecture materials — reading the lecture slides (PPTX/PDF) FIRST as the primary scope, using the weekly calendar only to know which materials to pull, then turning that material concept inventory (cross-checked against the syllabus objectives and resource references — Boards&Beyond / First Aid / Bootcamp / etc.) into unsuspended, tagged, pace-controlled Anki cards that cover everything the lecture taught. Requires Anki desktop open with the Anki MCP Server add-on (code 124672614).
---

# anki-week

## Overview

Turn this week's lectures into the right AnKing Step Deck cards to study. The cards already exist — the AnKing Step Deck (~28.6k notes) is one deck, almost all **suspended**, organized entirely by **hierarchical tags** that cross-reference every major resource (First Aid, Boards&Beyond, Bootcamp, Sketchy, Physeo, DirtyMedicine, OME) **and** by body system. So "build a deck" = mostly **find the right cards by tag and unsuspend them** — and, for the handful of lecture concepts AnKing doesn't card (definitions, the professor's named frameworks/lists/kinetics), **add a few custom cards** so the deck actually covers the lecture.

**Core loop (per-lecture, MATERIALS-DRIVEN):** intake — Calendar = **which lectures/materials to pull** (an index, not the scope); **the lecture MATERIALS (slides/PDF) = the primary source, read FIRST**; syllabus objectives = a cross-check that can only *add* scope. **Read the materials before mapping anything.** For **each lecture**, build a **concept inventory** from its materials (∪ its objectives) — that inventory is the **coverage FLOOR** — then map those concepts to AnKing cards, **verifying the subtree's sample cards actually match the subject** (keyword ≠ subject), defaulting to **all-tier for foundational/definitional lectures** (the 1+2 filter is board-system-optimized and silently drops basics). → **you approve** → unsuspend + tag `Sched::<week>::IM<##>-<Lecture>` + filtered deck → **coverage-audit every concept in the inventory** (pull more, or add a custom card, for any concept with no AnKing card) → log → **hand off to `study-week`** to turn the just-built decks into a paced weekly study plan + calendar blocks. Exam-aligned: school summatives/formatives test the *lectures*, not Step 1.

**⬆️ The floor rule: never cover LESS than the materials.** Everything the lecture materials teach must end up carded — real AnKing card or custom. No filter, tier setting, or trim may drop the last card covering a material concept.

**⬇️ …but the floor is a COVERAGE requirement, not a card-volume licence.** You reach it via the **Selection Protocol** in `data/config.md` — **⭐ Scope = tags ∩ slides:**

> **Resource tags say where a card *could* live; the slides say what the lecture *is about*. Scope is the INTERSECTION.**
>
> **1** Build a **Scope Spec** from the slides — a lecture `type` + typed entity lists (drugs · organisms · genes/proteins · diseases · stains/markers) + `named_rules` + slide-bold `high_yield`. **2** Cast a **WIDE NET**: `(B&B/Bootcamp) + FirstAid` always, **+ Sketchy only for pharm/micro**. **3** **INTERSECT** — keep a card only if its tag or content names a Scope-Spec entity. **4** Depth by `type`: pharm/micro **comprehensive**, path/genetics/immuno **lean**, foundational **all-tier recognition**. **5** HY gate 1+2 (+ all-tier for foundational and slide-flagged-HY with no 1+2 card).

**⚠️ The wide net is a CANDIDATE UNIVERSE — only intersected survivors get unsuspended.** Casting a whole chapter is fine; unsuspending one is the error. Measured: derm's net held `#SketchyPharm::07_Antimicrobials` = **429 HY**; intersecting the slide drug list collapsed it to **~77**, dropping ~352 systemic-antibiotic cards the lecture never names. **Completeness-by-chapter ≠ on-scope coverage.**

**FirstAid is mandatory on every lecture** (universal add — unique cards *and* the leaf granularity that lets you scope tight). **B&B/Bootcamp alone is never enough.** **Sketchy only for pharm & micro** (~0 unique value on concept lectures). **`#AK_Step1_v12::` only.**

**Under-covering the lecture and bloating the deck are both build failures.** The intersection is how you avoid trading one for the other. Full rule + the resource table: `data/config.md` → *⭐ THE SELECTION PROTOCOL*.

## Prerequisites (check first, every run)

- **Anki desktop must be OPEN** on this Mac with the **Anki MCP Server** add-on (AnkiWeb code `124672614`) enabled — it serves the `anki` MCP at `http://127.0.0.1:3141`. (NOT AnkiConnect; that's a different add-on and isn't used here.) If `list_decks` / `find_notes` errors, STOP and tell the user to open Anki — change nothing.
- **Set up once in Claude Code** (install Node, edit this config, connect Anki); after that the skill runs in **both Claude Code and Cowork** — the Anki MCP add-on is reachable from both.
- **A browser is what lets this skill feed itself.** When a lecture's materials are missing, Stage 0 opens `blackboard_url` and downloads them (reusing your logged-in session). **Claude Cowork has a browser; plain Claude Code usually does not** — there the skill will ask you to switch or to add the files yourself. Prefer Cowork for weekly builds.

## When to use

- Start of a study week / after lectures drop: "build this week's Anki," "unsuspend cards for X."
- Source library is the **AnKing Step Deck only** (v1). Anatomy decks are out of scope until extended.

## The procedure

Run the detailed steps in **reference/playbook.md** — it has the exact MCP call patterns, tag roots, and pacing math. Summary:

| Stage | What | Key tools |
|---|---|---|
| **0a · Fetch** | **Run this the moment the calendar names a lecture whose materials aren't on disk — before any mapping.** See *Materials missing → FETCH* below. | browser |
| 0 · Intake | **Calendar first, but only as an INDEX** — it names the week's lectures so you know *which materials to go read*. Then **READ THE MATERIALS** (PPTX→`pptx`, PDF→`pdf`) — the primary pass. Then **Syllabus objectives** as a cross-check (may *add* scope, never subtract). Produce the concept inventory (= the coverage floor) **and the SCOPE SPEC**: lecture `type` + typed entity lists + `named_rules` + slide-bold `high_yield`. **Materials outrank the title; the calendar never defines scope.** | Calendar, Read, pptx/pdf |
| 1 · Wide net | Cast the **candidate universe**: `(B&B/Bootcamp) + FirstAid` always, **+ Sketchy only if `type` is pharm/micro**. `#AK_Step1_v12::` only; exclude `!DELETE(Duplicate)`. **Nothing here gets unsuspended.** Dedup is a non-issue (one pre-deduped deck). | `find_notes` |
| 2 · **Intersect** | **The scoping step.** Expand entities via `synonym-map.md`, then keep a card only if its **tag or content names a Scope-Spec entity**. Apply the depth rule by `type` (pharm/micro comprehensive · path/genetics/immuno lean · foundational all-tier recognition). HY gate 1+2 + exceptions. Report the collapse (e.g. 429 → 77). | `find_notes`, `notes_info`, synonym-map |
| 3 · Propose | **Entity × on-scope cards** + the candidate→on-scope collapse + sample cards + new/day + any "won't fit"/"no AnKing card" flags + **which Scope-Spec entities are still uncovered**. **Wait for approval.** Never unsuspend before this. | — |
| 4 · Execute | `sync` → resolve notes→cards → `unsuspend` → add per-lecture `Sched::…` tags → **build a filtered deck per lecture** → report new/day → `sync`. | `card_management`, `tag_management`, `filtered_deck`, `sync` |
| **4.5 · Coverage audit** | **The floor check.** Walk **every concept in the material inventory** (∪ objectives) and confirm ≥1 card covers it. Uncovered → pull more AnKing cards, or if AnKing genuinely has none (named frameworks/lists/kinetics, pure definitions) **add a custom Basic/Cloze card** (`add_note`) tagged with the lecture's `Sched::` tag + `Sched::custom`. This IS "reconciliation" when new slides arrive — a coverage pass, not a light trim. **The deck is not done while any material concept is uncovered.** Report concepts-covered vs gaps. Then run the standard card-by-card **tangent audit** (config Operating-principles v2 §7) — it cuts cards that cover *no* inventory concept, and **may never remove the last card covering one**. | `find_notes`, `notes_info`, `add_note` |
| 5 · Log + learn | Append the run + the coverage report to `data/run-log.md`; record confirmed concept→leaf mappings into `data/tag-map.md`. | Write |
| **6 · Plan the week (`study-week` handoff)** | The week's cards now exist → invoke the **`study-week`** skill so the built decks become a study *plan*: it maps each lecture to its Boards & Beyond video(s), reserves daily Anki-review time (from your recent review volume), and stages pre-lecture study blocks in your 2–8 PM calendar window as `🟡 Proposed —` events to accept or delete. Runs **after** decks are built so the plan reflects real cards. | `study-week` |

### Materials missing → FETCH, never silently degrade

The calendar names the week's lectures. For **each** one, check
`<course_folder>/<Course>/Week <n>/` for its materials. If a lecture has none, do **not** proceed to
mapping — work this ladder in order and stop at the first rung that succeeds:

1. **Browser available → fetch it.** Open `blackboard_url`, find that course's materials area, and
   download the missing files into that lecture's week folder. If the session isn't logged in, **STOP
   and ask the user to log in**, then continue. Never guess at a URL, and never invent a filename.
2. **No browser on this surface → hand it back.** Tell the user plainly: *"I can't open Blackboard from
   here. Switch to Claude Cowork and re-run, or drop the files into `<path>` yourself."* Name the exact
   folder. **Then wait** — don't build around the gap.
3. **Only if both fail** → fall back to the syllabus objectives, and mark every deck built that way
   **🚧 materials pending** so the gap is visible in the run log and can be rebuilt later.

**Why this is a hard rule:** Stage 0 is materials-first, so a missing file doesn't degrade the build a
little — it silently redefines the scope to whatever the title implies. Rungs 1 and 2 are cheap; rung 3
is a real loss of coverage. Reaching rung 3 without having genuinely tried 1 and 2 is a build failure.

### Stage 6 — handing off to study-week

Once Stage 4/4.5 have built (and Stage 5 logged) this week's decks, call the sibling **`study-week`** skill to
plan the week around them. Pass the same week you just built (its `current_week`/`Sched::<week>`); study-week
reads the lecture calendar + your Anki review load and proposes the study/video/review blocks. It only ever
**proposes** calendar events (never auto-commits), so the handoff is safe to run automatically at the end of a
build. If Anki-deck building was skipped or partial, still fine — study-week plans time around whatever exists;
it just can't guarantee a matching card for every block. Skip the handoff only if the user just wants cards and
no schedule.

## Quick reference

- **Step-deck tag roots** (real, verified):
  - System tree: `#AK_Step1_v12::^Systems::<System>::<Topic>` (e.g. `…::Cardio::HeartSounds` = 31 cards)
  - Resource trees: `#AK_Step1_v12::#FirstAid::…`, `…::#B&B::…`, `…::#Bootcamp::…`, `…::#Physeo::…`, `…::#SketchyPharm/Physiology/Micro::…`
- **Altitude check** — same week, wildly different sizes: `^Systems::Cardio` ≈ 1,733 (whole block) vs `#FirstAid::07_Cardiovascular::03_Physiology` ≈ 616 (weeks) vs `^Systems::Cardio::HeartSounds` ≈ 31 (one lecture). **Aim for leaves.**
- **Weekly tag scheme:** `Sched::<YYYY-Www>::<System>::<Topic>` (e.g. `Sched::2026-W25::Cardio::HeartSounds`). Top-level `Sched` finds everything scheduled; `Sched::2026-W25` groups one week (undo = re-suspend that query).
- **Pacing:** `new/day = ceil(batch ÷ study-days-until-next-drop)`, clamped to the cap in `data/config.md` (default 25). If it won't fit under the cap, surface it at Stage 3 — never silently exceed.
- **Find suspended/actionable:** add `is:suspended` to any tag query to count what will actually change.

## Common mistakes

These first four are the failures that produced mis-scoped/incomplete Week-1 decks (slide-audited 2026-06-27) — they are the reason this skill is materials-driven now:

- **Mapping before reading the materials → mis-scope.** The calendar title and the syllabus line are *pointers to* the lecture, not the lecture. **Go read the slides first**, then map. "Cell Membrane" (IM04) was mapped to `#Biochem::Cellular` (organelles/ER/Golgi/cytoskeleton) when the lecture is membrane-transport **physiology** (lipid bilayer, osmosis, Na⁺/K⁺-ATPase) in `#Physiology` — ~zero overlap with what was taught. Always **sample-check that a subtree's cards actually match the subject** before committing.
- **Covering less than the materials.** The material concept inventory is a **floor**. A deck that omits something the professor taught is broken, no matter how clean its tags are.
- **Unsuspending the wide net.** The net is a *candidate universe*; only entity-intersected survivors get unsuspended. Skipping the intersection is how 429 cards become a deck instead of 77.
- **Scoping from the tag tree alone** → overscope. **Or from a narrow tag guess alone** → under-cover. It's the *intersection* that's correct, never either half.
- **Mis-typing the lecture.** An *intro-to-micro* lecture is `foundational`, **not** `micro` — get this wrong and the comprehensive depth rule drags in a 46-card organism leaf the lecture only name-drops.
- **Treating a synonym miss as a resource gap.** A 0-card entity is usually the slides and AnKing using different words (*gas gangrene* / *C. perfringens*). Check `data/synonym-map.md`, add the alias, re-intersect — *then* call it a gap.
- **Letting the 1+2 yield filter silently drop foundational content.** Definitions, basic structure, named forms (DNA A/B/Z, Gram-stain procedure, prokaryote-vs-eukaryote, helix stability) sit at tier 3–4 in AnKing → the board filter erases exactly what intro lectures test. For foundational/intro/definitional lectures, **include on-concept cards all-tier** (tier exception = the default, not the exception).
- **Not auditing coverage.** Pulling "the right tag" ≠ covering the lecture. Verify **every material concept** has a card. AnKing genuinely lacks cards for some lecture concepts (clonal selection, naïve/effector/memory definitions, primary/secondary response kinetics, the professor's named lists) — **add a custom card; never silently omit.** (Stage 4.5.)
- **Grabbing the system root** (`^Systems::Cardio`, 1,733 cards) instead of leaves → review avalanche. Always descend to concept leaves.
- **Unsuspending before approval.** Stage 3 is a hard gate.
- **Forgetting note vs card ids.** `find_notes`/`tag_management` use **note** ids; `card_management` (suspend/unsuspend) uses **card** ids → resolve via `notes_info` (`cards[]`). See playbook.
- **Skipping sync.** Sync at both ends or your phone won't match.
- **Silently dropping a topic** with zero matches → flag it for manual mapping instead.

## Artifacts (persistent state)

- `data/tag-map.md` — course vocabulary → AnKing leaf tags (*where to look*). Grows each week.
- `data/synonym-map.md` — slide term → AnKing term (*what to match on*). **The Selection Protocol's one ongoing tuning surface** — growing it carries coverage ~90% → ~95%.
- `data/run-log.md` — audit trail + undo reference per week.
- `data/config.md` — paths (course folder), new/day cap, deck name, tag prefix.
- `DESIGN.md` — why it's built this way + the locked decisions.
