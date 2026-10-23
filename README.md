# PSP NEXUS

A Cyber Blue Windows desktop launcher for your own PSP game backups. No coding is required to use the downloadable Windows build.

## Features
- Neon Cyber Blue desktop UI
- Add and search PSP game files: ISO, CSO, PBP, CHD
- Scan a chosen games folder
- Configure PPSSPP and launch games
- Remove library entries without deleting game files
- Saves settings in your Windows user folder

## Get the app
Open the **Actions** tab and select the latest **Build PSP NEXUS for Windows** run. When it completes successfully, download the **PSP-NEXUS-Windows** artifact and extract it. Run `PSP-NEXUS.exe`.

## Run from source
Install Python 3 for Windows, then run `python main.py`. Tkinter is included with standard Windows Python installations.

## Build locally
```bat
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --onefile --windowed --name PSP-NEXUS main.py
```

## First setup
1. Install PPSSPP from https://www.ppsspp.org/.
2. Open PSP NEXUS and click **Settings**.
3. Browse to the PPSSPP Windows executable.
4. Select your PSP games folder or use **Add Game**.
5. Click **PLAY** on a game.

PSP NEXUS is a launcher/library, not an emulator. It does not include or download commercial games. Use game files you are legally entitled to use. Cover tiles in this initial version are stylized placeholders.
