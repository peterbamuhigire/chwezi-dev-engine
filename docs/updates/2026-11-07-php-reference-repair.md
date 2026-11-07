# PHP deployment reference repair

Date: 2026-11-07. Kaizen action: D1.1.

The PHP modern standards skill pointed at a deployment reference under the
languages directory, where no such file exists. Its pointer now resolves to
the existing `devops-cloud/deployment-release-engineering` reference. No
reference content was copied or changed.

Validation: the old resolved target was absent; the new target exists and
contains the PHP deployment guidance. The skill's `quick_validate.py` check
passes. The catalogue guard reports zero errors and sixteen report-only size
warnings; the control-plane registry check reports zero findings. These
checks do not establish that a PHP application has been deployed.

An independent review confirmed the one-line skill diff and target identity.
Recovery is to restore that line from the preceding revision; doing so also
restores the broken pointer.

## Game release failure branches (D1.2)

The compliance review dispositioned all thirty scanner exceptions rather than
adding boilerplate to satisfy markers. One concrete gap was repaired:
`game-build-release-engineering` now explicitly stops promotion when required
toolchains, signing credentials or authority are missing, and requires channel
state reconciliation after an uncertain upload. It preserves unsigned test
artefacts as non-releasable and prohibits borrowing a personal signing identity.

The skill validator passes. Independent scenario review covered unavailable
SDK, revoked identity, rebuild-after-approval and unknown upload state. This
was instruction-level review, not a game build, store upload or signing test.
The post-change scanner still flags degraded mode because its lexical pattern
does not recognise the table's conditional wording; that is retained as a
scanner limitation, not removed by padding the skill.
