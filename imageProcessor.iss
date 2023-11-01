[Setup]
AppName=ImageRefiner
AppVersion=1.0
DefaultDirName={commonpf}\ImageRefiner
DefaultGroupName=ImageRefiner
OutputDir=Output
OutputBaseFilename=ImageRefinerSetup

[Files]
Source: "dist\ImageRefiner.exe"; DestDir: "{app}"
; Additional files or directories to be installed can be added here

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"
Name: "desktopicon\uninstall"; Description: "Remove desktop icon during uninstallation"; GroupDescription: "Additional icons:"

[Icons]
Name: "{group}\ImageRefiner"; Filename: "{app}\ImageRefiner.exe"
Name: "{commondesktop}\ImageRefiner"; Filename: "{app}\ImageRefiner.exe"; Tasks: desktopicon

[UninstallDelete]
Type: filesandordirs; Name: "{commondesktop}\ImageRefiner.lnk"; Tasks: desktopicon\uninstall

