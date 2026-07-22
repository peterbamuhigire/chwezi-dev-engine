---
name: avalonia-desktop-development
description: Use when building or reviewing cross-platform .NET desktop apps with Avalonia UI, AXAML, MVVM, compiled bindings, virtualised lists, accessibility, headless tests, WebViews, or Windows and macOS packaging. Use csharp-dotnet-development for non-UI .NET architecture.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Avalonia Desktop Development
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Building or reviewing a cross-platform desktop app (Windows, macOS, Linux) with Avalonia UI 11+ on .NET 8/10.
- Writing AXAML/XAML views, MVVM view models, data bindings, styles/themes, or custom controls in Avalonia.
- Displaying large collections (hundreds to thousands of items) that need virtualization and lightweight item templates.
- Bundling image/icon assets, localizing (multi-language), adding accessibility, hosting a WebView, testing, or packaging an Avalonia app.
- Migrating WPF/UWP/.NET MAUI thinking to Avalonia, or modernizing older Avalonia code to current 11.x practice.

## Do Not Use When

- The work is web-only (React/Next/HTML), mobile-only native (Swift/Kotlin/Flutter), or pure backend/API with no Avalonia UI.
- It is generic .NET/C# work unrelated to the Avalonia view layer (use a general .NET guide instead).
- A WPF-specific skill is needed for a Windows-only WPF app that will not run cross-platform.

## Required Inputs

- Target platforms (Windows / macOS / Linux), Avalonia version (assume 11.x unless told otherwise), and .NET version.
- The feature: views/controls involved, data shape and collection sizes, theming needs, and any native integration (WebView, file dialogs, DB).
- Existing project layout and MVVM toolkit in use (CommunityToolkit.Mvvm vs ReactiveUI vs hand-rolled).

## Workflow

1. Confirm project layout: shared UI project + thin per-platform entry projects + a domain/core project with no Avalonia reference.
2. Build the UI in `.axaml`; keep logic in view models; keep domain logic in the core project so it is unit-testable.
3. Wire the root view + `DataContext` in `App.OnFrameworkInitializationCompleted`, branching on `IClassicDesktopStyleApplicationLifetime` vs `ISingleViewApplicationLifetime`.
4. Apply MVVM with `CommunityToolkit.Mvvm` (`[ObservableProperty]`, `[RelayCommand]`); reach for ReactiveUI only for genuinely reactive streams.
5. Turn on compiled bindings everywhere: `x:DataType` on every view/`DataTemplate`, `AvaloniaUseCompiledBindingsByDefault` on.
6. Style with selectors + `Classes`; re-skin controls with `ControlTheme`; theme with `FluentTheme` + `RequestedThemeVariant` for light/dark.
7. Virtualize large lists, run IO/PDF/DB work async off the UI thread, localize all strings, set automation names, then test headless and package.

## Quality Standards

- Keep Avalonia UI logic in views and view models; keep domain logic in a core project with no Avalonia dependency.
- Use compiled bindings, typed data templates, async commands, virtualization, localization, and accessibility names as default quality gates.
- Preserve responsive layouts across Windows, macOS, and Linux; avoid fixed sizes unless the control has a fixed-format reason.
- Package with explicit runtime identifiers, signing/notarization where required, and a documented smoke test for each target platform.

## Project Layout

- `Core/` — models, services, domain (no Avalonia dependency; fully unit-testable).
- `App/` — shared Avalonia UI: `Views/`, `ViewModels/`, `Assets/`, `Styles/`.
- `Desktop/` — entry point referencing `Avalonia.Desktop` (one project serves Windows + macOS + Linux).
- `Tests/` — view-model unit tests + `Avalonia.Headless` UI tests.
- Files use the **`.axaml`** extension. `App.axaml` holds app-level resources/styles; `Program.cs` configures the `AppBuilder`.
- Core packages: `Avalonia`, `Avalonia.Desktop`, `Avalonia.Themes.Fluent`, `Avalonia.Diagnostics` (dev), `CommunityToolkit.Mvvm`.

## Application Lifecycle

```csharp
public override void OnFrameworkInitializationCompleted()
{
    if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        desktop.MainWindow = new MainWindow { DataContext = _provider.GetRequiredService<ShellViewModel>() };
    else if (ApplicationLifetime is ISingleViewApplicationLifetime single)
        single.MainView = new MainView { DataContext = _provider.GetRequiredService<ShellViewModel>() };
    base.OnFrameworkInitializationCompleted();
}
```

Create the root `DataContext` here (ideally resolved from a DI container). Do not scatter view-model construction across code-behind.

## MVVM + Compiled Bindings

Prefer source-generated view models over hand-written `INotifyPropertyChanged`:

```csharp
public partial class LibraryViewModel : ObservableObject
{
    public ObservableCollection<BookViewModel> Books { get; } = new();
    [ObservableProperty] private BookViewModel? _selectedBook;

    [RelayCommand(CanExecute = nameof(CanOpen))]
    private async Task OpenAsync(BookViewModel book) => await _reader.OpenAsync(book.FilePath);
    private bool CanOpen(BookViewModel b) => b is not null;
}
```

Always declare `x:DataType` and bind type-safely:

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:vm="using:App.ViewModels"
             x:DataType="vm:LibraryViewModel">
    <ListBox ItemsSource="{Binding Books}" SelectedItem="{Binding SelectedBook}">
        <ListBox.ItemTemplate>
            <DataTemplate x:DataType="vm:BookViewModel">
                <TextBlock Text="{Binding Title}" />
            </DataTemplate>
        </ListBox.ItemTemplate>
    </ListBox>
</UserControl>
```

Compiled bindings fail the build on typos, run faster (no reflection), and are essential for large lists. Bind `Button.Command` to a `[RelayCommand]`; make commands async to keep the UI responsive. Use async commands + `Dispatcher.UIThread.Post` for any background → UI update.

- **CommunityToolkit.Mvvm** is the default. **ReactiveUI** (`ReactiveObject`, `RaiseAndSetIfChanged`, `ReactiveCommand`, `WhenAnyValue`) is for complex reactive pipelines (e.g. debounced live search).
- **Binding sources:** `{Binding #Other.Prop}` (element), `{Binding $parent[Window].DataContext.Cmd}`, `RelativeSource FindAncestor`, `$self`/`$parent`.
- **Converters:** `IValueConverter` for type mismatches; prefer `FuncValueConverter<TIn,TOut>` and built-in `BoolConverters`/`StringConverters`/`ObjectConverters`.

## Navigation (ViewModel-First)

Avalonia ships no navigation framework. Use a `ViewLocator : IDataTemplate` that maps `FooViewModel` → `FooView` by name, register it in `Application.DataTemplates`, and drive a `CurrentPage` view-model property bound to a host `ContentControl`/`SplitView`. Honour the `*ViewModel` → `*View` naming convention. Keep window/dialog code (`Show`, `ShowDialog(owner)`) behind an `IDialogService` so view models stay testable.

## Layout & Controls

- Panels: `Grid` (most versatile/performant; sizes `Auto`/`*`/absolute), `StackPanel` (use `Spacing`), `WrapPanel`, `DockPanel` (menus/toolbars/status bars), `Canvas` (absolute), `RelativePanel`, `ScrollViewer` (never wrap a `ListBox`/`DataGrid`, never nest).
- Controls are content-rich: `Button`/`SplitButton`, `TextBox` (`Watermark`), `AutoCompleteBox` (type-ahead search), `ComboBox`, `CheckBox`, `Slider`, `DatePicker`, `Menu`/`MenuItem` (`_` mnemonics, `InputGesture`), `Flyout`, `Expander`, `TabControl`, `ProgressBar`.
- Avoid fixed positions/sizes; arrange in panels so the UI adapts. Favour `Auto`/`*` sizing and `TextWrapping="Wrap"` so layouts flex for long localized text.

## Styling, Control Themes & Theming

Style with **selectors** (CSS-like), not WPF keyed styles. Use `Classes` and pseudo-classes (`:pointerover`, `:pressed`, `:focus`, `:disabled`, `:checked`):

```xml
<Style Selector="Button.primary">
    <Setter Property="Background" Value="{DynamicResource AccentBrush}" />
    <Setter Property="CornerRadius" Value="6" />
</Style>
<Style Selector="Button.primary:pointerover">
    <Setter Property="Background" Value="#1E5BD0" />
</Style>
```

Apply via `Classes="primary"` (no per-control reference needed). For full re-skins use **`ControlTheme`** (`TargetType`, nested `^` selectors, `ControlTemplate` + `ContentPresenter` + `{TemplateBinding}`) applied with `Theme="{StaticResource …}"`. Theme the app with `<FluentTheme />` and switch light/dark via `RequestedThemeVariant` (follow OS by default, offer an override). Organize resources/styles into `.axaml` dictionaries merged with `ResourceInclude`/`StyleInclude`; use `DynamicResource` for theme colours, `StaticResource` elsewhere.

> Modernize legacy code: `<FluentTheme Mode="…"/>` → `RequestedThemeVariant`; `Items="{Binding}"` → `ItemsSource="{Binding}"`. Both old forms are pre-Avalonia-11.

## Virtualization for Large Collections

For hundreds/thousands of items, virtualization is mandatory:

- `ListBox` virtualizes by default (`VirtualizingStackPanel`) — keep it; bind `ItemsSource` to `ObservableCollection<T>`.
- `ItemsControl` does **not** virtualize by default — set its `ItemsPanel` to `VirtualizingStackPanel`.
- `ItemsRepeater` virtualizes and supports custom layouts (`UniformGridLayout` for cover grids).

```xml
<ListBox ItemsSource="{Binding Books}">
  <ListBox.ItemsPanel><ItemsPanelTemplate><VirtualizingStackPanel/></ItemsPanelTemplate></ListBox.ItemsPanel>
</ListBox>
```

Keep item templates lightweight, load thumbnails lazily/async, and filter/group in the view model rather than rendering all rows. `DataGrid` (package `Avalonia.Controls.DataGrid`, add its Fluent theme include) suits tabular detail/admin views with explicit columns, not the main browse experience.

## Assets & Image Bundling

Place images under `Assets/`, set Build Action `AvaloniaResource` (the default glob already covers `Assets/**`), and reference with `avares://`:

```xml
<Image Source="avares://App/Assets/icons/shelf.png" Width="32" Height="32" Stretch="Uniform" />
```

`Stretch`: `Uniform` (default), `UniformToFill`, `Fill`, `None`. Load runtime images via `new Bitmap(...)`. Ship icons at the resolutions you use to limit bundle size; for monochrome/scalable iconography prefer vectors (`PathIcon`/`StreamGeometry`, or SVG via `Avalonia.Svg.Skia`); keep colourful raster icons as PNGs. Set `Window.Icon` for the app/window icon.

## Localization

- Use `.resx` resource files per culture (`Resources.resx`, `Resources.fr.resx`, …) with the generated strongly typed accessor.
- Set `CultureInfo.CurrentUICulture` at startup; offer an in-app language switch persisted to settings.
- Route all user-facing strings through keys via a culture-aware indexer/`ILocalizer` exposed on view models so switching language refreshes bindings without restart.
- Format dates/numbers with the current culture; design layouts to flex (German/French run ~30% longer than English).

## Accessibility

- Set `AutomationProperties.Name` (and `HelpText`/`LabeledBy`) on interactive and icon-only controls so Narrator/VoiceOver announce them.
- Ensure logical tab order, keyboard operability, access keys, and visible `:focus` styles.
- Meet WCAG AA contrast in both light and dark variants. Custom templated controls should expose an `AutomationPeer` when they add new interaction semantics.

## Hosting a WebView

Avalonia has no first-party WebView. Use a community control (`Avalonia.WebView`, `WebViewControl-Avalonia`) wrapping the OS engine (WebView2/Edge-Chromium on Windows, WKWebView on macOS). Bundle web assets as `AvaloniaResource` (`avares://`) or serve from localhost loopback. Bridge C# ↔ JS via host objects/message channels and `ExecuteScript`/`PostMessage`; marshal results to the UI thread. On Windows, ensure the WebView2 evergreen runtime is installed (bundle the bootstrapper in the installer); WKWebView ships with macOS. Provide a native fallback view in case the WebView fails to initialize.

## Custom Controls

- **User controls** aggregate existing controls; expose bindable state via styled properties (`AvaloniaProperty.Register<TOwner,T>`) and custom routed events (`RoutedEvent.Register<…>` with a `RoutingStrategies`). Prefer these for composite UI.
- **Templated controls** are lookless: redefine appearance via `ControlTheme`/`ControlTemplate` + `ContentPresenter` + `{TemplateBinding}`; never hard-code sizes/colours in a template. Use only for genuinely new reusable widgets.

## Graphics & Animation

Use Skia-backed shapes (`Rectangle`/`Ellipse`/`Path`), `Style.Animations` keyframes (`KeyFrame Cue="x%"`, `Duration`, `IterationCount`, `Easing`), `Transitions` per setter (`DoubleTransition`, `BrushTransition`, `ThicknessTransition`, `TransformOperationsTransition`), and render transforms. Prefer lightweight declarative transitions for hover/selection micro-interactions over per-frame C#.

## Performance

- Compiled bindings everywhere; virtualize large lists with minimal templates.
- Async + background threads for PDF/DB/IO; never block the UI thread; marshal UI updates with `Dispatcher.UIThread.Post`.
- Prefer `Grid` over deeply nested `StackPanel`s; cache/lazy-load and dispose `Bitmap`s; avoid `Opacity`/effects on large lists.
- Inspect with Avalonia DevTools (`Avalonia.Diagnostics`, F12 in debug).

## Testing

- View models are plain C# — unit-test them with no Avalonia dependency (the main reason to keep logic out of code-behind).
- Use `Avalonia.Headless` (+ `Avalonia.Headless.XUnit`, `[AvaloniaTest]`) to render and drive the real UI headlessly: simulate input, call `Dispatcher.UIThread.RunJobs()`, assert on control/view-model state.
- Mock services behind interfaces (DI) so tests avoid filesystem/DB/WebView.

## Packaging (Windows + macOS)

- `dotnet publish -c Release -r win-x64 | osx-arm64 | osx-x64`; prefer self-contained so users need no separate .NET; trim cautiously (compiled bindings help).
- **Windows:** MSIX or Velopack/Squirrel installer; bundle the WebView2 evergreen runtime; sign binaries.
- **macOS:** build a `.app` bundle, codesign + notarize (Gatekeeper), distribute a notarized `.dmg`; set bundle id, `.icns`, `Info.plist`/entitlements.
- Keep platform-specific assets (icons, manifests, entitlements) in the desktop project; share everything else.

## Anti-Patterns

- Hand-written `INotifyPropertyChanged` boilerplate instead of `[ObservableProperty]`.
- Reflection bindings / missing `x:DataType`, especially on hot/large lists.
- Wrapping `ListBox`/`DataGrid` in a `ScrollViewer`; nesting `ScrollViewer`s; non-virtualized big lists.
- WPF `Style TargetType` thinking — Avalonia uses selectors + `ControlTheme`.
- Hard-coded strings, fixed widths that clip translations, hard-coded template values.
- `<FluentTheme Mode="…"/>` and `Items="{Binding}"` (outdated pre-11 forms).
- Blocking the UI thread or touching UI objects off the UI thread; navigation/dialog code embedded in view models.

## Outputs

- Avalonia view (`.axaml`) + view model, styles/`ControlTheme`, or a review of existing Avalonia code against these standards.
- Concrete, prescriptive guidance ("do X, avoid Y") with build-safe compiled-binding and virtualization defaults.

## Inputs

| Artifact | Produced by | Required? | Why |
|---|---|---|---|
| Target platforms and user flows | Product or project brief | required | Defines controls, accessibility, and packaging constraints |
| Existing solution and UI conventions | Repository inspection | optional | Preserves architecture and styling decisions |

## Decision rules

| Condition | Choice | Failure avoided |
|---|---|---|
| Large or frequently updated collection | Use a virtualising control with compiled bindings | UI stalls and excess allocation |
| Shared logic has no UI dependency | Keep it in a view model or service | Platform coupling |
| Platform API is unavoidable | Isolate it behind an interface | Broken cross-platform builds |

## Capability contract

Read and search the solution first. Edit only when authorised; execute the narrowest build and headless tests available. Network access is optional for version-specific documentation.

## Degraded mode

If repository access or execution is unavailable, provide a file-level plan and mark build, binding, packaging, and accessibility checks as unverified.

- This skill is self-contained. Load project files, Avalonia documentation, or related .NET skills only when the task needs version-specific API details or broader C#/.NET architecture guidance.
<!-- dual-compat-end -->
## Read next
- `csharp-dotnet-development` for language/runtime depth and `world-class-engineering` for release evidence.
