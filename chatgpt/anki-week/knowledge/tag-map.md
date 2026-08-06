# anki-week — Tag Map (your course vocabulary → AnKing leaf tags)

**Upload this to your GPT's Knowledge.** This is *your* file — it starts nearly empty and grows into
the most valuable thing you own here. Each row maps something you'd say (a lecture topic or a resource
reference) to one or more AnKing Step Deck **concept-leaf** tags, so a repeat topic resolves instantly
instead of being re-derived from scratch.

All tags live under `#AK_Step1_v12::`.

**Format:** `topic / ref  →  leaf tag(s)`  (omit the `#AK_Step1_v12::` prefix; it's assumed)

---

## ⚠️ How this file grows — read this once

ChatGPT **cannot write to its own Knowledge.** Knowledge files are read-only at run time, so the GPT
can't append a row for you. Growing this file is a deliberate loop you run:

1. **End of every build**, the GPT prints an **APPEND BLOCK** — ready-to-paste rows for any concept→leaf
   mapping it confirmed this run (and the same for `synonym-map.md`).
2. **Paste those rows** into the matching table below, in your local copy of this file.
3. **Re-upload** this file to the GPT's Knowledge, *replacing* the old copy (ChatGPT ▸ Edit GPT ▸
   Knowledge ▸ remove the old `tag-map.md`, upload the new one).
4. Next run, the GPT checks this file **first** — and your course's vocabulary is now permanent.

Skip step 3 and the memory is lost: the GPT will happily re-derive the same mapping next week and may
land somewhere different. **Re-upload after every run or two.** It takes about thirty seconds.

> Sibling brain: **`synonym-map.md`** = slide word → AnKing word (*what to match on*).
> **This file** = course concept → AnKing leaf tag (*where to look*). Different jobs; keep them separate.

---

## ⚠️ Altitude lesson: `^Systems` is COARSER than the resource trees

Worth knowing before you add rows. At the `^Systems` altitude, heart sounds **and** murmurs are bundled
into a single `^Systems::Cardio::HeartSounds` leaf (31 cards). The finer sounds-vs-murmurs split exists
only in the **resource trees** (e.g. B&B `…Cardiac_Auscultation::01_Heart_Murmurs` vs `::02_Heart_Sounds`).

So: use a `^Systems` leaf when *one lecture ≈ one concept cluster*; drop to a **resource leaf** when a
lecture is narrower than the Systems leaf. Recording which altitude worked is exactly what this file is for.

---

## Your mappings

Add a row whenever a build confirms a concept→leaf mapping. Note the card count you saw — it's how you
catch a leaf that's drifted or that you picked at the wrong altitude.

| Topic / resource ref | Leaf tag(s) | Notes |
|---|---|---|
| | | |

---

## Example rows (delete once you have your own)

These are real, verified mappings from a live collection. They're here to show the shape and the
altitude tradeoff — they are **not** your course, so replace them as you go.

| Topic / resource ref | Leaf tag(s) | Notes |
|---|---|---|
| heart sounds + murmurs (one lecture) | `^Systems::Cardio::HeartSounds` | verified 31 cards. Bundles sounds + murmurs. |
| murmurs only | `#B&B::06_Cardio::05_Cardiac_Auscultation::01_Heart_Murmurs` | resource leaf; use when sounds & murmurs are separate lectures |
| heart sounds only | `#B&B::06_Cardio::05_Cardiac_Auscultation::02_Heart_Sounds` | resource leaf counterpart |
| auscultation (First Aid frame) | `#FirstAid::07_Cardiovascular::03_Physiology::10_Auscultation_of_the_heart` | FA leaf for a heart-sounds lecture |

---

## Enumerating leaves properly (first run of a new subject)

Don't guess leaf paths and don't sample sequential note ids — ids cluster by topic, so a sample is
biased and you'll conclude a leaf is narrower than it is. Instead list the tag tree by prefix (the Anki
browser's tag sidebar, or a `get_tags`-style call filtered to e.g. `#SketchyMicro::`), then record the
confirmed rows here.

Microbiology in particular is tagged **organism-by-organism**, which follows Sketchy's shape rather than
a video curriculum — so `#SketchyMicro::` + `#FirstAid::03_Microbiology::` are the right roots for a bug
lecture, not a B&B infectious-disease chapter.
