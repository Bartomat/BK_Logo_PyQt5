# -*- mode: python ; coding: utf-8 -*-


# Meine Speck-Datei für windows

block_cipher = None


a = Analysis(
    ['BK_Logo_v4_71.py'],
    pathex=[],
    binaries=[],
    datas=[('ui', 'ui'),            # Hier müssen alle Projekt-Ordner rein !!!
           ('style', 'style')       # ('Source im Projekt)', (Target im Build)
           ],                       # Unterordner werden samt Inhalt mitkopiert (siehe 'style')
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BK LogoEditor v471',
    icon='style/icons/Polska.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)