# anki-week — Synonym Map (entity aliases for the intersection step)

**Upload this to your GPT's Knowledge.** Like `tag-map.md`, this starts nearly empty and is yours to
grow. It is **the highest-leverage upkeep in the whole method** — growing it carries coverage from
roughly **90% toward 95%**.

## Why it matters

Scoping keeps a card when its tag or content **names a Scope-Spec entity**. That match fails whenever
your slides and AnKing use *different words for the same thing* — the card is silently dropped, then
resurfaces in the audit as a **phantom coverage gap** that looks like a missing resource but isn't.
Every row here converts one such miss into a hit.

- *isotretinoin* = *13-cis-retinoic acid* = *Accutane*
- *gas gangrene* = *Clostridium perfringens* ← **disease-on-slides vs organism-in-AnKing is the most
  common micro miss**
- *S. aureus* ↔ *Staphylococcus aureus*; eponym ↔ description; enzyme ↔ pathway ↔ gene; class ↔ member

> Sibling brain: **`tag-map.md`** = course concept → AnKing leaf tag (*where to look*).
> **This file** = slide word → AnKing word (*what to match on*). Different jobs; keep them separate.

---

## ⚠️ How this file grows — the same loop as `tag-map.md`

ChatGPT **cannot write to its own Knowledge**, so this is a manual loop:

1. **End of every build**, the GPT prints an **APPEND BLOCK** with every new alias it discovered — the
   single most valuable output of a run.
2. **Paste the rows** into the table below.
3. **Re-upload** this file to Knowledge, replacing the old copy.
4. Next run, aliases expand automatically and those phantom gaps stop appearing.

---

## How the GPT uses it

1. During the **intersection step**, expand every Scope-Spec entity with its aliases *before* matching.
2. During the **coverage audit**, any entity reported as **0 cards** is a suspect: if AnKing has the card
   under a different name, that's a **synonym miss, not a resource gap** → add the row here and
   re-intersect. Only an entity with no card under *any* name is a real gap (→ custom card).

**Matching is case-insensitive.** Put the term *your slides* use in the left column and every
AnKing/board variant on the right. Always add the abbreviation when that's the form the slides use.

---

## Your aliases

| Slide term | AnKing / board variant(s) | Added after |
|---|---|---|
| | | |

---

## Example rows (delete once you have your own)

| Slide term | AnKing / board variant(s) | Added after |
|---|---|---|
| isotretinoin | 13-cis-retinoic acid · Accutane | derm pharm |
| gas gangrene | *Clostridium perfringens* · C. perfringens | micro |
| S. aureus | *Staphylococcus aureus* | micro |
