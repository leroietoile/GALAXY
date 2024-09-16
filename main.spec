# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/B1.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/B2.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/B3.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/B4.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/badge.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/bg1.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/Btn_border_white.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/Btn_color_black.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/Btn_color_gold.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/Btn_color_pink.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/Btn_color_white.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/close_window.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/Golden_medal.png', '.'), ('E:/Dossier/CODE/KIVY_PROJECTS/GALAXY/images/PhotoRoom-20231216_160928.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
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
