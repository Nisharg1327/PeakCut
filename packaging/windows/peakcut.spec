# PyInstaller spec for the PeakCut Windows program. Build from the repository root:
#   pyinstaller packaging/windows/peakcut.spec --noconfirm
from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules

ROOT = Path(SPECPATH).resolve().parent.parent

datas, binaries, hiddenimports = [], [], []
for pkg in ("sherpa_onnx", "soundfile", "yt_dlp", "psycopg", "psycopg_binary", "uvicorn", "certifi"):
    try:
        d, b, h = collect_all(pkg)
        datas += d; binaries += b; hiddenimports += h
    except Exception as e:                     # a package that is not installed is simply skipped
        print(f"collect_all({pkg}) skipped: {e}")

hiddenimports += collect_submodules("studio")
hiddenimports += collect_submodules("sqlalchemy.dialects.sqlite")
hiddenimports += collect_submodules("sqlalchemy.dialects.postgresql")
hiddenimports += ["tkinter", "tkinter.filedialog", "multipart", "python_multipart", "PIL._tkinter_finder"]

datas += [
    (str(ROOT / "web"), "web"),
    (str(ROOT / "studio" / "fonts"), "studio/fonts"),
    (str(ROOT / ".env.example"), "."),
    (str(ROOT / "LICENSE"), "."),
]

a = Analysis(
    [str(ROOT / "packaging" / "windows" / "launcher.py")],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["pytest", "IPython", "matplotlib"],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="PeakCut",
    console=True,                       # the window is how you quit PeakCut and see its messages
    icon=str(ROOT / "packaging" / "windows" / "peakcut.ico") if (ROOT / "packaging" / "windows" / "peakcut.ico").exists() else None,
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="PeakCut")
