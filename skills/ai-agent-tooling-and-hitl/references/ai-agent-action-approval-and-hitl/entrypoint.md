> Consolidated from skills/ai-agent-action-approval-and-hitl/SKILL.md into ai-agent-tooling-and-hitl on 2026-05-13. Load this through skills/ai-agent-tooling-and-hitl/SKILL.md, not as an active skill entrypoint.

# AI Agent Action Approval and Human-in-the-Loop
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Adding approval to agent actions that are irreversible or above a blast-radius threshold.
- Designing the **plan preview** UX (show the user the full plan before any action runs).
- Designing **bulk approval** ("approve all 12 outgoing emails" â€” with edit / drop per item).
- Designing **just-in-time approval** ("this step needs approval now"); choosing between blocking the agent vs background continuation.
- Designing **undo windows** for reversible actions ("Sending in 8s â€” Undo").
- Building the **agent inbox** where pending approvals queue when the user isn't actively in the conversation.
- Mobile-safe approval flows (notification â†’ one-tap approve / preview).

## Do Not Use When

- The task is the tool's reversibility classification itself â€” `ai-agent-tool-catalogue-and-action-gating`.
- The task is the agent loop state machine â€” `ai-agent-runtime-architecture`.
- The task is generic SaaS approval workflows (PO approval, leave approval) â€” use `saas-erp-system-design`.
- The task is the back-office approval (staff overriding tenant approvals) â€” `saas-admin-backoffice-tooling`.

## Required Inputs

- Tool reversibility classification (`ai-agent-tool-catalogue-and-action-gating`).
- Agent runtime state machine (`ai-agent-runtime-architecture`).
- Customer-facing UX framework (premium-ui-ux-design, `ai-agentic-ui`).
- Notification infrastructure (email, push, in-app).
- Mobile clients in scope: web responsive, native iOS, native Android.

## Workflow

1. Read this `SKILL.md`.
2. Pick the **approval pattern** per feature (Â§1). See `references/approval-ux-patterns.md`.
3. Define the **approval state machine** (Â§2). Includes timeouts, expiry, escalation.
4. Implement **plan preview** (Â§3) â€” what the user sees before approving.
5. Implement **bulk approval with per-item edit/drop** (Â§4).
6. Implement **just-in-time approval** (Â§5) and decide blocking vs background. See `references/just-in-time-approval-flow.md`.
7. Implement **undo window** for reversible auto-executed actions (Â§6).
8. Wire the **agent inbox** (Â§7) where pending approvals queue.
9. Apply **mobile-safe approval flow** (Â§8).
10. Apply anti-patterns (Â§9).

## Quality Standards

- Every irreversible action passes through an explicit approval; no auto-execute.
- Plan preview is **complete** â€” every action the agent will take is shown, in order, with concrete arguments.
- Approval payload shows **what** the agent will do, **why** (one-line rationale), and **what cannot be undone**.
- Bulk approval allows per-item edit and per-item drop without re-running the agent.
- Just-in-time approval offers two paths: block-and-wait or background-and-notify; user chooses on first approval.
- Reversible actions have an undo window of at least 5 seconds (configurable per feature).
- Mobile approval works from a push notification â†’ one-tap approve or one-tap "show details".
- Expired approvals do **not** auto-deny; they queue and notify so the user finishes the task on their schedule.

## Anti-Patterns

- "Are you sure?" modal as the entire approval UX. The user doesn't know what they're approving.
- Approval payload is the agent's natural-language summary only, with no concrete tool arguments.
- Bulk approval that auto-runs everything if any one item is approved.
- Just-in-time approval that holds the agent thread open for 24 hours, blocking other tasks.
- Mobile approval flow that requires the user to load a 4MB chat page to see context.
- Undo window with no actual undo wired up (button is fake or 500s).
- "Approve all future actions of this kind" â€” escalation of consent without scope (and without an expiry).
- Approval persisted in user session only â€” refresh loses it.

## Outputs

- Per-feature approval-pattern decision (single-shot / bulk / JIT / undo-window).
- Approval state-machine spec.
- Plan-preview UI component spec.
- Bulk approval list spec with per-item edit/drop.
- JIT approval blocking-vs-background decision.
- Undo window infrastructure (timer + cancel hook).
- Agent inbox spec.
- Mobile push approval flow.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| UX | Approval pattern decision per feature | Markdown / table | `docs/ai/agent-approval-patterns.md` |
| Architecture | Approval state machine spec | Markdown + diagram | `docs/ai/agent-approval-state-machine.md` |
| Release evidence | Approval flow user test report | Markdown | `docs/ux/agent-approval-test-2026-04.md` |
| Operability | Expired approval / escalation runbook | Markdown | `docs/runbooks/agent-approval-expiry.md` |

## References

- `references/approval-ux-patterns.md` â€” six patterns with when-to-use, screenshots/wireframes, anti-patterns.
- `references/just-in-time-approval-flow.md` â€” JIT implementation, blocking vs background, mobile.
- Companion: `ai-agent-tool-catalogue-and-action-gating`, `ai-agent-runtime-architecture`, `ai-agent-reversibility-and-blast-radius`, `ai-agent-mobile-and-web-ux-patterns`, `ai-agentic-ui`, `premium-ui-ux-design`.

<!-- dual-compat-end -->

## Â§1 Approval Patterns at a Glance

| Pattern | Best for | Friction |
|---|---|---|
| **Single-shot** | One irreversible action at the end of an agent run | Low |
| **Plan-preview** | Agent has a clear multi-step plan, all steps shown upfront | Medium |
| **Bulk approval** | Many similar items (12 emails, 30 invoices) | Medium |
| **Just-in-time** | Plan emerges as agent runs; irreversibility appears mid-task | High |
| **Undo window** | Reversible action, want low friction + safety | Very low |
| **Standing approval** | Trusted user, narrow scope, time-boxed | Lowest, riskiest |

See `references/approval-ux-patterns.md` for the full taxonomy and selection rule.

## Â§2 Approval State Machine

```
              created
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â–¼                â”‚
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”    edit   â”‚
   â”‚ pending â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â–ºâ”‚
   â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜           â”‚
        â”‚ â”Œâ”€â”€â”€â”€ reject â”€â”€â”˜
        â”‚ â”‚
        â”‚ â–¼
        â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”
        â”‚ â”‚rejectedâ”‚   terminal
        â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”˜
        â”‚ approve
        â–¼
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    undo (within window)
   â”‚ approved â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–º canceled (terminal)
   â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜
        â”‚ executed
        â–¼
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
   â”‚ executed â”‚   terminal
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
        â–²
        â”‚ expire (no decision)
   â”Œâ”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”
   â”‚ expired  â”‚   terminal (does NOT auto-execute, does NOT auto-deny)
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Key invariants:

- An expired approval is **inert**. It does not run, and it does not block â€” but the agent task is paused awaiting a fresh approval cycle.
- `undo` is only valid within `undo_window_seconds`. After that, undo becomes a compensating action (a new agent task or manual flow).
- `executed` is the terminal success. Anything that wants to "undo executed" creates a compensating task; the original approval row is immutable.

```sql
CREATE TABLE agent_approvals (
  id                  BIGINT PRIMARY KEY,
  task_id             BIGINT NOT NULL,
  tenant_id           BIGINT NOT NULL,
  user_id             BIGINT NOT NULL,
  approver_id         BIGINT,         -- may differ from user_id
  pattern             ENUM('single_shot','plan_preview','bulk','jit','undo_window','standing') NOT NULL,
  state               ENUM('pending','approved','rejected','expired','executed','canceled') NOT NULL,
  plan_payload        JSON NOT NULL,  -- full plan + concrete args
  rationale           TEXT,
  blast_radius        JSON,           -- estimated impact (e.g., recipients, amount)
  created_at          DATETIME NOT NULL,
  expires_at          DATETIME NOT NULL,
  decided_at          DATETIME,
  executed_at         DATETIME,
  undo_until          DATETIME,
  decision_reason     TEXT,
  decision_edits      JSON,           -- per-item edits
  notification_sent   JSON            -- {email, push, sms}
);
```

## Â§3 Plan Preview Component

A plan preview is **not** the agent's chat output. It is a structured component:

```
â”Œâ”€ Plan â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Goal: send invoice to ACME for May hours                â”‚
â”‚                                                          â”‚
â”‚  1. Look up ACME's billing contact   (read-only)         â”‚
â”‚  2. Calculate hours from time entries (read-only)        â”‚
â”‚  3. Create invoice draft #INV-1234   (reversible)        â”‚
â”‚  4. Send invoice to ben@acme.example (irreversible)  âš    â”‚
â”‚                                                          â”‚
â”‚  Estimated cost: $0.12                                   â”‚
â”‚  Will email: ben@acme.example                            â”‚
â”‚                                                          â”‚
â”‚  [Approve all]  [Edit step 4]  [Approve through step 3]  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

- Each step lists tool name, business label, classification, expected effect.
- Irreversible steps marked visually (âš ).
- "Approve through step N" allows partial approval â€” the agent will run to step N and pause for replanning.

## Â§4 Bulk Approval

For "send 12 emails" cases:

```
â˜ Approve all   12 items selected
â”Œâ”€ #1  Email to ben@acme.example â”€ "May invoice" â”€â”€â”€â”€ [edit] [drop]
â”‚   To: ben@acme.example
â”‚   Subject: ACME â€” May 2026 invoice
â”‚   Preview: Hi Ben, attached is the invoice for hours...
â”œâ”€ #2  Email to ana@beta.example â”€ "May invoice" â”€â”€â”€â”€ [edit] [drop]
â”‚   To: ana@beta.example
â”‚   ...
```

Per item:
- Edit: opens the args in a form; saves over the plan.
- Drop: removes from the bulk; doesn't fire.
- Selection: only ticked items execute. Default all ticked.

The agent does not re-plan on a drop â€” it skips that item. If the user edits, the edit is applied to the args; the tool runs with the edited args.

## Â§5 Just-In-Time Approval

When an irreversible action emerges mid-task:

1. Agent transitions to `AWAITING_APPROVAL`.
2. UI shows the **current step preview** (not the original plan), with: what just happened, what's next, why approval is needed.
3. The user picks one path:
   - **Approve and stay**: blocking, agent resumes when user clicks.
   - **Approve and run in background**: agent continues, notification on completion or next approval.
   - **Approve and auto-approve similar for this task**: standing approval within this task's scope.

After 24h with no decision â†’ `expired`; agent stays paused, queued in agent inbox.

Full implementation in `references/just-in-time-approval-flow.md`.

## Â§6 Undo Window

For **reversible** auto-executed actions only. The action fires; UI shows:

```
[ âœ“ Tagged 15 leads ]    Undo (8s)
```

Implementation:
1. Tool executes the action with a `staged_until` timestamp.
2. UI starts a countdown.
3. If user clicks Undo within the window, the agent runtime calls the tool's compensating action.
4. After the window, the tool transitions `staged â†’ committed`. Undo becomes "create a new compensating task".

Tools that support undo register a `compensate(args, original_result)` function.

## Â§7 Agent Inbox

Where pending approvals queue when the user is not actively in the agent's conversation:

- One row per pending approval.
- Sort: oldest expiring first.
- Bulk select + approve / reject from inbox.
- Filter by feature / agent / blast-radius.
- Mobile push for new pending items.
- Auto-archive on `expired`, `executed`, `rejected`.

Component spec in `references/agent-inbox-spec.md` (under `ai-agent-mobile-and-web-ux-patterns`).

## Â§8 Mobile Approval

Push notification payload:

```json
{
  "title": "Approve agent action",
  "body": "Send invoice $12,400 to ACME?",
  "actions": [
    { "id": "approve",     "title": "Approve" },
    { "id": "view",        "title": "View plan" },
    { "id": "reject",      "title": "Reject" }
  ],
  "data": { "approval_id": 12345, "tenant_id": 42 }
}
```

`approve` / `reject` from the notification require: app installed, user signed in, biometric or PIN re-auth for irreversible.
`view` deep-links to the plan preview screen.

## Â§9 Anti-Patterns

- Approval phrased as "Do you want me to proceed?" with no concrete args.
- Bulk approval that runs all items as a single transaction â€” one item's failure rolls back everything (often not desired).
- JIT approval that blocks the agent's thread holding a database transaction open.
- Expired approvals auto-execute "because the user probably meant yes".
- Undo button that's actually a delete-after-the-fact (sends two emails: one wrong, one correction).
- Standing approval with no scope and no expiry. Power user gets phished, agent drains the org.
- Approval payload renders the agent's free-text plan only. User cannot inspect actual arguments.
- Mobile approval that doesn't re-auth before an irreversible action.

---

## Â§10 Approval Events as Compliance Evidence (Enhancement)

Every approval event is a **compliance evidence point** for SOC 2 PI1.1 (system processing complete, accurate, timely, and authorised) and ISO 27001 A.9.4.1 (information access restriction). The approval record is the proof.

Schema additions for evidence-grade approvals:

```sql
ALTER TABLE approvals ADD COLUMN signature             TEXT NOT NULL;     -- ed25519 over canonical row
ALTER TABLE approvals ADD COLUMN signature_key_id      VARCHAR(64) NOT NULL;
ALTER TABLE approvals ADD COLUMN linked_action_chain_pos BIGINT NOT NULL; -- audit log chain pos of the action
ALTER TABLE approvals ADD COLUMN policy_version        VARCHAR(32) NOT NULL;
ALTER TABLE approvals ADD COLUMN dual_approver_id      VARCHAR(128);
ALTER TABLE approvals ADD COLUMN dual_approver_signature TEXT;
```

When an approval is granted:

1. Compute the canonical bytes (sorted keys, deterministic field set).
2. Sign with the approver's per-session key (delegated from SSO + 2FA; key validity â‰¤ 24h).
3. Capture `linked_action_chain_pos` from the audit log emitter so completeness checks can verify chain linkage (see `ai-agent-approval-audit-completeness`).
4. Emit `approval_received` event onto the action audit log with the signature embedded in `payload_summary`.

Approvals where:
- `approver_id == initiator_id` â†’ reject (self-approval).
- `approver_id NOT IN allowlist_at(tenant_id, policy_version)` â†’ reject (unauthorised).
- `dual_approver_required AND dual_approver_id IS NULL` â†’ reject (incomplete).

Cross-links: `ai-agent-approval-audit-completeness` (the completeness check that consumes these rows), `ai-agent-audit-log-integrity` (chain storage), `ai-agent-soc2-controls` (PI1.1).

