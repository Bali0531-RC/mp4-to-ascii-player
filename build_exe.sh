#!/usr/bin/env bash
# Build script for creating a standalone Windows executable (or Linux binary) using PyInstaller
# Usage (Linux/macOS to create Linux binary):
#   bash build_exe.sh
# Usage (from Windows Git Bash / WSL to create Windows .exe):
#   bash build_exe.sh --onefile --name ascii-player
# Cross-building pure-Python to Windows from Linux is NOT officially supported unless using Wine.
# Recommended: Run this script on Windows (CMD/PowerShell) or use the accompanying build_exe.bat

set -euo pipefail

# Default configuration
APP_NAME="ascii-player"
ENTRYPOINT="ascii.py"
DIST_DIR="build_output"
BUILD_DIR="build_build"
SPEC_DIR="build_spec"
ONEFILE=false
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --onefile|-F)
      ONEFILE=true
      shift
      ;;
    --name|-n)
      APP_NAME="$2"; shift 2;;
    --dist-dir)
      DIST_DIR="$2"; shift 2;;
    --build-dir)
      BUILD_DIR="$2"; shift 2;;
    --spec-dir)
      SPEC_DIR="$2"; shift 2;;
    --)*
      EXTRA_ARGS+=("$1"); shift;;
    *)
      echo "Unknown argument: $1"; exit 1;;
  esac
done

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "PyInstaller not found. Installing..." >&2
  pip install pyinstaller
fi

CMD=(pyinstaller "$ENTRYPOINT" \
  --name "$APP_NAME" \
  --distpath "$DIST_DIR" \
  --workpath "$BUILD_DIR" \
  --specpath "$SPEC_DIR" \
  --clean)

if $ONEFILE; then
  CMD+=(--onefile)
fi

# Ensure console (no --noconsole) so the ASCII output works
# Add any extra passthrough args
CMD+=("${EXTRA_ARGS[@]}")

echo "Running: ${CMD[*]}"
"${CMD[@]}"

echo "\nBuild complete. Output directory: $DIST_DIR"
if $ONEFILE; then
  echo "Executable: $DIST_DIR/$APP_NAME"$( [[ "$(uname -s)" =~ MINGW|MSYS|CYGWIN ]] && echo ".exe" )
fi
