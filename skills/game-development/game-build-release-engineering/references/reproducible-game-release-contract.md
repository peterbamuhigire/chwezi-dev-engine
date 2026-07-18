# Reproducible game release contract

Every release manifest records source revision, dirty-state result, engine/editor version, package/plugin locks, build image/toolchain, target, configuration, content/catalog version, protocol/save version, artefact path, checksum, symbols, signer identity reference, tests, approvals, and promotion history.

Required failure rehearsals: clean-machine dependency resolution; missing secret; expired/revoked signing identity; nearly-full storage; interrupted install/update; incompatible save; symbolication from a deliberate crash; failed staged rollout; rollback to the last compatible artefact.

The supplied Unity and Unreal books explain editor/build concepts but are not CI, signing, certification, or current store authorities. Verify all commands and requirements against pinned official documentation.

