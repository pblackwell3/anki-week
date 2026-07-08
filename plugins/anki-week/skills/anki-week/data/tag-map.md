# anki-week — Tag Map (course vocabulary → AnKing leaf tags)

The skill's growing brain. Each row maps something you'd say (a lecture topic or resource ref)
to one or more AnKing Step Deck **concept-leaf** tags. New confirmed mappings get appended at
Stage 5, so repeat topics resolve instantly. All tags are under `#AK_Step1_v12::`.

**Format:** `topic / ref  →  leaf tag(s)`  (omit the `#AK_Step1_v12::` prefix; the skill adds it)

## ⚠️ Altitude lesson (verified): `^Systems` is COARSER than resource trees
At the `^Systems` altitude, heart sounds **and** murmurs are bundled into a single
`^Systems::Cardio::HeartSounds` leaf (31 cards). The finer sounds-vs-murmurs split only
exists in the **resource trees** (e.g. B&B `…Cardiac_Auscultation::01_Heart_Murmurs` vs
`::02_Heart_Sounds`). So: use `^Systems` leaves for "one lecture ≈ one concept cluster";
drop to a **resource leaf** when a lecture is narrower than the Systems leaf.

## Seed: Cardio (verified against the live collection 2026-06-20)

| Topic / resource ref | Leaf tag(s) | Notes |
|---|---|---|
| heart sounds + murmurs (one lecture) | `^Systems::Cardio::HeartSounds` | **verified 31 cards.** Bundles sounds + murmurs. |
| murmurs only | `#B&B::06_Cardio::05_Cardiac_Auscultation::01_Heart_Murmurs` | resource leaf; use when sounds & murmurs are separate lectures |
| heart sounds only | `#B&B::06_Cardio::05_Cardiac_Auscultation::02_Heart_Sounds` | resource leaf counterpart |
| cardiac cycle | `#Bootcamp::Cardiology::09_Cardiac_Cycle` · `#SketchyPhysiology::03_Cardiovascular_Physiology::04_Cardiac_Cycle::01_Cardiac_Cycle` | no single `^Systems` leaf; anchor via resource trees |
| auscultation (First Aid frame) | `#FirstAid::07_Cardiovascular::03_Physiology::10_Auscultation_of_the_heart` | FA leaf for the heart-sounds lecture |

> The full set of `^Systems::Cardio::*` child leaves (1,733 cards total) was NOT enumerated —
> sequential note sampling clusters by topic and is biased. Enumerate properly at first real run
> (Anki browser tag tree, or `get_tags` filtered by the `^Systems::Cardio::` prefix).

## How to grow this
- At Stage 5, append every topic→leaf pair the user approved this week.
- Prefer **leaf** tags (one-lecture-sized). Pick the altitude that matches lecture granularity:
  `^Systems` leaf for a broad lecture, resource leaf for a narrow one.
- When a topic legitimately spans two systems, list both leaves on separate rows.

<!-- New mappings appended below this line -->

## M1 · (IM) Intro to Med — confirmed mappings (high-yield only)
| Lecture | Leaf tag | HY cards |
|---|---|---|
| IM20 Acute Inflammation | `#Pathoma::02_Inflammation::01_Acute_Inflammation` | 60 notes / 84 cards |

> Note: Pathoma chapter tags are precise — `#Pathoma::02_Inflammation::01_Acute_Inflammation` is the clean acute leaf. Chronic inflammation = the sibling `02_*Chronic*` leaf; cellular injury = `#Pathoma::01*`. Immuno intro = `#FirstAid::02_Immunology::*` minus hypersensitivity/immunodef/immunosupp/transplant.

## Inflammation — B&B leaves (confirmed 2026-07-01, card-sampled)
All under `#B&B::18_Pathology::01_General::`. HY = 1+2 note counts.

| Lecture / topic | B&B leaf | HY | Notes |
|---|---|---|---|
| Acute Inflammation (IM20) | `06_Inflammation_Principles` | 49 | mediators, 5 cardinal signs, vascular/cellular events, acute-phase reactants. A few cardio-physiology tangents live in `::Extra` (Starling/capillary — trim). |
| Acute **and** Chronic (IM20+IM21) | `07_Acute_and_Chronic_Inflammation` | 20 | **B&B bundles acute+chronic here — no separate acute/chronic leaves.** Serves both lectures → can't per-lecture split from B&B; use Pathoma `02_Inflammation::01/02` if a split is required. |
| Chronic — granuloma (IM21) | `08_Granulomatous_Inflammation` | 22 | granuloma formation (IL-12/IFN-γ), caseating/noncaseating; some specific-disease cards (sarcoid/TB/Crohn) = trim to recognition at intro depth. |
| ❌ NOT these lectures | `05_Necrosis` | (33) | necrosis *types* = Pathoma **Ch1 Cell Injury** = IM19. Lectures only touch caseous-necrosis-in-granulomas (covered by `08`). |
| ❌ NOT these lectures | `09_Wound_Healing_and_Scar` | (15) | own topic; padded w/ Vit-C/collagen biochem + bevacizumab pharm. |

> **Best-overlap inflammation set = `06`+`07`+`08`** (dedup 89 notes @1+2 / 53 @tier-1 / 144 all-tier). Built as combined deck `Inflammation (B&B · High-Yield)` on 2026-07-01.

## M1-W02 · (IM) Intro to Med Week 2 (confirmed 2026-07-03, card-sampled)
Neoplasia + genetics + molecular bio + biochem/metabolism. Tier noted per row; genetics IM25–31 built from objectives (no slides yet → decks 🚧).

| Lecture / topic | Leaf tag(s) | Tier | Notes |
|---|---|---|---|
| IM23-24 Neoplasia | `#Pathoma::03_Neoplasia::01_Neoplasia` + `#FirstAid::04_Pathology::03_Neoplasia::08_Oncogenes` | 1+2 | Full Pathoma Ch3 (158) / FA Neoplasia (202) are too big — use these two sub-leaves. Custom: 8 hallmarks list, dysplasia→CIS sequence, -oma/-carcinoma/-sarcoma naming, spread routes. |
| IM25-26 Cytogenetics/Karyotyping | `#B&B::11_Genetics::01_Genetic_Concepts::03_Meiosis` | 1+2 | Karyotype **procedure + ISCN nomenclature + multifactorial/threshold** have NO AnKing card → custom. Keep trisomy/aneuploidy leaves for IM27 (collision). |
| IM27 Aneuploidy syndromes | `#B&B::11_Genetics::02_Genetic_Disorders::01_Down_Syndrome` · `::06_Turner_and_Klinefelter_Syndromes` · `#FirstAid::01_Biochem::04_Genetics::15_Autosomal_trisomies` · `::17_Robertsonian_translocation` | 1+2 | AnKing's strongest genetics area. Robertsonian leaf's cards get captured by Meiosis (IM25-26) → 0 actionable here. Custom: Edwards/Patau feature lists. |
| IM28 Epigenetics/Imprinting | `#B&B::11_Genetics::01_Genetic_Concepts::06_Imprinting` · `#FirstAid::01_Biochem::04_Genetics::04_Disorders_of_imprinting` | 1+2 | **Already unsuspended in W01 IM09** (~10/11) → tag-only, no filtered deck. Custom: heterodisomy vs isodisomy; PWS vs Angelman parent-of-origin. |
| IM29 Transcription | `#B&B::07_Cell_Bio::01_Molecular::04_Transcription` | 1+2 | Custom: central dogma, mRNA processing (cap/polyA/splice). |
| IM30 Translation + PTM | `#B&B::07_Cell_Bio::01_Molecular::05_Translation` · `::02_DNA_Mutations` · `#FirstAid::01_Biochem::01_Molecular::05_Genetic_code_features` | 1+2 (genetic-code **all-tier** — small/foundational) | Custom: genetic-code features, PTM list. |
| IM31 Amino Acids & Protein Structure | `#FirstAid::01_Biochem::02_Cellular::12_Collagen` (+ prion) | 1+2 | **Custom-heavy** — the 20-AA table, 1°–4° structure hierarchy, α-helix/β-sheet, sickle cell all have NO AnKing leaf (B&B `04_Biochem::03_Amino_Acids` = AA **metabolism**, not structure). |
| IM32 Biomolecules (carbs/lipids) | — (0 AnKing) | — | AnKing carbs/lipids are all metabolism/disease, none structural → **custom-only**: aldose/ketose, reducing sugars, complex-carb taxonomy, 3 lipid classes. |
| IM33-34 Cell Signaling | `#B&B::09_Endocrinology::05_Other::06_Signaling_Pathways` | **tier-1 only** | Broad hormone-signaling leaf; tier-1 keeps the true 2nd-messenger/GPCR/RTK cards and drops steroid-synthesis tangents. Custom: autocrine/paracrine/endocrine, transduction components, receptor-class taxonomy. |
| IM35 Lysosomal Storage Diseases | `#B&B::04_Biochem::06_Other::01_Lysosomal_Storage_Diseases` (tier-1) · `#FirstAid::01_Biochem::02_Cellular::04_Cell_trafficking` (I-cell) | tier-1 (+I-cell 1+2) | I-cell disease lives under Cell_trafficking, NOT the LSD leaf. Custom: common LSD features, 3 classes. |
| IM36-37 Metabolic States (Fed/Fasting/Starvation) | `#B&B::04_Biochem::02_Metabolism::13_Exercise_and_Starvation` · `::10_Fatty_Acids` · `::04_Glycogen` | **tier-1 only, deduped** | These 3 leaves overlap heavily w/ each other + IM38/IM39. Assign all to IM36-37; IM38 does NOT re-pull. Custom: state overview, malonyl-CoA role. |
| IM38 Enzyme Regulation | — (shares IM36-37 leaves → custom-only) | — | Concept scaffolding (3 modes, induction/repression, compartmentation, zymogen) has no clean AnKing leaf → **custom-only** to avoid duplicating IM36-37 cards. |
| IM39 Enzyme & Receptor Kinetics | `#B&B::02_Basic_Pharmacology::01_General::01_Enzymes` · `::02_Enzyme_Inhibitors` · `#B&B::04_Biochem::02_Metabolism::12_Ethanol_Metabolism` | 1+2 | Km/Vmax, competitive/noncompetitive/uncompetitive, ethanol↔fomepizole antidote. Custom: 6 EC classes; enzyme-vs-receptor (Km↔EC50, Vmax↔Emax) parallels. |

> Genetics IM25–31 mappings are **objective-derived (no slides posted)** — reconcile against Forbes/Dash/Muthu/Liu slides when they drop; decks carry 🚧 until then.
