# Safari And WebKit 27 PWA Checks

Use this reference when an offline-first app must work on Safari, iOS/iPadOS
home-screen web apps, macOS Safari, or an embedded Apple web surface.

## Compatibility Rules

- Treat Safari as a first-class target, not as a Chromium variant.
- Keep service worker, cache, storage quota, push, background sync, file access,
  and installability checks separate for Safari, Chrome, Edge, and Firefox.
- Feature-detect every optional API and keep a tested fallback for iOS/iPadOS.
- Do not promise native-equivalent background execution on iOS home-screen apps.
- Test low-power mode, private browsing, storage pressure, and permission denial.

## WebKit 27 Watch Items

| Area | Check |
| --- | --- |
| Customizable Select | Confirm custom controls retain keyboard, pointer, screen-reader, and reduced-motion behavior. |
| `img sizes="auto"` | Verify responsive images do not download oversized assets on iPhone and iPad. |
| Layout changes | Re-test sticky headers, viewport units, safe areas, virtual keyboard resizing, and scroll restoration. |
| HTML `<model>` | Gate 3D product previews behind support checks and provide image fallback. |
| Web extensions | Keep extension behavior out of the core PWA path unless Safari support is explicitly required and tested. |
| Permissions | Confirm camera, microphone, location, notification, and file prompts have recoverable denied states. |

## PWA Release Gate

- Install from Safari and launch from the home screen on current iOS/iPadOS.
- Confirm login, offline read, offline write queue, reconnect sync, logout, and
  storage clear behavior.
- Verify app icons, splash behavior, theme color, status bar, safe-area insets,
  and orientation constraints.
- Run VoiceOver, Dynamic Type, keyboard navigation, and Reduced Motion checks.
- Capture device, OS, Safari/WebKit version, and network profile in release
  evidence.
