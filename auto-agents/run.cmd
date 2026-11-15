@echo off
powershell.exe -NoProfile -File "%~dp0run.ps1" %*
exit /b %ERRORLEVEL%
