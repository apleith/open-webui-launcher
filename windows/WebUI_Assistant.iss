; Open WebUI Launcher v2.0
; Place this .iss in your windows\ folder (next to launch_hidden.py)

[Setup]
AppName=Open WebUI Launcher
AppVersion=2.0
DefaultDirName={pf}\Open WebUI Launcher
DisableProgramGroupPage=yes
DisableDirPage=yes
OutputBaseFilename=Open_WebUI_Launcher_v2.0
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
; Use your bundled icon for the installer window:
SetupIconFile=..\common\logo.ico

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; Flags: unchecked

[Files]
; 1) your single‐file EXE
Source: "..\installer_input\WebUI_Assistant.exe"; DestDir: "{app}"; Flags: ignoreversion

; 2) the silent stub (to suppress console windows)
Source: "launch_hidden.py"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Open WebUI Launcher";         Filename: "{app}\WebUI_Assistant.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\Open WebUI Launcher"; Filename: "{app}\WebUI_Assistant.exe"; Tasks: desktopicon; WorkingDir: "{app}"

[Run]
Filename: "{app}\WebUI_Assistant.exe"; Description: "Launch Open WebUI Launcher"; Flags: nowait postinstall skipifsilent
