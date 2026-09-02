# Book-Driven Kaizen Wave 3 — 18-Source Cross-Engine Study

**Study date:** 2026-09-02  
**Scope:** All 18 supplied Markdown sources, all 11 canonical skill engines  
**Use:** Durable synthesis and implementation ledger; not a copy of the books

## Source admission and study status

The books are tertiary/secondary learning inputs. They are admitted for durable concepts,
examples, and hypotheses only. Current commands, APIs, standards, product capabilities, laws,
platform policies, benchmarks, and security controls are not admitted from a book without a
current authoritative source and verification record.

| # | Supplied source | Study status | Durable synthesis | Limitation/currentness boundary |
|---:|---|---|---|---|
| 1 | Wicked Cool Shell Scripts, 2e | REVIEWED / qualified | Small composable utilities, input validation, command wrappers, scheduled maintenance, web/file automation, backups, change tracking, and the value of experimenting by breaking and fixing scripts. | The cookbook contains unsafe historical patterns: unquoted expansion, temporary-file races, `which`, legacy HTTP scraping, `killall`, and weak cleanup. Use only as a prompt for safe re-engineering. Verify shell dialect, commands, APIs, and service assumptions. |
| 2 | UNIX Internals: The New Frontiers | REVIEWED / historical-only | Processes, credentials, kernel/user boundaries, threads, signals, scheduling, IPC, synchronization, filesystems, distributed filesystems, virtual memory, device I/O, and the trade-off between simplicity, portability, performance, and flexibility. | Treat SVR/BSD/Mach implementation details as historical mental models. Verify Linux/Windows/macOS behaviour against current OS documentation and lab evidence. |
| 3 | Information Dashboard Design | REVIEWED / historical principles | A dashboard is a communication instrument: define purpose and audience, show summaries/exceptions with context, use perceptually accurate encodings, minimise decorative pixels, support comparison and drill-through, and test usability. | Visual principles transfer; historical vendor/tool references do not. Current accessibility, chart semantics, responsive behaviour, and performance require current standards and rendered evidence. |
| 4 | Pro Git, 2e | REVIEWED / historical workflow plus durable concepts | Git snapshots, integrity, staging, branches, remotes, merging/rebasing, recovery, hooks, signing, internals, and the need to inspect state before destructive operations. | Verify modern command recommendations, default branch/hosting policy, branch protections, signing, hooks, worktrees, and remote workflows using current Git/hosting documentation. |
| 5 | Pro Spring Boot 4, 4e | REVIEWED / current-edition but volatile | Layered application design, externalised configuration, profiles, REST semantics, validation, error contracts, data access, reactive flows, messaging, Testcontainers, Actuator/OpenTelemetry, native images, Spring Cloud, and Spring AI. | Version and dependency claims are volatile. Verify against the current Spring reference, Java/Jakarta docs, dependency release notes, and security advisories before adoption. |
| 6 | A Bug Hunter’s Diary | REVIEWED / historical-only and safety-qualified | Trace untrusted input from entry point through code, combine static and dynamic analysis, use fuzzing to find parser boundaries, reproduce crashes, distinguish impact, remediate root causes, and disclose responsibly. | Exploit construction, kernel/browser/driver examples, and legacy mitigations are not operational recipes. Route to authorised defensive testing only; verify current secure-development guidance. |
| 7 | Bandit Algorithms for Website Optimization | REVIEWED / historical algorithms | Exploration versus exploitation, epsilon-greedy, softmax, UCB, simulation as a test, A/A tests, concurrent experiments, moving environments, contextual bandits, metric design, and regret. | Do not copy old code or assume a bandit is automatically better than an A/B test. Verify experiment methods, privacy, platform capabilities, and statistical assumptions. |
| 8 | Introduction to Information Retrieval | REVIEWED / preliminary-draft qualified | Inverted indexes, Boolean/phrase/proximity retrieval, tolerant matching, spelling correction, index construction/compression, tf-idf/vector scoring, evaluation, and the need to protect access boundaries in retrieval. | The file is a 2007 preliminary draft with OCR defects and incomplete exercises. Keep concepts only; verify modern search, embedding, ranking, RAG, and evaluation practice. |
| 9 | Mastering Local SEO with Google Maps | REVIEWED / claim-qualified | Search intent, entity consistency, local profile completeness, service/location content, reviews, citations, conversion paths, baseline benchmarking, and human review of AI-assisted local workflows. | Ranking, review, “AI-powered search,” and Gemini claims are not accepted as fact without current Google documentation and observed data. Never promise placement or fabricate reviews. |
| 10 | Python Tricks | REVIEWED / durable-language concepts | Readable idiomatic Python, first-class functions, decorators, explicit exceptions, context managers, data-structure choices, comprehensions, iterators, and careful object semantics. | Examples reflect an older Python era. Verify syntax, standard-library behaviour, supported versions, typing, packaging, and security guidance against current Python docs and project policy. |
| 11 | Perfect Software and Other Illusions About Testing | REVIEWED / durable testing philosophy | Testing supplies risk-reducing information, not perfection; choose tests by risk and information value; test the testing process; record timely evidence; avoid proxy metrics, tidy fabricated data, blame, and quantity-over-quality. | Not a current test standard. Pair the heuristics with current product, security, accessibility, performance, and release evidence. |
| 12 | Mastering Prompt Engineering | NOT_ASSESSED | No synthesis admitted. | Supplied Markdown is empty; the alternate PDF is a 548-byte HTML `404 Not Found` placeholder. Obtain a valid source before study. |
| 13 | Digital Image Processing, 4e | REVIEWED / mathematical foundation | Image acquisition and sampling, enhancement versus restoration, transforms, colour, compression, segmentation, feature extraction, classification, and the importance of task-specific quality criteria. | 2017 techniques and examples do not establish current browser formats, codec support, accessibility, ML APIs, or image policy. Verify current delivery and model/tool claims. |
| 14 | Learning JavaScript Data Structures and Algorithms, 3e | REVIEWED / historical-currently qualified | Arrays, stacks, queues, linked lists, sets/maps, hashing, recursion, trees, heaps, graphs, sorting/searching, complexity, ES2015+ and TypeScript transfer. | Verify current ECMAScript, Node.js, browser APIs, module systems, TypeScript, and package/tooling guidance before implementation. |
| 15 | Ace the Data Science Interview | REVIEWED / qualified | Explainable project impact, probability/statistics, ML trade-offs, SQL/data modelling, coding, product sense, case reasoning, communication, and audience-aware evidence. | Interview advice is contextual; do not turn examples or market claims into facts. Verify current data tooling and statistical methods when used operationally. |
| 16 | Building and Distributing Agentic AI Solutions | REVIEWED / current-edition but highly volatile | Productisation from opportunity to cost/pricing, agent architecture, RAG, MCP/tools, multi-agent workflows, evaluation before expansion, distribution, and responsible AI. | 2025/2026 model, framework, cloud, MCP, market, and regulatory claims require current primary-source verification. Examples are not security or architecture authority by themselves. |
| 17 | The Human-Agent Orchestrator | REVIEWED / framework qualified | The 6S canvas (Source, Success, Safety, Steering, Switch, Sharpen), explicit outcomes/audience, named ownership, enforceable constraints, decision rights, escalation, circuit breakers, containment, recovery, drift detection, and human skill preservation. | Framework is a design heuristic, not a standard or outcome guarantee. Validate autonomy and intervention decisions against risk, evidence, and accountable owners. |
| 18 | HTTP: The Definitive Guide | REVIEWED / historical protocol guide | HTTP resources/messages, methods/status, intermediaries, caches, gateways, identity/authentication, TLS, content negotiation, hosting, load balancing, and logs. | The guide predates HTTP/2, HTTP/3, current TLS, and modern RFC structure. Use current RFC 9110–9114 and deployment/security documentation. |

## Current-source ledger used for volatile claims

Access date for this wave: **2026-09-02 UTC**. These are primary or standards-track sources used
to qualify transfers; they are not substitutes for claim-specific verification in future work.

| Topic | Current authority | Transfer decision |
|---|---|---|
| HTTP semantics and transports | RFC 9110, RFC 9111, RFC 9112, RFC 9113, RFC 9114 — `https://www.rfc-editor.org/rfc/rfc9110.html` and linked RFCs | Replace book-era protocol assumptions; preserve method safety/idempotency, intermediaries, caching, and version-independent semantics. |
| Spring Boot | Spring Boot reference — `https://docs.spring.io/spring-boot/reference/` | Treat book examples as versioned examples; resolve stable release, Java, Jakarta, dependency, security, native-image, and observability details at task time. |
| Python | Python 3 documentation — `https://docs.python.org/3/` | Preserve language concepts; verify supported version and standard-library behaviour at task time. |
| Bash/POSIX shell | GNU Bash Reference Manual — `https://www.gnu.org/software/bash/manual/`; POSIX authority is resolved per task | Preserve quoting, exit-status, signal, and shell-contract lessons; never assume Bash syntax is portable `sh`. |
| Shell static analysis | ShellCheck guidance — `https://www.shellcheck.net/wiki/` | Require an explicit shebang/dialect and linting where shell is used. |
| OS command safety | OWASP OS Command Injection Defense — `https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html` | Prefer libraries/structured arguments; parameterise and validate when a command is unavoidable; use least privilege. |
| Web accessibility and image alternatives | W3C WCAG 2.2 — `https://www.w3.org/TR/WCAG22/`; WAI Images Tutorial — `https://www.w3.org/WAI/tutorials/images/` | Require current accessibility criteria and equivalent text for informative, functional, decorative, and complex images/charts. |
| Google Search and local structured data | Google Search Essentials — `https://developers.google.com/search/docs/essentials`; LocalBusiness structured data — `https://developers.google.com/search/docs/appearance/structured-data/local-business` | Preserve intent/entity/benchmark concepts; reject ranking guarantees and verify eligibility/policy requirements at task time. |
| Git | Git documentation — `https://git-scm.com/docs/`; hosting controls are verified with the relevant provider | Preserve snapshot/recovery/review discipline; replace obsolete checkout/reset advice where safer modern commands apply. |

## Engine crosswalk and adoption decisions

| Engine | Applicable books | Improvement target | Decision |
|---|---|---|---|
| SRS | Git; Spring Boot; HTTP; testing; bug hunting; data science; agentic AI; orchestrator; JS/Python | Add traceable operational contracts: API semantics, failure-path tests, evidence quality, agent decision rights, and version/currentness fields. | Upgrade existing Kaizen owner and add a focused reference; no new domain skill. |
| Business plan | Dashboard; bandits; local SEO; data science; agentic AI; testing | Connect value hypotheses to measurable outcomes, uncertainty, capacity/cash guardrails, benchmark baselines, and responsible AI economics. | Upgrade existing Kaizen owner and add a focused reference. |
| Website | Dashboard; bandits; IR; local SEO; image processing; HTTP; JS; agentic AI | Make page/dashboard purpose, retrieval/SEO evidence, experiment design, image QA, accessibility, protocol semantics, and AI fallback explicit. | Upgrade existing Kaizen owner and add a focused reference. |
| Social media | Bandits; local SEO; dashboard; IR; data science; agentic AI | Use outcome/guardrail experiments, channel evidence, local/entity consistency, content retrieval, cultural review, and human publication control. | Upgrade existing Kaizen owner and add a focused reference. |
| Linux | Shell; UNIX internals; Git; Python; HTTP; bug hunting; testing | Add safe script contracts, process/resource mental models, idempotence, observability, recovery, and current-command gates. | Upgrade existing Kaizen owner and add a focused reference. |
| Proposal | Testing; bug hunting; dashboard; IR; local SEO; agentic AI; orchestrator | Improve evaluator evidence, risk/assumption traceability, measurable M&E, defensible technical claims, and agent-delivery governance. | Upgrade existing Kaizen owner and add a focused reference. |
| Accounting | Dashboard; data science; testing; Git; agentic AI; orchestrator | Strengthen metric lineage, exception evidence, change control, segregation, approval, and automation rollback. | Upgrade existing Kaizen owner and add a focused reference. |
| Design | Dashboard; image processing; local SEO | Add task-first data communication, perceptual integrity, image-quality measurement, text alternatives, and current accessibility/performance verification. | Upgrade existing Kaizen owner and add a focused reference. |
| Digital research | IR; bandits; data science; bug hunting; HTTP; UNIX; agentic AI; orchestrator | Improve retrieval/evaluation, adaptive research waves, source/data quality, safe collection, agent delegation, and evidence reproducibility. | Upgrade the existing audit reference and add a focused Kaizen reference; no duplicate route. |
| Engineering | All except unavailable prompt engineering | Make currentness, testing, Git recovery, secure input handling, protocol contracts, data structures, image pipelines, and agent evaluation first-class. | Upgrade existing Kaizen owner and add a focused reference. |
| Windows administration | UNIX; shell; Git; Python; HTTP; bug hunting; testing; agentic AI; orchestrator | Add a Windows-native Kaizen loop with target/management-plane resolution, PowerShell safety, event/process/network evidence, R0–R5 controls, and recovery. | Add the one missing Kaizen owner skill, catalogue entry, reference, and routing test. |

## Implementation record

| Change class | Planned count | Result |
|---|---:|---|
| New skills | 1 | Windows Kaizen owner; justified by a missing distinct route. |
| Existing Kaizen owner surfaces upgraded | 10 | One in each other engine; Digital Research uses its existing audit reference as the owner surface. |
| New engine-specific references | 11 | One per engine, including Windows. |
| Central study/design/plan documents | 3 | This ledger plus the approved design specification and implementation plan. |
| Raw book text/OCR/exploit recipes | 0 | Excluded by design. |

## Residual gaps and next review

- The prompt-engineering source remains `NOT_ASSESSED` until a valid artifact is supplied.
- Live Windows-lab, Linux distro-matrix, rendered visual, production analytics, and external
  platform checks are not inherited from documentation changes; each remains a separate gate.
- All volatile claims must be rechecked at task time even when this ledger has a current source.
- Re-audit the changed routes and references after the next pull or by **2026-10-02**, whichever
  comes first.
