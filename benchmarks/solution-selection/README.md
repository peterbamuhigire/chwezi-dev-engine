# Solution-selection benchmark fixtures

`fixtures.json` is the original 16-case specification from the Kaizen protocol:
12 representative engineering cases plus four counterexamples. It covers
reuse, native controls, mature dependencies, new features, cross-component
bugs, refactoring, API validation, authentication/authorisation,
accessibility, migrations, asynchronous retry, money invariants, and cases
where native controls, compact code, or fewer dependencies are unsafe.

Validate the specification without invoking a model:

```powershell
python tools/validate_benchmark_fixtures.py
```

The fixtures remain `NOT_ASSESSED` until equivalent starting commits, public
and withheld tests, independent reference solutions, runtime manifests and
blinded reviewers are materialised. The validator deliberately does not turn a
written specification into execution evidence.
