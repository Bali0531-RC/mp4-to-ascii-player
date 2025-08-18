@echo off
REM Build script for creating a Windows executable using PyInstaller
REM Usage examples:
REM   build_exe.bat
REM   build_exe.bat --onefile --name ascii-player

setlocal ENABLEDELAYEDEXPANSION

set APP_NAME=ascii-player
set ENTRYPOINT=ascii.py
set DIST_DIR=build_output
set BUILD_DIR=build_build
set SPEC_DIR=build_spec
set ONEFILE=

:parse
if "%~1"=="" goto after_parse
if /I "%~1"=="--onefile" (
  set ONEFILE=--onefile
  shift
  goto parse
)
if /I "%~1"=="-F" (
  set ONEFILE=--onefile
  shift
  goto parse
)
if /I "%~1"=="--name" (
  set APP_NAME=%~2
  shift
  shift
  goto parse
)
if /I "%~1"=="-n" (
  set APP_NAME=%~2
  shift
  shift
  goto parse
)
if /I "%~1"=="--dist-dir" (
  set DIST_DIR=%~2
  shift
  shift
  goto parse
)
if /I "%~1"=="--build-dir" (
  set BUILD_DIR=%~2
  shift
  shift
  goto parse
)
if /I "%~1"=="--spec-dir" (
  set SPEC_DIR=%~2
  shift
  shift
  goto parse
)
REM Collect unrecognized args
set EXTRA_ARGS=%EXTRA_ARGS% %~1
shift
goto parse

after_parse:

where pyinstaller >nul 2>nul
if errorlevel 1 (
  echo PyInstaller not found. Installing...
  pip install pyinstaller || goto :error
)

echo Building %APP_NAME% ...
pyinstaller %ENTRYPOINT% --name "%APP_NAME%" --distpath "%DIST_DIR%" --workpath "%BUILD_DIR%" --specpath "%SPEC_DIR%" --clean %ONEFILE% %EXTRA_ARGS%
if errorlevel 1 goto :error

echo.
echo Build complete. See %DIST_DIR%\%APP_NAME%.exe (if onefile) or folder.
goto :eof

:error
echo Build failed.
exit /b 1
