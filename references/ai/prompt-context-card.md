# Versioned prompt/context card

`tools.ai.prompt_context.PromptContextCard` assembles a deterministic,
provider-neutral prompt from trusted instructions, objective, task,
constraints, provenance-tagged context, output schema, fallback, evaluator,
examples, and optional model/tool version labels. The returned `PromptBundle`
contains the exact prompt, prompt hash, card version and context hash.

Context is rendered inside explicit `TRUSTED DATA` or `UNTRUSTED DATA` blocks.
The assembler states that directives inside data blocks are evidence and must
not change the task, permissions, tenant scope, or tool policy. Missing
required context and invalid packet provenance raise named errors rather than
silently producing a weaker prompt.

The assembler does not call a model or claim provider-specific behaviour.
Provider adapter compatibility, model availability and production evaluation
are `NOT_ASSESSED` by this repository utility.
