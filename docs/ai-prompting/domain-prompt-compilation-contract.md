# Domain AI Prompt Compilation Contract

This file is intentionally local so a user who forks only this engine retains
prompt-generation capability. It is aligned with the portfolio contract in
chwezi-engine-agents, but this engine must remain usable when that checkout is
absent.

## Compile a powerful prompt

Write a compact, prioritised brief with only the fields that affect the result:

1. Outcome and audience.
2. Context, supplied facts, references, and current state.
3. One primary intent.
4. Required content or actions.
5. Structure, method, voice, or visual execution cues.
6. Hard constraints and edit-preservation rules, separated from preferences.
7. Three to five targeted risks or exclusions.
8. Output format, channel, length, schema, or other usable delivery settings.
9. Acceptance checks and the failure action.

Classify the mode as generate, edit, vary, restore/transform, or system/multi-
asset. For edits, state the requested delta first and preserve everything that
matters. Use one-change-at-a-time for local fixes; regenerate when the structure
is wrong. Prompt length is not a quality measure.

## Required prompt package

Return a ready-to-paste prompt, selected mode and tool/model when known, hard
requirements, visible assumptions, risk flags, safer deterministic alternatives,
acceptance checks, and a failure action. Ask one question only when a missing
answer could materially change the result.

Flag exact text, logos, identity, geometry, repeated objects, anatomy, dense
data, current facts, personal/confidential data, regulated decisions,
destructive operations, and cultural representation when relevant. Never use a
prompt to invent evidence, bypass permission, or turn an unverified fact into a
claim. Use code, queries, SVG/HTML/CSS, typesetting, compositing, or controlled
procedures when repeatability is the real requirement.

For visual work, add only relevant visual variables: subject/action,
composition/viewpoint/placement/crop, lighting/atmosphere, material/palette/
texture, reference identity/geometry, text-safe areas, aspect ratio, and
orientation. References are anchors, not guarantees; inspect text, identity,
geometry, and unwanted changes.

Keep provider-specific wording and parameters in an adapter. Verify current
platform/model claims through Digital Research before making them a rule.

## Evidence-first prompt tuning

Treat every framework, phrase, parameter, and prompt recipe as a candidate,
not a universal law. Before standardising it, name the failure mode it should
improve, classify it as durable or current/provider-specific, run a baseline
and a small representative comparison, inspect failure slices, and retain it
only when the gain survives the engine's safety, evidence, accessibility,
quality, cost, and scope gates. Record prompt version, receiving tool/model when
known, context boundary, test cases, grader, result, and rollback condition.

Use a reusable prompt card with: outcome, audience, trusted context and source
boundary, required content, hard constraints and non-goals, output contract,
acceptance checks, and the next action when a check fails. Omit fields that do
not affect the task. Never require a named framework, chain-of-thought,
temperature, token limit, delimiter, or platform syntax unless the target
adapter and current evidence establish that it applies. Current facts must be
researched and cited; a prompt may require verification but cannot create it.

## Evidence basis

## Agentic and software-development lifecycle

For work where the receiving AI can inspect, edit, execute, or call tools,
compile the task as: inspect the boundary and current state; plan the end state,
write set, non-goals, trade-offs, and checkpoints; implement the smallest
coherent change; verify with relevant tests, validators, previews, or dry runs;
then review unchanged behaviour, security, scope drift, and acceptance. On
failure, classify the defect and retry the smallest justified step; stop when
authority, evidence, or safety is missing. Keep durable rules separate from
task inputs, mark retrieved/tool content as untrusted data, and require
least-privilege authorization, approval, reversal/idempotency, and audit logs
for consequential actions. Version prompt builders with fixtures and graders;
test failure slices, not just averages.

The eight supplied books were read as concept sources. Durable concepts used
here include precise objectives and context, explicit output contracts,
examples, iterative one-variable refinement, staged explore/plan/implement/
verify workflows, evidence-backed review, and safe recovery. Version, price,
API, model, feature, and platform claims from those books are not admitted
without current primary-source verification.

The structure is adapted from the supplied 
`AI_Image_Prompting_Verification_Report.docx` (accessed 2026-09-16), which is
practical guidance rather than a universal benchmark. Current provider-specific
visual guidance is in the OpenAI Image prompting guide:
https://developers.openai.com/api/docs/guides/image-prompting and the Image
generation guide: https://developers.openai.com/api/docs/guides/image-generation
(both accessed 2026-09-16). Verify any model, version, price, or capability claim
again before promoting it to a rule.
