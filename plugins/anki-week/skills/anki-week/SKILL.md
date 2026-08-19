---
name: anki-week
description: Use when building or refreshing a week's AnKing Step Deck study set from medical-school lecture materials — reading the lecture slides (PPTX/PDF) FIRST as the primary scope, using the weekly calendar only to know which materials to pull, then turning that material concept inventory (cross-checked against the syllabus objectives and resource references — Boards&Beyond / First Aid / Bootcamp / etc.) into unsuspended, tagged, pace-controlled Anki cards that cover everything the lecture taught — scoped to the body system / course block you are currently in, so a shared mechanism doesn't drag another block's disease pathology into this week. Requires Anki desktop open with the Anki MCP Server add-on (code 124672614).
---

# anki-week

## Overview

Turn this week's lectures into the right AnKing Step Deck cards to study. The cards already exist — the AnKing Step Deck (~28.6k notes) is one deck, almost all **suspended**, organized entirely by **hierarchical tags** that cross-reference every major resource (First Aid, Boards&Beyond, Bootcamp, Sketchy, Physeo, DirtyMedicine, OME) **and** by body system. So "build a deck" = mostly **find the right cards by tag and unsuspend them** — and, for the handful of lecture concepts AnKing doesn't card (definitions, the professor's named frameworks/lists/kinetics), **add a few custom cards** so the deck actually covers the lecture.

**Core loop (per-lecture, MATERIALS-DRIVEN, BLOCK-SCOPED):** intake — Calendar = **which lectures/materials to pull** (an index, not the scope); **the lecture MATERIALS (slides/PDF) = the primary source, read FIRST**; syllabus objectives = a cross-check that can only *add* scope; **`current_block` = which body system this week belongs to**. **Read the materials before mapping anything.** For **each lecture**, build a **concept inventory** from its materials (∪ its objectives) — that inventory is the **coverage FLOOR** — then map those concepts to AnKing cards, **verifying the subtree's sample cards actually match the subject** (keyword ≠ subject), defaulting to **all-tier for foundational/definitional lectures** (the 1+2 filter is board-system-optimized and silently drops basics), then **gating by body system** so another block's disease pathology doesn't ride in on a shared mechanism → **you approve** → unsuspend + tag `Sched::<Class>::M<n>-W<nn>::<System>::IM<##>-<Lecture>` (the `<System>` node links each card to the block it was learned in) + filtered deck → **coverage-audit every concept in the inventory** (pull more, or add a custom card, for any concept with no AnKing card) → log → **hand off to `study-week`** to turn the just-built decks into a paced weekly study plan + calendar blocks. Exam-aligned: school summatives/formatives test the *lectures*, not Step 1.

**⬆️ The floor rule: never cover LESS than the materials.** Everything the lecture materials teach must end up carded — real AnKing card or custom. No filter, tier setting, **system gate**, or trim may drop the last card covering a material concept.

**⬇️ …but the floor is a COVERAGE requirement, not a card-volume licence.** You reach it via the **Selection Protocol** in `data/config.md` — **⭐ Scope = tags ∩ slides ∩ system:**

> **Resource tags say where a card *could* live; the slides say what the lecture *is about*; `current_block` says which body system you're here to learn. Scope is the INTERSECTION of all three.**
>
> **1** Build a **Scope Spec** from the slides — a lecture `type` + typed entity lists (drugs · organisms · genes/proteins · diseases · stains/markers) + `named_rules` + slide-bold `high_yield` + **`system`** (= `current_block`). **2** Cast a **WIDE NET**: `(B&B/Bootcamp) + FirstAid` always, **+ Sketchy only for pharm/micro**. **3** **INTERSECT** — keep a card only if its tag or content names a Scope-Spec entity. **4** **GATE by system** — sort survivors into **core** (this block, or system-agnostic) · **bridge** (one recognition card per slide-named foreign example) · **deferred** (another block's disease depth — logged, not built). **5** Depth by `type`: pharm/micro **comprehensive**, path/genetics/immuno **lean**, foundational **all-tier recognition**; HY gate 1+2 (+ all-tier for foundational and slide-flagged-HY with no 1+2 card).

**⚠️ The wide net is a CANDIDATE UNIVERSE — only intersected survivors get unsuspended.** Casting a whole chapter is fine; unsuspending one is the error. Measured: derm's net held `#SketchyPharm::07_Antimicrobials` = **429 HY**; intersecting the slide drug list collapsed it to **~77**, dropping ~352 systemic-antibiotic cards the lecture never names. **Completeness-by-chapter ≠ on-scope coverage.**

### 🧭 …and an on-scope card can still be in the WRONG BLOCK

The entity intersection asks *"is this card about the concept?"* — it never asks *"is this card in the system I'm studying?"* Shared mechanisms are the leak. **Type IV hypersensitivity** in an **MSK** lecture matches cards filed under Endo (**DM1**), GI (celiac), Derm (contact dermatitis), ID (TB/PPD) — so the deck arrives carrying diabetes autoantibodies, DKA and insulin regimens in a musculoskeletal week. The cards aren't wrong; **the block is.** They're worth learning *when you reach Endo.*

So Stage 2 gates every survivor by its **home system** (`^Systems::<System>` tag, else its resource chapter):

- **core** — home system == `current_block`, or **system-agnostic** (biochem, cell/molecular, general path/immuno/pharm — the mechanism cards) → build it;
- **bridge** — a foreign disease the slides actually *name*, as an example of this lecture's concept → **one recognition card**, not its workup ("DM1 is which hypersensitivity type?" ✓ · "DKA management" ✗);
- **deferred** — that system's own pathology depth → **not built**, logged with its query, and **re-offered the week you start that block**.

**⚖️ The gate cuts DEPTH in another system, never BREADTH of the shared concept.** Ask of each foreign card: *is it teaching the concept as it shows up in that organ, or that organ's disease?* "β2 → bronchial smooth-muscle relaxation" is the receptor's distribution → **core**, lung word and all; "stepwise asthma management" is pulmonology → deferred. And how much of a cross-body map is core comes from the slides: a foundational pharm lecture that teaches the α/β tissue table makes **every row** an inventory concept, while an **MSK** lecture that just uses β2-agonist tremor makes **only that row** core and defers the heart/lung breadth. **Slides set the breadth; the block sets the depth** — the same 84 β-receptor cards score 41 core in the first lecture and 7 in the second.

**Deferring is not dropping**, and the **floor still outranks the gate**: a disease the slides genuinely *teach* is core no matter which system cards it. `current_block` = `General` (a foundations block, no body system — the M1 IM course) → core is system-agnostic only, every organ-system card is bridge-or-deferred. Full rule: `data/config.md` → *🧭 The system gate*.

**FirstAid is mandatory on every lecture** (universal add — unique cards *and* the leaf granularity that lets you scope tight). **B&B/Bootcamp alone is never enough.** **Sketchy only for pharm & micro** (~0 unique value on concept lectures). **`#AK_Step1_v12::` only.**

**Under-covering the lecture and bloating the deck are both build failures.** The intersection is how you avoid trading one for the other. Full rule + the resource table: `data/config.md` → *⭐ THE SELECTION PROTOCOL*.

### 📄 What "lecture materials" MEANS — slide files only, never an Anki deck

Everywhere this skill says **materials** / **slides** / **the lecture**, it means **the professor's
posted slide files** — `.pptx` / `.ppt` / `.pdf` (and the occasional `.docx` handout) — living at
`<course_folder>/<Course>/Week <n>/`, or downloaded from `blackboard_url` when they're not there yet.
**Files on disk. Read with the `pptx` / `pdf` skills.**

**An Anki deck is NEVER lecture materials — not even one named after the slides.** A deck or subdeck
called **`Meharry Slides`** (or any similar "slides"-named deck in the collection) is *cards someone
already made*. It is **not** the lecture, **not** a source of scope, and **not** a substitute for the
PPTX. Do not read it to build a concept inventory, and do not treat its existence as "materials found."

**Anki is used for exactly one thing here: the card library** (`deck_name` = AnKing Step Deck,
`tag_namespace` = `#AK_Step1_v12`). No deck in the collection is ever a materials source.

**So the check is a FILE check.** "Does this lecture have materials?" = *is there a PPTX/PDF for it in
its week folder?* If no → the lecture has **no materials** and you go to the fetch ladder
(*Materials missing → FETCH*) → Blackboard. **A `Meharry Slides` deck sitting in Anki does not answer
that question and never closes the gap.**

## Prerequisites (check first, every run)

- **Anki desktop must be OPEN** on this Mac with the **Anki MCP Server** add-on (AnkiWeb code `124672614`) enabled — it serves the `anki` MCP at `http://127.0.0.1:3141`. (NOT AnkiConnect; that's a different add-on and isn't used here.) If `list_decks` / `find_notes` errors *while Anki is open*, STOP and tell the user — change nothing.
- **🔌 No `anki` connector at all? Install it yourself, now — don't ask the user to paste JSON.** Before Stage 0 on any run, confirm the `anki` MCP is actually reachable (one read-only call, e.g. `list_decks`). If the connector isn't there, run:

  ```bash
  node "<anki-week plugin>/skills/setup/scripts/install-anki-mcp.mjs"
  ```

  (from this skill's folder: `node ../setup/scripts/install-anki-mcp.mjs`). It merges the entry below into the **Claude Desktop config** — preserving every other MCP server, backing the file up first, refusing to overwrite unparseable JSON — so the connector is live in **Claude Chat and Claude Cowork**, not just wherever you're running now:

  ```json
  { "mcpServers": { "anki": { "command": "npx", "args": ["mcp-remote", "http://127.0.0.1:3141"] } } }
  ```

  Then tell the user to **fully quit and reopen Claude** and re-run; on this surface also offer `claude mcp add anki -- npx mcp-remote http://127.0.0.1:3141`. Requires Node (`npx --version`; else <https://nodejs.org> LTS). No shell here → fall back to walking them through **Settings ▸ Developer ▸ Edit Config**. Full walkthrough: the **anki-week-setup** skill.
- **🪄 Say "switch to Claude Cowork" — every run.** Cowork is where this workflow is whole: it has a **browser**, so it opens `blackboard_url`, logs in with the session you already have, and **pulls each week's lecture slides down itself** — then builds decks off the real slides instead of a lecture title. Plain Claude Code can't fetch materials; you'd be downloading every lecture by hand. So: **open every run outside Cowork with a one-line nudge**, repeat it the moment a materials fetch is blocked (*Materials missing → FETCH*, rung 2), and close the run with it. Keep it to one line each time — a standing offer, not a lecture. The connector installed above is already live in Cowork, so switching costs them nothing.
- **Set up once** (install Node, write the config above, connect Anki); after that the skill runs in **both Claude Code and Cowork** — the Anki MCP add-on is reachable from both.

## When to use

- Start of a study week / after lectures drop: "build this week's Anki," "unsuspend cards for X."
- Source library is the **AnKing Step Deck only** (v1). Anatomy decks are out of scope until extended.

## The procedure

Run the detailed steps in **reference/playbook.md** — it has the exact MCP call patterns, tag roots, and pacing math. Summary:

| Stage | What | Key tools |
|---|---|---|
| **0a · Fetch** | **Run this the moment the calendar names a lecture whose materials aren't on disk — before any mapping.** See *Materials missing → FETCH* below. | browser |
| 0 · Intake | **Read `current_block` from config** (the week's body system; confirm it if the syllabus says the block just changed). **Calendar first, but only as an INDEX** — it names the week's lectures so you know *which materials to go read*. Then **READ THE MATERIALS** (PPTX→`pptx`, PDF→`pdf`) — the primary pass. Then **Syllabus objectives** as a cross-check (may *add* scope, never subtract). Produce the concept inventory (= the coverage floor) **and the SCOPE SPEC**: lecture `type` + typed entity lists + `named_rules` + slide-bold `high_yield` + **`system`** (= `current_block`). **Materials outrank the title; the calendar never defines scope.** | Calendar, Read, pptx/pdf |
| 1 · Wide net | Cast the **candidate universe**: `(B&B/Bootcamp) + FirstAid` always, **+ Sketchy only if `type` is pharm/micro**. `#AK_Step1_v12::` only; exclude `!DELETE(Duplicate)`. **Nothing here gets unsuspended.** Dedup is a non-issue (one pre-deduped deck). | `find_notes` |
| 2a · **Intersect** | **The subject step.** Expand entities via `synonym-map.md`, then keep a card only if its **tag or content names a Scope-Spec entity**. Apply the depth rule by `type` (pharm/micro comprehensive · path/genetics/immuno lean · foundational all-tier recognition). HY gate 1+2 + exceptions. Report the collapse (e.g. 429 → 77). | `find_notes`, `notes_info`, synonym-map |
| 2b · **🧭 System gate** | **The block step.** Classify each survivor's **home system** (`^Systems::<System>` tag → else resource chapter → else system-agnostic) and sort: **core** (in-block or system-agnostic) · **bridge** (one recognition card per slide-named foreign example) · **deferred** (foreign-system disease depth — not built, query logged, re-offered at that block). **The floor overrides the gate: a slide-taught disease is core in any system.** Report the split (e.g. 91 on-scope → 44 in-block + 47 deferred). | `find_notes`, `notes_info` |
| 3 · Propose | **Entity × on-scope cards** + the candidate→on-scope collapse + **the system-gate split (in-block / bridge / deferred by foreign system, offered to pull now)** + sample cards + new/day + any "won't fit"/"no AnKing card" flags + **which Scope-Spec entities are still uncovered**. **Wait for approval.** Never unsuspend before this. | — |
| 4 · Execute | `sync` → resolve notes→cards → `unsuspend` → add per-lecture `Sched::<Class>::M<n>-W<nn>::<System>::IM<##>-<Topic>` tags (**the system node is what links a card to the block it was learned in**) + `Sched::xsys::<ForeignSystem>` on bridge cards → **build a filtered deck per lecture** → report new/day → `sync`. | `card_management`, `tag_management`, `filtered_deck`, `sync` |
| **4.5 · Coverage audit** | **The floor check.** Walk **every concept in the material inventory** (∪ objectives) and confirm ≥1 card covers it. Uncovered → pull more AnKing cards, or if AnKing genuinely has none (named frameworks/lists/kinetics, pure definitions) **add a custom Basic/Cloze card** (`add_note`) tagged with the lecture's `Sched::` tag + `Sched::custom`. This IS "reconciliation" when new slides arrive — a coverage pass, not a light trim. **The deck is not done while any material concept is uncovered.** Report concepts-covered vs gaps **and the system split**, then **gate self-check** — too tight (a floor concept sitting in the deferred set) and too loose (foreign-system depth in the built deck) are both build failures. Then run the standard card-by-card **tangent audit** (`reference/playbook.md` → Stage 4.5 step 4) — it cuts cards that cover *no* inventory concept, and **may never remove the last card covering one**. | `find_notes`, `notes_info`, `add_note` |
| 5 · Log + learn | Append the run + the coverage report + **the deferred sets (system · entity · query · count)** to `data/run-log.md`; record confirmed concept→leaf mappings, block→`^Systems` rows and newly-seen cross-system attractors into `data/tag-map.md`. **Starting a new block? replay the log's deferred queries for it first.** | Write |
| **6 · Plan the week (`study-week` handoff)** | The week's cards now exist → invoke the **`study-week`** skill so the built decks become a study *plan*: it maps each lecture to its Boards & Beyond video(s), reserves daily Anki-review time (from your recent review volume), and stages pre-lecture study blocks in your 2–8 PM calendar window as `🟡 Proposed —` events to accept or delete. Runs **after** decks are built so the plan reflects real cards. | `study-week` |

### Materials missing → FETCH, never silently degrade

The calendar names the week's lectures. For **each** one, check
`<course_folder>/<Course>/Week <n>/` for its materials — **a PPTX/PDF file on disk; an Anki deck named
`Meharry Slides` is not a hit.** If a lecture has no slide file, do **not** proceed to
mapping — work this ladder in order and stop at the first rung that succeeds:

1. **Browser available → fetch it.** Open `blackboard_url`, find that course's materials area, and
   download the missing files into that lecture's week folder. If the session isn't logged in, **STOP
   and ask the user to log in**, then continue. Never guess at a URL, and never invent a filename.
2. **No browser on this surface → hand it back, and name the fix.** Tell the user plainly: *"I can't
   open Blackboard from here. **Switch to Claude Cowork** and re-run — it has a browser, it'll log in
   with your existing session and pull these slides down itself — or drop the files into `<path>`
   yourself."* Name the exact folder. **Then wait** — don't build around the gap. This is the moment
   the Cowork nudge is worth most; don't soften it into "you could also…".
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

**Close the run with the Cowork line (when you're not already in Cowork).** One sentence, after the
report — and make it specific to what this run actually cost them: *"Heads up: you downloaded 4
lectures' slides by hand for this build. In **Claude Cowork** I'd have pulled them off Blackboard
myself — same `anki` connector, same decks, nothing to reinstall."* If nothing was missing this week,
keep it to a single line anyway. Once per run, at the end — never mid-report.

## Quick reference

- **Step-deck tag roots** (real, verified):
  - System tree: `#AK_Step1_v12::^Systems::<System>::<Topic>` (e.g. `…::Cardio::HeartSounds` = 31 cards)
  - Resource trees: `#AK_Step1_v12::#FirstAid::…`, `…::#B&B::…`, `…::#Bootcamp::…`, `…::#Physeo::…`, `…::#SketchyPharm/Physiology/Micro::…`
- **Altitude check** — same week, wildly different sizes: `^Systems::Cardio` ≈ 1,733 (whole block) vs `#FirstAid::07_Cardiovascular::03_Physiology` ≈ 616 (weeks) vs `^Systems::Cardio::HeartSounds` ≈ 31 (one lecture). **Aim for leaves.**
- **Weekly tag scheme:** `Sched::<Class>::M<n>-W<nn>::<System>::IM<##>-<Topic>` (e.g. `Sched::IM::M1-W01::General::IM20-Acute_Inflammation`). The **`<System>` node is the block the card was learned in** — that's the link the tags used to be missing. Top-level `Sched` finds everything scheduled; `Sched::IM::M1-W01` groups one week (undo = re-suspend that query); `tag:Sched::*::MSK::*` = everything you built while in MSK; `Sched::xsys::<System>` = bridge cards borrowed from a block you haven't reached yet.
- **Pacing:** `new/day = ceil(batch ÷ study-days-until-next-drop)`, clamped to the cap in `data/config.md` (default 25). If it won't fit under the cap, surface it at Stage 3 — never silently exceed.
- **Find suspended/actionable:** add `is:suspended` to any tag query to count what will actually change.
- **Bleed check (post-build):** `tag:Sched::*::<Block>::* -tag:#AK_Step1_v12::^Systems::<Block>::*` — everything you built in a block that isn't that block's card. System-agnostic + bridge cards are expected; another system's workup is bleed.

## Common mistakes

These first four are the failures that produced mis-scoped/incomplete Week-1 decks (slide-audited 2026-06-27) — they are the reason this skill is materials-driven now:

- **Mistaking an Anki deck for the lecture materials.** A deck named **`Meharry Slides`** is pre-made cards, not the professor's slides. Reading it instead of the PPTX means your concept inventory is *someone else's card selection* — you inherit their omissions and never see the slides the exam is written from. **Materials = a file in the week folder.** No file → fetch from Blackboard; never let a slides-named deck mark the lecture as "materials found."
- **Mapping before reading the materials → mis-scope.** The calendar title and the syllabus line are *pointers to* the lecture, not the lecture. **Go read the slides first**, then map. "Cell Membrane" (IM04) was mapped to `#Biochem::Cellular` (organelles/ER/Golgi/cytoskeleton) when the lecture is membrane-transport **physiology** (lipid bilayer, osmosis, Na⁺/K⁺-ATPase) in `#Physiology` — ~zero overlap with what was taught. Always **sample-check that a subtree's cards actually match the subject** before committing.
- **Covering less than the materials.** The material concept inventory is a **floor**. A deck that omits something the professor taught is broken, no matter how clean its tags are.
- **Unsuspending the wide net.** The net is a *candidate universe*; only entity-intersected survivors get unsuspended. Skipping the intersection is how 429 cards become a deck instead of 77.
- **Scoping from the tag tree alone** → overscope. **Or from a narrow tag guess alone** → under-cover. It's the *intersection* that's correct, never either half.
- **🧭 Ignoring the block you're in → cross-system bleed.** The entity match only proves a card is *about the concept*; it says nothing about *which system* the card lives in. Shared mechanisms (hypersensitivity types, inflammation, apoptosis, autoimmunity/HLA, signaling, collagen, cytokines, inheritance patterns) are carded under every system that has a disease using them — so **Type IV hypersensitivity in an MSK week pulls the full pathology of Diabetes Mellitus Type 1** (autoantibodies, DKA, insulin, complications). Right concept, wrong block. Gate by home system: in-block + system-agnostic = build, slide-named foreign example = **one** bridge card, foreign-system depth = defer + log it for the block where it belongs.
- **Over-correcting the gate into a floor break — cutting breadth instead of depth.** The mirror-image failure: deferring a disease *the slides actually teach*, or gutting a shared concept's cross-body reach, because the cards live in other systems. A receptor-distribution card that names the lung is still a receptor card. Test the **answer**, not the words: concept-in-that-organ = core, that-organ's-disease = deferred. If the professor taught it — including every row of a table he put up — it's core, whatever tag tree it sits in.
- **Deferring by deleting.** A deferred set that isn't logged with its query is just a dropped set. Write it to the run log, and replay it when `current_block` becomes that system.
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

- `data/tag-map.md` — course vocabulary → AnKing leaf tags (*where to look*), **block → `^Systems` node**, and the **cross-system attractor** list (*which entities overpull across systems*). Grows each week.
- `data/synonym-map.md` — slide term → AnKing term (*what to match on*). **The Selection Protocol's one ongoing tuning surface** — growing it carries coverage ~90% → ~95%.
- `data/run-log.md` — audit trail + undo reference per week, **plus each week's deferred cross-system sets** (system · entity · query · count) so they can be pulled when that block starts.
- `data/config.md` — paths (course folder), new/day cap, deck name, tag prefix, **`current_block` + `cross_system_policy`**, and the ⭐ Selection Protocol / 🧭 system gate.
- `DESIGN.md` — why it's built this way + the locked decisions. *(Not in this repo — it lives with the author's private copy; ignore the pointer if you don't have one.)*
