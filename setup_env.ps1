$ErrorActionPreference = "Stop"

$ToolDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CondaExe = "D:\Miniconda3\Scripts\conda.exe"
$EnvDir = "D:\Miniconda3\envs\answer_autofill"
$PythonExe = Join-Path $EnvDir "python.exe"

if (-not (Test-Path $CondaExe)) {
    throw "Cannot find conda: $CondaExe"
}

if (-not (Test-Path $PythonExe)) {
    & $CondaExe create -y -p $EnvDir python=3.11 pip
}

& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install -r (Join-Path $ToolDir "requirements.txt")
& $PythonExe -m pip freeze | Set-Content -Path (Join-Path $ToolDir "requirements.txt") -Encoding UTF8

Write-Host "Environment ready: $EnvDir"
