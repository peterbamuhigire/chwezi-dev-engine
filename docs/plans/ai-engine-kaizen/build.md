# chwezi-dev-engine · AI capability implementation

**Current Jidoka handoff.** E01 and E02 are committed and both have valid acceptance receipts. During the operator recovery session (the driver prompt contains the line beginning with RECOVERY), the entire assigned slice is to reconcile these already committed results. If Git status is clean and E01 and E02 are complete, return immediately with the candidate SHA so the supervisor runs its independent gate. No further edits or commits are due in that recovery session. During the subsequent ordinary session (driver prompt has no RECOVERY line), begin E03. E04 through E06 follow their listed dependencies.

**Accountable owner** Peter. **Execution role** Public engineering maintainer. **Observed starting revision** `9354c95bab654ad38a2bf86da5d599a405bd496e`. Recheck the revision on staging. Apply ordinary commits to the isolated JAD branch. Link a receipt for each criterion. All tasks begin pending.

**User journey** model choice → worked implementation → diagnostics → code review. Maintain the public examples directly in their owning skills. Public content uses original synthetic data and its own evidence. Avoid a dependency on the private Development repository.

**Entry condition** Use the published-safe SRS contract or the casebook fixture and record which input was used. No copying private engine text.

**Inputs** Use [casebook.md](casebook.md) for the fixture data and expected outcomes and [sources.json](sources.json) for external evidence. B1 Joel Grus, B2 Thomas Nield, B3 Albrecht/Ramachandran/Winkler, B4 Parikh/Johri, B5 Neroda/Escaravage/Peters, B6 David Foster, B7 Sanseviero/Cuenca/Passos/Whitaker, B8 Brousseau/Sharp. R IDs refer to primary sources in the register. Use the latest verified source for any new API, model version, security or vendor-specific claim. Close the capability through its normal route.

## Ordered tasks

### E01 · Replace modality shortcuts in the public ML guide

**Depends on** Entry condition only. **Owned surfaces** `skills/languages/python-ml-predictive`, `skills/ai/ai-opportunity-canvas`. **Basis** B1 B2 B3 R03 R04.

Rework the existing when-ML-versus-LLM reference and its parent route. Give the practitioner an original sparse-text baseline, rule comparator and hand-computed error costs. Show when additional training or a larger model adds no demonstrated value.

Ship a minimal, public, offline example with separate training and scoring, a fixture dataset, a reloadable artifact and class-wise held-out results. Provide an original input with negation and one rare identifier. Explain which tokenization choices help or hurt those cases.

**AC-E01.** K1 holds input modality constant while the preferred policy changes with workload or missed-case cost. Old absolute numerical speed/cost claims either gain scoped measurements or are removed. A text label task can choose a conventional classifier. The documented commands generate the model and independently score the unseen examples. The measured results are kept separate from K1’s hand-calculated policy table. The K1 regression fixture rejects a mislabeled scorer and distinguishes MSE of 1/3 from R-squared of 7/8.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/E01/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

### E02 · Test corpus preparation, retrieval and answer quality independently

**Depends on** E01. **Owned surfaces** `skills/ai/ai-rag-patterns`, `skills/ai/ai-evaluation`, `tests`. **Basis** B3 B7 B8 R05 R06.

Extend the existing curated corpus example with noisy/negated text, case-sensitive IDs, stale versions and no-answer questions. Compare lexical retrieval with any candidate under equal corpus permissions. Preserve original text offsets or record a reversible mapping.

Include a text-normalization ablation on exact identifiers and negation. If the evaluation admits synthetic relevance judgments, hold out a fresh family of queries from tuning.

**AC-E02.** K2 permits a correct ranking with a failed answer-support grade. With no eligible document the system abstains. Original identifiers survive normalization and retrieval output contains no inaccessible or withdrawn row. The evaluator can identify a wrong result introduced by removing a meaningful token, recover its unmodified source and rerun the comparison.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/E02/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

### E03 · Select adaptation or media generation against a fixed comparator

**Depends on** E01. **Owned surfaces** `skills/ai/ai-llm-integration`, `skills/ai/ai-evaluation`, `skills/ai/ai-app-architecture`. **Basis** B6 B7 B8 R02 R07 R08.

Write a practitioner guide for adapting an existing model and evaluating generated outputs. Cover tokenizer/adapter compatibility, sample-setting manifests, a disjoint test set, rights and representative human review. Keep the example independent of a hosted API.

Include a worked choice among changing the prompt, retrieving current information or learning a stable label/style behavior. Specify model revision, tokenizer, generation template and decode settings. Quantization, training or serving speed claims require measurements of the actual artifact and workload.

**AC-E03.** K4 rejects a candidate adapter on the wrong base. K5 detects duplicated outputs and missing rights. The guide reports which quality measures still require a real model and reviewers. No GPU, training or provider performance is claimed from metadata. A missing model or license produces a complete decision record with the unrun inference or training step visibly unresolved.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/E03/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

### E04 · Diagnose data, model and serving failures with recoverable releases

**Depends on** E02, E03. **Owned surfaces** `skills/ai/ai-observability-and-debugging`, `skills/ai/ai-incident-response`, `skills/languages/python-ml-predictive`, `tests`. **Basis** B4 B5 B7 B8 R09 R10.

Connect the existing drift and rollback references. Emit a fixture trace for a data shift with delayed labels, a serving transform mismatch, and an incompatible revision after deployment. Exercise replay and escalation to a named operator.

**AC-E04.** K4 distinguishes all three failure classes, restores the compatible bundle and prevents duplicate effects on retry. An alert with missing labels states what is observable and defers any accuracy claim.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/E04/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

### E05 · Use repository-aware coding assistance and independent review

**Depends on** Entry condition only. **Owned surfaces** `skills/sdlc-meta/ai-assisted-development`, `skills/ai/coding-agent-optimization`, `tests`. **Basis** B1 B4 B5 B8 R10 R12 R15.

Give the existing AI-generated code review gate a reproducible small change. Include entry-point behavior, source files, change scope, compatibility and retry cases, reviewer-owned checks, correction time and residual risk. Keep ordinary resource inventory out of the workflow.

**AC-E05.** K3 fails the original defect, rejects a plausible incorrect implementation, and passes a correct one through a normal caller. Include pre-change persisted data and evidence from independent execution. Scope, fallback and rework stay in the receipt.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/E05/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

### E06 · Prove the public routes and catalog still work

**Depends on** E01, E02, E03, E04, E05. **Owned surfaces** `scripts`, `tests`, `skills`. **Basis** B3 B5 R05 R09.

Reuse the local catalog, source, collision and routing checks. Add positive, neighboring and negative fixtures for changed intents. Inventory overlaps and retire duplicate proposals in favor of the owning reference. Check provenance and rights of new fixtures.

**AC-E06.** A user seeking predictive text classification reaches the intended public route; ground an answer, recover an incident and review an AI-authored patch each reach an appropriate owner. Show before/after routing on the same fixtures and retain unrelated baseline warnings.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/E06/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

## Verification, replay and handoff

Preserve the repository's configured slice and final checks. Run the narrow check for the changed behavior as well. Exercise a negative control by removing a required input or introducing the named defect. Record which assertion fails. Repeat on the repaired revision. Existing tests cover only their actual scope. A documentation example may be validated by an independent walkthrough with observed outputs. A trained-model, hosted or production claim requires that environment's evidence.

Keep an independent test oracle and the frozen synthetic case IDs. Use original product-safe work in public repositories. The book files and window receipts stay outside all engines. Link any additional task-specific code, catalogue, generated projections and test fixtures to the ownership decision in the evidence record. Avoid unrelated edits.

For interruption, inspect JAD status, branch, plan and the verification receipt. A matching digest can identify an existing artifact. Reconcile partial effects by their operation ID. Resume the existing lane after confirming the saved intent. Never reissue an uncertain external action. A gate failure retains its log and remains failed until repaired and rerun. Continue independent tasks. Enter a blocked result only if no permitted work remains.
