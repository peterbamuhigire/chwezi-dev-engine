#!/usr/bin/env pwsh
# install.ps1 — standalone installer entrypoint for this Chwezi engine (Windows-native).
#
# Works with zero other Chwezi components present. Delegates to the vendored
# scripts/install-engine.js (Node, cross-platform). Resolves through symlinks
# the way ECC's install.ps1 does, so invocation via a linked path still finds
# the real script.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptPath = $PSCommandPath
while ($true) {
    $item = Get-Item -LiteralPath $scriptPath -Force
    if (-not $item.LinkType) { break }
    $targetPath = $item.Target
    if ($targetPath -is [array]) { $targetPath = $targetPath[0] }
    if (-not $targetPath) { break }
    if (-not [System.IO.Path]::IsPathRooted($targetPath)) {
        $targetPath = Join-Path -Path $item.DirectoryName -ChildPath $targetPath
    }
    $scriptPath = [System.IO.Path]::GetFullPath($targetPath)
}

# install.ps1 lives at the engine root; the installer runtime is vendored
# one level down, at scripts/install-engine.js.
$engineRoot = Split-Path -Parent $scriptPath
$installerScript = Join-Path -Path $engineRoot -ChildPath 'scripts/install-engine.js'

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js >= 18 is required. Install it, or use the native Claude Code plugin path instead: /plugin marketplace add <this repo>"
    exit 1
}

& node $installerScript install --engine $engineRoot @args
exit $LASTEXITCODE
