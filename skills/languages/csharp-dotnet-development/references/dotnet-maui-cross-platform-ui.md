# .NET MAUI Cross-Platform UI

Self-contained reference prepared from the supplied .NET MAUI book and current Microsoft documentation. Use for .NET MAUI apps targeting Android, iOS, Mac Catalyst, and Windows.

## Table Of Contents

- Fit and platform choice
- Project shape
- XAML and MVVM
- Platform services
- Performance and responsiveness
- Packaging
- Anti-patterns

## Fit And Platform Choice

Use .NET MAUI when one .NET codebase must deliver native app experiences across mobile and desktop targets. Do not choose it only because the backend is .NET; validate platform controls, device features, team skills, release channels, and UI complexity.

| Need | MAUI fit |
|---|---|
| Android/iOS app with shared business logic | Strong fit |
| Windows/macOS/Linux desktop app | Consider Avalonia for Linux; MAUI desktop is Windows/Mac Catalyst |
| Highly custom animations/game-like UI | Validate early with prototype |
| Existing native app with heavy platform code | Shared library + incremental screens may be safer |
| Offline field app | Strong fit if storage/sync is designed deliberately |

## Project Shape

```text
App.Maui/              XAML views, resources, platform adapters
App.Application/       use cases, validation, state orchestration
App.Domain/            entities, value objects, policies
App.Infrastructure/    API clients, local DB, auth, storage
App.Tests/             domain, application, view-model tests
```

Keep platform-specific code under `Platforms/` or behind interfaces. Keep view models independent of MAUI APIs where practical.

## XAML And MVVM

- Use XAML for layout and resources; keep code-behind to view-only glue.
- Use compiled bindings with `x:DataType` to catch binding errors at build time.
- Use `CommunityToolkit.Mvvm` for observable properties and commands.
- Use resource dictionaries for colours, typography, spacing, and styles.
- Treat visual states, loading, empty, error, offline, and permission-denied states as normal screens.
- Use global XML namespaces in .NET 10+ projects when it reduces boilerplate without making XAML ambiguous.

Command pattern:

```csharp
public partial class CheckoutViewModel : ObservableObject
{
    [ObservableProperty] private bool isBusy;

    [RelayCommand]
    private async Task SubmitAsync(CancellationToken cancellationToken)
    {
        if (IsBusy) return;
        IsBusy = true;
        try { await checkout.SubmitAsync(cancellationToken); }
        finally { IsBusy = false; }
    }
}
```

## Platform Services

- Permissions: request at point of need, explain consequence, handle denial and "do not ask again".
- Storage: keep secrets in secure storage; keep cache data separately; encrypt sensitive offline data when required.
- Camera/media/files: handle cancellation, large files, compression, orientation, and upload retry.
- Network: detect offline and degraded network; queue changes only when conflict handling exists.
- Push notifications: design token registration, user opt-in, topic scoping, and delivery fallbacks.

## Performance And Responsiveness

- Do not block the UI thread. Use async I/O and background work with progress/cancellation.
- Virtualize or page large lists; avoid complex templates in collection views.
- Cache images deliberately and dispose streams.
- Keep startup work small; defer non-critical initialization.
- Test on low-end Android devices and real iOS hardware, not only emulators.

## Packaging

- Android: signing config, version codes, permissions, Play policy, ABI choices, and crash reporting.
- iOS/Mac Catalyst: bundle identifiers, provisioning profiles, entitlements, Info.plist privacy strings, TestFlight/App Store flow.
- Windows: MSIX or other installer, app identity, signing, and update path.
- Keep app version, backend compatibility, and feature flags coordinated.

## Anti-Patterns

- Business rules in XAML code-behind.
- One giant `MainPage.xaml` that handles navigation, API calls, storage, and validation.
- Assuming UI looks right on every platform without per-platform visual checks.
- Requesting permissions on first launch without context.
- Treating offline support as a cache instead of a conflict-aware workflow.
- Ignoring app store privacy declarations and signing until release day.

## MAUI Done Checklist

- Core workflows tested on every target platform in scope.
- View models have unit tests without device dependencies.
- Permission, offline, loading, empty, error, and retry states exist.
- Build, signing, and store metadata are reproducible.
- Telemetry captures startup, screen navigation, crashes, API latency, and sync failures.
