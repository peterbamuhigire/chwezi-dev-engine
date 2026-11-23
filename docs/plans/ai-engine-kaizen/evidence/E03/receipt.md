# E03 evidence receipt

- **Acceptance ID:** AC-E03
- **Input:** Synthetic cases K4 and K5 in `docs/plans/ai-engine-kaizen/casebook.md`; no private or production material.
- **Source revision:** `a7824ab971af6be35877d09b9d75461b6af02674`; implementation and checks ran on this revision plus the uncommitted E03 changes.
- **Scope:** `skills/ai/ai-evaluation/references/model-adaptation-and-generation-review.md`, its offline metadata fixture and tests, and entry links from the three E03 owner skills.
- **Receipt digest:** SHA-256 is recorded in `build.contract.json` after this receipt is final.

## Reproduction and result

From the repository root:

```sh
python -B skills/ai/ai-evaluation/examples/adaptation-review/review.py
python -B skills/ai/ai-evaluation/examples/adaptation-review/review.py --fixture skills/ai/ai-evaluation/examples/adaptation-review/compatible-fixture.json
python -B -m unittest discover -s skills/ai/ai-evaluation/examples/adaptation-review -p "test_*.py" -v
```

`result.json` records the deliberately incompatible candidate: adapter base `model-r6` paired with candidate model `model-r7`. The report rejects it with `adapter_base_revision_mismatch`. It reports `img-a` and `img-b` as a byte-identical digest group, routes low-fidelity `img-c` for reviewer attention, excludes rights-unknown `img-d` from training and publication, and marks `img-d` as using a changed sampler revision. `compatible-result.json` records the matching-base positive control. The focused suite passes 4/4 tests, including a tokenizer mismatch rejection.

The fixture freezes `prompt-baseline-P0` as the comparator (model `model-r7`, tokenizer `tokenizer-r3`, template `template-p0`, fixed decode settings) and `K5-review-v1` as the held-out set. The comparison remains `NOT_RUN`. Its complete decision record selects a hold: the actual runtime model is missing, licence status is unresolved, training and inference were not run, and quality is `NOT_ASSESSED`. Its next action is to identify a compatible model, verify asset permissions, and then run a disjoint evaluation with human review. These are synthetic metadata checks. No model, image, provider, training job, GPU, or external asset was used. The checks do not establish visual quality, rights to real assets, near-duplicate detection, or performance.

| Evidence | SHA-256 | Purpose |
|---|---|---|
| `docs/plans/ai-engine-kaizen/evidence/E03/result.json` | `8ae63893966f00289ce01be50e0651c6790afc6a664e5435818c094a50487b1e` | Deliberate wrong-base candidate and K5 fixture outcomes |
| `docs/plans/ai-engine-kaizen/evidence/E03/compatible-result.json` | `450af1370258a1a7f2c621ea9e382be0c1a088758d4f05e7169606881b998fb4` | Positive matching-base control |
| `docs/plans/ai-engine-kaizen/evidence/E03/tests.txt` | `fc50a0062cf6aaa1e70ccb844c519af2bb3255f8519332600eaf38e65814bbb9` | Four test results |

## Source and currentness record

| Claim or source | Scope; publication/version | Access and review | Freshness and support | Limit |
|---|---|---|---|---|
| [Model Cards for Model Reporting, R02](https://arxiv.org/abs/1810.03993) | v2, 2019-01-14; recommends describing intended use and evaluation conditions for model releases. | Accessed and verified 2026-11-23; review by 2027-02-23 or on material change. | Context-bound; primary paper supports the reporting rationale. | Does not validate a particular model, fairness result, or asset right. |
| [LoRA, R07](https://arxiv.org/abs/2106.09685) | v2, 2021-10-16; describes freezing pretrained weights and training low-rank updates, with results scoped to the paper's experiments. | Accessed and verified 2026-11-23; review by 2027-02-23 or on material change. | Context-bound; primary paper verified. | No quality, training-time, memory, or serving claim is transferred to this fixture. |
| [Latent Diffusion Models, R08](https://arxiv.org/abs/2112.10752) | v2, 2022-04-13; describes latent-space diffusion and conditioning. | Accessed and verified 2026-11-23; review by 2027-02-23 or on material change. | Context-bound; primary paper verified. | Does not establish rights, quality, or local performance for another artifact. |
| [OpenAI Model Release Notes](https://help.openai.com/en/articles/9624314-model-release-notes) | Official page reports GPT-6.2 Astra (`gpt-6.2-astra`) and GPT-6.2 Sol (`gpt-6.2-sol`) API announcements dated 2026-11-17. | Accessed 2026-11-23; recheck on a release or before the next Kaizen cycle. | Time-sensitive; primary vendor release statement verified. | The notice is not evidence of this account's model access, task quality, latency, or cost. |
| [ChatGPT Work and Codex release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) and [Work and Codex model guidance](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex) | Official notice dated 2026-11-17 says GPT-6.2 Astra and Sol are in preview in Work and Codex desktop; access depends on plan, seat, workspace settings, and client version. | Accessed 2026-11-23; recheck on a release or before the next Kaizen cycle. | Time-sensitive; primary vendor release statement verified. | The active account/runtime catalogue is not exposed to this task and remains `NOT_ASSESSED`. |

The Codex policy check `python .codex/ensure_model_policy.py --runtime codex --check` reported `DRIFT: root model policy drift`. No host configuration was changed. The actual runtime/account catalogue and this session's selectable alternatives were not available for inspection, so candidate availability and a task-fit, cost, latency, and quality comparison remain `NOT_ASSESSED`. No model-policy change is proposed. Since the active instructions disagree and the runtime catalogue is unavailable, the model-policy decision remains `NOT_ASSESSED` for owner reconciliation; the release is a trigger for review, not evidence to switch.

## Operator replay

On 23 November 2026 the operator replayed both documented metadata checks and the four unit tests. Both JSON outputs matched the recorded decisions. The JSON records are stored in UTF-8 for reuse across platforms. The incompatible fixture serves as the negative control and the matching-base fixture as the positive control.
