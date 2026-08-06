# anki-week — Synonym Map (entity aliases for the intersection step)

The **one piece of ongoing tuning** in the Selection Protocol (`config.md` → *Scope = tags ∩ slides*).

Scoping keeps a card when its tag or content **names a Scope-Spec entity**. That match fails whenever
the slides and AnKing use *different words for the same thing* — so the card is silently dropped and
shows up later as a phantom coverage gap. Every row here converts one such miss into a hit.

**Growing this file carries coverage from ~90% toward ~95%.** It is the highest-leverage upkeep in the
skill.

> Sibling brains: **`tag-map.md`** = course concept → AnKing leaf tag (*where to look*).
> **This file** = slide word → AnKing word (*what to match on*). Different jobs; keep them separate.

## How to use it

1. During the **intersection step**, expand every Scope-Spec entity with its aliases before matching.
2. During the **Stage-4.5 coverage audit**, any entity reported as 0-card is a suspect: if AnKing *does*
   have the card under a different name, **that's a synonym miss, not a resource gap** → add the row
   here and re-intersect. Only a genuine no-card-at-any-name entity is a real gap (→ custom card).

**Matching is case-insensitive.** Prefer the *slide* term in the left column and every AnKing/board
variant on the right. Add the abbreviation whenever it's the form the slides use.

## Format

`slide term | AnKing / board term(s) | type | notes`

<!-- Seed rows — the two named in the protocol decision, plus common shapes. Verify against the
     collection on first use and correct anything that doesn't match. -->

| Slide term | AnKing / board term(s) | Type | Notes |
|---|---|---|---|
| isotretinoin | 13-cis-retinoic acid · Accutane | drug | The protocol's worked example. |
| gas gangrene | *Clostridium perfringens* · *C. perfringens* | disease ↔ organism | Disease name on the slides, organism name in AnKing. **This shape — disease-named-on-slides vs organism-tagged-in-AnKing — is the most common synonym miss in micro.** |

<!-- New rows appended below this line, newest last. Record the run that found each miss. -->

## Alias shapes worth watching (each has burned a real build somewhere)

- **Disease ↔ causative organism** — slides say the syndrome, AnKing tags the bug (*gas gangrene* ↔
  *C. perfringens*).
- **Generic ↔ chemical ↔ brand** — *isotretinoin* ↔ *13-cis-retinoic acid* ↔ *Accutane*.
- **Genus abbreviation** — *S. aureus* ↔ *Staphylococcus aureus* ↔ *staph aureus*. Expand both
  directions; slides abbreviate, tags usually don't.
- **Eponym ↔ description** — a named sign/body vs its plain-language description.
- **Enzyme ↔ pathway ↔ gene** — the slides may name any one of the three for the same fact.
- **Drug class ↔ member** — slides teach the class, AnKing cards the exemplar (or the reverse).

## What does NOT belong here

- **Concept → leaf-tag mappings** → those go in `tag-map.md`.
- **Entity-less concepts** (the protocol's `named_rules` — mechanisms/eponyms with no proper noun).
  They have no name to alias; they're handled by keyword/content search or a custom card, and they are
  the *expected* residue of the method, not a synonym problem.
