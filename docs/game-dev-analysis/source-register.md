# Game-development source register

**Assessment date:** 2026-07-16  
**Purpose:** claim-level admission record for the capability implementation in this repository.

These locally supplied books are tier-4 secondary/tertiary technical sources under the Digital Research Engine credibility ladder. They are suitable for durable concepts and workflow orientation. They are not sufficient authority for current engine APIs, Apple/Google/store rules, SDK services, signing, security, privacy, certification, or performance targets. Those claims must be verified against pinned official documentation at execution time.

| ID | Source and local evidence | Tier | Admitted use | Excluded use | Confidence |
|---|---|---:|---|---|---|
| GD-01 | Marco Secchi, *Multiplayer Game Development with Unreal Engine 5*, Packt, first published October 2023, ISBN 978-1-80323-287-4. Local Markdown: `C:\Users\Peter\Downloads\gmg-skill_markdown\Multiplayer Game Development with Unreal Engine 5.md` | 4 | Unreal networking progression; authority, actor/property replication, RPC, debugging, sessions, deployment concepts | Current Unreal/EOS APIs, security sufficiency, production scale or service availability | Medium-high for chapter scope; medium for implementation transfer |
| GD-02 | Joseph Hocking, *Unity in Action, Third Edition: Multiplatform Game Development in C#*, Manning, 2022, ISBN 9781617299339. Local Markdown filename begins `Unity in Action, Third Edition` | 4 | Unity scene/component, C# gameplay, 2D/3D, integration and multiplatform deployment orientation | Current package/API/store/build-farm rules or production-readiness claims | High for bibliographic identity; medium for implementation transfer |
| GD-03 | Stephen Haney, *Game Development with Swift*, Packt, first published July 2015, ISBN 978-1-78355-053-1. Local Markdown filename begins `[Bookflare.net]` | 4 | SpriteKit scenes/nodes, atlas concepts, physical-device testing, Game Center as a platform adapter | Swift 1.2/Xcode 6.3/iOS 7/OS X APIs and historic pixel-density workarounds | High for bibliographic identity; low for current API detail |
| GD-04 | Theresa Hill, *3D Game Development Practical Introduction*. Local OCR-derived Markdown: `C:\Users\Peter\Downloads\markdown\3D Game Development Practical I - Theresa Hill.md` | 4 | Greybox scenes, transforms/hierarchies, materials/lights/cameras, input archetypes, collision/physics and bounded mechanic scenes | Bibliographic details not present in the file; legacy Unity APIs; uncited performance figures; current budgets | Medium for chapter content; low for bibliographic completeness/current detail |
| GD-05 | Armin Halač, *A Complete Guide to Character Rigging for Games Using Blender* (2024) | 4 | Rig planning, export/control separation, deformation, correctives and engine export gates | Current APIs and universal budgets | High for lifecycle; medium for transfer |
| GD-06 | Enrico Valenza, *Blender 3D Cookbook* (2015) | 4 | Character modelling, retopology, UV, bake, rig, skin and animation linking | Blender 2.7 UI/API and current exporter behaviour | High for scope; low for APIs |
| GD-07 | Arijan Belec, *Blender 3D Incredible Models* (2022) | 4 | Hard-surface blockout/detail, modifiers, UV, baking and materials | Runtime budgets or engine compatibility | Medium-high |
| GD-08 | David Millet et al., *Blender 3D: Noob to Pro* (2012 compilation) | 4 | Durable modelling, topology, material and animation fundamentals | Blender Game Engine, old Python/UI and export instructions | Medium for fundamentals; very low for APIs |
| GD-09 | Jason van Gumster and Stefan Maurus, *Farming Simulator Modding With Blender* (2025) | 4 | Hierarchy, pivots, simplified physics, LOD, host testing and publishing discipline | I3D/XML/ModHub rules outside Farming Simulator | High for host workflow; medium for transfer |
| GD-10 | Tony Mullen, *Introducing Character Animation with Blender* (2011) | 4 | Armature/skin, shape keys, F-curves, NLA and animation-production concepts | Blender 2.54 UI/API and current export behaviour | High for principles; low for APIs |
| GD-11 | Craig Caldwell, *Story Structure and Development*, 2nd ed. (2025) | 4 | Causality, character action/change, setup/payoff, interactive modes and audience testing | Project canon, cultural authority or runtime proof | High for narrative framework |
| GD-12 | Marco Secchi, *Artificial Intelligence in Unreal Engine 5* (2024; UE 5.4) | 4 | Navigation, behaviour trees, perception, EQS, StateTree, Mass, Smart Objects and debugging | UE 5.8 status, performance sufficiency or non-Unreal equivalence | High for 5.4; medium for transfer |
| GD-13 | Laurie Annis, *Blender 3D for Jobseekers…* supplied Markdown contains only `# 642439815` (13 bytes) | n/a | None | All substantive claims | Unusable; reacquisition required |

## Claim links

| Engine artifact | Source support | Synthesis status |
|---|---|---|
| `online-multiplayer-and-game-backend`, `unreal-game-development` | GD-01 | Authority/session/test gates are a synthesis, not quoted book rules |
| `unity-mobile-game-development`, build/release boundary | GD-02 | Existing architecture doctrine plus deployment orientation; current commands deliberately omitted |
| `apple-game-platform-delivery`, `game-2d-art-animation-and-vfx-pipeline` | GD-03 | Scene/service/physical-device patterns retained; obsolete APIs rejected |
| `level-world-and-content-production`, `game-3d-asset-pipeline` | GD-04 | Greybox and component-dependency gates are synthesis; no numeric budget admitted |
| `blender-game-asset-production` | GD-05–GD-10 | Version-gated Blender production and rig/export synthesis; no tutorial budget admitted |
| `game-narrative-and-interactive-story-design` | GD-11 | Dramatic principles translated into interactive state, delivery and evidence contracts |
| `game-ai-behaviour-and-navigation`, `unreal-game-development` | GD-12 | Engine-neutral architecture separated from the Unreal adapter; official docs override the book |

No direct quotation from the books is required by the implementation. Exact book prose and code remain in the user-provided files and were not copied into the skill engine.
