# Builds PeakCut-Setup.exe on Windows. Run from the repository root:
#   powershell -ExecutionPolicy Bypass -File packaging\windows\build.ps1
# Needs: Python 3.10+ (64-bit) and Inno Setup 6 (https://jrsoftware.org/isinfo.php).
param([string]$Version = "1.0.0")
$ErrorActionPreference = "Stop"
$root = Resolve-Path "$PSScriptRoot\..\.."
Set-Location $root

python -m venv .build-venv
& .\.build-venv\Scripts\python.exe -m pip install --upgrade pip
& .\.build-venv\Scripts\python.exe -m pip install -r requirements.txt pyinstaller

Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
& .\.build-venv\Scripts\pyinstaller.exe packaging\windows\peakcut.spec --noconfirm

# ffmpeg + ffprobe (the GPL build: PeakCut's captions need libass and libx264)
$tmp = Join-Path $env:TEMP "peakcut-build"; New-Item -ItemType Directory -Force $tmp | Out-Null
$ff = Join-Path $tmp "ffmpeg.zip"
Invoke-WebRequest "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip" -OutFile $ff
Expand-Archive $ff -DestinationPath $tmp -Force
$bin = (Get-ChildItem $tmp -Directory -Filter "ffmpeg-*" | Select-Object -First 1).FullName + "\bin"
New-Item -ItemType Directory -Force dist\PeakCut\ffmpeg | Out-Null
Copy-Item "$bin\ffmpeg.exe", "$bin\ffprobe.exe" dist\PeakCut\ffmpeg\

# deno: yt-dlp needs a JavaScript runtime for YouTube
$dn = Join-Path $tmp "deno.zip"
Invoke-WebRequest "https://github.com/denoland/deno/releases/latest/download/deno-x86_64-pc-windows-msvc.zip" -OutFile $dn
New-Item -ItemType Directory -Force dist\PeakCut\deno | Out-Null
Expand-Archive $dn -DestinationPath dist\PeakCut\deno -Force

$pf86 = ${env:ProgramFiles(x86)}
$iscc = @("$pf86\Inno Setup 6\ISCC.exe", "$env:ProgramFiles\Inno Setup 6\ISCC.exe", "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe") |
        Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $iscc) { $cmd = Get-Command ISCC.exe -ErrorAction SilentlyContinue; if ($cmd) { $iscc = $cmd.Source } }
if (-not $iscc) { throw "Inno Setup 6 was not found. Install it from https://jrsoftware.org/isdl.php" }
& $iscc "/DAppVersion=$Version" packaging\windows\installer.iss
Write-Host "`nDone: installer-output\PeakCut-Setup.exe"
