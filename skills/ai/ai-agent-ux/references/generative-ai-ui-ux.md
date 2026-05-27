# Generative AI UI/UX Patterns

This reference is self-contained. It distills the user's supplied Design Studio UI/UX
generative-AI design article into durable AI interface rules.

Source used:

- https://www.designstudiouiux.com/blog/generative-ai-ui-ux-design/

## Core Rule

AI UX must make uncertainty manageable. The user should know what the AI is doing, what
it used, how confident it is, what can be changed, and how to recover.

## Required AI UI Patterns

| Pattern | Use When | Requirement |
|---|---|---|
| Prompt composer | User gives intent or constraints | Support examples, attachments where relevant, history, and clear submit state. |
| Streaming response | Output takes more than a second | Stream progressively, preserve layout stability, and allow stop/cancel. |
| Evidence / source panel | Output depends on retrieved or external facts | Show citations, source freshness, and unavailable-source warnings. |
| Confidence or quality signal | Output may be wrong or incomplete | Use plain-language confidence, missing-data warnings, or review-needed labels. |
| Edit and refine loop | User must shape output | Provide inline edit, retry, regenerate with instructions, and compare versions. |
| Human override | Action has business, legal, financial, or safety risk | Require approval, expose the proposed action, and keep audit evidence. |
| Failure recovery | Model, tool, or data source fails | Show what failed, what was saved, retry path, and support/escalation path. |
| Cost / quota cue | AI usage is metered or limited | Show remaining credits or cost where it affects user decisions. |

## Trust Requirements

- Never present generated content as certain when source evidence is weak.
- Keep user control visible: stop, retry, edit, approve, reject, undo where possible.
- Distinguish model output from verified system records.
- Avoid raw JSON unless the target user is explicitly technical and asked for it.
- Log approvals, rejected suggestions, and final user-edited output for audit-sensitive domains.

## Design States

Every AI surface must define:

- Idle with prompt guidance.
- Drafting / streaming.
- Tool call in progress.
- Needs more information.
- Completed with review controls.
- Low confidence / missing sources.
- Blocked by policy, permission, quota, or unavailable data.
- Failed with retry and handoff path.

## SRS Acceptance Criteria

Example requirement shape:

`AI-UX-###: The system shall display generated recommendations with source evidence,
confidence status, and approve/reject controls before any irreversible user-facing or
business-critical action is executed. Verification: prototype walkthrough, audit-log
fixture, and usability test.`

## Anti-Patterns

- A single chat box replacing the product's workflow.
- Model output inserted into records without review.
- Confidence shown as a precise percentage when no defensible calibration exists.
- Disappearing loading states that leave the user unsure whether work continues.
- Retry controls that rerun the same failing prompt without explaining what changed.
