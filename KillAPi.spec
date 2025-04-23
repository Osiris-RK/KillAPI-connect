# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['killfeed.py'],
    pathex=[],
    binaries=[],
    datas=[('fonts', 'fonts'), ('KillAPI.ico', '.')],
    hiddenimports=['logmonitor', 'transmitter', 'checkversion'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
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
    name='KillAPi',
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
    icon=['KillAPI.ico'],
)
