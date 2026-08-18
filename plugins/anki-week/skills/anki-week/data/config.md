# anki-week — Config

Edit these to match **your** setup. The skill reads this at Stage 0. Most values are a shared
Meharry M1 preset; the rows marked **← SET THIS** are yours.

| Key | Value | Notes |
|---|---|---|
| `course_folder` | `← SET THIS` (e.g. `~/Lecture Materials`) | Your local folder of lecture slides. Layout: `<course_folder>/<Course>/Week <n>/` with the PPTX/PDF directly inside. When a lecture's materials are missing here, Stage 0 fetches them from `blackboard_url` rather than building without them. **"Materials" = these slide FILES only.** An Anki deck named `Meharry Slides` (or any slides-named deck) is *not* materials, does not satisfy this check, and is never read for scope — Anki is only the card library (`deck_name` below). |
| `blackboard_url` | `← SET THIS` (e.g. `https://blackboard.yourschool.edu/`) | Your school's LMS login / course-list page. Stage 0 opens this in a browser (reusing your logged-in session) to download missing lecture materials into `course_folder`. Leave blank only if you always add materials by hand. **No credentials are ever stored — if you're not logged in, the skill stops and asks you to log in.** |
| `syllabus` | `← SET THIS` (path to your syllabus `.docx`/`.pdf`) | **Read in Stage 0.** Its Course Outline table gives each lecture's Learning Objectives = the authoritative card scope. You already have this as an enrolled student — point the skill at your own copy. |
| `current_week` | `1` | Curriculum week to build. Bump each week. |
| `current_block` | `General` | **← SET THIS each block.** The **body system / course block you are in right now** — the third scope axis. Use an `^Systems` node name (`MSK`, `Cardio`, `Renal`, `Endo`, `Neuro`, `GI`, `Pulm`, `Repro`, `Heme_Onc`, `Derm`, `Psych`) when you're in an organ-system block, or **`General`** for a pre-clinical/foundations block that has no body system (biochem, genetics, general path, general immuno, intro micro — the M1 IM course is `General`). Bump it when the block changes. Block name → real `^Systems` node is recorded in `data/tag-map.md` → *Block → `^Systems` node*. |
| `cross_system_policy` | `bridge` | What happens to an on-entity card whose **home system isn't `current_block`** (see *The system gate* below). `bridge` *(default)* = keep one recognition card per slide-named example, defer that system's deeper pathology · `strict` = defer all of it, bridge cards included · `include` = no gate, pre-fix behavior (only for a deliberately cross-system review week) · `ask` = show the split at Stage 3 and let you choose per lecture. |
| `class_calendar_id` | `← SET THIS` | The class calendar that lists the numbered IM lectures (`IM (n) Title`). Subscribe to the shared class calendar and paste its id (a long string ending in `calendar.google.com`), or leave blank and feed lectures manually. |
| `deck_name` | `AnKing Step Deck` | The card-source library. |
| `tag_namespace` | `#AK_Step1_v12` | Step-deck tag root. Setup detects your actual version and writes it here. |
| `backbone_resource` | `#B&B` | **Your primary study resource = the deck's backbone + naming lens.** Options that live under `tag_namespace`: `#B&B` (Boards & Beyond), `#Pathoma`, `#FirstAid`, `#Physeo`, `#Bootcamp`, `#SketchyMicro` / `#SketchyPharm` / `#SketchyPhysiology`, `#DirtyMedicine`, or `^Systems` (body-system tree). Map each lecture's objectives to leaves under THIS tree first; fall back to other trees only where your backbone has no clean leaf. Setup writes this from what it finds in your deck. |
| `yield_filter` | `1+2` | AnKing high-yield tiers to include: `1` = High-Yield only · `1+2` = + Relatively-High-Yield (recommended) · `1+2+3` = + High-Yield-temporary · `off` = all tiers. Foundational/intro/definitional lectures auto-include all tiers regardless. |
| `new_per_day_cap` | `25` | Runaway ceiling for new cards/day. The MCP can't set New/day — set it in Anki ▸ deck ▸ Options ▸ New cards/day. |
| `leaf_size_hint` | `60` | A tag subtree bigger than this (notes) is "too high" — descend to leaves. |

---

# ⭐ THE SELECTION PROTOCOL

> ## **Scope = tags ∩ slides ∩ system**
>
> **Resource tags say where a card *could* live. The slides say what the lecture *is about*.
> `current_block` says what system you are here to learn.
> Scope is the INTERSECTION of all three — miss any one axis and the deck breaks in a different way.**

| Axis | Answers | Drop it and you get |
|---|---|---|
| **tags** | where the cards live | nothing to pull from |
| **slides** | what this lecture teaches | completeness-by-chapter — 429 antimicrobial cards for a 12-drug lecture |
| **system** | which block you're in | **cross-system bleed — the full pathology of Diabetes Mellitus Type 1 in an MSK hypersensitivity lecture** |

## The five steps

**1 · Scope Spec** — built from the slides at Stage 0: lecture `type` + typed entity lists
(drugs · organisms · genes/proteins · diseases · stains/markers) + `named_rules` + slide-bold
`high_yield` + **`system`** (defaults to `current_block`).

**2 · WIDE NET** — the candidate universe: `(B&B/Bootcamp) + FirstAid` always, **+ Sketchy only for
pharm/micro**. `#AK_Step1_v12::` only. **Nothing here gets unsuspended.**

**3 · INTERSECT (slides)** — keep a card only if its tag or content names a Scope-Spec entity
(expand entities through `data/synonym-map.md` first).

**4 · GATE (system)** — sort the survivors by **home system** into core / bridge / deferred. *This is
the step that keeps another block's disease pathology out of this block's deck.* Full rule below.

**5 · DEPTH + HY gate** — depth by `type` (pharm/micro **comprehensive** · path/genetics/immuno
**lean** · foundational **all-tier recognition**); tiers 1+2, all-tier for foundational lectures and
for slide-flagged-HY entities with no 1+2 card.

## Resource combination

| Resource | When | Why |
|---|---|---|
| `#FirstAid` | **every lecture (mandatory)** | unique cards *and* the leaf granularity that lets steps 3–4 scope tight |
| `#B&B` / `#Bootcamp` | every lecture (the backbone frame) | frames the lecture — **never sufficient alone** |
| `#Sketchy*` | **only** `type` = `pharm` or `micro` (plus skin/MSK path) | ~0 unique value on concept lectures; pure noise cost there |
| `#Pathoma` | path lectures | precise chapter leaves for general pathology |
| `^Systems` | broad lectures + **the system gate** (step 4) | coarser than resource trees; its `::<System>::` node is what the gate reads |

---

## 🧭 The system gate (step 4) — *the fix for cross-system bleed*

**The failure it exists to stop.** An MSK lecture teaches **Type IV hypersensitivity**. The entity
intersection is doing its job — every card it keeps genuinely names Type IV. But Type IV is a
**cross-system attractor**: AnKing cards it under Endo (DM1), GI (celiac), Derm (contact dermatitis),
ID (TB / PPD), MSK (RA). So the deck arrives carrying the **full pathology of Diabetes Mellitus Type
1** — autoantibodies, DKA, insulin regimens, complications — in a musculoskeletal week. Not wrong
cards. **Wrong block.** They're worth learning *when you reach Endo.*

### Step 1 — classify each surviving card by home system

1. **`^Systems::<System>::…` tag** → that's its home system (a card may carry more than one).
2. **No `^Systems` tag** → read the resource-tree chapter (`#FirstAid::09_Endocrine::…`,
   `#B&B::09_Endocrinology::…` → Endo).
3. **Neither resolves to an organ system** — general chapters: biochem, molecular/cell bio, genetics
   principles, general pathology, general immunology, general pharm, general micro → the card is
   **system-agnostic**. These are the mechanism cards. They are always core.

### Step 2 — sort into three buckets

| Bucket | What it is | What happens to it |
|---|---|---|
| **CORE** | home system **==** `current_block`, **or** system-agnostic | unsuspended + tagged, exactly as before |
| **BRIDGE** | foreign-system card that teaches **the lecture's own concept** through a foreign example — the answer is the mechanism/classification ("DM1 is which hypersensitivity type?"), not that disease's workup — **and the slides name that example** | **one recognition card per named example.** Same shape as the organism-depth guardrail |
| **DEFERRED** | foreign-system **depth**: that disease's own presentation, labs, diagnosis, treatment, complications, prognosis | **not unsuspended.** Offered at Stage 3 as an opt-in add-on and written to the run log as a re-runnable query, so it's waiting for you when that block arrives |

**When `current_block = General`** (a foundations block with no body system) core = **system-agnostic
only**; every organ-system card is bridge-or-deferred. This is the common M1 case, and it is what
keeps an immunology lecture from importing endocrinology.

### Step 2b — ⚖️ what the gate NEVER cuts (the over-blocking guard)

**The gate cuts DEPTH in another system. It never cuts BREADTH of the shared concept.** A concept
whose whole point is that it shows up all over the body — **β-adrenergic receptors**, autonomic tone,
collagen types, hypersensitivity, second messengers — *is* its distribution. Cutting the organs out of
it doesn't scope the deck, it guts the lecture.

So for every foreign-system card ask the one question that separates the two:

> **Is this card teaching the CONCEPT (as it appears in that organ), or is it teaching that ORGAN'S
> disease?**

(Verdicts below assume the lecture **teaches the receptor map** — the foundational pharm case. If it
only *uses* one row, the floor shrinks with it: see *Same entity, different lecture* two sections down.)

| Card | Verdict | Why |
|---|---|---|
| "β1 → ↑heart rate, ↑contractility, renin release" | **CORE** | the receptor's distribution map *is* the lecture — Cardio words, not a Cardio card |
| "β2 → bronchial smooth-muscle relaxation" | **CORE** | same map, lung row |
| "α1 vs α2 vs β1 vs β2 tissue table" | **CORE** | the map itself |
| "Albuterol vs salmeterol in stepwise asthma management" | **DEFERRED** | pulmonology therapeutics, not receptor pharmacology |
| "Which β-blocker is contraindicated in decompensated heart failure?" | **DEFERRED** | Cardio disease management |
| "Beta-blocker overdose → glucagon antidote" | **DEFERRED** | tox depth (unless the slides teach it) |
| "DM1 is which hypersensitivity type?" | **BRIDGE** | one recognition card for a slide-named example |
| "DKA management / insulin regimens" | **DEFERRED** | Endo disease depth |

**The tell is the ANSWER, not the words.** A card is core when its answer is the shared mechanism —
even if the question mentions the heart, the lung, or the pancreas. It is deferred when its answer is
that organ's presentation, diagnosis, treatment, or complications. **Organ vocabulary is not
organ-system scope.**

Two corollaries, both about not over-blocking:

- **A card's organ-system tag is evidence, not a verdict.** Cards carrying *both* a general chapter
  (basic pharm, general physio, biochem) and an organ-system tag are usually the shared-mechanism card
  filed under where it's used. Read it before you defer it — the general chapter usually wins.
- **The effector map is floor only when the slides teach it.** If the professor put up the α1/α2/β1/β2
  tissue table, **every row is an inventory concept** and gets its card. If the lecture merely *uses*
  one row — an MSK lecture noting β2 agonists cause skeletal-muscle tremor — then **only that row is
  floor**, and the heart/lung rows are foreign-system breadth: one recognition card at most, the rest
  deferred. **The slides decide the breadth; the block decides the depth.** The one-card bridge cap
  applies to what the slides name in passing, never to a table the professor taught.

### Step 3 — the floor still wins (non-negotiable)

The system gate is a **depth and priority** filter. It is **never** a coverage filter.

- **It may never remove the last card covering a Stage-0 inventory concept.** If the slides teach it,
  it is core — whatever system the card lives in.
- A disease the slides genuinely **teach** (not name-drop) is *this lecture's* subject and is core
  even when it belongs to another system. `current_block` never overrides the slides; it only decides
  what happens to everything the slides *didn't* ask for.
- Deferring is not dropping. Every deferred set is logged with its query and re-offered when
  `current_block` becomes that system.

### Worked example — β-adrenergic receptors, foundational pharm lecture (`General`)

```
entity: beta-adrenergic receptors   type: pharm   current_block: General
  wide net .................................. 260 candidates
  ∩ slides (entity match) ................... 84
  ∩ system (gate) ...........................
      CORE      41  receptor map + G-protein/cAMP mechanism + agonist/antagonist classes
                    ↑ INCLUDES the cardiac (β1) and pulmonary (β2) rows — that IS the concept
      BRIDGE     3  asthma · heart failure · glaucoma — one card each, the uses the slides name
      DEFERRED  40  Pulm/asthma-COPD regimens 18 · Cardio/HF + antiarrhythmic + HTN selection 15 ·
                    tox & ophtho depth 7          → offered, not unsuspended
```

**Note what did NOT get cut:** every organ in the receptor's distribution stayed. The gate removed
40 cards of *disease management in those organs* — asthma step-therapy, HF drug selection — not the
lung and heart rows of the receptor table. **Breadth of the concept: kept. Depth in the other block:
deferred.**

### Same entity, different lecture — β-receptors inside the **MSK** block

Now the block is `MSK` and a lecture only *uses* β-receptors (β2 agonists → skeletal-muscle tremor,
hypokalemia). The professor never put up the tissue table, so **the table is not in the inventory** —
and the carve-out above does not apply to it:

```
entity: beta-adrenergic receptors   type: physio   current_block: MSK
  ∩ slides (entity match) ................... 84
  ∩ system (gate) ...........................
      CORE       7  what the slides teach: β2 on skeletal muscle, tremor, K+ shift,
                    + the definitional "β1/β2 are Gs → cAMP" card the lecture leans on
      BRIDGE     2  one card each for the uses it name-drops (asthma · heart failure)
      DEFERRED  75  the whole cross-body receptor map + Cardio/Pulm therapeutics
                    → offered, logged, and waiting when Cardio and Pulm come around
```

**Same 84 on-scope cards, opposite verdicts — because the two lectures taught different things.**
In the foundational pharm lecture the cross-body map *was* the lecture (41 core). In the MSK lecture
it's another block's breadth riding in on a shared receptor (7 core). Nothing here is decided by how
"related" a card feels: **the inventory sets what's core, the block sets what's deferred.**

### Worked example — Type IV hypersensitivity, MSK block

```
entity: Type IV hypersensitivity      type: immuno      current_block: MSK
  wide net .................................. 214 candidates
  ∩ slides (entity match) ................... 91
  ∩ system (gate) ...........................
      CORE      38  MSK (RA, PM/DM) + system-agnostic immunology (T-cell mech, 4 types, timing)
      BRIDGE     6  one card each: DM1 · celiac · contact dermatitis · TB/PPD · MS · Hashimoto
      DEFERRED  47  Endo/DM1 pathology 22 · GI/celiac 14 · Derm 11   → offered, not unsuspended
  built: 44        deferred: 47 (logged, re-offered in the Endo/GI/Derm blocks)
```

Before the gate this lecture built **91 cards, half of them another block's disease pathology.**

---

## Method (backbone + coverage supplement)

1. **Your `backbone_resource` IS the deck + naming lens.** Map each lecture's objectives to its leaf tags; deck names follow that resource's chapter topics.
2. **Supplement from other trees ONLY to fill specific coverage gaps** — pull the individual card that closes a gap, never a whole other chapter (that over-pulls). Author a custom card only for genuine framework gaps AnKing has no card for at any tag.
3. **Tier = `yield_filter`** (default `1+2`); foundational/intro/definitional lectures go all-tier.
4. **Verify every build with a coverage audit** — map the finished deck against the slides' concepts; confirm every concept has ≥1 card. Then a card-by-card keep-vs-cut pass against the slides to drop off-lecture ride-alongs.
5. **One deck per lecture**, tagged `Sched::<Class>::M<n>-W<nn>::<System>::<lecture>`; merge only when two lectures map to one unsplittable leaf.

## Operating principles

1. **Propose-only until Stage 3.** Nothing is unsuspended, tagged, or decked before explicit approval.
2. **The floor rule.** Everything the materials teach ends up carded — AnKing card or custom. No
   filter, tier, gate, or trim may drop the last card covering a material concept.
3. **The wide net is a candidate universe.** Casting a whole chapter is fine; unsuspending one is the
   error.
4. **Scope = tags ∩ slides ∩ system** (above). All three axes, every lecture.
5. **Deck status marker.** A slide-verified deck gets the clean name; a deck built without slides
   (objectives/title only) gets a trailing ` 🚧`, dropped when it's reconciled against the materials.
6. **Depth follows `type`, not appetite.** pharm/micro comprehensive · path/genetics/immuno lean ·
   foundational recognition. An *intro-to-micro* lecture is `foundational`, not `micro`.
7. **The tangent audit.** After coverage is proven, a card-by-card keep-vs-cut pass against the slides
   re-suspends cards covering **no** inventory concept — and may never remove the last card covering
   one. Procedure: `reference/playbook.md` → Stage 4.5 step 4.
8. **Deferring ≠ dropping.** Cross-system depth is logged with its query and re-offered when you reach
   that block.
