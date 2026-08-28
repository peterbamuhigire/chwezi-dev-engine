# Uganda EFRIS Offline and Device Deployment

The supplied offline/enabler documents describe an intermediary local service
that can receive ERP transactions while disconnected and upload them when the
authority connection returns. Public URA guidance also describes bounded offline
operation. The exact permitted period, values, volume, platform, ports, and
manual upload procedure are currentness gates.

## Deployment controls

- Separate online, authority-approved offline, manual exception, and disabled
  configurations.
- Bind device number, certificate/thumbprint, branch, software version, and
  taxpayer profile; audit activation/deactivation and replacement.
- Keep local queue encrypted and durable, with a clock check, bounded age,
  storage limits, upload receipt, retry history, and operator escalation.
- Do not place private keys or authority credentials in Android APKs, browser
  bundles, logs, or client-managed configuration.
- For multi-tenant systems, isolate offline stores/enablers per approved fiscal
  identity; never use a global local queue keyed only by invoice ID.

## Failure policy

An unknown response is reconciled by exchange ID/idempotency key before retry.
Expired offline items become manual-review exceptions. A manual document is
never silently converted into a fiscalised one; it must retain reason, actor,
number, source hash, upload attempt, and reviewer disposition.

The installation guide's runtime/port/hardware values are deployment notes,
not permanent requirements. Test the authority-approved package on the actual
BIRDC host and archive the installation evidence.
