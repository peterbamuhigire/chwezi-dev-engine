# Source Study Notes

This reference records the source synthesis used for `csharp-dotnet-development`. It is self-contained; future agents do not need access to the original files.

## Source Material Used

Local markdown sources supplied by the user under `Downloads/Documents/docs_markdown`:

- `.NET MAUI Projects: A guide to building applications for Windows, macOS, Android, and iOS` (2025).
- `C# 14 and .NET 10 - Modern Cross-Platform Development Fundamentals, Tenth Edition`.
- `Core C# and .NET Quick Reference`.
- `C# 12 for Cloud, Web, and Desktop Applications`.
- `Learning C# Through Small Projects` (2024).
- `Microsoft Visual C#: Introduction to Object Oriented Programming`.
- `Parallel Programming with C# and .NET`.
- `Artificial Intelligence for .NET` was present but contained only a title in the available markdown.

Current Microsoft documentation was also checked for .NET 10, C# 14, ASP.NET Core 10, EF Core 10, .NET MAUI 10, and Semantic Kernel so version-sensitive guidance did not rely only on book text.

## Distillation Rules Applied

- No long passages were copied from the books.
- Repeated introductory syntax material was converted into operational checklists and review rules.
- Beginner examples were generalized into production defaults: project boundaries, validation, async, testing, packaging, and observability.
- Version-specific material was kept in references where it can be revised later without changing routing.
- Broad platform topics were split by practical use: language/runtime, APIs/services, EF Core, MAUI, concurrency, operations, and AI.

## Useful Routing Map

| User task | Load |
|---|---|
| "Modernize this C# codebase" | `csharp-language-and-runtime.md`, then `testing-packaging-and-operations.md` |
| "Build an ASP.NET Core API" | `aspnet-core-and-services.md`, `ef-core-data-access.md` if persistence exists |
| "Fix EF performance" | `ef-core-data-access.md` |
| "Build a .NET MAUI mobile app" | `dotnet-maui-cross-platform-ui.md` |
| "Make this async code safe" | `concurrency-and-parallelism.md` |
| "Package and deploy this service" | `testing-packaging-and-operations.md` |
| "Add AI to a .NET app" | `ai-in-dotnet.md` plus the repository AI skill relevant to the architecture |

## Maintenance Notes

- Keep this as the only source-map file. Do not add book summaries by chapter unless a future task needs a specific missing topic.
- Re-check Microsoft docs before changing guidance about current LTS, C# version, EF Core release behavior, MAUI platform support, or Semantic Kernel APIs.
- If a focused skill is later created for ASP.NET Core, EF Core, MAUI, or .NET AI, move only that topic's routing-heavy material into the new skill and leave this skill as the general parent.
