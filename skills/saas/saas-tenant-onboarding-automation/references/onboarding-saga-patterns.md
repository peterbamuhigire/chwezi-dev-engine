# Onboarding Saga Patterns — Reference

The execution engine for the onboarding workflow. Choose based on volume, latency requirements, and existing stack.

## Pattern 1: DB-State-Machine + Worker

Simplest. Best for: low-to-mid volume SaaS (< 1k onboardings/day), pool deployment with sub-second steps.

```
[ Signup HTTP request ]
   ↓
[ Insert into onboarding_runs with status='pending', current_step='create_tenant' ]
   ↓
[ Worker picks pending runs, executes one step, advances current_step ]
   ↓
[ On step success → next step; on failure → retry / fail ]
   ↓
[ Final step → status='succeeded' ]
```

**Pros:** simple, no extra infra, debuggable with SQL.
**Cons:** worker bottleneck at scale; manual handling of timeouts.

Schema in `saas-tenant-onboarding-automation` §10.

## Pattern 2: Queue-Driven Saga

Each step puts the next step's message on a queue.

```
SignupController → publish('onboarding.step.create_tenant')
StepWorker:create_tenant → publish('onboarding.step.bootstrap_identity')
StepWorker:bootstrap_identity → publish('onboarding.step.create_stripe_customer')
...
```

**Pros:** scales horizontally; each step is an independent consumer.
**Cons:** state is implicit (which message is in which queue?); compensations require explicit reverse-flow; debugging is harder.

## Pattern 3: Temporal / Cadence

Purpose-built workflow engines. Best for: mid-to-large SaaS, silo deployment with multi-minute provisioning, complex compensations.

```python
@workflow.defn
class OnboardingWorkflow:
    @workflow.run
    async def run(self, signup: SignupPayload) -> TenantId:
        try:
            tenant = await workflow.execute_activity(
                create_tenant, signup,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=RetryPolicy(maximum_attempts=3)
            )
            await workflow.execute_activity(bootstrap_identity, tenant, ...)
            await workflow.execute_activity(provision_infra, tenant, ...)
            await workflow.execute_activity(create_stripe_customer, tenant, ...)
            await workflow.execute_activity(seed_defaults, tenant, ...)
            await workflow.execute_activity(send_welcome_email, tenant, ...)
            await workflow.execute_activity(emit_ready_event, tenant, ...)
            return tenant.id
        except ActivityError as e:
            await workflow.execute_activity(compensate, e.activity_name, tenant)
            raise
```

**Pros:** durable, retry-built-in, compensations declarative, observable, time-travel debugging.
**Cons:** Temporal cluster to operate (or use Temporal Cloud); learning curve.

## Pattern 4: AWS Step Functions

Managed AWS state machine. Good if already on AWS.

```yaml
StartAt: CreateTenant
States:
  CreateTenant:
    Type: Task
    Resource: arn:aws:lambda:...:CreateTenant
    Retry: [...]
    Catch: [{ ErrorEquals: ["States.ALL"], Next: FailOnboarding }]
    Next: BootstrapIdentity
  BootstrapIdentity:
    Type: Task
    Resource: ...
    Next: ProvisionInfra
  ProvisionInfra:
    Type: Task
    Resource: ...
    TimeoutSeconds: 600
    Next: CreateStripeCustomer
  ...
  FailOnboarding:
    Type: Task
    Resource: arn:aws:lambda:...:Compensate
    End: true
```

**Pros:** managed, integrated with AWS services.
**Cons:** AWS-only; pricier than Temporal at very high volume.

## Choice Matrix

| Volume | Latency | Stack | Recommendation |
|---|---|---|---|
| < 100/day | sub-second sync steps | Any | DB-state-machine |
| 100-1k/day | sub-second sync + some async | Any | DB-state-machine OR queue-driven |
| 1k-10k/day | mixed | AWS | Step Functions |
| 1k-10k/day | mixed | Any | Temporal |
| > 10k/day | mixed | Any | Temporal (purpose-built) |

## Compensation Patterns

Every step that has external side-effects needs a compensation:
- create_tenant → delete_tenant_row
- bootstrap_identity → delete_idp_user
- provision_infra → terraform_destroy
- create_stripe_customer → stripe_delete_customer
- seed_defaults → truncate_tenant_tables (only if still in pending state)
- send_welcome_email → (none — emails are non-compensatable)
- emit_ready_event → (none — terminal step)

Compensations run in **reverse order** of the steps that completed.

```python
def compensate(failed_step, completed_steps, tenant):
    for step in reversed(completed_steps):
        try:
            COMPENSATIONS[step](tenant)
        except Exception as e:
            # compensation failure logged but doesn't abort the rest
            log.error(f"compensation_failed step={step} tenant={tenant.id}", exc_info=e)
```

## Idempotency Pattern

Every external call carries an idempotency key derived from `(onboarding_run_id, step_name)`:

```python
stripe.Customer.create(
    email=signup.email,
    metadata={'tenant_id': tenant.id},
    idempotency_key=f"onboarding-{run.id}-stripe-customer",
)
```

Replaying the saga with the same run_id is safe — Stripe returns the same Customer for the same key.

## Observability

Each step emits:
```json
{
  "event": "onboarding.step.started",
  "correlation_id": "ob_2026_05_11_abc",
  "tenant_id": null,         // null on first step
  "step": "create_tenant",
  "attempt": 1,
  "timestamp": "..."
}
```

And:
```json
{
  "event": "onboarding.step.completed",
  "correlation_id": "ob_2026_05_11_abc",
  "tenant_id": 12345,
  "step": "create_tenant",
  "duration_ms": 423,
  "status": "ok",
  "timestamp": "..."
}
```

Dashboards: completion rate per step, latency per step, retry count per step.

## See Also

- `saas-tenant-onboarding-automation` — the umbrella skill.
- `distributed-systems-patterns` — saga theory + outbox + idempotency.
- `microservices-resilience` — circuit breakers complementary to retries.
