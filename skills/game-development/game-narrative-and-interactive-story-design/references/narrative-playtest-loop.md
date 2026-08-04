<!-- Source basis: Digital Storytelling; Video Game Storytelling. Durable craft synthesis; historical platform examples are not current production guidance. -->

# Narrative and Gameplay Playtest Loop

Treat story as a system shared by design, engineering, art, audio, level,
localisation, QA, and production. A narrative document is not accepted merely
because the prose is coherent.

## Build the shared contract

For every mission, quest, or interactive sequence record:

| Field | Required decision |
|---|---|
| Player verbs | What the player can do and what the story assumes they will do |
| Dramatic objective | Conflict, stakes, opposition, escalation, and consequence |
| Choice structure | Critical path, optional branches, rejoin points, rewards, and failure recovery |
| Character intent | Want, belief, capability, change, and relationship state |
| Delivery channel | Dialogue, animation, environment, UI, audio, systemic event, or combination |
| Cross-discipline owner | Writer/narrative, design, engineering, art, audio, QA, and localisation handoff |
| Evidence | Comprehension, agency, pacing, emotional response, accessibility and defect signals |

## Iterate a playable slice

1. State a player hypothesis, such as “players understand the mission conflict
   before the first irreversible choice.”
2. Build the smallest representative slice with placeholders that preserve the
   final timing, camera, affordance, and delivery channel.
3. Test normal play, branch selection, branch rejoin, failure/retry, and a
   silent/audio-off or localisation-expansion case.
4. Observe what players do and say; separate comprehension, preference,
   balance, correctness, and emotional response.
5. Change one causal variable, rerun the slice, and preserve the failed evidence.
6. Standardise the successful contract in the game brief, requirement, content
   schema, test plan, and implementation checklist.

## Quality gates

- Player story and authored game story do not contradict the intended objective.
- Choices have legible consequences and do not strand progression.
- Character motivation is expressed through action or available interaction,
  not only exposition.
- Environment, AI, audio, and dialogue use the same intent and state names.
- Failed-path, accessibility, localisation, and placeholder evidence is retained.

The source books provide craft principles, not current engine APIs or a substitute
for user research, accessibility standards, or rights review.
