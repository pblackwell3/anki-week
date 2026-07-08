---
name: anki-week
description: Use when building or refreshing a week's AnKing Step Deck study set from medical-school lecture materials — turning lecture slides (PPTX/PDF), a syllabus, resource references (Boards&Beyond / First Aid / Bootcamp / etc.), or a weekly calendar into unsuspended, tagged, pace-controlled Anki cards. Requires Anki desktop open with the Anki MCP Server add-on (code 124672614).
---

# anki-week

## Overview

Turn this week's lectures into the right AnKing Step Deck cards to study. The cards already exist — the AnKing Step Deck (~28.6k notes) is one deck, almost all **suspended**, organized entirely by **hierarchical tags** that cross-reference every major resource (First Aid, Boards&Beyond, Bootcamp, Sketchy, Physeo, DirtyMedicine, OME) **and** by body system. So "build a deck" = mostly **find the right cards by tag and unsuspend them** — and, for the handful of lecture concepts AnKing doesn't card (definitions, the professor's named frameworks/lists/kinetics), **add a few custom cards** so the deck actually covers the lecture.

**Core loop (per-lecture, OBJECTIVE-driven):** intake — Calendar = lecture list, **Syllabus = each lecture's learning objectives = the authoritative scope**, slides = the detail. For **each lecture**, map **its objectives** (not its title) to AnKing cards — and **verify the subtree's sample cards actually match the lecture's subject** (keyword ≠ subject) — defaulting to **all-tier for foundational/definitional lectures** (the 1+2 filter is board-system-optimized and silently drops basics). → **you approve** → unsuspend + tag `Sched::<week>::IM<##>-<Lecture>` + filtered deck → **coverage-audit every objective** (pull more, or add a custom card, for any objective with no AnKing card) → log → **hand off to `study-week`** to turn the just-built decks into a paced weekly study plan + calendar blocks. Exam-aligned: school summatives/formatives test the *lectures*, not Step 1.

## Prerequisites (check first, every run)

- **Anki desktop must be OPEN** on this Mac with the **Anki MCP Server** add-on (AnkiWeb code `124672614`) enabled — it serves the `anki` MCP at `http://127.0.0.1:3141`. (NOT AnkiConnect; that's a different add-on and isn't used here.) If `list_decks` / `find_notes` errors, STOP and tell the user to open Anki — change nothing.
- Runs only in **Claude Code** (local). Cowork cannot reach the localhost Anki MCP server.

## When to use

- Start of a study week / after lectures drop: "build this week's Anki," "unsuspend cards for X."
- Source library is the **AnKing Step Deck only** (v1). Anatomy decks are out of scope until extended.

## The procedure

Run the detailed steps in **reference/playbook.md** — it has the exact MCP call patterns, tag roots, and pacing math. Summary:

| Stage | What | Key tools |
|---|---|---|
| 0 · Intake | Calendar (lecture list) + **Syllabus → each lecture's learning OBJECTIVES = the authoritative scope** (+ exam structure) + week folder slides (PPTX→`pptx`, PDF→`pdf`). Produce per-lecture `{objectives[], topics[], refs[]}`. **Objectives outrank the title and the folder.** | Calendar, Read, pptx/pdf |
| 1 · Narrow | For each lecture, map **its objectives** (not its title) to AnKing subtrees. **Verify subject** before committing: sample 2–3 cards of a candidate subtree and confirm they match the objective — *keyword ≠ subject* (e.g. membrane **transport** lives in `#Physiology`, NOT `#Biochem::Cellular` which is organelles). Prefer leaves under your `backbone_resource` tree (config) first; fall back to other trees only where the backbone has no clean leaf. | `find_notes`, `notes_info` |
| 2 · Leaf-select | Pick concept-**leaf** tags per objective. **Tier rule: include on-objective cards regardless of yield tier for foundational/intro/definitional lectures** — 1+2 is optimized for board-dense *systems* and drops the basics (DNA forms, Gram procedure, prokaryote/eukaryote, definitions). | `find_notes`, tag-map |
| 3 · Propose | **Objectives × candidate leaves** + counts + sample cards + new/day + any "won't fit"/"no AnKing card" flags. **Wait for approval.** Never unsuspend before this. | — |
| 4 · Execute | `sync` → resolve notes→cards → `unsuspend` → add per-lecture `Sched::…` tags → **build a filtered deck per lecture** → report new/day → `sync`. | `card_management`, `tag_management`, `filtered_deck`, `sync` |
| **4.5 · Coverage audit** | **The step that was missing.** Walk **every objective** and confirm ≥1 card covers it. Uncovered → pull more AnKing cards, or if AnKing genuinely has none (named frameworks/lists/kinetics, pure definitions) **add a custom Basic/Cloze card** (`add_note`) tagged with the lecture's `Sched::` tag + `Sched::custom`. This IS "reconciliation" when slides/syllabus arrive — a coverage pass, not a light trim. Report objectives-covered vs gaps. | `find_notes`, `notes_info`, `add_note` |
| 5 · Log + learn | Append the run + the coverage report to `data/run-log.md`; record confirmed objective→leaf mappings into `data/tag-map.md`. | Write |
| **6 · Plan the week (`study-week` handoff)** | The week's cards now exist → invoke the **`study-week`** skill so the built decks become a study *plan*: it maps each lecture to its Boards & Beyond video(s), reserves daily Anki-review time (from your recent review volume), and stages pre-lecture study blocks in your 2–8 PM calendar window as `🟡 Proposed —` events to accept or delete. Runs **after** decks are built so the plan reflects real cards. | `study-week` |

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

These first three are the failures that produced mis-scoped/incomplete Week-1 decks (slide-audited 2026-06-27) — they are the reason this skill is objective-driven now:

- **Mapping by lecture TITLE/keyword instead of the syllabus OBJECTIVES → mis-scope.** "Cell Membrane" (IM04) was mapped to `#Biochem::Cellular` (organelles/ER/Golgi/cytoskeleton) when the lecture is membrane-transport **physiology** (lipid bilayer, osmosis, Na⁺/K⁺-ATPase) in `#Physiology` — ~zero overlap with what was taught. Always scope from objectives + slides, and **sample-check that a subtree's cards actually match the subject** before committing.
- **Letting the 1+2 yield filter silently drop foundational content.** Definitions, basic structure, named forms (DNA A/B/Z, Gram-stain procedure, prokaryote-vs-eukaryote, helix stability) sit at tier 3–4 in AnKing → the board filter erases exactly what intro lectures test. For foundational/intro/definitional lectures, **include on-objective cards all-tier** (tier exception = the default, not the exception).
- **Not auditing coverage.** Pulling "the right tag" ≠ covering the lecture. Verify **every objective** has a card. AnKing genuinely lacks cards for some lecture concepts (clonal selection, naïve/effector/memory definitions, primary/secondary response kinetics, the professor's named lists) — **add a custom card; never silently omit.** (Stage 4.5.)
- **Grabbing the system root** (`^Systems::Cardio`, 1,733 cards) instead of leaves → review avalanche. Always descend to concept leaves.
- **Unsuspending before approval.** Stage 3 is a hard gate.
- **Forgetting note vs card ids.** `find_notes`/`tag_management` use **note** ids; `card_management` (suspend/unsuspend) uses **card** ids → resolve via `notes_info` (`cards[]`). See playbook.
- **Skipping sync.** Sync at both ends or your phone won't match.
- **Silently dropping a topic** with zero matches → flag it for manual mapping instead.

## Artifacts (persistent state)

- `data/tag-map.md` — your course vocabulary → AnKing leaf tags. The brain; grows each week.
- `data/run-log.md` — audit trail + undo reference per week.
- `data/config.md` — paths (course folder), new/day cap, deck name, tag prefix.
