# Receiving Review Feedback

Load when a reviewer, a person or an agent, has left comments on your change and you must decide
what to do with each one. Giving a review is covered by
[two-axis-code-review.md](two-axis-code-review.md); this file covers the other side.

The aim is a correct change, not a quiet reviewer. Agreeing with a wrong comment ships a defect with
two signatures on it. Arguing with a right one wastes a round. Both are avoided the same way: check
the comment against the code and the tests before replying.

## The loop, per comment

1. **Restate it.** Write the comment back in one sentence of your own: what the reviewer believes is
   wrong, and what they want changed. If you cannot restate it, ask one precise question and do
   nothing else on that comment until it is answered.
2. **Verify it against the code.** Open the lines. Trace the path the reviewer is worried about.
   Run the relevant test, or write the smallest one that would fail if the reviewer is right.
3. **Classify it.**
   - *Correct:* the evidence shows the problem is real.
   - *Correct but out of scope:* real, but belongs to another change; say where it will go.
   - *Preference:* style or naming with no behaviour effect; follow the project's written
     standard, and where there is none, the reviewer's call is usually cheaper than a debate.
   - *Incorrect:* the evidence shows the code already handles the case.
   - *Unclear:* you cannot tell without information you do not have.
4. **Respond with evidence.** Each reply names what you checked and what it showed: the test name
   and result, the line that already guards the case, or the command output.
5. **Change only what the evidence supports.** Then rerun the checks that cover the changed lines.

## Disagreeing

Disagree when the evidence supports it, and say so plainly: "I checked X; the guard at
`path:line` already rejects that input, and `test_name` covers it. Leaving as is." Offer the test
as proof rather than asserting you are right. If the reviewer still disagrees after seeing the
evidence, escalate to the change owner with both positions; do not loop.

## No performative agreement

Do not open replies with praise or thanks as a reflex, and do not write "good catch, fixed" before
the fix exists and its check has run. Do not accept a suggestion to end the conversation. Each of
these hides whether the comment was actually verified.

## Worked example

A reviewer asks you to drop the retry wrapper around a payment webhook call and to rename
`PaymentSvc` to `PaymentService`.

- Retry wrapper: restate ("they think the retry is redundant because the queue already retries").
  Verify: the queue retries the whole job, but the wrapper retries only the provider call inside
  an idempotency key. Removing it would make every provider timeout re-run the full job, including
  the ledger write. Classify: incorrect. Respond with the idempotency test that shows the wrapper
  prevents a double posting. Keep it.
- Rename: restate, check the project naming standard (it spells out "Service"), classify as
  correct, rename, run the suite.

## Record declined suggestions

Keep a short list in the pull request description or review record:

| Comment | Decision | Evidence |
|---|---|---|
| Drop retry wrapper in `WebhookHandler` | Declined | `test_webhook_timeout_does_not_double_post` fails without it |

A declined suggestion with its reason saves the next reviewer from raising it again, and lets the
owner overrule you with full information.

(Adapted from obra/superpowers, MIT, https://github.com/obra/superpowers, commit
8ca22dba9a94f28898bbce59f2537ff4d87c747d. Paraphrased; no text copied.)
