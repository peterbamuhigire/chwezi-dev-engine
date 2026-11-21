[CmdletBinding()]
param(
    [ValidateSet('Start', 'Run', 'Watch', 'Status', 'Resume', 'Stop', 'Cancel', 'Recover', 'Check', 'Help')]
    [string] $Action = 'Start',
    [string] $PythonPath,
    [switch] $NoWatch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Show-LauncherHelp {
    @'
Jidoka (JAD) local launcher

  .\run.ps1                         Check readiness, start detached run, watch status
  .\run.ps1 -NoWatch                Check readiness and start without watching
  .\run.ps1 -Action <name>          Start, Run, Watch, Status, Resume, Stop,
                                     Cancel, Recover, Check, or Help
  .\run.cmd [same options]          Command Prompt entry point

Before Start/Run/Resume/Recover, commit a scoped plan and configure auto-agents\config.json
with the approved runner (Codex or Claude), bounded limits, and project checks.
Check validates readiness without starting an agent. It does not skip review or
change model, login, authentication, permissions, or sandbox settings.

Stop lets the current operation finish and then stops. Cancel requests termination
and leaves an interrupted operation for inspection. Recover is a deliberate operator
action governed by recovery_policy; inspect status and recovery evidence first.
Automatic resume registration is opt-in: see RECOVERY.md and register-resume.ps1.
'@ | Write-Output
}

function Resolve-PythonExecutable([string] $Requested) {
    if ([string]::IsNullOrWhiteSpace($Requested)) {
        $command = Get-Command python.exe -CommandType Application -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if (-not $command) { throw 'python.exe was not found on PATH. Pass -PythonPath with an absolute executable path.' }
        $Requested = $command.Source
    }
    if (-not [IO.Path]::IsPathRooted($Requested)) { throw 'PythonPath must be an absolute executable path.' }
    if (-not (Test-Path -LiteralPath $Requested -PathType Leaf)) { throw "Python executable not found: $Requested" }
    $resolved = (Resolve-Path -LiteralPath $Requested).Path
    if ([IO.Path]::GetExtension($resolved) -ine '.exe') { throw 'PythonPath must name a .exe file.' }
    if ($resolved -match '\\Microsoft\\WindowsApps\\') { throw 'PythonPath resolves to a Windows app execution alias.' }
    return $resolved
}

function Invoke-Driver([string] $Python, [string] $Driver, [string[]] $Arguments) {
    & $Python -I -B $Driver @Arguments | Out-Host
    $driverExitCode = $LASTEXITCODE
    return [int] $driverExitCode
}

if ($Action -eq 'Help') {
    Show-LauncherHelp
    exit 0
}
if ($NoWatch -and $Action -ne 'Start') {
    [Console]::Error.WriteLine('-NoWatch is valid only with -Action Start.')
    exit 2
}

$driverPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'driver.py'))
if (-not (Test-Path -LiteralPath $driverPath -PathType Leaf)) {
    [Console]::Error.WriteLine("Driver not found: $driverPath")
    exit 2
}

try {
    $python = Resolve-PythonExecutable $PythonPath
    $helpOutput = & $python -I -B $driverPath --help 2>&1
    if ($LASTEXITCODE -ne 0 -or (($helpOutput -join "`n") -notmatch '\bcheck\b')) {
        throw 'Selected Python could not load the driver or its check command.'
    }

    if ($Action -eq 'Start') {
        $checkExit = Invoke-Driver $python $driverPath @('check')
        if ($checkExit -ne 0) { exit $checkExit }
        $startExit = Invoke-Driver $python $driverPath @('start')
        if ($startExit -ne 0 -or $NoWatch) { exit $startExit }
        $watchExit = Invoke-Driver $python $driverPath @('watch')
        if ($watchExit -ne 0) { exit $watchExit }
        exit $startExit
    }

    $exitCode = Invoke-Driver $python $driverPath @($Action.ToLowerInvariant())
    exit $exitCode
}
catch {
    [Console]::Error.WriteLine("Jidoka launcher failed: $($_.Exception.Message)")
    exit 2
}
