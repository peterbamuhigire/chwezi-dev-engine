# Persistence, quest and narrative state

Back to [Gameplay Systems Architecture](../SKILL.md).

Persist versioned plain data with stable IDs, content/game version, slot, timestamp and migration chain. Write temp, validate, replace and retain backup. Test missing, corrupt, interrupted, incompatible, nearly-full-storage and clock-change cases.

Represent quests and dialogue as validated graphs with entry conditions, effects, terminal states, localisation keys and debug traversal. Keep the irreversible world-state mutation separate from presentation. Do not concatenate translated phrases. Preserve alternate narrative accounts rather than forcing disputed cultural history into one “truth” flag.
