# Resource vitality and carrying capacity systems

Back to [Gameplay Systems Architecture](../SKILL.md).

Use this reference when a living, civic, ecological, faction, settlement or herd system has one or more health indexes that change under resource pressure, player priorities and environmental shocks.

## System contract

Define the promise in player-visible terms before tuning numbers. A vitality system should make pressure readable, tradeoffs meaningful and recovery possible without hiding the rule that caused the change.

Model the system as plain authoritative state plus explicit inputs:

| Element | Examples | Rule |
|---|---|---|
| Primary health indexes | sacred animal health, herd health, settlement morale, crop health | Keep them separate when the player can protect one at the expense of another. |
| Population or stock | herd size, citizens, crop plots, soldiers | Never let growth ignore carrying capacity. |
| Support resources | water, forage, soil, shelter, medicine, labour | Convert each to named units before combining. |
| Stressors | drought, distance from water, disease, raid, fire, flood | Store as pressure values that rise and decay visibly. |
| Player priority | balanced care, protect leader, grow population, conserve resources | Encode as a command or mode with explicit multipliers. |

## Carrying capacity

Compute carrying capacity from current conditions, not from a fixed designer constant. A practical first model is:

```text
capacity = base + resource_value
capacity *= water_factor
capacity *= catastrophe_factor
capacity *= shelter_or_resilience_factor
```

Use overcapacity pressure when `stock > capacity`. Apply that pressure to health, growth and leader strain rather than instantly deleting stock unless the fiction demands a discrete event.

## Resource conversion

Prefer explicit conversion constants over hidden balancing math.

| Resource pattern | Implementation rule | Player-facing consequence |
|---|---|---|
| Natural renewable resource | Regenerates or remains stable under normal use | Reliable baseline, lower yield. |
| Cultivated or improved resource | Higher yield than natural equivalent | Creates management pressure elsewhere. |
| Depleting resource | Productivity falls with repeated extraction or farming | Rewards rotation, rest, irrigation or investment. |
| Strategic non-food resource | Stored separately from immediate vitality math | Enables future crafting, trade, defence or ritual systems. |

When a cultivated land tile is worth more than a natural tile, state the multiplier in code and documentation. If some resources are exempt from depletion, encode that exception directly so future tuning does not erase the design intent.

## Player priorities

Priority modes should move cost between indexes, not simply make the system better.

| Priority | Typical effect | Anti-cheese check |
|---|---|---|
| Balance | Moderate drain and recovery across all indexes | Should not dominate every context. |
| Protect leader or sacred asset | Reduces leader drain | Stock, morale or output must pay a visible cost. |
| Grow stock or population | Improves short-term growth | Leader, soil, water or resilience must take extra pressure. |
| Disaster response | Reduces catastrophe decay time or impact | Costs labour, route choice, stores or opportunity. |

## Simulation rules

- Use bounded `deltaTime` or fixed-step updates for rule state.
- Clamp indexes to named ranges and expose derived pressure values for debug HUDs.
- Keep presentation separate from simulation state; UI should read the state, not own it.
- Make shocks impulses and pressures rather than one-frame hidden penalties.
- Test normal, overcapacity, resource-starved, recovery and priority-switch cases.

## Anti-patterns

- One combined "health" value for systems with real tradeoffs. Fix: split indexes and show the exchange rate.
- Fixed capacity that ignores current resources. Fix: recompute capacity from live support conditions.
- Depletion hidden in narrative text only. Fix: store productivity and reduce it in simulation.
- Player priority that is always optimal. Fix: attach a visible cost to every mode.
- Strategic resources stuffed into immediate food math. Fix: maintain a ledger until a system consumes them.
