# Model adaptation and generated-output review

Use this workflow when a proposed change could be handled by a prompt, retrieval, an adapter or a trained model, or when generated media may be evaluated, trained on, or published.

## Choose the smallest intervention that meets the outcome

| Need | First candidate | Evidence to move on |
|---|---|---|
| A one-off instruction, format, or example changes the output | Prompt or workflow change | Frozen examples show the prompt change meets the acceptance threshold without worsening the fixed baseline cases. |
| The output needs current or case-specific facts | Retrieval from a permitted, versioned source | The selected source is eligible, traceable, current enough for the task, and supports the answer. |
| Stable labels, terminology, or style remain inconsistent after prompt and retrieval checks | Adaptation candidate | A disjoint test set shows a useful improvement over the unchanged prompt/retrieval comparator, with rights and rollback recorded. |
| No candidate has evidence, model, tokenizer, or permission | Hold decision | Record the missing input, the unrun step, its owner, and the next evidence needed. |

Do not adapt a model to supply facts that change; retrieve those facts. An example decision can select prompt iteration for a small, stable style change, retrieval for current product facts, and adaptation only when a stable behavior still fails on a held-out set. This is a decision rule, not a performance claim.

## Freeze the candidate contract

For each candidate, record the base model family and immutable revision, tokenizer revision, adapter base revision, prompt or generation template revision, and decode settings. For media, also record model revision, sampler revision, seed, conditioning inputs, and output IDs. Preserve the exact candidate and baseline manifests with the evaluation result. Reject a base-model or tokenizer mismatch before inference. Matching metadata makes a candidate eligible for evaluation; it does not establish quality or bit-for-bit reproducibility.

Freeze a named comparator, its model and prompt revisions, decode settings, and a disjoint test-set revision before selecting prompt, adapter, or sampling settings. Run the comparator and candidate on the same held-out cases. If the model is missing, record the comparator and test-set IDs while marking the comparison `NOT_RUN`; do not fill the record with guessed scores. A generated-media review should score fidelity and diversity separately. Byte-identical outputs can expose a duplicate; a perceptual or human check is needed for near-duplicates. A changed sampler or tokenizer revision invalidates a same-seed reproducibility claim unless it is evaluated again.

## Record rights and human review

For every input, training item, and output intended for training or publication, record a stable ID, provenance, rights status, permitted use, and reviewer. Unknown or unverified permission excludes the item from training and publication until resolved. A synthetic fixture can test this exclusion rule; it cannot establish that real assets are licensed.

Name the representative reviewer group, rubric, held-out review sample, threshold, disagreements, and correction path. Keep an independent human review for material fidelity, safety, or rights decisions. State which quality measures require a real model and reviewer. If no model or licensed asset is available, write the decision record anyway and mark training and inference `NOT_RUN`, quality `NOT_ASSESSED`, and rights unresolved.

## Offline fixture

From the repository root:

```sh
python -B skills/ai/ai-evaluation/examples/adaptation-review/review.py
python -B -m unittest discover -s skills/ai/ai-evaluation/examples/adaptation-review -p "test_*.py" -v
```

The review script reads only the local synthetic JSON fixture and emits a deterministic report. Its fixture intentionally pairs an adapter with the wrong base, repeats an output digest, includes an output with unknown rights, and changes a sampler revision. It must reject the adapter, flag the duplicate, exclude the rights-unknown item, and leave generated quality unassessed. `compatible-fixture.json` is the positive base-match control. The example uses no model, image, provider, GPU, or real asset and makes no inference or performance claim.

## Evidence basis and limits

Model Cards recommends documenting intended uses and evaluation conditions; this supports recording scope and measured results, not a guarantee of fairness or fitness ([Mitchell et al., 2019](https://arxiv.org/abs/1810.03993), v2). LoRA describes one parameter-efficient adaptation method and reports results for its named experiments; those findings do not predict a new model's quality or cost ([Hu et al., 2021](https://arxiv.org/abs/2106.09685), v2). Latent diffusion describes a conditional image-generation method; its paper does not establish rights, local performance, or output quality for another artifact ([Rombach et al., 2022](https://arxiv.org/abs/2112.10752), v2).
