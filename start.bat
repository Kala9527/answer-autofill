@echo off
setlocal EnableExtensions

set "TOOL_DIR=%~dp0"
set "ENV_DIR=D:\Miniconda3\envs\answer_autofill"
set "PYTHON_EXE=%ENV_DIR%\python.exe"
set "PYTHONUTF8=1"
set "DOUBLE_CLICK_MODE=0"

for %%I in ("%TOOL_DIR%..\excle_deal") do set "DEFAULT_INPUT_FOLDER=%%~fI"

if "%~1"=="" (
  set "DOUBLE_CLICK_MODE=1"
  set "INPUT_FOLDER=%DEFAULT_INPUT_FOLDER%"
  set "EXTRA_ARGS=--concurrency 8"
) else if /I "%~1"=="--dry-run" (
  set "INPUT_FOLDER=%DEFAULT_INPUT_FOLDER%"
  set "EXTRA_ARGS=--dry-run"
) else if /I "%~1"=="--smoke-test" (
  set "INPUT_FOLDER=%DEFAULT_INPUT_FOLDER%"
  set "EXTRA_ARGS=--smoke-test --concurrency 8"
) else (
  set "INPUT_FOLDER=%~1"
  set "EXTRA_ARGS=--concurrency 8"
  shift
  :collect_args
  if "%~1"=="" goto args_done
  set "EXTRA_ARGS=%EXTRA_ARGS% %1"
  shift
  goto collect_args
)
:args_done

if not exist "%PYTHON_EXE%" (
  echo Environment not found: "%ENV_DIR%"
  echo Please run "%TOOL_DIR%setup_env.bat" first.
  if "%DOUBLE_CLICK_MODE%"=="1" pause
  exit /b 1
)

if not exist "%INPUT_FOLDER%" (
  echo Input folder not found: "%INPUT_FOLDER%"
  if "%DOUBLE_CLICK_MODE%"=="1" pause
  exit /b 1
)

cd /d "%TOOL_DIR%"
echo Input folder: "%INPUT_FOLDER%"
"%PYTHON_EXE%" -m answer_autofill "%INPUT_FOLDER%" %EXTRA_ARGS%
set "EXIT_CODE=%ERRORLEVEL%"

if "%DOUBLE_CLICK_MODE%"=="1" (
  echo.
  echo Done. Press any key to close this window.
  pause >nul
)

exit /b %EXIT_CODE%
