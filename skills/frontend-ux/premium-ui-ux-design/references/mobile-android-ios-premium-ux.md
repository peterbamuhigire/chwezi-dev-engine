# Mobile Android And iOS Premium UX

Native mobile products must feel intentionally made for the platform. Do not ship a squeezed website.

## Shared Mobile Principles

- Design for thumb reach, one-handed use, interruption, poor networks, small screens, and short sessions.
- Keep primary tasks within 1-2 taps from the main screen when the task is frequent.
- Use bottom navigation for 3-5 top-level destinations; avoid overcrowded tab bars.
- Use clear empty, offline, loading, permission-denied, and sync-conflict states.
- Make forms short, grouped, resumable, and keyboard-aware.
- Use native date, time, picker, camera, biometric, share, and notification patterns where possible.
- Haptics should confirm meaningful actions, not decorate every tap.
- Motion should preserve spatial orientation and respect reduced-motion settings.
- Support dynamic type/font scaling without clipping.
- Minimum touch target: 44 pt on iOS, 48 dp on Android unless a platform component safely handles density.

## Android Premium UX

- Use Material 3 as the platform baseline, then brand it through tokens, shape, typography, and component theming.
- Use Jetpack Compose state-driven UI; each screen must explicitly model loading, content, empty, error, offline, and permission states.
- Apply adaptive navigation: bottom bar on compact phones, navigation rail on wider screens, drawer only when information architecture requires it.
- Use `WindowSizeClass` for phone, tablet, foldable, and landscape decisions.
- Respect Android edge-to-edge behavior, system bars, back navigation, predictive back where applicable, and platform permission flows.
- Use Material motion and container transforms only when they clarify hierarchy.
- Use custom PNG icons only when the project standard requires them; keep size, optical alignment, and naming consistent.
- For business apps, reports over 25 rows should use table-first or dense list patterns rather than card walls.

## iOS Premium UX

- Use SwiftUI with platform-native navigation stacks, tab bars, sheets, forms, menus, and lists.
- Follow iOS principles: clarity, deference to content, and depth through hierarchy and motion.
- Use SF Symbols consistently unless a custom icon system is required.
- Support Dynamic Type, VoiceOver, Reduce Motion, Increase Contrast, and Dark Mode.
- Use tab bars for primary destinations, navigation bars for hierarchy, sheets for focused tasks, and full-screen covers sparingly.
- Preserve swipe-back and native gestures unless a strong product reason exists.
- Use haptics sparingly for success, warning, selection, and impact moments.
- Avoid Android-style components, dense desktop tables, and web-like hamburger navigation unless the app domain truly requires it.

## Mobile Dashboard Rules

- Start with a compact summary and the most urgent exception.
- Use cards only when each card is a meaningful unit; avoid endless KPI tiles.
- Prefer sparklines, bullet indicators, ranked lists, and drill-down over complex multi-series charts.
- Keep comparisons visible; do not hide every metric behind horizontal carousels.
- Let users freeze or pause live updates when monitoring a changing dashboard.

## Mobile Quality Gate

- Main task works on the smallest supported phone and a large phone/tablet.
- Text scaling does not clip labels or controls.
- Keyboard does not cover active fields or submit actions.
- Offline and slow-network states are useful.
- Permissions are explained before the system prompt when context is needed.
- Native back/swipe behavior matches platform expectations.
- Touch targets and spacing feel comfortable in repeated use.
