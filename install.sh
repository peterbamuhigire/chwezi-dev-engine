#!/usr/bin/env bash
# install.sh — standalone installer entrypoint for this Chwezi engine.
#
# Works with zero other Chwezi components present. Delegates to the vendored
# scripts/install-engine.js (Node, cross-platform). On Windows under Git
# Bash / MSYS2, converts the POSIX script path to a native Windows path
# before invoking node, because Node is a native Windows binary and MSYS2's
# automatic path conversion otherwise produces a doubled, invalid path
# (e.g. "G:\g\projects\..." instead of the real path). This is the same
# fix documented in ECC's install.sh (github.com/affaan-m/ECC).

set -euo pipefail

SCRIPT_PATH="$0"
while [ -L "$SCRIPT_PATH" ]; do
  link_dir="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
  SCRIPT_PATH="$(readlink "$SCRIPT_PATH")"
  [[ "$SCRIPT_PATH" != /* ]] && SCRIPT_PATH="$link_dir/$SCRIPT_PATH"
done
# install.sh lives at the engine root; the installer runtime is vendored
# one level down, at scripts/install-engine.js.
ENGINE_ROOT="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

if ! command -v node &>/dev/null; then
  echo "[chwezi] Node.js >= 18 is required. Install it, or use the native" >&2
  echo "[chwezi] Claude Code plugin path instead: /plugin marketplace add <this repo>" >&2
  exit 1
fi

if command -v cygpath &>/dev/null; then
  INSTALLER_SCRIPT="$(cygpath -w "$ENGINE_ROOT/scripts/install-engine.js")"
  ENGINE_ROOT_ARG="$(cygpath -w "$ENGINE_ROOT")"
else
  INSTALLER_SCRIPT="$ENGINE_ROOT/scripts/install-engine.js"
  ENGINE_ROOT_ARG="$ENGINE_ROOT"
fi

exec node "$INSTALLER_SCRIPT" install --engine "$ENGINE_ROOT_ARG" "$@"
