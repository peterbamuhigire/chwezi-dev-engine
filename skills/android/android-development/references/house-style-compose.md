# Chwezi Business-App House Style in Jetpack Compose

Parent skill: [`android-development`](../SKILL.md). Sibling: [`ui-design-system.md`](ui-design-system.md)
(generic Material 3 tokens; this file supersedes its sample colour values for Chwezi apps).

The canonical standard is owned by the design engine, not this file:

- `chwezi-design-engine` -> `skills/09-design-systems-tokens-and-theming/chwezi-business-app-house-style/SKILL.md`
  (roles, tokens, components, motion, guardrails).
- `chwezi-design-engine` -> `skills/12-data-viz-and-dashboards/money-figures-and-statement-display/SKILL.md`
  (compact amounts, hero figures, statement and summary layouts).
- Audit record: `chwezi-design-engine` -> `docs/kaizen/2026-11-app-house-style/README.md`
  (kept patterns K1-K19, rejected R1-R11, probation P1-P2).

This file covers how to build that standard in Kotlin, Jetpack Compose and Material 3. When this
file and the design skill disagree, the design skill wins; fix this file.

Reference implementation: the Maduuka Android app (November 2026). Other apps swap the brand
primary and its derived containers; every role, rule and guardrail stays.

## 1. Set up the colour roles

Put every colour in one theme package (for example `presentation/common/theme/`). Nothing outside
that package may write a colour literal (guardrail G1).

### Light roles (reference values)

| Material 3 role | Value | Use |
|---|---|---|
| `primary` / `onPrimary` | `#1A6DB3` / `#FFFFFF` | Filled buttons, selected nav pill, links (5.41:1) |
| `primaryContainer` / `onPrimaryContainer` | `#D6E8FA` / `#0B3566` | Selected chips, info bands (9.78:1) |
| `background` | `#E8F1FC` | Page ground: pale brand tint (K1) |
| `surface` | `#F9FCFF` | Sheets, bars |
| `surfaceContainerLowest` | `#FFFFFF` | Cards |
| `onBackground` / `onSurface` | `#1D273B` | Ink (13.1:1 on ground, 14.9:1 on white) |
| `onSurfaceVariant` | `#565E6C` | Muted labels (6.54:1 on white, 5.73:1 on ground) |
| `outlineVariant` | `#C3D0E1` | 1 dp hairline (decorative, 1.56:1; never the only cue) |
| `error` / `onError` | `#B42323` / `#FFFFFF` | Errors, destructive outlines (6.55:1) |
| `tertiary` / `onTertiary` | `#F8B020` / `#1B2430` | The ONE accent next step (8.36:1) (K2) |
| `tertiaryContainer` / `onTertiaryContainer` | `#FFE9B8` / `#3D2A00` | Highlight tile, first rank badge (11.51:1) |

Money-up green `#2E7D32` (5.13:1 on white) is not a Material role. Hold it, and any other
semantic tone, in a small `@Immutable` class exposed through a `CompositionLocal`
(for example `HouseTheme.money.up`).

Rule R7: never draw `primary` (4.32:1) or money green (4.10:1) text on `primaryContainer`. On a
container, text uses `onPrimaryContainer`; money colours are for surfaces only.

### Dark roles

Reference values: background `#161C24`, surface `#1E2631`, primary `#8DBBF2`. Derive the rest by
role and measure each pair. Example pairs computed for this file on 2026-11-07: `#0B3566` on
`#8DBBF2` 6.13:1; ink `#E6EDF5` on `#1E2631` 12.93:1; muted `#A9B3C1` on `#1E2631` 7.19:1; the
amber accent with `#1B2430` text keeps 8.36:1 in both themes. These dark ink and muted values are
illustrative; the Maduuka dark roles beyond the three above are `NOT_ASSESSED` here.

```kotlin
private val Light = lightColorScheme(
    primary = BrandBlue, onPrimary = White,
    primaryContainer = BlueContainer, onPrimaryContainer = BlueInk,
    background = PageGround, surface = SoftSurface, surfaceContainerLowest = White,
    onBackground = Ink, onSurface = Ink, onSurfaceVariant = Muted,
    outlineVariant = Hairline, error = Danger, tertiary = Amber, onTertiary = AmberInk,
    tertiaryContainer = WarmContainer, onTertiaryContainer = WarmInk,
)
```

Do not turn on dynamic colour for a house-style app: wallpaper colours would replace the brand
roles and break the measured pairs. Light is the default theme; offer System, Light and Dark in
settings.

## 2. Set up type with bundled fonts

- Body and labels: Atkinson Hyperlegible. Headings and money: Public Sans. Bundle static subsets
  in `res/font` (keep the OFL licence files in the repo). Do not use downloadable fonts for money:
  a missing font changes figure widths. Banned primary faces (Inter, Roboto and the rest of the
  design engine's list) stay banned even as fallbacks you rely on.
- Floor: 12 sp for every role. No literal `fontSize` outside the theme (guardrail G7).
- Money uses tabular figures so columns align and count-ups do not jitter:

```kotlin
@Immutable
data class AmountStyles(val large: TextStyle, val medium: TextStyle, val small: TextStyle, val compact: TextStyle)

private fun money(size: Int, weight: FontWeight) = TextStyle(
    fontFamily = PublicSans, fontWeight = weight, fontSize = size.sp,
    fontFeatureSettings = "tnum", // tabular figures
)
val HouseAmounts = AmountStyles(
    large = money(32, FontWeight.SemiBold), medium = money(22, FontWeight.SemiBold),
    small = money(16, FontWeight.Medium), compact = money(12, FontWeight.Medium),
)
```

Expose the styles through a `CompositionLocal` (for example `HouseTheme.amounts.compact`). Rule R6:
amounts inside sentences also use the figure face (an `AnnotatedString` span), so one zero shape
appears on a screen.

## 3. Set up spacing, shapes and targets

```kotlin
object Space { val xxs = 2.dp; val xs = 4.dp; val s = 8.dp; val m = 12.dp
    val l = 16.dp; val xl = 24.dp; val xxl = 32.dp; val xxxl = 48.dp }
object Radii { val s = 8.dp; val m = 12.dp; val l = 16.dp; val card = 20.dp; val xl = 28.dp }
val MinTarget = 48.dp
```

Map `Radii` into `MaterialTheme.shapes` once. Every tappable thing is at least 48 dp; use
`Modifier.minimumInteractiveComponentSize()` on custom controls. Off-grid `dp` literals and inline
`RoundedCornerShape(n.dp)` outside the theme are ratcheted (guardrails G3, G4).

## 4. Format money once

Write one formatter object and use it everywhere (guardrail G6).

| Use | Function | Output |
|---|---|---|
| Tiles, rows, summaries | `compact(value)` | `950`, `1.20K`, `79.43M`, `888.88B` |
| Documents, closing balances, inputs | `full(value)` | `32,450,000.00` |
| Screen readers, always | `full(value)` | set as `contentDescription` |

Compact rules: below 1,000 show the whole number; otherwise K, M or B with exactly two decimals.
Round first, then pick the unit, so `999,995` becomes `1.00M`, never `1000.00K`. Use `BigDecimal`
with `RoundingMode.HALF_UP`; never `String.format("%.2f")` on money, never a currency symbol.

```kotlin
fun compact(v: BigDecimal): String {
    val a = v.abs()
    if (a.setScale(0, HALF_UP) < THOUSAND) return v.setScale(0, HALF_UP).toPlainString()
    val units = listOf(THOUSAND to "K", MILLION to "M", BILLION to "B")
    var i = units.indexOfLast { a >= it.first }
    var scaled = a.divide(units[i].first).setScale(2, HALF_UP)
    if (scaled >= THOUSAND && i < units.lastIndex) { i++; scaled = a.divide(units[i].first).setScale(2, HALF_UP) }
    return (if (v.signum() < 0) "-" else "") + scaled.toPlainString() + units[i].second
}
```

Percentages (R2): never show `0%` for a non-zero value; show "less than 1%".

## 5. Build the components

Each component is one file in the shared components package. Callers never restyle them.

### 5.1 Hub menu card (K3)

Whole card tappable, `heightIn(min = 88.dp)`, 16 dp padding, `surfaceContainerLowest`,
`BorderStroke(1.dp, outlineVariant)`, 0 elevation, `Radii.card`. A 44 dp illustrated icon drawn as
it is, a semibold title, a muted description up to 3 lines, a chevron.

```kotlin
@Composable
fun MenuCard(title: String, body: String, @DrawableRes icon: Int, onClick: () -> Unit) {
    Card(onClick = onClick, shape = MaterialTheme.shapes.extraLarge,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
        colors = CardDefaults.cardColors(MaterialTheme.colorScheme.surfaceContainerLowest),
        modifier = Modifier.fillMaxWidth().heightIn(min = 88.dp)) {
        Row(Modifier.padding(Space.l), verticalAlignment = Alignment.CenterVertically) {
            Image(painterResource(icon), contentDescription = null, Modifier.size(44.dp)) // untinted, no disc (R10)
            Column(Modifier.weight(1f).padding(horizontal = Space.m)) {
                Text(title, style = MaterialTheme.typography.titleMedium)
                Text(body, maxLines = 3, overflow = TextOverflow.Ellipsis,
                    color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null)
        }
    }
}
```

Use `Image`, not `Icon`: `Icon` tints by default and would flatten a multicolour drawing. Every
illustrated icon needs a recorded source and licence before release (R11).

### 5.2 KPI tile with change chip (K4)

Small tinted line icon, label, a large compact figure, and a change chip that carries an arrow, a
word and a colour together ("Up 12%", "Down 3%"). Colour is never the only cue. The tile's
`contentDescription` reads the full amount and the change in words. Merge semantics with
`Modifier.semantics(mergeDescendants = true)`.

### 5.3 Hero summary card with softened decimals (K5)

Soft vertical gradient from the theme (named brushes, not literals), the period range only (R1:
the period name appears once on the page, in the top bar or navigator), a label, one large figure
and three mini tiles. Soften the decimals and unit with an `AnnotatedString`:

```kotlin
fun softAmount(text: String, soft: Color): AnnotatedString = buildAnnotatedString {
    val cut = text.indexOfFirst { it == '.' }.let { if (it < 0) text.length else it }
    append(text.substring(0, cut))
    withStyle(SpanStyle(color = soft, fontSize = 0.6.em)) { append(text.substring(cut)) }
}
// Text(softAmount(compact(total), muted), style = amounts.large,
//      modifier = Modifier.semantics { contentDescription = "Came in " + full(total) })
```

Pair it with the money-in-plain-words row (K6): "Came in", "Went out", "Profit", and a bar captioned
"You kept N% of what came in".

### 5.4 Top three with rank badge (K8)

Three rows: a round rank badge (first on `tertiaryContainer`, second and third neutral), the name on
the left with `weight(1f)` and ellipsis, the compact amount on the right in `amounts.compact`. One
highlight tile per page (K7) uses the warm container for the single best item.

### 5.5 Period navigator (K9)

`Row` of previous `IconButton`, a pill (`Surface` with `Radii.xl`) holding a calendar glyph, the
period name and a dropdown arrow that opens a month sheet or day picker, and a next `IconButton`
disabled at the latest period. Each icon button has a content description naming the target
("Previous month, October 2026"). Dates read "6 Nov 2026" or "Fri 6 Nov", one format per app (R4).

### 5.6 Accent button (K2, K13)

```kotlin
@Composable
fun AccentButton(text: String, onClick: () -> Unit, modifier: Modifier = Modifier) =
    Button(onClick, modifier.heightIn(min = MinTarget), colors = ButtonDefaults.buttonColors(
        containerColor = MaterialTheme.colorScheme.tertiary,
        contentColor = MaterialTheme.colorScheme.onTertiary)) { Text(text) }
```

At most one per screen part (guardrail G2). Other main actions use the filled primary button;
destructive exits use an outlined button in `error`; top bars use text buttons.

### 5.7 Statement row (K10)

Date and type on the left; on the right, stacked and each labelled: "Due", "Paid", "Balance",
all in `amounts.compact`. The closing balance under the list stays in `full()`. Ten rows per page
with a pagination bar. The row's `contentDescription` reads every amount in full.

Trial balance (K11) is a list of collapsible group cards with group debit and credit totals in the
header, muted account codes, and a pinned closing footer; not a wide table.

### 5.8 Context strip and insight line (K14, K18)

Hub and report pages show a date chip, a Switch action and the place name centred. One insight
sentence with a lightbulb and an action link turns a figure into the next step. No run ids, raw
statuses or doubled labels on screen (R3, guardrail G5).

## 6. Add motion with a reduced-motion gate (K15)

Motion plays once per visit and stops entirely when the system or the app asks for reduced motion.

```kotlin
@Composable
fun rememberMotionAllowed(appReducedMotion: Boolean): Boolean {
    val ctx = LocalContext.current
    return remember(appReducedMotion) {
        val scale = Settings.Global.getFloat(ctx.contentResolver,
            Settings.Global.ANIMATOR_DURATION_SCALE, 1f)
        !appReducedMotion && scale > 0f
    }
}
```

On API 26+ `ValueAnimator.areAnimatorsEnabled()` also reports battery-saver disablement; use it
when `minSdk` allows.

| Helper | Values | Notes |
|---|---|---|
| `Modifier.staggerReveal(index, allowed)` | 70 ms stagger, max 8 items, 420 ms, 24 dp rise with fade | Items past the eighth appear with the eighth |
| `CountUpText(target, allowed)` | 900 ms, once | Formats every frame with `compact()`; semantics carry the final full amount from the first frame |
| `growBars(allowed)` | 700 ms after 250 ms | Bars start at final height when not allowed |

"Once per visit" means the played flag is held in `rememberSaveable` keyed by the screen, so
recomposition, scrolling and returning from a sheet do not replay it. When not allowed, render the
final state directly. No `rememberInfiniteTransition` outside a reduced-motion check (guardrail G8).

## 7. Hold the style with guardrail tests (K19)

Guardrails are plain JUnit tests in `src/test` that read Kotlin sources as text. They run in the
normal unit suite, so they are release gates. Each ratchet constant may only go down: when a change
removes violations, lower the constant in the same commit.

```kotlin
object SourceScan {
    val root = File("src/main/java")
    fun files(filter: (File) -> Boolean = { true }) =
        root.walkTopDown().filter { it.extension == "kt" && filter(it) }.toList()
    fun count(regex: Regex, filter: (File) -> Boolean = { true }) =
        files(filter).sumOf { f -> regex.findAll(f.readText()).count() }
}

class DesignGuardrailsTest {
    @Test fun `no raw colour literals outside theme`() {
        val n = SourceScan.count(Regex("""Color\(0x[0-9A-Fa-f]{6,8}\)""")) { "/theme/" !in it.path }
        assertTrue(n <= RAW_COLOUR_BASELINE, "raw colours $n > $RAW_COLOUR_BASELINE")
    }
    companion object { const val RAW_COLOUR_BASELINE = 0 }
}
```

| # | Guard | Rule | Baseline |
|---|---|---|---|
| G1 | Raw colour | No `Color(0x...)` or `Color.Red`-style literal outside the theme package | 0 |
| G2 | One accent | Per composable function body, at most one `AccentButton(` | hard rule |
| G3 | Off-grid spacing | `n.dp` in `padding`/`Arrangement.spacedBy`/`Spacer` where n is not in the scale | ratchet |
| G4 | Shape literals | `RoundedCornerShape(` outside the theme | ratchet |
| G5 | Raw identifiers | `Text(` fed by `.id`, `runId`, `.status` wire values or `"#$id"` | ratchet |
| G6 | Formatter | No `String.format`/`"%.2f"` on money, no currency symbols, `compact()` banned in table and statement files except listed exceptions | 0 plus allow-list |
| G7 | Typography | No literal `fontSize =` outside the theme; every role at least 12 sp | 0 |
| G8 | Reduced motion | `rememberInfiniteTransition` only in files that call `rememberMotionAllowed` | 0 |
| G9 | Contrast tokens | Recompute WCAG ratios from the theme constants for every declared pair | all pass |

Write G2 by splitting each file on `@Composable` and counting per chunk; it is a heuristic, so name
any reasoned exception in an allow-list with a comment. Write G9 as a real computation, not a
copied table:

```kotlin
private fun lum(c: Color) = listOf(c.red, c.green, c.blue).map {
    if (it <= 0.04045f) it / 12.92 else Math.pow((it + 0.055) / 1.055, 2.4) }
    .let { 0.2126 * it[0] + 0.7152 * it[1] + 0.0722 * it[2] }
fun ratio(a: Color, b: Color) = (maxOf(lum(a), lum(b)) + 0.05) / (minOf(lum(a), lum(b)) + 0.05)

@Test fun `text pairs meet 4_5`() = TEXT_PAIRS.forEach { (fg, bg, name) ->
    assertTrue(ratio(fg, bg) >= 4.5, "$name ${ratio(fg, bg)}") }
```

Declare pairs for: ink and muted on ground, surface and card; `onPrimary` on `primary`;
`onPrimaryContainer` on `primaryContainer`; `onTertiary` on `tertiary`; `onTertiaryContainer` on
`tertiaryContainer`; money up and error on card; and the same set in dark. Use 3:1 only for large
text and non-text indicators (selected pill, focus ring, chart marks).

Source scans miss composition at runtime. Add a few Compose UI tests for font scale 2.0 and a
48 dp target check on the hub and statement screens.

## 8. Adopt in an existing app

1. Add the theme package (roles, amounts, `Space`, `Radii`, money formatter) and G9 first.
2. Add G1 to G8 with baselines set to today's counts; commit; the ratchet only falls from here.
3. Replace private copies of cards, KPI tiles and buttons with the shared components, lowering
   baselines as each screen moves.
4. Record per screen: font scale 2.0, dark theme, TalkBack reading of amounts, reduced motion on.
   Device checks not run are `NOT_ASSESSED`, never a pass.

## 9. Anti-patterns

- Primary or green text on the pale blue container (R7).
- Two accent buttons on one screen; an accent for a destructive action.
- `Icon()` for an illustrated drawing, or any icon on a tinted disc (R10).
- Period name repeated in the bar, navigator and hero (R1).
- `1000.00K`, `0%` beside a non-zero figure, a currency symbol, or a compact figure read aloud.
- Alternating grey bands that look like selection (R5); a house-shaped placeholder instead of
  initials on a category tint (R9).
- More than eight illustration hues in the theme (R8).

## Evidence/currentness

Access date 2026-11-07.

- WCAG 2.2 (W3C Recommendation, 12 Dec 2024), https://www.w3.org/TR/WCAG22/ : SC 1.4.3 text
  contrast 4.5:1, large text 3:1 (18 pt, or 14 pt bold); SC 1.4.11 non-text contrast 3:1; SC 2.5.8
  target size minimum 24 by 24 CSS px (AA); SC 2.5.5 44 by 44 (AAA); SC 2.3.3 animation from
  interactions (AAA). The 48 dp target is a house rule above these minimums.
- Android `Settings.Global.ANIMATOR_DURATION_SCALE` ("scaling factor for Animator-based
  animations") and `ValueAnimator.areAnimatorsEnabled()` (API 26; false when the scale is 0 or
  battery saver disables animations):
  https://developer.android.com/reference/android/provider/Settings.Global and
  https://developer.android.com/reference/android/animation/ValueAnimator
- Material 3's 48 dp touch-target guidance: the m3.material.io page fetched on 2026-11-07 did not
  render its text; `NOT_ASSESSED` here. Compose `minimumInteractiveComponentSize` behaviour is
  `NOT_ASSESSED` for the Compose version in use; confirm in the project's BOM.
- Contrast ratios in this file were recomputed from the hex values on 2026-11-07 with the WCAG
  relative-luminance formula.
- Device, TalkBack and 200% text behaviour of these patterns in a new app: `NOT_ASSESSED`.

Sources: Maduuka Android app theme and guardrail tests (Nov 2026), read by role only; the design
engine's house-style audit record of 7 Nov 2026.
