# anki-week — Operating Manual (ChatGPT Knowledge file)

**Upload this to the Custom GPT's Knowledge.** It is the single authoritative ruleset for building a
week's AnKing Step Deck. It is written *for ChatGPT* — unlike the Claude Code `config.md` / `playbook.md`,
it contains no git/Cowork/localhost-MCP transport instructions and **no superseded historical rules**.
Where those files disagree with this one, **this file wins**.

Each section below is self-contained so it retrieves cleanly on its own.

---

## SECTION 1 — Intake: read the MATERIALS first

**Order matters. The calendar is an INDEX, not a scope.**

1. **Calendar** → tells you *which lectures exist this week*, so you know **which materials to go read**.
   Never map cards from a calendar title.
2. **THE MATERIALS (slides / PDF) → the primary source. Read them FIRST and in full.** Ask the user to
   paste the slide text or upload the PPTX/PDF.
3. **Syllabus objectives → a cross-check that may only ADD scope.** An objective naming something the
   slides don't spell out *adds* to the floor. An objective may **never** remove a slide concept.

**Output: a per-lecture CONCEPT INVENTORY** — every distinct thing the slides teach: definitions, named
frameworks and ordered lists, mechanisms, numbers/kinetics, organisms, drugs, diseases. Read the whole
deck, not just title/objective slides. **A concept you fail to write down is a concept the deck will
silently miss.**

**No materials posted?** Do not hold the lecture. Build **wide from the objectives** — scope
deliberately large, since there's no floor to measure against — and mark the deck **🚧**. Reconcile with
a full coverage pass when the materials arrive; that's what flips 🚧 → Final.

**Never invent concepts.** If materials are missing, ask.

---

## SECTION 2 — The COVERAGE FLOOR (and what it is *not*)

**The concept inventory is a floor.** Everything the lecture teaches must end up covered by a card —
a real AnKing card or a custom one. A deck that omits something the professor taught is broken, however
clean its tags look.

**But the floor is a COVERAGE requirement, NOT a card-volume licence.**

- "Err bigger" means: *when a specific concept looks uncovered, include the card that might cover it.*
- It does **NOT** mean: unsuspend more in case it's useful. Casting a wide **candidate** net is correct
  (Section 3); **unsuspending** anything the slide-entity intersection didn't keep is the failure.
- **A bloated deck and an under-covered deck are both build failures.** The **Selection Protocol**
  (Section 3) — *scope = tags ∩ slides* — is how you avoid trading one for the other.

**No filter outranks the floor.** The yield filter, tier settings, and pace trimming are
*prioritisation* devices. If a material concept's only card sits below the configured tier, take it
anyway — **for that concept only** — and flag it in the proposal.

---

## SECTION 3 — THE SELECTION PROTOCOL: **Scope = tags ∩ slides**

> **Resource tags tell you where a card *could* live. The slides tell you what this lecture *is about*.
> Scope is the INTERSECTION.**

**Never scope from the tag tree alone** — whole-chapter pulls overscope. **Never scope from a narrow tag
guess alone** — that under-covers. Cast a **wide candidate net**, then **intersect it with the named
entities the slides actually contain.** The intersection is what "knows" to keep antifungals and drop
systemic antibiotics — *terbinafine* is on the slides, *piperacillin* isn't.

**⚠️ The wide net is a CANDIDATE UNIVERSE ONLY. Only entity-intersected survivors get unsuspended.**
Casting a whole chapter is free and expected; *unsuspending* one is the error.

### Step 1 — Build the SCOPE SPEC from the slides
Regenerate every run. It needs no prior domain knowledge, which is what makes this work on any lecture.

```yaml
lecture: IM45
type: pharm        # pharm|micro|path|genetics|immuno|physio|histo|anatomy|embryo|foundational
entities:
  drugs:           [terbinafine, griseofulvin, ...]
  organisms:       [Trichophyton rubrum, ...]
  genes_proteins:  [squalene epoxidase, ...]
  diseases:        [tinea capitis, ...]
  stains_markers:  [KOH prep, Wood's lamp, ...]
named_rules:       ["squalene epoxidase inhibition", ...]   # mechanisms/eponyms with NO proper noun
high_yield:        [terbinafine, ...]                        # slide BOLD/RED
```

### Step 2 — Cast the WIDE NET

| Resource | When | Why |
|---|---|---|
| **First Aid** | **EVERY lecture — mandatory** | Concept-leaf granularity adds unique cards *and* lets you scope tight. `(B&B/Bootcamp)+FA` = **95–100%** coverage on concept lectures. |
| **B&B / Bootcamp** | Every lecture, as the frame | **Never sufficient alone** — 66–95% coverage, tags too coarse to self-tighten. |
| **Sketchy** | **Only pharm & micro** (plus skin/MSK path) | ~**0 unique value** on pure concept lectures — don't pay the noise cost. |

Namespace: **`#AK_Step1_v12::` only.** Ignore `#AK_Step2_v12`, `#AK_Step3_v12`, `#PANCE`, `#AK_Other`.
Exclude `!DELETE(Duplicate)`.

### Step 3 — INTERSECT
**Keep a card only if its tag or its content names a Scope-Spec entity.** Expand entities with the
synonym map first (Section 4a). Everything else in the net is discarded.

### Step 4 — Depth rule by lecture `type`

| Type | Depth |
|---|---|
| **pharm · micro** | **COMPREHENSIVE** — keep the **whole drug/bug entity** (cumulative, heavily tested) |
| **path · genetics · immuno** | **LEAN** — the on-concept card; tangent-trim the rest |
| **foundational** | **all-tier, RECOGNITION depth** |

**⚠️ An intro-to-micro lecture is `foundational`, NOT `micro`.** That distinction is what keeps a
46-card *S. pyogenes* leaf out of a normal-flora lecture.

### Step 5 — HY gate
Tiers **1+2**, with all-tier exceptions for **foundational** lectures and any **slide-flagged-HY entity
with no 1+2 card** (the board filter drops basics).

### Dedup is a non-issue
AnKing is **one pre-deduped deck** — each card carries *all* its resource tags, so the union never
double-counts. Excluding `!DELETE(Duplicate)` is the whole dedup story. No separate pass.

### Worked proof (Week-2 derm pharmacology)
Wide net included `#SketchyPharm::07_Antimicrobials` = **429 HY cards**. Entity-intersecting against
the slide drug list collapsed it to **~77** (dropping ~**352** systemic-antibiotic cards the lecture
never names). Final deck ≈ **68 notes**.
**Completeness-by-chapter ≠ on-scope coverage. The intersection is the difference.**

### Anti-bloat guardrails that still apply
- **Both directions are failures** — under-covering and bloating are equally build defects.
- **Excluding `::Extra`** up front lowers the noise (AnKing's supplementary-card marker).
- **Custom cards** close true resource gaps only. Never custom-duplicate an existing card.

---

## SECTION 4 — Where the missing 5–10% lives

The intersection is a name-match, so it misses in exactly three shapes. All three are **expected**, and
two of them are fixable.

### 4a. Synonyms — the fixable one (KEEP A SYNONYM MAP)
The slides and AnKing often use **different words for the same thing**, so the card is silently dropped
and resurfaces as a *phantom* coverage gap:
- *isotretinoin* = *13-cis-retinoic acid* = *Accutane*
- *gas gangrene* = *Clostridium perfringens* ← **disease-on-slides vs organism-in-AnKing is the most
  common micro miss**
- *S. aureus* ↔ *Staphylococcus aureus*; eponym ↔ description; enzyme ↔ pathway ↔ gene; class ↔ member

**Expand every entity with its aliases before matching.** When the coverage audit reports a 0-card
entity, check whether AnKing has it under another name — if so that's a **synonym miss, not a resource
gap**: add the alias and re-intersect. **This is the one piece of ongoing tuning; growing it carries
coverage from ~90% toward ~95%.**

**Where it lives here:** the `synonym-map.md` Knowledge file. You **cannot write to Knowledge** — it is
read-only at run time — so every new alias must go out in the run's **APPEND BLOCK** as a ready-to-paste
row, and the user pastes it in and re-uploads the file. An alias you discover but don't emit is lost,
and the same phantom gap returns next week. (The Claude Code skill keeps the same file at
`data/synonym-map.md`, where the skill can append directly.)

### 4b. Entity-less concepts (`named_rules`) — the expected residue
Mechanisms and eponyms with **no proper noun** can't be name-matched. Run a **keyword/content search**;
whatever still misses becomes a **custom card**. **This is the biggest source of misses and it is not a
failure of the method.**

### 4c. True resource gaps
The entity genuinely has no card at any name or tier → **custom card**. AnKing is board-fact-oriented,
not lecture-framing-oriented, so the professor's named frameworks, ordered lists, and kinetics reliably
land here.

### The accuracy meter
The coverage audit (Section 6) already checks every Scope-Spec concept has ≥1 card.
**Report `covered ÷ total` every run**, and say which gaps were synonym misses (with the aliases added)
versus real resource gaps.

---

## SECTION 5 — Finding the right cards: altitude, tiers, subject verification

### Tag roots (AnKing Step Deck v12)
- System tree: `#AK_Step1_v12::^Systems::<System>::<Topic>`
- Resource trees: `#AK_Step1_v12::` + `#B&B::…` · `#FirstAid::…` · `#Pathoma::…` · `#SketchyMicro::…` ·
  `#SketchyPharm::…` · `#SketchyPhysiology::…` · `#Bootcamp::…` · `#Physeo::…` · `#DirtyMedicine::…`
- `#AK_Step2_v12::…` is **out of scope** unless the user asks.

### Altitude — aim for concept LEAVES
Same week, three altitudes: `^Systems::Cardio` ≈ **1,733** notes (a whole block, months of work) ·
`#FirstAid::07_Cardiovascular::03_Physiology` ≈ **616** (a chapter, weeks) ·
`^Systems::Cardio::HeartSounds` ≈ **31** (one lecture).
**A node over ~60 notes is too high — descend to children.** Grabbing a system root causes a review
avalanche.

Note `^Systems` is **coarser** than resource trees: its `HeartSounds` leaf bundles sounds *and* murmurs,
while B&B splits them. Use a `^Systems` leaf for a broad lecture; drop to a resource leaf when the
lecture is narrower.

### Subject verification (the mis-scope trap)
**Before committing a subtree, sample 2–3 of its cards and confirm they match the concept as the
materials teach it. Keyword ≠ subject.** The same word lives in different trees: membrane *structure* is
in `#Biochem::02_Cellular`; membrane *transport physiology* is in `#Physiology`. A "Cell Membrane"
lecture was once built from `#Biochem::Cellular` and came out as organelle/ER/Golgi cards with ~zero
overlap with what was taught.

### Yield tiers
Tags live under `#AK_Step1_v12::#Low/HighYield::…`.
- `1` = `1-HighYield` · `1+2` = adds `2-RelativelyHighYield` **(the standing default)** ·
  `1+2+3` = adds `3-HighYield-temporary` · `off` = all tiers.
- Apply the default **silently**; never re-ask it.
- **EXCEPTION (the default, not rare): foundational / intro / definitional lectures → all-tier.** The
  1+2 filter is tuned for board-dense organ systems and erases exactly the basics these lectures test
  (DNA A/B/Z forms, Gram-stain procedure, prokaryote-vs-eukaryote, plain definitions).
- **The filter always yields to the floor** (Section 2).

### Sizing a subtree cheaply
`find_notes` returns a `total` even with `limit:1` — use it to size before pulling ids. Add
`is:suspended` to any tag query to count what will **actually change** (already-unsuspended cards are
skipped, so reruns are idempotent).

---

## SECTION 6 — The two audits (they catch opposite problems)

Run them in this order. They are **not** the same check.

### 6a. Coverage audit — "does every concept have a card?"
Walk **every concept in the inventory** as an explicit checklist. "Probably covered" is not covered.
Close each gap by walking the ladder (Section 3). AnKing reliably **misses the professor's scaffolding**
— named frameworks, ordered lists, specific numbers/kinetics, step mechanisms, and pure definitions —
so expect a few custom cards per lecture. **The deck is not done while any concept is uncovered.**

### 6b. Tangent audit — "does every card belong?"
Coverage audit confirms every concept HAS a card; it does **not** catch cards that don't belong. Even a
correctly-matched backbone leaf carries deep ride-alongs — the `::Extra` subtag especially, plus
specific-disease, biochem, and adjacent-lecture cards filed under a general leaf.

Go **card by card against the slides**: KEEP if the card tests a slide concept at lecture depth; CUT if
it's an off-lecture disease/drug/other-lecture ride-along. Then untag + re-suspend the cuts.
**Observed cut rates ~40% even on fresh backbone decks** (173→92, 151→91, 57→21, 48→28).

### The invariant tying them together
**The trim may NEVER remove the last card covering an inventory concept.**
Order: **coverage-audit → trim → re-verify coverage is still 100%.** A cut that breaks the floor is a
bug, not a trim.

---

## SECTION 7 — Executing a build (tags, decks, custom cards)

### Weekly tag scheme
`Sched::<Class>::M<n>-W<nn>::IM<##>-<Topic>` — e.g. `Sched::IM::M1-W01::IM20-Acute_Inflammation`.
Slices: class `tag:Sched::IM::*` · all M1 `…::M1-*` · one week `…::M1-W01::*` · one lecture `*::IM20-*`.
Custom cards additionally get **`Sched::custom`** so every hand-made card is listable and undoable.

### note ids vs card ids (the classic trap)
`find_notes` and tagging use **note** ids. Suspend/unsuspend use **card** ids. Resolve via
`notes_info` → each note's `cards[]`. **A note can have more than one card** (60 notes → 84 cards is
normal). `notes_info` caps around 100 notes per batch.

### Filtered decks — one per lecture
Build from the lecture's `Sched::` tag with **reschedule ON**, e.g. search
`tag:Sched::IM::M1-W01::IM20-*`, limit 200, order `added`.
**Gotchas:** a card **cannot be in two filtered decks** (the second gets nothing) · `create_or_update`
on an existing name creates a `+`-suffixed **duplicate** rather than updating → **to replace a deck,
DELETE the old one first** (cards return home, FSRS scheduling intact), then create fresh · you must
unsuspend before building or it gathers nothing.

### Deck status marker
A slide-verified deck gets a clean name (`IM06 · Cell Cycle & Division`). A deck built without
materials gets a trailing **` 🚧`** (`IM07 · DNA Replication 🚧`). Drop the 🚧 once reconciled against
the real materials.

### Custom cards
`add_note` into deck **AnKing Step Deck**, model `Cloze` or `Basic`, in the professor's exact wording,
tagged with the lecture's `Sched::` tag **+ `Sched::custom`**.
**⚠️ This collection's Cloze model requires a `Back Extra` field — pass it (even as `""`) or the add
fails with "Missing required fields."**

### Pacing
Target: finish each week's cards by **that week's Saturday**.
`new/day = ceil(remaining new cards ÷ study-days left until Saturday)`.
**You cannot set New/day programmatically** — report the recommended number and have the user set it in
**Anki ▸ AnKing Step Deck ▸ Options ▸ New cards/day**.

### Sync
Sync at both ends of a build so the phone matches.

### Undo
`find_notes query="tag:Sched::<week>::* -is:suspended"` → `notes_info` → `cards[]` →
`card_management` suspend. Optionally remove the `Sched::` tags and delete the filtered decks.

---

## SECTION 8 — Edge cases

| Situation | Handling |
|---|---|
| Anki not reachable | In advisory mode this is normal — produce the plan. In live mode, stop and ask the user to open Anki; change nothing. |
| Zero matches for a concept | Flag it "no AnKing match — map manually?" — never silently drop. It survives to the coverage audit as a custom-card candidate. |
| Lecture has no materials | Build wide from objectives, mark 🚧, reconcile later (Section 1). |
| Materials arrive mid-week | Re-read them, rebuild the inventory, re-run the coverage audit, flip 🚧 → Final. |
| Over the pacing cap | Surface it with raise / trim / spillover options — and say which concepts a trim would leave uncovered. |
| Re-running the same week | Idempotent: `is:suspended` skips already-unsuspended cards; don't double-add tags. |
| Concept maps to two systems | Show both subtrees in the proposal and let the user pick. |
| Calendar lists a lecture whose materials can't be found | Say so explicitly and build from objectives (🚧) — never quietly skip the lecture. |
