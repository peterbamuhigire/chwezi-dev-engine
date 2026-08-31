# Algorithm Selection Matrix

This reference is a self-contained operational synthesis prepared from Aniket
Wattamwar, *Algorithms Every Programmer Should Know*, Manning Early Access
Program, version 1 (2026). It is organised by engineering decision rather than
by the source's chapter order. The MEAP status means examples and claims still
require local verification before production use.

## Selection notes

| Family | Useful question | Evidence to retain |
|---|---|---|
| Matching and assignment | Is the output a stable pairing or a minimum-cost allocation? | Preference/cost model, tie policy, feasibility and result validation |
| String search | Can input be rewound? Are there many patterns? Is text static and diverse? | Pattern corpus, collision checks, stream behaviour, alphabet distribution |
| Optimisation | Is an exact answer required, or is a bounded heuristic acceptable? | Objective function, constraint model, stopping rule, approximation risk |
| Graphs | Do we need all-pairs distances, maximum flow, cliques, or one path? | Graph size, edge semantics, negative-cycle policy, no-solution behaviour |
| Caching | Is workload governed by recency, frequency, or both? | Hit rate, eviction trace, memory overhead, workload replay |

## Review checklist

1. State the invariant that makes an output correct.
2. Name the largest expected input and the hostile input.
3. Separate asymptotic analysis from measurements on one machine.
4. Test empty input, duplicate values, repeated patterns, disconnected graphs,
   impossible assignments, capacity overflow, and no-path results as applicable.
5. Record whether a result is exact, approximate, probabilistic, or dependent on
   a heuristic assumption.
6. Keep a rollback path to the baseline or a simpler policy when the measured
   benefit disappears.
