# anki-week — Playbook (detailed procedure)

The exact steps the skill runs each week. All Anki actions go through the `anki` MCP (the **Anki MCP Server** add-on, code `124672614`, serving `http://127.0.0.1:3141`). **Propose-only until Stage 3 approval.**

---


## Stage 0 — Intake

Goal: produce `{ week, study_days, next_drop, topics[], resource_refs[], exam_date? }`.

**First: Anki `sync`** so you begin from the latest cards.

1. **Read config** from `data/config.md` (course folder path, deck name, cap, tag prefix).
2. **Calendar = the lecture LIST.** Read the week's lecture events from the Meharry calendar (id in `config.md`) via `list_events`. The events (`IM (n) <Lecture>`) ARE the authoritative lecture list — extract every lecture title + the Mon–Fri boundary + any exam/holiday. **Do not infer the week's scope from the folder** — it's often a partial download (Week 1's folder missed all immunology + most molecular bio and wrongly included next-week neoplasia). NOTE the imported gcal can DROP a lecture (it omitted IM17 Normal Flora) — cross-check against the syllabus Course Outline.
2b. **Syllabus = the OBJECTIVES (authoritative scope).** Read the course syllabus (path in `config.md`; extract the .docx via `unzip -p <docx> word/document.xml`, split on `</w:tr>`/`</w:tc>`, strip tags). Its **Course Outline** table gives **each lecture's Learning Objectives** + the exam structure (`Session # == IM (#)`). These objectives — NOT the lecture title — define what each deck must cover. They are the scope you audit against in Stage 4.5.
3. **Week folder(s) = supplementary slide content** (may be incomplete — the calendar list wins). Per `config.md`: `<course_folder>/<Course>/Week <n>/`, materials **directly inside**; use slide text to *enrich* the calendar's lecture topics, not to define the week:
   - `*.pptx` / `*.ppt` → titles + bolded terms + objectives via the **pptx** skill (legacy `.ppt` that won't parse: use the filename as the topic).
   - `*.pdf` → same via the **pdf** skill.
   - optional `refs.md` / `notes.md` if present → resource refs / objectives. Skip non-lecture files (e.g. "How to Learn Anatomy", Anatomage links, sample-question decks).
4. **Fallbacks:** if no folder, accept slides/refs pasted in chat. If a connector is unavailable, ask the user for the missing piece — never invent topics.
5. Consolidate into a **topic list** (concept-level) + **resource_refs** (precise) for Stages 1–2.

---

## Stage 1 — Narrow (deterministic)

Goal: a candidate card pool per topic, at the right **altitude**.

**⚠️ Yield filter — read `yield_filter` from `config.md` and apply it silently every run; never re-ask** (it's a set-once preference; standing default `1+2`). Build the OR-clause from the value and AND it into *every* candidate/size query (tags under `#AK_Step1_v12::#Low/HighYield::…`):
- `1` → `(tag:…::1-HighYield)`
- `1+2` *(current default)* → `(tag:…::1-HighYield OR tag:…::2-RelativelyHighYield)`
- `1+2+3` → add `OR tag:…::3-HighYield-temporary` (re-enables the tier dropped 2026-06-21 to protect Qbank time)
- `off` → no filter (all tiers, incl. low-yield/unrated)

Never propose or unsuspend tiers outside the configured set. Apply the filter to the size probes too, so every count reflects what you'd actually unsuspend. If `yield_filter` is missing from config, default to `1+2`, note it once, and continue — don't stop to ask.
**EXCEPTION (default, not rare): foundational / intro / definitional lectures → drop the filter, go all-tier.** AnKing rates the basics these lectures test (DNA A/B/Z forms, Gram-stain procedure, prokaryote-vs-eukaryote, helix stability, plain definitions) at tier 3–4, so 1+2 erases exactly the testable content. When an objective returns ~0 at 1+2 but real cards all-tier, include them all-tier. 1+2 stays the default only for board-dense organ-system lectures.

**🔬 Subject-verification (anti-mis-scope — the IM04 lesson):** before you commit a subtree, `notes_info` 2–3 of its cards and confirm they actually match the OBJECTIVE — **keyword ≠ subject.** The same word lives in different resource trees: membrane *structure* is in `#Biochem::02_Cellular`, membrane *transport physiology* is in `#Physiology`; "Gene Structure & Function" = transcription/translation (a different lecture than DNA-structure). IM04 "Cell Membrane" was built from `#Biochem::Cellular` and came out as organelle/ER/Golgi cards with ~zero membrane-transport overlap. A subtree whose name matches the title can still be the wrong subject.

**Tag roots (AnKing Step Deck v12, verified against this collection):**
- System tree: `#AK_Step1_v12::^Systems::<System>::<Topic>`
- Resource trees: `#AK_Step1_v12::#FirstAid::…`, `#AK_Step1_v12::#B&B::…`, `#AK_Step1_v12::#Bootcamp::…`, `#AK_Step1_v12::#Physeo::…`, `#AK_Step1_v12::#SketchyPharm::…` / `#SketchyMicro::…` / `#SketchyPhysiology::…`, `#AK_Step1_v12::#DirtyMedicine::…`, `#AK_Step1_v12::#Pathoma::…`
- Step 2 equivalents live under `#AK_Step2_v12::…` (ignore in v1 unless the user asks).

**Resolution order per topic:**
1. **backbone-first** — prefer concept leaves under your `backbone_resource` tree (config; e.g. `#AK_Step1_v12::#B&B::…`). Deck names follow that resource's chapter topics. Sample-verify subject (keyword ≠ subject) before committing.
2. **tag-map hit** — if `data/tag-map.md` already maps the topic/ref → leaf tag(s), use them directly.
3. **resource ref** — map a `refs.md` entry to its resource subtree, e.g. `FA Cardiovascular Physiology` → `tag:#AK_Step1_v12::#FirstAid::07_Cardiovascular::03_Physiology::*`.
4. **system anchor** — map the topic to a system subtree, e.g. cardio → `tag:#AK_Step1_v12::^Systems::Cardio::*`.

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

## Stage 2 — Leaf-select

Goal: the final set of concept-**leaf** tags to act on.

1. List the child leaves under each narrowed subtree (enumerate `^Systems::Cardio::*` children and their counts).
2. For each lecture topic, match to leaves:
   - clean topic names / resource refs → deterministic match (no LLM needed).
   - messy slide-only input → judge which leaves the slide concepts correspond to; prefer recall (include adjacent leaves) since Stage 3 lets the user trim.
3. For each chosen leaf, also compute `… is:suspended` count = the cards that will actually change (already-unsuspended ones are skipped, keeping reruns idempotent).
4. Produce the **candidate table**: `leaf tag | total | suspended(actionable) | source topic`.

---

## Stage 3 — Propose → approve  (HARD GATE)

Show the user, then **wait**:

```
Week 2026-W25 · Cardio (from: Calendar 4 lectures + slides/cardio_phys.pptx)
  ✓ Cardio::HeartSounds        31 cards (31 new)      ← "heart sounds" lecture
  ✓ Cardio::Murmurs            28 cards (24 new)      ← "murmurs" lecture
  ? Cardio::CardiacCycle       40 cards (40 new)      ← adjacent, include?
  Total if approved: 95 new cards
  Pacing: 95 ÷ 7 study-days = 14/day  (under cap 25 ✓)
  Sample (HeartSounds): "Apex (Supine; Bell)… {{c1::Single S1 S2}}"
Approve / trim which leaves?
```

- Never call `unsuspend`/`add_tags` before explicit approval.
- If `Total ÷ study-days > cap`: show the conflict + 3 options (raise cap / trim / accept spillover). User decides here.

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

1. **Enumerate the lecture's objectives** (syllabus Course Outline + the slides' objective/title slides).
2. **For each objective, confirm ≥1 card covers it** — read the deck's cards (`notes_info include_fields:["Text"]` on the `Sched::` tag) and map each objective to a card.
3. **Close each gap:**
   - Objective HAS an AnKing card under a tag you didn't pull → **widen** (unsuspend+tag it in). Apply the Stage-1 subject-verification rule.
   - Objective has **NO** usable AnKing card at any tier (named frameworks, ordered lists, response kinetics, pure definitions — AnKing is board-fact-oriented, not lecture-framing-oriented) → **add a custom card.**
4. **Trim board tangents** the lecture never taught (SIRS / superantigens / NF-κB drifted into the intro-immuno deck; methemoglobinemia/calcification into cellular injury) → re-suspend + untag.
5. **Report** objectives-covered vs gaps (which got custom cards) → into the run-log.

**Custom card (`add_note`):** `add_note` a `Cloze` (or `Basic`) note into deck **AnKing Step Deck**, fields = the lecturer's exact fact, then tag it `Sched::IM::M1-W01::IM##-<Topic>` **+ `Sched::custom`**. The filtered deck's `tag:Sched::…IM##-*` search pulls it on rebuild; `Sched::custom` lets you list/undo every hand-made card. Keep them atomic and in the professor's wording (the definition, the named list, the specific numbers/kinetics).

**Reconciliation = this audit.** When slides/syllabus arrive for a title-built (🚧) deck, running Stage 4.5 against them IS the reconcile — a full coverage pass, not a light trim. Flip 🚧→Final once every objective is covered (AnKing card or custom).

---

## Stage 5 — Log + learn

1. Append to `data/run-log.md` (see its format): week, date, leaves + counts, new/day applied, source inputs.
2. Add any **newly-confirmed** topic→leaf mappings to `data/tag-map.md` so the same topic resolves instantly next time.
3. Tell the user: what was unsuspended, the new/day, and the one-line undo (`re-suspend tag:Sched::<week>::*`).
4. **Anki `sync`** — push the cards so your phone matches.

---

## Edge cases

| Situation | Handling |
|---|---|
| Anki not open | `find_notes` errors → STOP, ask user to open Anki, change nothing. |
| Zero matches for a topic | Flag it in the proposal as "no AnKing match — map manually?"; don't silently drop. |
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
