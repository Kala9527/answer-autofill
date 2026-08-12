param(
    [string]$InputFolder
)

$ErrorActionPreference = "Stop"
$ToolDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$EnvDir = "D:\Miniconda3\envs\answer_autofill"
$PythonExe = Join-Path $EnvDir "python.exe"
$env:PYTHONUTF8 = "1"

if (-not $InputFolder) {
    $InputFolder = Read-Host "请输入需要处理的Excel文件夹路径"
}

if (-not (Test-Path $PythonExe)) {
    throw "Environment not found: $EnvDir. Please run setup_env.ps1 first."
}

Set-Location $ToolDir
& $PythonExe -m answer_autofill $InputFolder
