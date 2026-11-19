# PeakCut Windows installer kit

Builds `PeakCut-Setup.exe`: a normal Windows installer (Start Menu + optional desktop shortcut, uninstaller).
ffmpeg, ffprobe and deno are bundled, so users only need to install it. The speech model (about 480 MB)
downloads on first start.

## Easiest: build it on GitHub (no Windows PC needed)
1. Copy the `packaging/` and `.github/` folders from this kit into your PeakCut repository and push.
2. On GitHub: Actions, "Build Windows installer", Run workflow.
3. Download `PeakCut-Setup` from the finished run (or push a tag like `v1.0.0` to get it attached to a Release).

## Or build on your own Windows PC
Install Python 3.10+ (64-bit) and Inno Setup 6, then from the repository root:

    powershell -ExecutionPolicy Bypass -File packaging\windows\build.ps1

Output: `installer-output\PeakCut-Setup.exe`

## How the installed program behaves
- Videos, clips, database and settings go in `%LOCALAPPDATA%\PeakCut` (the install folder stays read-only).
  Uninstalling does not delete them.
- API keys can be saved in the dashboard, or in `%LOCALAPPDATA%\PeakCut\.env`.
- Starting PeakCut opens a console window and your browser at http://127.0.0.1:8765. Closing the window quits it.
- The git-based update notice is turned off; update by running a newer installer over the old one.
- Optional: put a `peakcut.ico` in this folder before building to get a custom icon.

## Licensing note
The bundled ffmpeg is a GPL build (needed for captions). If you distribute the installer publicly, link to
ffmpeg's source (https://github.com/BtbN/FFmpeg-Builds) alongside it.
