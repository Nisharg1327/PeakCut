; Inno Setup script: wraps the PyInstaller output (dist\PeakCut) into PeakCut-Setup.exe
#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

[Setup]
AppId={{B6F1D3C2-5A4E-4C57-9E0B-0A1B2C3D4E5F}
AppName=PeakCut
AppVersion={#AppVersion}
AppPublisher=PeakCut
AppPublisherURL=https://github.com/haziqahmedqasmi/PeakCut
DefaultDirName={autopf}\PeakCut
DefaultGroupName=PeakCut
DisableProgramGroupPage=yes
OutputDir=..\..\installer-output
OutputBaseFilename=PeakCut-Setup
Compression=lzma2/max
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayName=PeakCut
LicenseFile=..\..\LICENSE
WizardStyle=modern
#ifexist "peakcut.ico"
SetupIconFile=peakcut.ico
#endif

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Shortcuts:"

[Files]
Source: "..\..\dist\PeakCut\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\PeakCut"; Filename: "{app}\PeakCut.exe"
Name: "{group}\Uninstall PeakCut"; Filename: "{uninstallexe}"
Name: "{autodesktop}\PeakCut"; Filename: "{app}\PeakCut.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\PeakCut.exe"; Description: "Start PeakCut now"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; your videos, clips and settings live in %LOCALAPPDATA%\PeakCut and are deliberately left alone
Type: filesandordirs; Name: "{app}"
