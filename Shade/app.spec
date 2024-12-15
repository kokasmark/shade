# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\met4y\\Desktop\\shade\\Shade\\app.py'],
    pathex=['C:\\Users\\met4y\\Desktop\\shade\\Shade'],
    binaries=[],
    datas=[('C:\\Users\\met4y\\Desktop\\shade\\Shade\\frontend', 'frontend'), ('C:\\Users\\met4y\\Desktop\\shade\\Shade\\frontend\\assets', 'assets')],
    hiddenimports=['pkg_resources', 'pkg_resources.extern'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('-OO', None, 'OPTION')],
    name='app',
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
    icon=['C:\\Users\\met4y\\Desktop\\shade\\Shade\\frontend\\favicon.ico'],
)
