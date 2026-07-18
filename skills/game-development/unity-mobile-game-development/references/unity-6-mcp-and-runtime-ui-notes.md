# Unity 6 MCP and runtime UI notes

Use this reference when a Unity 6 project needs AI-client control through Unity MCP, runtime-generated UGUI, or fast greybox/editor automation.

## Unity MCP setup

- Verify current Unity documentation for the installed editor and AI Assistant package before pinning versions.
- Unity MCP requires Unity 6 or later and the `com.unity.ai.assistant` package.
- Add the package through Unity Package Manager or `Packages/manifest.json`, then let Unity resolve packages in the editor.
- After package resolution, confirm the bridge in `Edit > Project Settings > AI > Unity MCP Server` or `Edit > Project Settings > AI > Unity MCP`, depending on package version.
- The Windows relay binary should appear at `%USERPROFILE%\.unity\relay\relay_win.exe`; external MCP clients must launch it with `--mcp`.
- Direct external clients require user approval in Unity's MCP settings before tools can run.
- If the relay is missing, fix compile errors first, restart Unity, and verify the package directory exists under `Packages/com.unity.ai.assistant`.

## Runtime UGUI on Unity 6

- `Resources.GetBuiltinResource<Font>("Arial.ttf")` is invalid in Unity 6.5 and throws at runtime.
- Use `Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf")` for quick generated UGUI text, or use a committed font asset for production UI.
- Treat runtime-generated UGUI as prototype scaffolding. Production UI should move to prefabs, UI Toolkit, TextMeshPro, or a documented project UI standard.

## Greybox editor automation

- For fast scene spikes, a runtime bootstrap can inject temporary player, camera, HUD, and objective objects without repeatedly mutating scene YAML.
- Keep the bootstrap scene-gated by a stable root object name so it does not run in unrelated scenes.
- Document the evidence boundary: playable greybox proof is not device performance, cultural review, art approval, live player validation, or release readiness.
