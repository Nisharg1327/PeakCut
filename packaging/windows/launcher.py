"""Starts PeakCut from the installed program: sets up a per-user data folder, runs the server, opens the browser.

Used only by the Windows installer build (PyInstaller). Running PeakCut from source is unchanged:
    python -m studio.server
"""
import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

# The folder picker in Settings runs `python -c <code>`. In the installed program "python" is this exe, so
# handle that call here instead of starting a second server.
if len(sys.argv) >= 3 and sys.argv[1] == "-c":
    exec(compile(sys.argv[2], "<picker>", "exec"))
    sys.exit(0)


def _app_dir() -> Path:
    return Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent


def _setup_environment() -> Path:
    """Program files are read-only for normal users, so everything PeakCut writes goes in the user's own folder."""
    home = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local") / "PeakCut"
    home.mkdir(parents=True, exist_ok=True)
    app = _app_dir()

    os.environ.setdefault("PEAKCUT_STORAGE_FILE", str(home / "storage.json"))
    if not os.environ.get("PEAKCUT_DATA"):
        # Settings, Storage can still move it: storage.json is only read when PEAKCUT_DATA is not set,
        # so only force the default when the owner has not chosen a folder.
        if not (home / "storage.json").exists():
            os.environ["PEAKCUT_DATA"] = str(home / "data")
    os.environ.setdefault("PEAKCUT_UPDATE_CHECK", "0")   # updates come from a new installer, not git

    # bundled ffmpeg / ffprobe / deno (yt-dlp needs a JavaScript runtime for YouTube)
    for sub in ("ffmpeg", "deno"):
        d = app / sub
        if d.is_dir():
            if sub == "ffmpeg":
                os.environ.setdefault("PEAKCUT_FFMPEG_DIR", str(d))
            os.environ["PATH"] = str(d) + os.pathsep + os.environ.get("PATH", "")

    # settings file the user can edit: %LOCALAPPDATA%\PeakCut\.env
    env_file = home / ".env"
    if not env_file.exists():
        sample = app / "_internal" / ".env.example"
        if not sample.exists():
            sample = app / ".env.example"
        try:
            env_file.write_text(sample.read_text(encoding="utf-8") if sample.exists() else "", encoding="utf-8")
        except OSError:
            pass
    for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return home


def _port_in_use(host: str, port: int) -> bool:
    import socket
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def _open_browser_when_ready(url: str, host: str, port: int):
    for _ in range(240):                      # up to ~2 minutes (first start can be slow)
        if _port_in_use(host, port):
            webbrowser.open(url)
            return
        time.sleep(0.5)


def main():
    home = _setup_environment()
    os.chdir(home)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    os.system("title PeakCut") if os.name == "nt" else None

    from studio import config
    url = config.PUBLIC_URL
    if _port_in_use("127.0.0.1", config.PORT):
        print(f"\n  PeakCut is already running. Opening {url}\n")
        webbrowser.open(url)
        time.sleep(2)
        return

    print("\n  Starting PeakCut. Keep this window open while you use it; close it to quit.")
    print(f"  Your videos and clips are kept in: {config.DATA_DIR}")
    print("  The first start downloads the speech model (about 480 MB, once).\n", flush=True)
    threading.Thread(target=_open_browser_when_ready, args=(url, "127.0.0.1", config.PORT), daemon=True).start()

    from studio import server
    server.main()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        import traceback
        traceback.print_exc()
        input("\nPeakCut could not start. Press Enter to close this window.")
        sys.exit(1)
