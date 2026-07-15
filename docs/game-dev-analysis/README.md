# Game-development capability audit

**Audit date:** 2026-07-15  
**Engine assessed:** `skills-web-dev` at `C:\Users\Peter\.claude\skills`  
**Decision:** whether the engine can support a world-class game-development agency delivering for Android, iOS and macOS  
**Current capability score:** **59/100**  
**Scoring ceiling imposed for this baseline:** **65/100**  
**Target:** **95/100**

## Executive verdict

The engine has a credible mobile-game foundation, but it is not yet an end-to-end game-agency operating system.

Its strongest feature is disciplined project control. The game family prevents premature production, separates design from implementation, requires real-device profiling, treats art and audio as production pipelines, and connects testing to release evidence. The catalog and routing machinery also work: 13 game skills are discoverable, all 132 repository routing fixtures land within the top three, and the catalog guardrail reports no structural defects.

The score is held to **59/100** because the engine can guide a capable team through a bounded Unity or Godot mobile project, but it cannot yet carry the full burden implied by “world-class agency.” In particular:

- Android and iOS are covered as Unity/Godot export targets, but native platform integration is shallow.
- macOS is named by the orchestration scope but has no dedicated implementation, certification, packaging, input, graphics, signing or distribution workflow.
- Unreal Engine is absent.
- Multiplayer, authoritative servers, matchmaking, lobby/session services, latency compensation and backend operations are not owned by a specialist game skill.
- Game security, cheat resistance and abuse operations are not a defined delivery discipline.
- Build engineering is described as an outcome, not supplied as executable CI/CD templates, validators or build-farm runbooks.
- 2D art, technical animation, VFX, level/world production and procedural-content workflows are under-specified.
- Analytics, economy operations, experimentation, community safety and live-service incident operations are too thin for long-lived commercial games.
- The engine has no reference game repository, golden vertical slice, production telemetry pack, certification rehearsal or case-study evidence proving repeatable delivery.

This is a good pre-production and mobile-production doctrine set. It is not yet sufficient evidence that the agency can repeatedly ship, operate and improve games across the three requested platforms.

## What was assessed

The audit inspected:

- the root router in `SKILL.md`;
- `docs/skill-routing-index.md` and the game routing fixtures;
- all **13** active `skills/game-development/**/SKILL.md` files;
- all **26** Markdown references in the game-development family;
- the mandatory `anti-ai-slop` and `ai-slop-audit` gates;
- the delivery evidence-pack template;
- the two existing July 2026 game-family release audits;
- the source-book synthesis record in `book-extractions/`;
- catalog guardrails, routing smoke tests and routing-collision output.

This is a capability audit of an instruction engine. It is not an audit of staff résumés, shipped titles, source code, player data, revenue, art portfolios or production infrastructure. Those were not present and therefore were not scored as if they existed.

## Scoring method

The rubric measures whether the engine can cause repeatable delivery, not whether it mentions a topic. A high score requires five layers:

1. **Routing:** the engine can select the right specialist.
2. **Doctrine:** the specialist states correct boundaries, decisions and failure modes.
3. **Execution assets:** templates, scripts, examples and checklists make the guidance actionable.
4. **Verification:** tests or gates can reject an inadequate result.
5. **Proof:** a representative project demonstrates that the workflow works end to end.

The user requested a deliberately conservative baseline capped at 65. The uncapped evidence score is 59, so no artificial cap adjustment was needed.

| Capability domain | Weight | Score | Maturity finding |
|---|---:|---:|---|
| Product strategy and production governance | 8 | 7 | Strong stage gates and decision discipline |
| Game design, validation and player experience | 10 | 8 | Strong mobile-first design; limited genre and content-design depth |
| Gameplay architecture, math and simulation | 10 | 7 | Sound foundations; incomplete networking and advanced AI coverage |
| Engines and target-platform implementation | 14 | 8 | Unity/Godot mobile foundation; no Unreal; macOS materially missing |
| Art, graphics, animation and audio production | 10 | 7 | Strong 3D/render/audio pipeline; 2D, VFX and animation ownership incomplete |
| Online multiplayer and game backend | 10 | 2 | Mostly a boundary mention, not an operating capability |
| QA, performance, accessibility and localisation | 10 | 7 | Good device/performance gates; automation and certification matrices thin |
| Build, signing, distribution and release engineering | 10 | 6 | Good release intent for mobile; insufficient executable automation and macOS depth |
| Live operations, data, economy and community | 8 | 4 | Basic rollout/support/live-event coverage; weak data and trust operations |
| Agency delivery system and demonstrable proof | 10 | 3 | Useful documents and gates; no reference implementation or delivery proof |
| **Total** | **100** | **59** | **Capable foundation; not yet agency-complete** |

### Rating bands

| Score | Meaning |
|---:|---|
| 0-24 | Topic awareness only |
| 25-44 | Fragmented practitioner guidance |
| 45-64 | Capable foundation with major delivery gaps |
| 65-79 | Production-capable for defined project classes |
| 80-89 | Strong multi-project studio system |
| 90-94 | Elite, evidence-rich agency operating model |
| 95-100 | World-class, continuously verified and demonstrably repeatable |

## Evidence snapshot

### Structural and routing evidence

Commands run on 2026-07-15:

```powershell
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
python -X utf8 scripts\routing_smoke_test.py --report-only
python -X utf8 scripts\routing_smoke_test.py --collisions
```

Results:

| Check | Result | Interpretation |
|---|---:|---|
| Active skills | 155 | Within the 200 hard cap |
| Game-development skills | 13 | Broad mobile-game discipline coverage |
| Game-development references | 26 | Two focused references per active game skill |
| Catalog findings | 0 | No structural catalog defect detected |
| Routing fixtures | 132 | Repository-wide test set |
| Precision at rank 1 | 125/132, 94% | Strong but not perfect first-choice routing |
| Precision within top 3 | 132/132, 100% | Every fixture finds the expected skill |
| Game collision pairs above threshold | 0 | Current game descriptions are sufficiently distinct |

There are 13 game-specific fixtures, one for each active game skill. That is good symmetry. The fixtures test obvious positive routes, however; they do not test ambiguous requests, platform-specific macOS cases, cross-skill conflicts, negative routing, or end-to-end compositions.

### Existing game skill map

| Skill | What it owns well | Material limitation |
|---|---|---|
| `game-development-orchestration` | lifecycle, evidence gates, discipline routing, risk registers | does not supply staffing economics, vendor governance or portfolio operations in depth |
| `lean-game-product-development` | falsifiable hypotheses, prototype choice, pivot/stop decisions | needs benchmark protocols, sample artefacts and player-research data handling |
| `mobile-game-design` | touch, sessions, interruption, progression, accessibility, ethical monetisation | mobile-only framing; thin level, narrative, social and systemic design practice |
| `unity-mobile-game-development` | C# separation, scenes, prefabs, packages, device builds | Android/iOS oriented; no complete Unity services/netcode/editor-tooling/build-farm practice |
| `godot-mobile-game-development` | scenes, resources, signals, migrations, exports | limited production-scale C#/GDScript governance, multiplayer and console/desktop delivery |
| `gameplay-systems-architecture` | explicit state, ownership, saves, AI and content schemas | networking is an input, not a worked discipline; advanced animation/gameplay coupling is thin |
| `game-math-and-simulation` | coordinate contracts, determinism, probability and numerical tests | lacks deeper physics, navigation, procedural generation and network-prediction exemplars |
| `real-time-game-graphics` | render architecture, GPU diagnosis, shader/material contracts | no engine-specific shader library, Metal workflow, VFX production or automated visual lab |
| `game-3d-asset-pipeline` | concept-to-engine 3D, budgets, provenance, rigging and LOD | no dedicated 2D pipeline, technical animation discipline or asset automation scripts |
| `game-audio-implementation` | event taxonomy, buses, rights, localisation, profiling | limited middleware-specific implementation, voice pipeline automation and platform audio detail |
| `mobile-game-performance` | physical-device profiling, budgets, thermal and frame pacing | lacks owned device-lab automation, benchmark scenes and regression thresholds |
| `game-testing-polish` | bug contract, playtesting, balance and milestone gates | no detailed automation architecture, compatibility lab, soak/fuzz testing or certification suite |
| `mobile-game-release-liveops` | mobile signing, stores, privacy, rollout, rollback, support | no macOS distribution path; thin analytics, economy ops, community safety and incident command |

## Platform evaluation

### Android: 72/100 within the platform subscore

Android is the strongest target. Unity and Godot both name Android builds and physical-device validation. The performance skill requires real chipset/GPU, RAM, OS, resolution, storage and thermal context. Release guidance covers signing, store submission, permissions, privacy, package inspection, rollout and rollback.

What prevents a higher score:

- No game-specific Android platform skill owns Play Games Services, achievements, leaderboards, saved games, integrity signals, billing failure recovery, asset delivery or device-vendor failure patterns.
- There is no executable Gradle/AAB build reference, symbol-upload check, store-track promotion script or device-farm configuration.
- Android API-level, graphics-backend and input-device compatibility matrices are deferred to live research rather than expressed as a reusable verification artifact.
- The engine has no proven low-end Android reference game or retained performance traces.

### iOS/iPadOS: 66/100 within the platform subscore

iOS is explicitly supported by the Unity and Godot skills, and the broader engine has a mature native iOS family. The game release skill recognizes Apple signing, privacy and store gates. Mobile design covers safe areas, interruption, input, accessibility and device testing.

What prevents a higher score:

- The game family does not define an integration route to native Apple game services such as Game Center, controller handling, haptics, cloud saves or platform authentication.
- Metal diagnosis is not an owned game workflow; graphics guidance remains engine-neutral.
- There is no game-focused Xcode archive/export, symbolication, crash triage, TestFlight cohort or store-review response playbook.
- In-app purchases are treated mainly as a release/privacy dependency, not as a tested entitlement and recovery system.
- No iPhone/iPad reference build proves suspend/resume, thermal, memory-pressure and purchase recovery behavior.

### macOS: 24/100 within the platform subscore

macOS is the largest platform-specific weakness. The orchestration skill says the family can start a PC game, but the Unity and Godot entrypoints are explicitly framed around Android and iOS. No skill owns a macOS game delivery path.

Missing or insufficiently defined:

- Apple Silicon and Intel strategy;
- Metal feature/performance validation;
- keyboard, mouse and game-controller behavior;
- windowing, full-screen, multiple displays, Retina scaling and resolution changes;
- sandboxing, entitlements, hardened runtime, signing and notarisation;
- Mac App Store versus direct distribution versus third-party storefronts;
- package, patcher, delta-update and rollback design;
- save locations, cloud synchronization and permissions;
- crash logs, symbols and post-release diagnostics;
- macOS compatibility matrix and release-candidate rehearsal.

The current engine should not claim professional macOS game delivery until these have dedicated doctrine, templates and proof.

## Detailed capability analysis

### 1. Product strategy and production governance — 7/8

The orchestration skill is unusually disciplined. It separates concept, paper proof, interaction proof, foundation, vertical slice, production, alpha, beta, release candidate and sustain. It treats the vertical slice as risk evidence rather than a miniature content dump. It also demands a risk register, decision register, fact/fiction ledger, rights evidence and milestone exit criteria.

This deserves a high score because weak project governance destroys game budgets before code quality becomes relevant.

Remaining gaps:

- Estimation doctrine does not cover content throughput, burn rates, outsourcing ratios, rework reserves or milestone confidence calibration in sufficient detail.
- There are no contract templates for co-development, art outsourcing, audio talent, porting partners or work-for-hire intellectual property.
- Portfolio governance across several concurrent titles is absent.
- There is no greenlight committee rubric connecting creative proof, technical risk, commercial evidence and runway.
- The family does not define producer, design, engineering, art, audio, QA, data and live-operations role accountability at each phase.

### 2. Game design and player experience — 8/10

The mobile design skill makes correct platform-specific choices: prove the repeated action first; design for interruption; map the first 30 seconds and repeat session; test touch zones, handedness and failure recovery; separate value-based retention from punishment. The progression reference models sources, sinks, caps, unlocks and non-paying paths.

The weakness is breadth. A full agency also needs reusable practice for:

- level and world design;
- encounter pacing and difficulty curves;
- narrative design and branching-content production;
- social/cooperative/competitive design;
- tutorial instrumentation and comprehension analysis;
- genre-specific design patterns and counterexamples;
- controller, keyboard and mouse design for macOS;
- user-generated content, moderation and creator tools;
- child-directed design and age-appropriate monetisation controls where applicable.

### 3. Gameplay architecture, mathematics and simulation — 7/10

The engine has a sound architecture stance: explicit authoritative state, deterministic tests, injectable time/randomness, versioned saves, stable identifiers, content validators and debug views. The math skill adds coordinate-system declarations, fixed steps, tolerances, probability and reproducibility.

The missing depth becomes visible in larger games:

- authoritative multiplayer simulation;
- client prediction, reconciliation, interpolation and lag compensation;
- rollback simulation and deterministic replay;
- navigation mesh generation, crowd movement and pathfinding budgets;
- advanced animation state, inverse kinematics and gameplay/animation contracts;
- procedural generation with validity, seed and replay guarantees;
- physics determinism and cross-platform variance;
- large-world streaming, origin shifting and partitioning;
- modding and data-driven extension safety.

### 4. Engines and platform implementation — 8/14

Unity and Godot are useful and correctly separated. Both require pinned versions, plugin review, explicit architecture, physical-device tests and reproducible exports. The engine also quarantines obsolete book APIs instead of copying them into current projects.

This domain loses six points because:

- Unreal Engine is absent despite its importance to 3D, PC and high-fidelity client work.
- macOS is not owned by either engine workflow.
- Unity editor tooling, import automation, custom inspectors, content validation and package governance lack concrete examples.
- Godot production governance is too concise for larger projects, especially mixed-language, addon, export-template and platform-plugin work.
- No engine-selection bake-off template compares the same representative scene, team skills, licensing, deployment, tooling, performance and long-term maintenance.
- There is no reference project proving the architecture conventions compile and survive a release pipeline.

### 5. Art, graphics, animation and audio — 7/10

The 3D asset and real-time graphics skills are substantive. They cover silhouettes, scale, topology, UVs, baking, materials, rigs, LOD, colliders, runtime budgets, render passes, bandwidth, shader variants, golden images and target-device acceptance. Audio covers rights, recording, buses, concurrency, adaptive states, localization and device routing.

Gaps:

- no 2D art/sprite/tilemap pipeline;
- no dedicated technical animation and rigging skill;
- VFX ownership is scattered between graphics and asset guidance;
- no Houdini/procedural-content pipeline;
- no automated DCC validation/export tooling examples;
- no asset-database schema, review dashboard or content-build traceability implementation;
- no platform-specific texture/audio format decision matrix;
- no tested color-management and HDR/SDR delivery workflow;
- no audio middleware integration exemplar or voice-localisation production kit.

### 6. Online multiplayer and backend — 2/10

This is the most serious technical gap. The existing skills mention networking needs, secure API boundaries, telemetry and live operations, but no specialist owns the online game.

A production-capable engine needs explicit workflows for:

- topology selection: peer-to-peer, relay, client/server and dedicated server;
- authority and trust boundaries;
- lobby, party, presence, matchmaking and session lifecycle;
- protocol and serialization contracts;
- tick rates, bandwidth budgets, interest management and replication;
- prediction, reconciliation, interpolation, rewind and lag compensation;
- disconnect, reconnect, host migration and partial outage behavior;
- regional deployment, capacity, autoscaling and queue protection;
- persistence, inventory, entitlements and idempotent game transactions;
- anti-cheat signals, ban appeals, abuse evidence and privacy;
- load, soak, chaos and synthetic-player testing;
- cross-version compatibility and safe protocol rollout.

The general architecture, backend, database, security and DevOps families can contribute, but the game router does not compose them into a game-backend operating model. Generic SaaS doctrine is not a substitute for frame/tick-sensitive online play.

### 7. QA, performance, accessibility and localisation — 7/10

The device-performance and testing skills provide strong manual doctrine. They require physical-device captures, release-like builds, controlled scenarios, before/after evidence, hitch analysis, thermal behavior, clear bug reproduction and separate playtest questions.

What is missing:

- game-specific automated test pyramid by engine and subsystem;
- replay-based regression testing;
- deterministic simulation test harnesses with retained fixtures;
- input fuzzing, save corruption, clock manipulation and network-condition automation;
- device-lab orchestration and results schema;
- certification/compliance matrices for each platform;
- accessibility acceptance aligned to actual game interactions, not only screen UI;
- localisation pseudo-localisation, font coverage, subtitle, voice and layout automation;
- crash-free session, ANR/hang, memory-kill and symbolication operations;
- long-duration soak and suspend/resume cycling.

### 8. Build, release and distribution engineering — 6/10

The engine understands the right outcomes: pin tools, protect secrets, create signed reproducible artifacts, inspect packages, preserve symbols, stage rollout and keep rollback evidence.

However, most of this remains prose. There are no reusable pipeline files, build scripts, signing-secret interfaces, artifact manifests, checksum conventions, promotion policies or release dashboards. The engine also lacks:

- macOS notarisation and hardened-runtime delivery;
- desktop patching and differential updates;
- build-cache and content-cache strategy;
- reproducible asset-bundle/content-build promotion;
- branch/release train policy for game and content versions;
- symbol-store retention and crash-to-commit traceability;
- automated store metadata validation;
- provenance/SBOM and third-party SDK license gates tailored to games.

### 9. Live operations, data, economy and community — 4/8

The release/live-operations skill provides staged rollout, rollback, support and live-event concepts. The design skill treats economy and monetisation ethically. That is a useful base.

It does not yet provide an operating system for:

- event taxonomy and analytics contracts;
- data quality, late/duplicate events and consent-aware telemetry;
- cohort, funnel, retention, progression and difficulty analysis;
- economy monitoring, inflation detection and source/sink reconciliation;
- remote configuration and feature-flag safety;
- experimentation guardrails and sample-size/decision rules;
- live-event authoring, preview, approval and rollback;
- community moderation, player safety and incident response;
- customer support tooling, account recovery and purchase disputes;
- live-service SLOs, on-call, incident command and postmortems.

### 10. Agency delivery system and proof — 3/10

The engine can produce plans and evidence packs, but world-class agency status depends on repeatability demonstrated under delivery pressure.

Missing proof assets:

- a small but complete Unity reference game shipping to Android, iOS and macOS;
- a Godot reference game proving the alternative stack;
- a multiplayer vertical slice with a deployable backend;
- a device-performance corpus with retained captures and regression thresholds;
- a complete art/audio/content production sample with source-to-runtime traceability;
- a build farm that emits signed test artifacts and evidence manifests;
- a certification rehearsal and defect-closeout record;
- a launch simulation with rollback and incident response;
- anonymized case studies showing schedule, defects, performance, player evidence and post-launch learning;
- staffing, estimation, proposal, statement-of-work and change-control templates specific to game projects.

Until these exist, “world-class” is an aspiration and design target, not an evidence-backed status.

## Critical gaps ranked by risk

| Priority | Gap | Why it blocks agency maturity | Recommended owner |
|---:|---|---|---|
| P0 | macOS game platform delivery | One of the three named target platforms lacks an owned workflow | New platform specialist skill |
| P0 | Online multiplayer and backend | Excludes a major class of commercial game engagements | New game-network/backend skill |
| P0 | Reference implementations and proof | Doctrine cannot demonstrate repeatability without executable exemplars | Game orchestration + engineering QA |
| P0 | Game build engineering | Manual prose cannot guarantee reproducible multi-platform delivery | New game DevOps skill |
| P0 | Game security and anti-cheat | Online authority, abuse and fraud risks have no specialist owner | New game security skill |
| P1 | Unreal Engine | Limits high-fidelity, PC/macOS and client-stack coverage | New Unreal skill |
| P1 | Analytics, economy and experimentation | Live products cannot be operated safely from release guidance alone | New game data/live-economy skill |
| P1 | 2D, animation, VFX and level pipelines | Current content coverage is 3D-heavy and discipline boundaries are incomplete | New/expanded content skills |
| P1 | Automated QA/device lab | Manual gates do not scale across projects, devices and releases | Expand testing and performance skills |
| P1 | Agency commercial/delivery operations | Scoping, staffing, estimating and outsourcing need game-specific controls | New studio operations skill |
| P2 | Genre-specific playbooks | General doctrine needs adaptations for actual client project classes | References after core gaps close |
| P2 | Console/VR/AR | Valuable later, but outside the requested platform core | Defer until 95-path foundations pass |

## Roadmap from 59 to 95

The catalog currently has 155 active skills. The stated target range is 150-170, so indiscriminately adding skills would recreate catalog sprawl. Add no more than ten high-separation skills; deepen existing skills through references, templates, scripts and exemplars where ownership already exists.

### Phase 1 — close platform and architecture blockers (59 → 72)

**Target duration:** one focused capability release.  
**Exit condition:** the engine can route and specify a single-player game for Android, iOS and macOS plus an online multiplayer slice.

Add or establish:

1. `apple-game-platform-delivery`
   - iOS/iPadOS/macOS platform services;
   - Metal diagnostics routing;
   - Game Center, controller, haptics and cloud-save contracts;
   - signing, sandbox, hardened runtime, notarisation and distribution;
   - Mac-specific window/input/display behavior.
2. `online-multiplayer-and-game-backend`
   - topology and authority;
   - replication and latency handling;
   - matchmaking/session lifecycle;
   - backend persistence and regional operations;
   - network testing and safe protocol evolution.
3. `game-build-release-engineering`
   - Unity/Godot/Unreal build interfaces;
   - CI templates, build manifests, symbols, signing boundaries and artifact promotion;
   - Android, Apple mobile and macOS release trains.
4. `game-security-anti-cheat-and-abuse`
   - client trust model, server validation, tamper/cheat signals, economy fraud, abuse response and privacy.

Expand rather than duplicate:

- add macOS routes to the root router and fixtures only after the new skill exists;
- connect existing Android/iOS platform skills through explicit game-platform handoffs;
- add negative and ambiguous routing fixtures.

### Phase 2 — complete production disciplines (72 → 84)

**Exit condition:** a multidisciplinary team can produce representative content and a release candidate without inventing missing workflows.

Add or establish:

5. `unreal-game-development`
6. `game-2d-art-animation-and-vfx-pipeline`
7. `level-world-and-content-production`
8. `game-data-analytics-and-live-economy`

Deepen existing skills with:

- executable Unity and Godot content validators;
- deterministic replay fixtures;
- automated save-migration tests;
- device-lab result schemas;
- localization and accessibility test matrices;
- art/audio asset validation scripts;
- certification checklists for each supported platform;
- crash, hang and symbolication runbooks;
- remote-config and live-event change controls.

### Phase 3 — build agency repeatability (84 → 91)

**Exit condition:** two teams can use the engine independently and produce comparable evidence.

Add or establish:

9. `game-studio-delivery-and-commercial-operations`
10. `game-accessibility-localisation-and-player-safety`

Create agency templates for:

- discovery and technical due diligence;
- estimates with confidence, content throughput and contingency;
- staffing/RACI by milestone;
- statements of work, acceptance criteria and change control;
- outsourcing briefs and vendor acceptance;
- greenlight review;
- milestone health, RAID and build readiness;
- client demos and decision records;
- launch command, support and postmortem;
- case-study evidence without inflated claims.

### Phase 4 — prove the system (91 → 95)

**Exit condition:** all proof gates pass. Documentation alone cannot award these final four points.

Build and retain:

1. **Unity reference title:** a small complete game with Android, iOS and macOS builds, saves, accessibility, telemetry, IAP sandbox tests, device profiles and release manifests.
2. **Godot reference title:** a smaller alternate implementation proving scene/resource conventions, export automation and regression tests.
3. **Online vertical slice:** authoritative service, matchmaking/session flow, synthetic load, reconnect, version skew, abuse controls and rollback drill.
4. **Content pipeline specimen:** 2D/3D art, animation, VFX and audio from licensed source through validators into engine and device acceptance.
5. **Operational rehearsal:** staged rollout, telemetry alert, simulated regression, rollback, player communication and postmortem.
6. **Independent replication:** a second team follows the engine without oral coaching and passes the same evidence gates.

Only then should the engine claim a score of 95.

## Target 95 scorecard

| Domain | Current | Target | Evidence required for target |
|---|---:|---:|---|
| Product/production governance | 7/8 | 8/8 | greenlight rubric, staffing and estimate calibration demonstrated |
| Game design/player experience | 8/10 | 10/10 | level/social/narrative playbooks plus observed-player evidence |
| Gameplay/math/simulation | 7/10 | 9/10 | deterministic, networked and procedural exemplars |
| Engines/platforms | 8/14 | 14/14 | Unity, Godot, Unreal and proven Android/iOS/macOS delivery |
| Art/graphics/audio | 7/10 | 9/10 | 2D/3D/animation/VFX/audio automated pipeline specimen |
| Multiplayer/backend | 2/10 | 9/10 | deployed vertical slice, load/chaos/reconnect/version evidence |
| QA/performance/accessibility | 7/10 | 9/10 | automated device lab, certification, replay and accessibility gates |
| Build/release | 6/10 | 9/10 | reproducible signed pipelines and rollback rehearsals |
| Live operations/data/community | 4/8 | 8/8 | telemetry, economy, experiments, moderation and incident evidence |
| Agency system/proof | 3/10 | 10/10 | two-team repeatability and client-grade case evidence |
| **Total target** | **59/100** | **95/100** | **All release-blocking proof gates passed** |

## Acceptance tests for the next engine release

The next game-development enhancement should not be accepted merely because new Markdown exists. Require these tests:

### Catalog and routing

- zero catalog guardrail findings;
- no duplicate frontmatter names;
- no new near-collision without a documented boundary;
- at least one positive, one ambiguous and one negative fixture per new skill;
- explicit fixtures for Android, iOS and macOS variants;
- composition fixtures for multiplayer + backend + security + DevOps.

### Skill quality

- each skill names what it owns and refuses;
- required inputs include versions, target hardware, risk and evidence;
- outputs have objective acceptance conditions;
- every volatile platform fact routes to current official documentation;
- references include worked decisions, failure recovery and test evidence;
- no skill claims production readiness from editor or desktop-only behavior.

### Executable proof

- build commands run in clean environments;
- dependency and package versions resolve;
- automated tests contain meaningful assertions;
- device captures identify build, device, OS, scene and conditions;
- signed artifacts are promoted rather than rebuilt;
- symbols, checksums, manifests and rollback assets are retained;
- network tests include loss, latency, reorder, disconnect and version mismatch;
- save tests include corruption, migration, interruption and nearly-full storage;
- accessibility tests cover gameplay controls and feedback, not only menus;
- release rehearsal includes a failed rollout and successful rollback.

## Recommended governance

Create a game capability council with one accountable owner for each of these lines: production, design, client engineering, online/backend, graphics/technical art, content, audio, QA/accessibility, build/release, security, data/live operations and commercial delivery. One person may hold several roles in a small agency, but no line should be ownerless.

Review the score quarterly. A score may rise only when the named evidence is committed or linked. New prose can improve clarity, but it cannot earn proof points assigned to executable builds, device results, operational drills or independent replication.

Recommended release rule:

> No capability is called “world-class” because its skill file is comprehensive. The claim requires a reproducible artifact, an independent reviewer, a failed-path test and evidence that another team can repeat the result.

## Final assessment

**Score: 59/100, capped by design at 65 for this baseline.**

The engine is already better than a generic collection of game-development prompts. It has a coherent mobile-first production philosophy, strong evidence gates and disciplined separation of concerns. Those are valuable foundations.

The distance to 95 is primarily an execution-system gap, not a writing gap. The next investment should go into macOS ownership, online/backend, build automation, security, production content pipelines and reference games. If the agency completes the four-phase plan and refuses to award itself points without executable evidence, a 95 score is achievable and defensible.

## Audit integrity and limitations

- Repository files were read in their current working-tree state; several game-family and routing files are uncommitted. This audit does not assume they have been released.
- Existing July 2026 audits grade structural safety and AI-slop quality. Their clean verdicts are compatible with this lower capability score: clean documentation is not the same as complete agency capability.
- No external staff, portfolio, client, revenue or player evidence was supplied.
- No Unity, Godot, Unreal, Xcode or Android build was executed because no reference game project is present in this engine repository.
- Platform procedures change; implementation work must verify current official platform and engine documentation at the time of use.

## AI-slop audit of this report

**Verdict:** A — clean.  
**Estimated genericness:** 12/100.  
**Blocking findings:** none.

Evidence for the verdict:

- Findings cite concrete repository counts, paths, commands, scores and missing capability owners.
- The report distinguishes measured repository facts from judgments and absent proof.
- The score is not inflated by catalog health or by the engine’s own prior audit language.
- Hard cases—macOS, multiplayer, security, build automation and proof—are addressed directly.
- The roadmap has named deliverables and release gates rather than generic improvement language.

Pre-ship checks completed: no fabricated statistic, citation, package or platform promise; no placeholder content; no unsupported claim that the engine has shipped a game; risks and unassessed surfaces are explicit.
