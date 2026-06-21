# Apple Framework Watch Items WWDC26

Use this file for specialty Apple-platform capabilities introduced or emphasized
at WWDC26. Do not add these to every app by default; route only when the product
uses the domain.

## Media And Audio

- **NowPlaying:** playback apps should verify Lock Screen, Control Center,
  Dynamic Island, and CarPlay integration.
- **Music Understanding:** audio apps can analyze music/audio dimensions on
  device; verify privacy, battery, and model availability.
- **Generated subtitles / MusicKit / camera sessions:** review current Apple
  session docs before implementation.

## Camera And Photos

- Test responsive camera launch on real devices.
- Verify high-resolution photo capture paths and memory pressure.
- Test Center Stage front-camera support only on compatible hardware.
- Review Core Image RAW v9 output before changing production photo pipelines.

## Games And Spatial

- Game Porting Toolkit 4 and Steam Asset Converter are specialty paths for
  porting games to Apple platforms.
- Background Assets can reduce game install size by localizing downloaded asset
  packs; include fallback behavior for missing preferred language assets.
- Unity teams should review Apple's official StoreKit and Background Assets
  plugins before building custom wrappers.
- Reality Composer Pro 3 and Spatial Preview apply only to spatial/3D/Vision Pro
  workflows.

## StoreKit And App Store

Load `ios-monetization` for StoreKit or in-app purchase work. WWDC26 references
Apple In-App Purchase updates and group/organization subscription sessions, so
read current App Store documentation before adding new subscription behavior.
