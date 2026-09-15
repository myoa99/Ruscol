@echo off
setlocal enabledelayedexpansion

set "ENV_NAME=tp_project_env"
set "PYTHON_VERSION=3.11"
set "REQUIREMENTS_FILE=requirements.txt"
set "TEST_SCRIPT=broken_env.py"

:: Переходим в корень проекта (на один уровень выше папки со скриптом)
cd /d "%~dp0.."

echo [INFO] Looking for Conda...

set "CONDA_BAT="

:: 1. Поиск conda.bat в системном PATH
where conda.bat >nul 2>&1
if %ERRORLEVEL% equ 0 (
    for /f "delims=" %%i in ('where conda.bat') do (
        set "CONDA_BAT=%%i"
        goto :FOUND_CONDA
    )
)

:: 2. Поиск по стандартным путям установки Anaconda / Miniconda
set "POSSIBLE_PATHS="
set "POSSIBLE_PATHS=!POSSIBLE_PATHS!;"%USERPROFILE%\anaconda3\condabin\conda.bat""
set "POSSIBLE_PATHS=!POSSIBLE_PATHS!;"%USERPROFILE%\miniconda3\condabin\conda.bat""
set "POSSIBLE_PATHS=!POSSIBLE_PATHS!;"C:\ProgramData\anaconda3\condabin\conda.bat""
set "POSSIBLE_PATHS=!POSSIBLE_PATHS!;"C:\ProgramData\miniconda3\condabin\conda.bat""
set "POSSIBLE_PATHS=!POSSIBLE_PATHS!;"%LOCALAPPDATA%\Continuum\anaconda3\condabin\conda.bat""
set "POSSIBLE_PATHS=!POSSIBLE_PATHS!;"%LOCALAPPDATA%\Miniconda3\condabin\conda.bat""

for %%p in (!POSSIBLE_PATHS!) do (
    if exist %%p (
        set "CONDA_BAT=%%~p"
        goto :FOUND_CONDA
    )
)

:FOUND_CONDA
if "%CONDA_BAT%"=="" (
    echo [ERROR] Conda was not found in PATH or standard installation directories.
    echo Please ensure Anaconda or Miniconda is installed.
    pause
    exit /b 1
)

echo [INFO] Conda found: "%CONDA_BAT%"

call "%CONDA_BAT%" --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to run Conda.
    pause
    exit /b 1
)

echo [INFO] Checking if environment "%ENV_NAME%" exists...
call "%CONDA_BAT%" env list | findstr /R /C:"\<%ENV_NAME%\>" >nul 2>&1

if errorlevel 1 (
    echo [INFO] Creating environment %ENV_NAME% with Python %PYTHON_VERSION%...
    call "%CONDA_BAT%" create -y -n "%ENV_NAME%" python=%PYTHON_VERSION%
    if errorlevel 1 (
        echo [ERROR] Failed to create environment.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Environment %ENV_NAME% already exists.
)

if not exist "%REQUIREMENTS_FILE%" (
    echo [ERROR] %REQUIREMENTS_FILE% was not found in %CD%.
    pause
    exit /b 1
)

if not exist "%TEST_SCRIPT%" (
    echo [ERROR] %TEST_SCRIPT% was not found in %CD%.
    pause
    exit /b 1
)

echo [INFO] Installing dependencies from %REQUIREMENTS_FILE%...
call "%CONDA_BAT%" run -n "%ENV_NAME%" python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip.
    pause
    exit /b 1
)

call "%CONDA_BAT%" run -n "%ENV_NAME%" python -m pip install -r "%REQUIREMENTS_FILE%"
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [INFO] Running smoke test...
call "%CONDA_BAT%" run -n "%ENV_NAME%" python "%TEST_SCRIPT%"
if errorlevel 1 (
    echo [ERROR] Smoke test failed.
    pause
    exit /b 1
)

echo [OK] Environment is ready.
pause
exit /b 0