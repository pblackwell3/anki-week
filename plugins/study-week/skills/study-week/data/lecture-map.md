# study-week — Lecture → B&B map (grows each run)

Confirmed mappings from an IM lecture title to Boards & Beyond leaf video(s) in `bb-videos.json`.
The skill consults this first (Stage 4) so mappings stay consistent week to week. Append new
confirmed rows after each run. `—` = no clean B&B match (attend only). Runtimes are the verified
minutes from `bb-videos.json`.

| IM # | Lecture | B&B video(s) [min] | Notes |
|---|---|---|---|
| 17 | Normal Flora | — | No dedicated B&B leaf; touched under Microbiology basics. Attend only. |
| 18 | Cytokines: T and B Cell Activation | Immunology → T-cells [29]; B-cells [30] | Innate Immunity optional add. |
| 19 | Cellular Injury, Repair and Adaptation | Pathology → Cellular Adaptations [17]; Cell Injury [10]; Wound Healing and Scar [23] | |
| 20 | Acute Inflammation | Pathology → Inflammation Principles [25]; Acute and Chronic Inflammation [16] | |
| 21 | Chronic Inflammation | Pathology → Acute and Chronic Inflammation [16]; Granulomatous Inflammation [8] | Shares a video with IM 20 — schedule once. |
| 22 | Formative #1 | — | Assessment. Attend only. |
| 23-24 | Neoplasia | Pathology → Neoplasia [24] | |
| 25 | Multifactorial Disorders | Genetics → Genetic Principles [24]; Hardy-Weinberg Law [11] | No dedicated multifactorial/polygenic leaf; these are the closest correct-subject fits. |
| 26 | Cytogenetics and Chromosomal Abnormalities | Genetics → Meiosis [15]; Trisomy Disorders [7]; Cell Biology → Microarrays and FISH [5] | Microarrays/FISH = cytogenetic detection. Trisomy Disorders shared with IM 27 — schedule once. |
| 27 | Autosomal and Sex Chromosomal Aberrations | Genetics → Down Syndrome [13]; Trisomy Disorders [7]; Turner and Klinefelter Syndromes [13]; Deletion Syndromes [5] | Down Syndrome (Trisomy 21) is the prototype — verifier added it. Trisomy Disorders shared with IM 26. |
| 28 | Epigenetics and Imprinting | Genetics → Imprinting [6] | Only imprinting leaf in the library. |
| 29 | Gene Transcription and Transcription Factors | Cell Biology → Transcription [23] | |
| 30 | Translation and Post-Translational Modification | Cell Biology → Translation [20] | |
| 31 | Amino Acids and Protein Structures/Functions | Biochemistry → Amino Acids [18] | |
| 32 | Biomolecules in Medicine (Carbs & Lipids) | Biochemistry → Glucose [7]; Lipid Metabolism [19] | |
| 33-34 | Cell Signaling | Endocrinology → Signaling Pathways [20]; Insulin [24] | Signaling Pathways = GPCR/RTK/second messengers. Insulin = RTK worked example (overlaps IM 36). |
| 35 | Lysosomal Storage Diseases | Biochemistry → Lysosomal Storage Diseases [31] | |
| 36 | Control of Metabolism in Fed and Fasting States | Biochemistry → Exercise and Starvation [21]; Endocrinology → Glucagon & Hypoglycemia [22] | Exercise and Starvation shared with IM 37/38 — schedule once (earliest deadline). |
| 37 | Control of Metabolism in Starvation | Biochemistry → Exercise and Starvation [21]; Ketone Bodies [8] | Exercise and Starvation same video as IM 36. |
| 38 | Enzyme Regulation in Metabolic Pathways | Biochemistry → Exercise and Starvation [21] | Metabolic-pathway (allosteric/hormonal) regulation. Pharmacology "Enzymes" REJECTED (that's kinetics = IM 39). No dedicated metabolic-enzyme-regulation leaf. |
| 39 | Enzyme and Receptor Kinetics | Basic Pharmacology → Enzymes [13]; Enzyme Inhibitors [7]; Dose-Response [20] | Enzymes+Inhibitors = enzyme kinetics (Km/Vmax); Dose-Response = receptor kinetics. |
| 40 | Peer Instruction | — | Active-learning session. Attend only. |
| 42 | Glycolysis | Biochemistry → Glycolysis [31] | |
| 43 | Disorders of Fructose and Galactose Metabolism | Biochemistry → Fructose and Galactose [11] | |
| 44 | Tri-Carboxylic Krebs Cycle | Biochemistry → TCA Cycle [13] | |
| 45 | Electron Transport and Oxidative Phosphorylation | Biochemistry → Electron Transport Chain [20] | |
| 46-47 | Glycogenolysis / Glycogen Metabolism | Biochemistry → Glycogen [22] | |
| 48 | Lipogenesis: Fatty Acid Synthesis | Biochemistry → Fatty Acids [26] | Shares with IM 53 — schedule once, before IM 48. |
| 53 | Fatty Acid Oxidation | Biochemistry → Fatty Acids [26] | Same video as IM 48. |
| 54 | Gluconeogenesis | Biochemistry → Gluconeogenesis [17] | |
| 55 | Ketogenesis | Biochemistry → Ketone Bodies [8] | Same video as IM 37. |
| 56 | Pentose Phosphate Pathway | Biochemistry → HMP Shunt [14] | |

Sessions like Formative, Peer Instruction, PPM (communication), Midterm Review/Exam, Summative Review,
and library training have no B&B mapping — always attend-only.

**Verified 2026-07-02** (adversarial mapping run for the week of Jul 6–12): IM 22–40 rows above were
confirmed against `bb-videos.json` (exact titles + runtimes). Two corrections were caught in review —
IM 27 gained Down Syndrome; IM 38 dropped the pharmacology "Enzymes" keyword-collision.

**Refreshed 2026-08-18** against `bb-videos.json` **schema v2** (live web-app extraction, 502 videos):
every runtime above was re-read from the current library — most dropped by 1 min (the v1 PDF rounded
up, the site floor-rounds), `Glycogen` genuinely grew 21→22 — and `Trisomies` was renamed by B&B to
**`Trisomy Disorders`**. Titles all still resolve; no mapping changed subject. When adding rows, match
concepts against each video's `video_index` rather than its title.
