# Unity project architecture

Back to [Unity Mobile Game Development](../SKILL.md).

Use a bootstrap/composition root, bounded feature assemblies, additive frontend/persistent/location scenes, explicit input/platform/save abstractions, ScriptableObjects for authored definitions, plain C# for testable rules, stable persistent IDs and versioned save DTOs. Keep presentation components thin.

Scene transition sequence: request, suspend input, checkpoint, fade, unload, load dependencies/content asynchronously, bind, warm, activate, fade in, resume. Test repeated transitions and failure recovery.

Quarantine `SendMessage`, pervasive singletons, scene searches, string coroutines, general-purpose `Resources.Load`, mutable ScriptableObject saves and synchronous non-atomic persistence. Verify current Input System, Addressables, URP, IL2CPP, stripping and package APIs for the pinned editor.
