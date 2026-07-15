# Godot architecture and migration

Back to [Godot Mobile Game Development](../SKILL.md).

Use scenes for reusable composition, Resources for typed authored data, signals for notification, explicit calls for command authority, and few autoloads for true process-lifetime services. Separate simulation from nodes when rules benefit from deterministic tests.

Treat Felicia (2021) as Godot 3 orientation. Translate `Spatial`, `KinematicBody`, `File.new`, `instance`, old `export/onready`, `NetworkedMultiplayerENet` and old TileMap/networking patterns through current migration documentation. Never promote its URL-parameter/PHP/raw-SQL example into production.
