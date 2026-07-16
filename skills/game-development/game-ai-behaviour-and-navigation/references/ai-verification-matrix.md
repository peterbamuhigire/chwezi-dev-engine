# AI Verification Matrix

| Risk | Scenario | Oracle | Evidence |
|---|---|---|---|
| Invalid transition | Exhaust state/event table | Only declared transitions occur; every bounded action terminates | Trace + test |
| Perception omniscience | Occlusion/range/affiliation/forgetting cases | Knowledge changes only through specified stimuli/memory | Perception log |
| Stuck agent | Blocked, partial and changing paths | Recovery ladder completes within project threshold | Path trace/video |
| Oscillation | Competing equal-priority goals | Hysteresis/cooldown prevents rapid flip above threshold | Decision trace |
| Reservation leak | Death/unload/cancel/disconnect during use | Capacity returns and no orphan owner remains | Reservation log |
| Animation deadlock | Missing/interrupted event | Timeout/fallback returns agent to valid state | Event trace |
| Save/load mismatch | Save in each critical state | Restored state is valid or deliberately normalised | State diff |
| Network divergence | Authority/latency/loss scenarios | Authoritative outcome and presentation meet project rule | Network capture |
| Budget breach | Maximum simultaneous agents in worst geometry | CPU/memory/query budgets and frame-time percentile pass | Profiler capture |
| Unfair behaviour | Blind tests across difficulty variants | Knowledge, reaction and telegraph rules match design | Playtest report |

Projects must provide thresholds, target hardware, build identifiers, seeds and retention locations. A screenshot of a working NPC is not sufficient evidence.
