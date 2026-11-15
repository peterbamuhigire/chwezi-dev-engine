[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    [switch] $Apply,
    [switch] $Remove,
    [switch] $Run,
    [string] $RepositoryRoot = (Split-Path -Parent $PSScriptRoot),
    [string] $PythonPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:ResumeRegistrationScript = [IO.Path]::GetFullPath($PSCommandPath)

function Stop-Setup([string] $Message) {
    throw $Message
}

function Get-RepositoryIdentity([string] $Path, [bool] $RequireExisting) {
    if (-not [IO.Path]::IsPathRooted($Path)) {
        Stop-Setup 'RepositoryRoot must be an absolute path.'
    }
    $full = [IO.Path]::GetFullPath($Path).TrimEnd('\')
    if ($RequireExisting) {
        if (-not (Test-Path -LiteralPath $full -PathType Container)) {
            Stop-Setup "Repository directory not found: $full"
        }
        $full = (Resolve-Path -LiteralPath $full).Path.TrimEnd('\')
        $git = Get-Command git.exe -CommandType Application -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if (-not $git) { Stop-Setup 'git.exe is required to validate the repository root.' }
        $gitRoot = & $git.Source -C $full rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -ne 0 -or -not $gitRoot) {
            Stop-Setup 'RepositoryRoot is not a Git working tree.'
        }
        $gitRoot = [IO.Path]::GetFullPath(($gitRoot | Select-Object -First 1).Trim()).TrimEnd('\')
        if (-not [string]::Equals($full, $gitRoot, [StringComparison]::OrdinalIgnoreCase)) {
            Stop-Setup "RepositoryRoot must be the Git root. Resolved root: $gitRoot"
        }
    }
    if ($full.Length -lt 4 -or $full -match '^[A-Za-z]:$') {
        Stop-Setup 'RepositoryRoot is too broad to identify a repository safely.'
    }
    return $full
}

function Get-Sha256([string] $Text) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Text.ToUpperInvariant())
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally { $sha.Dispose() }
}

function Resolve-Python([string] $RequestedPath, [string] $DriverPath) {
    if ([string]::IsNullOrWhiteSpace($RequestedPath)) {
        $found = Get-Command python.exe -CommandType Application -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if (-not $found) { Stop-Setup 'python.exe was not found on PATH; pass -PythonPath with its absolute executable path.' }
        $RequestedPath = $found.Source
    }
    if (-not [IO.Path]::IsPathRooted($RequestedPath)) {
        Stop-Setup 'PythonPath must resolve to an absolute executable path.'
    }
    if (-not (Test-Path -LiteralPath $RequestedPath -PathType Leaf)) {
        Stop-Setup "Python executable not found: $RequestedPath"
    }
    $resolved = (Resolve-Path -LiteralPath $RequestedPath).Path
    if ([IO.Path]::GetExtension($resolved) -ine '.exe') {
        Stop-Setup 'PythonPath must name a Windows executable (.exe).'
    }
    if ($resolved -match '\\Microsoft\\WindowsApps\\') {
        Stop-Setup 'PythonPath resolves to a Windows app execution alias; pass the installed python.exe path.'
    }
    $versionProbe = & $resolved -I -B -c "import sys; print('Python', sys.version.split()[0]); raise SystemExit(sys.version_info < (3, 9))"
    if ($LASTEXITCODE -ne 0) { Stop-Setup 'Python 3.9 or later is required by the current driver.' }
    $probe = & $resolved -I -B $DriverPath --help 2>&1
    if ($LASTEXITCODE -ne 0 -or (($probe -join "`n") -notmatch '\bresume\b')) {
        Stop-Setup 'The selected Python executable could not load this driver and its resume command.'
    }
    return $resolved
}

function Get-SchedulerLogPaths([string] $Root) {
    $git = Get-Command git.exe -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if (-not $git) { Stop-Setup 'git.exe is required to locate durable scheduler logs.' }
    $commonRaw = & $git.Source -C $Root rev-parse --git-common-dir 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $commonRaw) {
        Stop-Setup 'Could not resolve the Git common directory for scheduler logs.'
    }
    $commonValue = ($commonRaw | Select-Object -First 1).Trim()
    if ([IO.Path]::IsPathRooted($commonValue)) {
        $common = [IO.Path]::GetFullPath($commonValue)
    }
    else {
        $common = [IO.Path]::GetFullPath((Join-Path $Root $commonValue))
    }
    if (-not (Test-Path -LiteralPath $common -PathType Container)) {
        Stop-Setup "Git common directory is missing: $common"
    }
    $logDirectory = Join-Path $common 'auto-agents'
    if (-not (Test-Path -LiteralPath $logDirectory -PathType Container)) {
        New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
    }
    return [pscustomobject]@{
        Stdout = Join-Path $logDirectory 'scheduler-resume.stdout.log'
        Stderr = Join-Path $logDirectory 'scheduler-resume.stderr.log'
    }
}

function Quote-Argument([string] $Value) {
    if ($null -eq $Value) { Stop-Setup 'Cannot encode a null task argument.' }
    if ($Value.Contains('"')) { Stop-Setup 'A task path contains an unsupported quote character.' }
    return '"' + $Value + '"'
}

function Get-TaskSpec([string] $Root, [string] $Python, [switch] $ForRemoval) {
    $driver = Join-Path $Root 'auto-agents\driver.py'
    $config = Join-Path $Root 'auto-agents\config.json'
    if (-not $ForRemoval) {
        foreach ($required in @($driver, $config, (Join-Path $Root 'auto-agents\execution.py'),
                (Join-Path $Root 'auto-agents\durable.py'))) {
            if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
                Stop-Setup "Required auto-agents file is missing: $required"
            }
        }
    }

    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    if (-not $identity.User) { Stop-Setup 'The current Windows identity has no user SID.' }
    $powerShell = (Get-Process -Id $PID).Path
    if (-not $powerShell -or -not (Test-Path -LiteralPath $powerShell -PathType Leaf)) {
        Stop-Setup 'Could not resolve the current PowerShell executable to an absolute file path.'
    }
    if ([Security.Principal.WindowsPrincipal]::new($identity).IsInRole(
            [Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Stop-Setup 'Run this script unelevated. The task is limited privilege and must not be registered from an elevated session.'
    }
    if (-not [Environment]::UserInteractive -or (Get-Process -Id $PID).SessionId -eq 0) {
        Stop-Setup 'An interactive user session is required; this task cannot run before user logon.'
    }

    $rootDigest = Get-Sha256 $Root
    $taskDigest = Get-Sha256 ($Root + "`n" + $identity.User.Value)
    $taskName = "Chwezi Auto-Agents Resume $($taskDigest.Substring(0, 16))"
    $marker = "ChweziAutoAgentsResume/v1;repo=$rootDigest;identity=$taskDigest;owner=$($identity.User.Value)"
    $scriptPath = [IO.Path]::GetFullPath((Join-Path $Root 'auto-agents\register-resume.ps1'))
    if (-not $ForRemoval -and -not [string]::Equals(
            (Resolve-Path -LiteralPath $script:ResumeRegistrationScript).Path,
            $scriptPath, [StringComparison]::OrdinalIgnoreCase)) {
        Stop-Setup 'Run the registration script from this repository root.'
    }
    # PowerShell switches and values must remain separate Windows command-line arguments.
    $arguments = @(
        '-NoLogo', '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden',
        '-File', (Quote-Argument $scriptPath), '-Run',
        '-RepositoryRoot', (Quote-Argument $Root), '-PythonPath', (Quote-Argument $Python)
    ) -join ' '

    $login = New-ScheduledTaskTrigger -AtLogOn -User $identity.Name
    $periodic = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
        -RepetitionInterval ([TimeSpan]::FromMinutes(5))
    # An empty duration means repeat indefinitely; it does not impose a run limit.
    $periodic.Repetition.Duration = ''
    $periodic.Repetition.StopAtDurationEnd = $false
    $principal = New-ScheduledTaskPrincipal -UserId $identity.Name -LogonType Interactive -RunLevel Limited
    $action = New-ScheduledTaskAction -Execute $powerShell -Argument $arguments -WorkingDirectory $Root
    $settings = New-ScheduledTaskSettingsSet -Hidden -StartWhenAvailable `
        -MultipleInstances IgnoreNew -ExecutionTimeLimit ([TimeSpan]::Zero)

    return [pscustomobject]@{
        Name = $taskName
        Path = '\'
        Root = $Root
        Python = $Python
        Identity = $identity
        Marker = $marker
        PowerShell = $powerShell
        Arguments = $arguments
        Action = $action
        Triggers = @($login, $periodic)
        Principal = $principal
        Settings = $settings
    }
}

function Test-OwnedTask($Task, $Spec) {
    if (-not $Task) { return $false }
    if ($Task.Description -cne $Spec.Marker) { return $false }
    if ($Task.Principal.LogonType -ne 'Interactive' -or $Task.Principal.RunLevel -ne 'Limited') { return $false }
    if ($Task.Principal.UserId -notin @($Spec.Identity.Name, $Spec.Identity.User.Value)) { return $false }
    if ($Task.Actions.Count -ne 1) { return $false }
    $action = $Task.Actions[0]
    $actionPath = [IO.Path]::GetFullPath($action.Execute)
    if ([IO.Path]::GetFileName($actionPath) -notin @('powershell.exe', 'pwsh.exe')) { return $false }
    if (-not (Test-Path -LiteralPath $actionPath -PathType Leaf)) { return $false }
    $scriptPath = [IO.Path]::GetFullPath((Join-Path $Spec.Root 'auto-agents\register-resume.ps1'))
    $prefix = '-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -File ' +
        (Quote-Argument $scriptPath) + ' -Run -RepositoryRoot ' +
        (Quote-Argument $Spec.Root) + ' -PythonPath '
    if (-not $action.Arguments.StartsWith($prefix, [StringComparison]::Ordinal)) { return $false }
    $pythonArgument = $action.Arguments.Substring($prefix.Length)
    if ($pythonArgument -notmatch '^"([^"\r\n]+\.exe)"$' -or
            -not [IO.Path]::IsPathRooted($Matches[1])) { return $false }
    if (-not [string]::Equals([IO.Path]::GetFullPath($action.WorkingDirectory),
            $Spec.Root, [StringComparison]::OrdinalIgnoreCase)) { return $false }
    if ($Task.Triggers.Count -ne 2 -or -not $Task.Settings.Hidden -or
            $Task.Settings.ExecutionTimeLimit -ne 'PT0S' -or
            $Task.Settings.MultipleInstances -ne 'IgnoreNew' -or
            -not $Task.Settings.StartWhenAvailable) { return $false }
    $logon = @($Task.Triggers | Where-Object { $_.CimClass.CimClassName -eq 'MSFT_TaskLogonTrigger' })
    $time = @($Task.Triggers | Where-Object { $_.CimClass.CimClassName -eq 'MSFT_TaskTimeTrigger' })
    if ($logon.Count -ne 1 -or $time.Count -ne 1) { return $false }
    if ($logon[0].UserId -ne $Spec.Identity.Name) { return $false }
    if ($time[0].Repetition.Interval -ne 'PT5M' -or $time[0].Repetition.Duration) { return $false }
    return $true
}

try {
    if ($Run -and ($Apply -or $Remove)) { Stop-Setup '-Run cannot be combined with -Apply or -Remove.' }

    if ($Run) {
        $root = Get-RepositoryIdentity $RepositoryRoot $true
        $driver = Join-Path $root 'auto-agents\driver.py'
        $python = Resolve-Python $PythonPath $driver
        $logs = Get-SchedulerLogPaths $root
        $pythonArguments = @('-I', '-B', (Quote-Argument $driver), 'resume') -join ' '
        $process = Start-Process -FilePath $python -ArgumentList $pythonArguments `
            -WorkingDirectory $root -RedirectStandardOutput $logs.Stdout `
            -RedirectStandardError $logs.Stderr -WindowStyle Hidden -Wait -PassThru
        exit $process.ExitCode
    }

    $root = Get-RepositoryIdentity $RepositoryRoot (-not $Remove)
    if ($Remove -and [string]::IsNullOrWhiteSpace($PythonPath)) {
        # Removal checks the stored action shape and does not invoke this placeholder.
        $python = Join-Path $env:SystemRoot 'System32\python.exe'
    }
    else {
        $python = Resolve-Python $PythonPath (Join-Path $root 'auto-agents\driver.py')
    }
    $spec = Get-TaskSpec $root $python -ForRemoval:$Remove
    $existing = Get-ScheduledTask -TaskName $spec.Name -TaskPath $spec.Path -ErrorAction SilentlyContinue

    if ($Remove) {
        if (-not $existing) {
            Write-Output "No resume task exists for repository identity $($spec.Name)."
            return
        }
        if (-not (Test-OwnedTask $existing $spec)) {
            Stop-Setup "Task name collision or ownership mismatch; refusing to remove $($spec.Path)$($spec.Name). Inspect it in Task Scheduler."
        }
        if (-not $Apply) {
            Write-Output "PREVIEW: unregister only owned task $($spec.Path)$($spec.Name) for $root. No task was changed. Use -Remove -Apply to remove it."
            return
        }
        if ($PSCmdlet.ShouldProcess("$($spec.Path)$($spec.Name)", 'Unregister owned interactive resume task')) {
            Unregister-ScheduledTask -TaskName $spec.Name -TaskPath $spec.Path -Confirm:$false
            Write-Output "Removed owned task $($spec.Path)$($spec.Name)."
        }
        return
    }

    if ($existing -and -not (Test-OwnedTask $existing $spec)) {
        Stop-Setup "Task name collision or ownership mismatch; refusing to update $($spec.Path)$($spec.Name). Inspect it in Task Scheduler."
    }
    $operation = if ($existing) { 'Update owned resume task' } else { 'Register current-user resume task' }
    if (-not $Apply) {
        $triggerSummary = 'At current-user logon and every five minutes while the user is logged in'
        Write-Output "PREVIEW: $operation $($spec.Path)$($spec.Name) for $root. PowerShell=$($spec.PowerShell); Python=$python; WorkingDirectory=$root. $triggerSummary. RunLevel=Limited; LogonType=Interactive; hidden action; no scheduler execution timeout. No task was registered. Use -Apply to proceed."
        return
    }
    if ($PSCmdlet.ShouldProcess("$($spec.Path)$($spec.Name)", $operation)) {
        Register-ScheduledTask -TaskName $spec.Name -TaskPath $spec.Path -Action $spec.Action `
            -Trigger $spec.Triggers -Principal $spec.Principal -Settings $spec.Settings `
            -Description $spec.Marker -Force | Out-Null
        $registered = Get-ScheduledTask -TaskName $spec.Name -TaskPath $spec.Path
        if (-not (Test-OwnedTask $registered $spec)) {
            Stop-Setup 'Task registration returned, but the stored task does not match the expected definition. Inspect Task Scheduler; no automatic cleanup was attempted.'
        }
        Write-Output "Registered verified task $($spec.Path)$($spec.Name). It runs only in the current user's interactive session; inspect with driver.py status/watch."
    }
}
catch {
    Write-Error -ErrorRecord $_
    exit 2
}
