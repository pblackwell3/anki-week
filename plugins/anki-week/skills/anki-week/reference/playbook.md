# anki-week — Playbook (detailed procedure)

The exact steps the skill runs each week. All Anki actions go through the `anki` MCP (the **Anki MCP Server** add-on, code `124672614`, serving `http://127.0.0.1:3141`). **Propose-only until Stage 3 approval.**

---

## Multi-device sync (git + AnkiWeb) — every run

If you keep this skill in a git repo, multi-device sync is optional but recommended once you run from
more than one Mac. Two sync streams, same rhythm — **latest before, save after**:

**Start of run (before Stage 0):**
- `git pull --rebase --autostash` in the skill's repo — pull the latest tag-map/run-log from the other Mac.
- Anki `sync` — pull the latest cards.
- Conflict in `data/tag-map.md` / `data/run-log.md`? Both are append-only → resolve by **keeping both sides' new lines**, then continue.

**End of run (after Stage 5 writes):**
- `git add -A && git commit -m "anki-week: <week> run" && git push`
- Anki `sync` — push the cards.

Skip the start-pull → you risk overwriting the other Mac's brain. Skip the end-push → its growth never travels. **One machine at a time; sync both ends** — same discipline for git and AnkiWeb.


---

## Stage 0 — Intake  (MATERIALS-FIRST)

Goal: produce `{ week, study_days, next_drop, lectures[{concepts[], objectives[], refs[]}], exam_date? }`
— where each lecture's **`concepts[]` is the inventory of what its MATERIALS actually teach**. That
inventory is the **coverage floor** for Stages 1–4.5.

**Order matters.** The calendar tells you *which materials to go read*; the materials tell you *what the
deck must cover*. Never map cards straight off a calendar title or a syllabus line — that is the IM04
failure mode.

**📄 "Materials" = the professor's slide FILES — `.pptx` / `.ppt` / `.pdf` in the week folder (or pulled
from Blackboard). An Anki deck is never materials.** In particular a deck named **`Meharry Slides`** is
pre-made cards, not the lecture: **never** read it to build `concepts[]`, and **never** count it as
"materials present." The only thing Anki supplies in this skill is the **card library** (`deck_name` /
`tag_namespace`). If the PPTX/PDF isn't on disk, the lecture has **no materials** → step 5 / the fetch
ladder → Blackboard.

**First: sync** — run the start-of-run sync from *Multi-device sync* above (`git pull` + Anki `sync`) so you begin from the latest brain + cards.

1. **Read config** from `data/config.md` (course folder path, deck name, cap, tag prefix).
2. **Calendar = the INDEX of what to read.** Read the week's lecture events from the Meharry calendar (id in `config.md`) via `list_events`. The events (`IM (n) <Lecture>`) enumerate **which lectures exist this week**, the Mon–Fri boundary, and any exam/holiday — so you know **which materials to hunt down**. It is an index, **not a scope**: never map a lecture from its calendar title. NOTE the imported gcal can DROP a lecture (it omitted IM17 Normal Flora) — cross-check the list against the syllabus Course Outline.
3. **READ THE MATERIALS — the primary pass.** For every lecture the calendar named, locate and fully read its **slide files** in `<course_folder>/<Course>/Week <n>/` (they sit **directly inside**). **This is a filesystem check — you are looking for PPTX/PDF files, not for anything inside Anki.** This is the step that defines scope:
   - `*.pptx` / `*.ppt` → full slide text via the **pptx** skill (legacy `.ppt` binary → the PowerPoint-atom parser; see `config.md`).
   - `*.pdf` → full text via the **pdf** skill / **PyMuPDF** (see `config.md` — the old zlib method mangles CID PDFs).
   - optional `refs.md` / `notes.md` → resource refs. Skip non-lecture files (e.g. "How to Learn Anatomy", Anatomage links, sample-question decks).
   - **Enumerate a concept inventory per lecture** — every distinct thing the slides teach: definitions, named frameworks/lists, mechanisms, numbers/kinetics, diagrams, drugs/diseases named. Read the *whole* deck, not just title/objective slides. This list is what Stage 4.5 audits against, so be exhaustive: **a concept you fail to write down is a concept the deck will silently miss.**
   - **A lecture's folder can be incomplete** (Week 1's folder missed all immunology). Missing materials ≠ no lecture — the calendar already told you it exists; go to step 5.
4. **Syllabus = cross-check + supplement.** Read the course syllabus (path in `config.md`; extract the .docx via `unzip -p <docx> word/document.xml`, split on `</w:tr>`/`</w:tc>`, strip tags). Its **Course Outline** table gives each lecture's Learning Objectives + the exam structure (`Session # == IM (#)`). Use them to **catch what the slides imply but don't spell out** — an objective naming something absent from your inventory **adds** to the floor. Objectives may **only widen** scope, never narrow it: never drop a slide concept because the syllabus omits it.
5. **No materials posted yet?** (= no PPTX/PDF in the week folder **and** the fetch ladder failed — *not* "there's a `Meharry Slides` deck in Anki," which changes nothing here.) Do NOT hold the lecture. Build it **generously from the objectives** (then the title), scope **deliberately wide** — there is no material floor to measure against, so err large — and mark the deck **🚧**. Reconcile via a full Stage-4.5 pass when the materials land (that's what flips 🚧 → Final).
6. **Fallbacks:** if no folder at all, accept slides/refs pasted in chat. If a connector is unavailable, ask the user for the missing piece — never invent concepts.
7. Consolidate per lecture into `concepts[]` (the floor) + `resource_refs[]` (precise) for Stages 1–2.
8. **Build the SCOPE SPEC** — the input the Selection Protocol runs on (`config.md` → *Scope = tags ∩ slides*). Regenerate it every run from the slides; it needs no prior domain knowledge, which is what lets this work on any lecture:
   - **`type`** (one of): `pharm` · `micro` · `path` · `genetics` · `immuno` · `physio` · `histo` · `anatomy` · `embryo` · `foundational`. **This drives the depth rule at Stage 2** — an *intro-to-micro* lecture is `foundational`, NOT `micro`.
   - **Typed entity lists:** `drugs[]`, `organisms[]`, `genes_proteins[]`, `diseases[]`, `stains_markers[]`.
   - **`named_rules[]`** — mechanisms/eponyms with **no proper noun** to match on. Track these separately: they can't be entity-matched and are the biggest source of misses (keyword search, else a custom card). Expected residue, not a failure.
   - **`high_yield[]`** — entities the slides **bold/red**. Flag them; they get the all-tier exception at Stage 2 if 1+2 has no card.

---

## Stage 1 — Cast the WIDE NET (candidate universe)

Goal: a **candidate pool**, deliberately wide. Per `config.md` → *Selection Protocol*:
**`(B&B/Bootcamp) + FirstAid` for every lecture, `+ Sketchy` only if `type` is `pharm` or `micro`** (or skin/MSK path). **FA is mandatory on every lecture** — it both adds unique cards and gives the concept-leaf granularity that lets Stage 2 scope tight. Namespace: **`#AK_Step1_v12::` only** (ignore `#AK_Step2_v12`, `#AK_Step3_v12`, `#PANCE`, `#AK_Other`). Exclude `!DELETE(Duplicate)`.

**⚠️ THE NET IS A CANDIDATE UNIVERSE — NOTHING HERE GETS UNSUSPENDED.** Casting a whole chapter is fine and expected; *unsuspending* one is the error. Stage 2's entity intersection is what collapses it (measured: `#SketchyPharm::07_Antimicrobials` 429 HY → ~77 on-scope). **Dedup is a non-issue** — AnKing is one pre-deduped deck and each card carries all its resource tags, so the union never double-counts.

**⚠️ Yield filter — read `yield_filter` from `config.md` and apply it silently every run; never re-ask** (it's a set-once preference; standing default `1+2`). Build the OR-clause from the value and AND it into *every* candidate/size query (tags under `#AK_Step1_v12::#Low/HighYield::…`):
- `1` → `(tag:…::1-HighYield)`
- `1+2` *(current default)* → `(tag:…::1-HighYield OR tag:…::2-RelativelyHighYield)`
- `1+2+3` → add `OR tag:…::3-HighYield-temporary` (re-enables the tier dropped 2026-06-21 to protect Qbank time)
- `off` → no filter (all tiers, incl. low-yield/unrated)

Never propose or unsuspend tiers outside the configured set. Apply the filter to the size probes too, so every count reflects what you'd actually unsuspend. If `yield_filter` is missing from config, default to `1+2`, note it once, and continue — don't stop to ask.
**EXCEPTION (default, not rare): foundational / intro / definitional lectures → drop the filter, go all-tier.** AnKing rates the basics these lectures test (DNA A/B/Z forms, Gram-stain procedure, prokaryote-vs-eukaryote, helix stability, plain definitions) at tier 3–4, so 1+2 erases exactly the testable content. When a concept returns ~0 at 1+2 but real cards all-tier, include them all-tier. 1+2 stays the default only for board-dense organ-system lectures.
**THE FILTER YIELDS TO THE FLOOR (per-concept, always).** The yield filter is a *prioritization* device, never a coverage device. If a concept in the material inventory has no card at the configured tier but has one at a lower tier, **take the lower-tier card** — for that concept only. A tier setting must never be the reason the deck fails to teach something the professor taught. Flag each such drop-to-all-tier in the Stage-3 proposal so the tier picture stays honest.

**🔬 Subject-verification (anti-mis-scope — the IM04 lesson):** before you commit a subtree, `notes_info` 2–3 of its cards and confirm they actually match the CONCEPT as the materials teach it — **keyword ≠ subject.** The same word lives in different resource trees: membrane *structure* is in `#Biochem::02_Cellular`, membrane *transport physiology* is in `#Physiology`; "Gene Structure & Function" = transcription/translation (a different lecture than DNA-structure). IM04 "Cell Membrane" was built from `#Biochem::Cellular` and came out as organelle/ER/Golgi cards with ~zero membrane-transport overlap. A subtree whose name matches the title can still be the wrong subject.

**Tag roots (AnKing Step Deck v12, verified against this collection):**
- System tree: `#AK_Step1_v12::^Systems::<System>::<Topic>`
- Resource trees: `#AK_Step1_v12::#FirstAid::…`, `#AK_Step1_v12::#B&B::…`, `#AK_Step1_v12::#Bootcamp::…`, `#AK_Step1_v12::#Physeo::…`, `#AK_Step1_v12::#SketchyPharm::…` / `#SketchyMicro::…` / `#SketchyPhysiology::…`, `#AK_Step1_v12::#DirtyMedicine::…`, `#AK_Step1_v12::#Pathoma::…`
- Step 2 equivalents live under `#AK_Step2_v12::…` (ignore in v1 unless the user asks).

**Resolution order per concept** (work the Stage-0 inventory, concept by concept — not the lecture title):
0. **🦠 RESOURCE-COMBINATION CHECK — do this FIRST.** Read the Scope Spec's `type`. **FirstAid goes in on EVERY lecture (mandatory).** **Sketchy goes in ONLY if `type` is `pharm` or `micro`** (plus skin/MSK path) — `#SketchyMicro::…` for bugs, `#SketchyPharm::…` for drugs; it has ~0 unique value on pure concept lectures, so don't pay its noise cost there. B&B/Bootcamp frames every lecture but is **never sufficient alone**. See `config.md` → *Selection Protocol · Resource combination*.
1. **tag-map hit** — if `data/tag-map.md` already maps the concept/ref → leaf tag(s), use them directly.
2. **resource ref** — map a `refs.md` entry to its resource subtree, e.g. `FA Cardiovascular Physiology` → `tag:#AK_Step1_v12::#FirstAid::07_Cardiovascular::03_Physiology::*`.
3. **system anchor** — map the topic to a system subtree, e.g. cardio → `tag:#AK_Step1_v12::^Systems::Cardio::*`.

**Enumerating an unmapped Sketchy subtree:** `get_tags` filtered by the `#AK_Step1_v12::#SketchyMicro::` prefix (or the browser tag tree) — **never** by sampling sequential note ids, which cluster by topic. Record confirmed organism → leaf pairs into `data/tag-map.md` at Stage 5.

**Query form (standard Anki search syntax):** quote the whole thing, `::` for hierarchy, trailing `*` for descendants, e.g.
`find_notes query="tag:#AK_Step1_v12::^Systems::Cardio::HeartSounds*"`.
`find_notes` returns a `total` even with `limit:1` — use it to size a subtree cheaply before pulling ids.

**Altitude rule:** if a node returns more than ~one-lecture's worth (rule of thumb >60 notes), it's too high — descend to children. Record the sizes; you'll show them at Stage 3.

**`^Systems` is coarser than resource trees (verified):** a `^Systems` leaf can bundle what a
lecture splits — e.g. `^Systems::Cardio::HeartSounds` (31) contains both sounds AND murmurs, while
B&B separates `…Cardiac_Auscultation::01_Heart_Murmurs` vs `::02_Heart_Sounds`. Rule: use a
`^Systems` leaf for a broad lecture; drop to a **resource leaf** when the lecture is narrower than
the Systems leaf. Enumerate a system's child leaves via the Anki browser tag tree or `get_tags`
filtered by prefix — NOT by sampling sequential note ids (they cluster by topic and mislead).

---

## Stage 2 — INTERSECT the net with the slides (this is the scoping step)

Goal: the final on-scope set. **Scope = tags ∩ slides.**

**Keep a card only if its TAG or its CONTENT names a Scope-Spec entity.** Everything else in the net is discarded — not unsuspended, not tagged. This one step is what distinguishes on-scope coverage from completeness-by-chapter.

1. **Expand entities with `data/synonym-map.md` first.** The slides and AnKing often use different words for the same thing (*isotretinoin* / *13-cis-retinoic acid*; *gas gangrene* / *C. perfringens*). An un-expanded entity silently drops its cards and resurfaces as a phantom gap at Stage 4.5.
2. **Match** each candidate card against the expanded entity lists (`drugs`, `organisms`, `genes_proteins`, `diseases`, `stains_markers`) — tag text **or** card content counts as a hit.
3. **Apply the depth rule for the lecture's `type`:**
   - **`pharm` · `micro` → COMPREHENSIVE.** Keep the **whole entity** for every drug/bug the slides name — these are cumulative and heavily tested. Don't thin them.
   - **`path` · `genetics` · `immuno` → LEAN.** The on-concept card; tangent-trim the rest at Stage 4.5.
   - **`foundational` → all-tier, RECOGNITION depth.** The intro-lecture rule. *An intro-to-micro lecture is `foundational`, not `micro`* — that distinction is what keeps a 46-card `Streptococcus_pyogenes` leaf out of a normal-flora lecture (as IM17 correctly did).
4. **HY gate** = tiers 1+2, with the all-tier exception for `foundational` lectures **and** for any `high_yield`-flagged entity that has no 1+2 card.
5. **`named_rules[]` don't entity-match** — they have no proper noun. Run a keyword/content search for each; whatever still misses becomes a Stage-4.5 custom card. **Expected residue, not a failure.**
6. For each survivor set, compute `… is:suspended` = what will actually change (reruns stay idempotent).
7. Produce the **scope table**: `entity | source tag(s) | candidates | on-scope kept | suspended(actionable)` — and report the collapse (e.g. "429 candidates → 77 on-scope") so the intersection is visible at Stage 3.
8. **Floor pre-check** — mark every Scope-Spec entity and `named_rule` with **zero** on-scope cards. These are the Stage-3 "no AnKing card" flags and Stage-4.5 custom-card candidates. Carry the list forward; never let it silently empty.

---

## Stage 3 — Propose → approve  (HARD GATE)

Show the user, then **wait**:

```
Week 2026-W25 · Cardio  (materials read: cardio_phys.pptx 41 slides, murmurs.pdf 28 pp)
  Concept inventory: 23 concepts across 2 lectures
  ✓ Cardio::HeartSounds        31 cards (31 new)      ← covers 6 concepts
  ✓ Cardio::Murmurs            28 cards (24 new)      ← covers 7 concepts
  ? Cardio::CardiacCycle       40 cards (40 new)      ← adjacent, include?
  ⚠ UNCOVERED (3): Levine grading scale · maneuvers table (squat/Valsalva) · S3 age-dependence
      → no AnKing card at any tier; propose 3 custom cloze
  ⓘ 2 concepts pulled all-tier (below yield_filter 1+2) to hold the floor: JVP waveform, pulsus paradoxus
  Total if approved: 95 AnKing + 3 custom
  Pacing: 95 ÷ 7 study-days = 14/day  (under cap 25 ✓)
  Sample (HeartSounds): "Apex (Supine; Bell)… {{c1::Single S1 S2}}"
Approve / trim which leaves?
```

- Never call `unsuspend`/`add_tags` before explicit approval.
- **Always show the uncovered-concept list** (even when empty — "floor met, 23/23"). It is the whole point of the proposal: the user is approving *coverage*, not just a tag list.
- If `Total ÷ study-days > cap`: show the conflict + 3 options (raise cap / trim / accept spillover). User decides here. **Trimming for pace may cut breadth, never a floor concept** — if pace forces a real cut, say which concepts would go uncovered and let the user choose explicitly.

---

## Stage 4 — Execute (only after approval)

1. **`sync`** — pull latest first.
2. **Resolve notes → cards.** `find_notes` gives **note** ids; suspend/unsuspend need **card** ids. For the approved leaves: `find_notes` → `notes_info(noteIds, include_fields:[])` → collect each note's `cards[]`. Keep the noteIds (for tagging) and cardIds (for unsuspend).
3. **Unsuspend:** `card_management` action `unsuspend` with the card ids. (Idempotent — only currently-suspended cards change.)
4. **Tag per lecture:** `tag_management` `add_tags` (or `replace_tags{note_ids,old_tag,new_tag}` when renaming) with `Sched::<Class>::M<n>-W<nn>::IM<##>-<Topic>` — e.g. `Sched::IM::M1-W01::IM20-Acute_Inflammation`. Class = course code; `M-W` = academic year+week. One tag per calendar lecture.
5. **Filtered deck per lecture:** `filtered_deck` `create_or_update` named e.g. `IM20 · Acute Inflammation`, `search_terms:[{search:"tag:Sched::IM::M1-W01::IM20-*", limit:200, order:"added"}]`, **reschedule ON**. **Status marker:** a slide-verified deck gets the clean name; a **title-only** deck (no slides reconciled) gets a trailing ` 🚧` (= In Progress) — drop the 🚧 when you later reconcile it against slides. See *Operating principles* in `config.md`. Must unsuspend first (step 3) or it pulls nothing. **To replace a deck: `delete` the old deck(s) first, THEN create fresh** — a card can't be in two filtered decks (else 0), and `create_or_update` on an existing name makes a `+` duplicate instead of updating. (unsuspend = `{action:"unsuspend", card_ids:[…]}`; notes→cards via `notes_info().cards[]` — a note can have >1 card.)
6. **Pace:** the MCP has **no New/day setter** (only `filtered_deck`/`create_deck`/`card_management`). **Report the recommended number**; user sets it in Anki ▸ Deck Options ▸ New cards/day. Standing New/day meters intake — graceful, not blocking. Don't `set_due_date` brand-new cards to fake pacing.
7. **`sync`** — push so the phone matches.

---

## Stage 4.5 — Coverage audit (the step that was missing)

After the deck is built, **prove it covers the lecture** — don't assume "right tag" = "covered." This is what a 2026-06-27 slide audit found absent: decks pulled plausible tags but missed the professor's frameworks/lists/definitions, and IM04 was pointed at the wrong subject entirely.

1. **Take the Stage-0 concept inventory** (the materials' concepts ∪ the syllabus objectives). This is the floor — audit against the *inventory*, not just the objectives; the slides always teach more than the syllabus lists.
2. **For each concept, confirm ≥1 card covers it** — read the deck's cards (`notes_info include_fields:["Text"]` on the `Sched::` tag) and map each concept to a card. Track it as an explicit checklist; "probably covered" is not covered.
3. **Close each gap, cheapest fix first** — per uncovered entity/`named_rule`, stopping the moment it's covered:
   - **A synonym miss?** Check `data/synonym-map.md` first — see step 5. Cheapest possible fix; costs nothing but an alias row.
   - **Widen the net or the entity match** — a sibling leaf, or a keyword/content search for a `named_rule` that has no proper noun to match on.
   - **Drop the tier for that entity only** and take the lower-tier card (the filter yields to the floor). Per entity, not per deck; flag it.
   - **Author a custom card** — only when AnKing has nothing under any name or tier (named frameworks, ordered lists, kinetics, pure definitions). Never custom-duplicate an existing card.
   - **Depth guardrail throughout:** obey the Scope Spec's `type`. `pharm`/`micro` → keep the **whole** drug/bug entity (comprehensive). `path`/`genetics`/`immuno` → lean. **`foundational` → recognition depth**: a name-dropped disease/drug/organism earns **one** card, not the workup/tetrad/MOA set. *An intro-to-micro lecture is `foundational`, not `micro`.*
4. **Then trim tangents** — the standard card-by-card keep-vs-cut pass against the slides. **⚠️ How hard to trim is set by the lecture `type` (Selection Protocol depth rule), not a fixed rate:** **light on `pharm`/`micro`** (the whole drug/bug entity is deliberately kept — don't thin it), **normal on `path`/`genetics`/`immuno`** (the old ~40% figure came from these). Entity-intersected builds start far cleaner than the old whole-leaf backbones, so expect smaller cuts across the board. It removes cards covering **no** inventory concept: off-lecture disease/drug depth, `::Extra` ride-alongs, adjacent-lecture content (SIRS/superantigens/NF-κB drifted into intro-immuno; methemoglobinemia/calcification into cellular injury) → re-suspend + untag.
   - **Invariant: the trim may never remove the last card covering an inventory concept.** Coverage-audit first, trim second, then **re-verify the checklist is still 100%** — a cut that breaks the floor is a bug, not a trim.
5. **⚖️ Distinguish a SYNONYM MISS from a real gap** — the accuracy step. For every entity reporting **0 cards**, check whether AnKing has it under a *different name*:
   - **It does** → that's a **synonym miss, not a resource gap.** Add the alias to `data/synonym-map.md`, re-intersect, and the card comes back. **This is the one piece of ongoing tuning that carries coverage from ~90% toward ~95% — do it every run.**
   - **It genuinely has no card at any name or tier** → a real **resource gap** → custom card. Resource gaps are expected; they are not protocol failures.
6. **Report the accuracy meter** → `covered ÷ total` over the Scope Spec (entities + `named_rules`), plus: which gaps got custom cards, which were synonym misses (and the aliases added), and the trim count. Into the run-log. **The deck is not done while any Scope-Spec concept is uncovered.**

**Custom card (`add_note`):** `add_note` a `Cloze` (or `Basic`) note into deck **AnKing Step Deck**, fields = the lecturer's exact fact, then tag it `Sched::IM::M1-W01::IM##-<Topic>` **+ `Sched::custom`**. The filtered deck's `tag:Sched::…IM##-*` search pulls it on rebuild; `Sched::custom` lets you list/undo every hand-made card. Keep them atomic and in the professor's wording (the definition, the named list, the specific numbers/kinetics).

**Reconciliation = this audit.** When materials finally arrive for an objective-built (🚧) deck, **read them (Stage 0 step 3) to build the real concept inventory**, then run Stage 4.5 against it — that IS the reconcile: a full coverage pass, not a light trim. A 🚧 deck was scoped wide without a floor, so expect the reconcile to both **add** (concepts the objectives never named) and **trim** (breadth the slides don't support). Flip 🚧→Final once every inventory concept is covered (AnKing card or custom).

---

## Stage 5 — Log + learn

1. Append to `data/run-log.md` (see its format): week, date, leaves + counts, new/day applied, source inputs.
2. Add any **newly-confirmed** topic→leaf mappings to `data/tag-map.md` so the same topic resolves instantly next time.
3. Tell the user: what was unsuspended, the new/day, and the one-line undo (`re-suspend tag:Sched::<week>::*`).
4. **Sync back** — run the end-of-run sync from *Multi-device sync* above: `git add -A && git commit && git push` (saves the grown brain) + Anki `sync` (pushes the cards).

---

## Edge cases

| Situation | Handling |
|---|---|
| Anki not open | `find_notes` errors → STOP, ask user to open Anki, change nothing. |
| Zero matches for a concept | Flag it in the proposal as "no AnKing match — map manually?"; don't silently drop. Survives to Stage 4.5 as a custom-card candidate. |
| Lecture has no materials | Don't hold it. Build wide from objectives/title, mark the deck **🚧**, reconcile (re-read + Stage 4.5) when materials land. |
| Materials land mid-week | Re-read them, rebuild the concept inventory, run Stage 4.5 → flip 🚧→Final. This is the `finalize-week` cascade. |
| Calendar lists a lecture whose materials you can't find | Say so explicitly and build from objectives (🚧) — never quietly skip the lecture. |
| Over-cap week | Surface at Stage 3 with raise/trim/spillover options. |
| Rerun same week | Idempotent: `is:suspended` filter skips already-unsuspended; don't double-add tags. |
| Wrong batch | Undo = re-suspend `tag:Sched::<week>::*` (and optionally remove that tag). |
| Sync conflict | Stop and report; never force a direction. |
| Ambiguous topic (maps to 2 systems) | Show both subtrees at Stage 3, let user pick. |

## Undo recipe

```
find_notes query="tag:Sched::2026-W25::* is:suspended:no"   # what this week unsuspended
# → notes_info → cards[] → card_management suspend(cardIds)
# optional: tag_management remove_tags(noteIds, "Sched::2026-W25::…")
```
