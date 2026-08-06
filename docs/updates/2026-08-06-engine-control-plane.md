# Engine Control Plane Update — 2026-08-06

Added a shared ten-engine control-plane skill and registry covering agents,
commands, hooks, evidence, handoffs, and bounded recovery. Added deterministic
validation with optional local-router checks and a CI guard.

Verification: registry validation PASS; local ten-engine router validation PASS;
control-plane tests PASS.
