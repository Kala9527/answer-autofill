@echo off
setlocal

set "TOOL_DIR=%~dp0"
set "CONDA_EXE=D:\Miniconda3\Scripts\conda.exe"
set "ENV_DIR=D:\Miniconda3\envs\answer_autofill"
set "PYTHON_EXE=%ENV_DIR%\python.exe"

if not exist "%CONDA_EXE%" (
  echo Cannot find conda: "%CONDA_EXE%"
  exit /b 1
)

if not exist "%PYTHON_EXE%" (
  "%CONDA_EXE%" create -y -p "%ENV_DIR%" python=3.11 pip
  if errorlevel 1 exit /b 1
)

"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 exit /b 1

"%PYTHON_EXE%" -m pip install -r "%TOOL_DIR%requirements.txt"
if errorlevel 1 exit /b 1

"%PYTHON_EXE%" -m pip freeze > "%TOOL_DIR%requirements.txt"
if errorlevel 1 exit /b 1

echo Environment ready: "%ENV_DIR%"
