# Apple game delivery gates

## Durable evidence from the supplied Swift source

Stephen Haney's *Game Development with Swift* is a legacy, introductory secondary source. It supports three durable patterns: separate game areas into scenes, test performance on physical devices rather than trusting the simulator, and isolate Game Center integration for achievements and leaderboards. Its Swift 1.2, Xcode 6.3, iOS 7, OS X, and historical asset-scale instructions are not current implementation authority.

## Gate matrix

| Surface | Required proof | Failed-path proof |
|---|---|---|
| Lifecycle | save-safe suspend, resume, terminate, memory pressure | interruption during write does not corrupt the last good save |
| Input | keyboard, mouse, supported controllers, remapping, haptics | disconnect/reconnect and focus loss recover |
| Display | window, full screen, Retina, resolution and display changes | invalid/removed display returns to a usable window |
| Services | authenticated and signed-out flows; local fallback | outage, cancellation and account change preserve play/save state |
| Graphics | release-build capture on target Apple GPU classes | shader/feature fallback is visible and diagnosable |
| Distribution | channel-specific signing and current official checks | expired identity or entitlement mismatch blocks promotion clearly |

Record every current platform claim with its official source, access date, target version, and reversal trigger.

