Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Infographics Design and Production Quality Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Worked review: A2 safety process poster (fictional)

All names and figures are fictional. "Example Hardware Ltd" asked for a portrait A2 poster, "Seven
steps to safe concrete mixing", for its yard wall, read from 1 m and seen from 3 m, plus a phone
version for its WhatsApp group (1,080 px square shown in about a 360 px slot).

## Findings

| # | Finding | Rule | Gate | Evidence | Fix |
|---|---|---|---|---|---|
| 1 | The checker reported "possible duplicate stage: S1 and S5" ("Mix cement and sand" appeared twice) and "orphan node S8" | INFO-FLOW-001 | 05 | TOPO | Duplicate removed; the orphan "Wear gloves" moved into step 1's prerequisites |
| 2 | Step "4. Add water" happened after step 5 on the drawn arrows | INFO-FLOW-001 | 05 | TOPO | Renumbered to the true order; checker re-run: no failures |
| 3 | Body text at 14 pt; the 1 m minimum is 23.6 pt | INFO-TYPE-003 | 02 | CALC | Body 24 pt, title 72 pt (3 m minimum 70.7 pt), source line 12 pt (0.5 m) |
| 4 | Step labels drawn by an image model read "Mlx cemnet" at full size | INFO-TYPE-002 | 02 | RENDER | Illustration regenerated without text; labels set as live text on their own layer |
| 5 | The hero image was a photorealistic generated worker | INFO-ILLUS-002 | 03 | REVIEW | Replaced with a flat vector illustration |
| 6 | "Saves 40% of cement" had no source | INFO-DATA-001/002 | 01 | REG | Claim removed; the owner could not supply evidence |
| 7 | A bubble chart of bag sizes scaled radius with weight (25 kg vs 50 kg shown at 4x the area) | INFO-CHART-003 | 04 | CALC | Lie factor 3.0 reduced to 1.0 by scaling area; radius ratio sqrt(2) |
| 8 | Hazard steps shown in red only | INFO-COLOUR-001 | 07 | AT | Warning icon and the word "Danger" added; greyscale proof checked |
| 9 | The phone version used 14 px text on the 1,080 px canvas (under 5 CSS px in the slot) | INFO-SOCIAL-002 | 02 | CALC | Phone version recomposed as a three-card series with 48 px body text |

Print preflight: the background photograph was 2,000 x 2,800 px over the 426 x 600 mm bleed size,
about 119 ppi effective; read from 1 m it needs 87 ppi, so it passed the requirement but not the
150 ppi poster floor, and was replaced with a vector texture.

## Verdict

Before fixes: BLOCKED (INFO-GATE-01, 02, 03, 04, 05 and 07 open; score not computed). After fixes,
expert sign-off on the mixing steps, actual-size proofs of both renditions and a re-run of every check
on `MEASURED` evidence, the weighted score was 89: released with the signed declaration and the
sources archived.
