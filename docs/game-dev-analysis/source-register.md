# Game-development source register

**Assessment date:** 2026-07-16  
**Purpose:** claim-level admission record for the capability implementation in this repository.

These four locally supplied books are tier-4 secondary/tertiary technical sources under the Digital Research Engine credibility ladder. They are suitable for durable concepts and workflow orientation. They are not sufficient authority for current engine APIs, Apple/Google/store rules, SDK services, signing, security, privacy, certification, or performance targets. Those claims must be verified against pinned official documentation at execution time.

| ID | Source and local evidence | Tier | Admitted use | Excluded use | Confidence |
|---|---|---:|---|---|---|
| GD-01 | Marco Secchi, *Multiplayer Game Development with Unreal Engine 5*, Packt, first published October 2023, ISBN 978-1-80323-287-4. Local Markdown: `C:\Users\Peter\Downloads\gmg-skill_markdown\Multiplayer Game Development with Unreal Engine 5.md` | 4 | Unreal networking progression; authority, actor/property replication, RPC, debugging, sessions, deployment concepts | Current Unreal/EOS APIs, security sufficiency, production scale or service availability | Medium-high for chapter scope; medium for implementation transfer |
| GD-02 | Joseph Hocking, *Unity in Action, Third Edition: Multiplatform Game Development in C#*, Manning, 2022, ISBN 9781617299339. Local Markdown filename begins `Unity in Action, Third Edition` | 4 | Unity scene/component, C# gameplay, 2D/3D, integration and multiplatform deployment orientation | Current package/API/store/build-farm rules or production-readiness claims | High for bibliographic identity; medium for implementation transfer |
| GD-03 | Stephen Haney, *Game Development with Swift*, Packt, first published July 2015, ISBN 978-1-78355-053-1. Local Markdown filename begins `[Bookflare.net]` | 4 | SpriteKit scenes/nodes, atlas concepts, physical-device testing, Game Center as a platform adapter | Swift 1.2/Xcode 6.3/iOS 7/OS X APIs and historic pixel-density workarounds | High for bibliographic identity; low for current API detail |
| GD-04 | Theresa Hill, *3D Game Development Practical Introduction*. Local OCR-derived Markdown: `C:\Users\Peter\Downloads\markdown\3D Game Development Practical I - Theresa Hill.md` | 4 | Greybox scenes, transforms/hierarchies, materials/lights/cameras, input archetypes, collision/physics and bounded mechanic scenes | Bibliographic details not present in the file; legacy Unity APIs; uncited performance figures; current budgets | Medium for chapter content; low for bibliographic completeness/current detail |

## Claim links

| Engine artifact | Source support | Synthesis status |
|---|---|---|
| `online-multiplayer-and-game-backend`, `unreal-game-development` | GD-01 | Authority/session/test gates are a synthesis, not quoted book rules |
| `unity-mobile-game-development`, build/release boundary | GD-02 | Existing architecture doctrine plus deployment orientation; current commands deliberately omitted |
| `apple-game-platform-delivery`, `game-2d-art-animation-and-vfx-pipeline` | GD-03 | Scene/service/physical-device patterns retained; obsolete APIs rejected |
| `level-world-and-content-production`, `game-3d-asset-pipeline` | GD-04 | Greybox and component-dependency gates are synthesis; no numeric budget admitted |

No direct quotation from the books is required by the implementation. Exact book prose and code remain in the user-provided files and were not copied into the skill engine.
