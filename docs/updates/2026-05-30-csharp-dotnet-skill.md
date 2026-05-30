# 2026-05-30 C#/.NET Skill Addition

## Summary

Added `skills/languages/csharp-dotnet-development` as the general active
entrypoint for C# and .NET work. The skill distills the supplied markdown books
into self-contained references for:

- C# language and runtime choices.
- ASP.NET Core and service hosting.
- EF Core data access.
- .NET MAUI cross-platform UI.
- Concurrency and parallelism.
- Testing, packaging, and operations.
- AI integration in .NET.

## Validation

- `python -X utf8 skills\sdlc-meta\skill-writing\scripts\quick_validate.py skills\languages\csharp-dotnet-development`
- `python -X utf8 scripts\skill_catalog_guardrails.py --report-only`

## Related Fix

Normalized `C:\Users\Peter\.agents\skills\skills\finance\finance-module-audit\SKILL.md`
to UTF-8 without BOM so strict skill loaders recognise the opening YAML
frontmatter delimiter.
