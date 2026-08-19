# study-week — Lecture → video map (grows each run)

Confirmed mappings from an IM lecture title to leaf video(s) in the video library you run
(`video_library` in `config.md` — `bb-videos.json` or `bootcamp-videos.json`).
The skill consults this first (Stage 4) so mappings stay consistent week to week. Append new
confirmed rows after each run. `—` = no clean match (attend only). Runtimes are the verified
minutes from the library.

**Rows below are Boards & Beyond** (`Library` blank = `bb`, which is what every pre-Bootcamp row
meant). If you study from **Bootcamp**, add your rows with `Library = bootcamp` and write each video as
**`Subject › Section › Title`** — Bootcamp titles repeat (`Board-style Question Breakdown` ×166), so a
bare title is not a mapping. Don't mix libraries in one row.

| IM # | Lecture | Library | Video(s) [min] | Notes |
|---|---|---|---|---|
| 17 | Normal Flora | bb | — | No dedicated B&B leaf; touched under Microbiology basics. Attend only. |
| 18 | Cytokines: T and B Cell Activation | bb | Immunology → T-cells [29]; B-cells [30] | Innate Immunity optional add. |
| 19 | Cellular Injury, Repair and Adaptation | bb | Pathology → Cellular Adaptations [17]; Cell Injury [10]; Wound Healing and Scar [23] | |
| 20 | Acute Inflammation | bb | Pathology → Inflammation Principles [25]; Acute and Chronic Inflammation [16] | |
| 21 | Chronic Inflammation | bb | Pathology → Acute and Chronic Inflammation [16]; Granulomatous Inflammation [8] | Shares a video with IM 20 — schedule once. |
| 22 | Formative #1 | bb | — | Assessment. Attend only. |
| 23-24 | Neoplasia | bb | Pathology → Neoplasia [24] | |
| 25 | Multifactorial Disorders | bb | Genetics → Genetic Principles [24]; Hardy-Weinberg Law [11] | No dedicated multifactorial/polygenic leaf; these are the closest correct-subject fits. |
| 26 | Cytogenetics and Chromosomal Abnormalities | bb | Genetics → Meiosis [15]; Trisomy Disorders [7]; Cell Biology → Microarrays and FISH [5] | Microarrays/FISH = cytogenetic detection. Trisomy Disorders shared with IM 27 — schedule once. |
| 27 | Autosomal and Sex Chromosomal Aberrations | bb | Genetics → Down Syndrome [13]; Trisomy Disorders [7]; Turner and Klinefelter Syndromes [13]; Deletion Syndromes [5] | Down Syndrome (Trisomy 21) is the prototype — verifier added it. Trisomy Disorders shared with IM 26. |
| 28 | Epigenetics and Imprinting | bb | Genetics → Imprinting [6] | Only imprinting leaf in the library. |
| 29 | Gene Transcription and Transcription Factors | bb | Cell Biology → Transcription [23] | |
| 30 | Translation and Post-Translational Modification | bb | Cell Biology → Translation [20] | |
| 31 | Amino Acids and Protein Structures/Functions | bb | Biochemistry → Amino Acids [18] | |
| 32 | Biomolecules in Medicine (Carbs & Lipids) | bb | Biochemistry → Glucose [7]; Lipid Metabolism [19] | |
| 33-34 | Cell Signaling | bb | Endocrinology → Signaling Pathways [20]; Insulin [24] | Signaling Pathways = GPCR/RTK/second messengers. Insulin = RTK worked example (overlaps IM 36). |
| 35 | Lysosomal Storage Diseases | bb | Biochemistry → Lysosomal Storage Diseases [31] | |
| 36 | Control of Metabolism in Fed and Fasting States | bb | Biochemistry → Exercise and Starvation [21]; Endocrinology → Glucagon & Hypoglycemia [22] | Exercise and Starvation shared with IM 37/38 — schedule once (earliest deadline). |
| 37 | Control of Metabolism in Starvation | bb | Biochemistry → Exercise and Starvation [21]; Ketone Bodies [8] | Exercise and Starvation same video as IM 36. |
| 38 | Enzyme Regulation in Metabolic Pathways | bb | Biochemistry → Exercise and Starvation [21] | Metabolic-pathway (allosteric/hormonal) regulation. Pharmacology "Enzymes" REJECTED (that's kinetics = IM 39). No dedicated metabolic-enzyme-regulation leaf. |
| 39 | Enzyme and Receptor Kinetics | bb | Basic Pharmacology → Enzymes [13]; Enzyme Inhibitors [7]; Dose-Response [20] | Enzymes+Inhibitors = enzyme kinetics (Km/Vmax); Dose-Response = receptor kinetics. |
| 40 | Peer Instruction | bb | — | Active-learning session. Attend only. |
| 42 | Glycolysis | bb | Biochemistry → Glycolysis [31] | |
| 43 | Disorders of Fructose and Galactose Metabolism | bb | Biochemistry → Fructose and Galactose [11] | |
| 44 | Tri-Carboxylic Krebs Cycle | bb | Biochemistry → TCA Cycle [13] | |
| 45 | Electron Transport and Oxidative Phosphorylation | bb | Biochemistry → Electron Transport Chain [20] | |
| 46-47 | Glycogenolysis / Glycogen Metabolism | bb | Biochemistry → Glycogen [22] | |
| 48 | Lipogenesis: Fatty Acid Synthesis | bb | Biochemistry → Fatty Acids [26] | Shares with IM 53 — schedule once, before IM 48. |
| 53 | Fatty Acid Oxidation | bb | Biochemistry → Fatty Acids [26] | Same video as IM 48. |
| 54 | Gluconeogenesis | bb | Biochemistry → Gluconeogenesis [17] | |
| 55 | Ketogenesis | bb | Biochemistry → Ketone Bodies [8] | Same video as IM 37. |
| 56 | Pentose Phosphate Pathway | bb | Biochemistry → HMP Shunt [14] | |

Sessions like Formative, Peer Instruction, PPM (communication), Midterm Review/Exam, Summative Review,
and library training have no video mapping in either library — always attend-only.

**Verified 2026-07-02** (adversarial mapping run for the week of Jul 6–12): IM 22–40 rows above were
confirmed against `bb-videos.json` (exact titles + runtimes). Two corrections were caught in review —
IM 27 gained Down Syndrome; IM 38 dropped the pharmacology "Enzymes" keyword-collision.

**Refreshed 2026-08-18** against `bb-videos.json` **schema v2** (live web-app extraction, 502 videos):
every runtime above was re-read from the current library — most dropped by 1 min (the v1 PDF rounded
up, the site floor-rounds), `Glycogen` genuinely grew 21→22 — and `Trisomies` was renamed by B&B to
**`Trisomy Disorders`**. Titles all still resolve; no mapping changed subject. When adding rows, match
concepts against each video's `video_index` rather than its title.
