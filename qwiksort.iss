[Setup]
AppName=QwikSort
AppVersion=1.0
DefaultDirName={userpf}\QwikSort
DefaultGroupName=QwikSort
UninstallDisplayIcon={app}\QwikSort.exe
OutputDir=dist
OutputBaseFilename=QwikSortInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\QwikSort"; Filename: "{app}\QwikSort.exe"
Name: "{userdesktop}\QwikSort"; Filename: "{app}\QwikSort.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Registry]
; Associate .qsr files with QwikSort
Root: HKCR; Subkey: ".qsr"; ValueType: string; ValueName: ""; ValueData: "QwikSort.Ruleset"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "QwikSort.Ruleset"; ValueType: string; ValueName: ""; ValueData: "QwikSort Ruleset File"
Root: HKCR; Subkey: "QwikSort.Ruleset\DefaultIcon"; ValueType: string; ValueData: "{app}\QwikSort.exe,0"
Root: HKCR; Subkey: "QwikSort.Ruleset\shell\open\command"; ValueType: string; ValueData: """{app}\QwikSort.exe"" ""%1"""
