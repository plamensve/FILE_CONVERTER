# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['FlexConverter.py'],
    pathex=[],
    binaries=[],
    datas=[('ui', 'ui'), ('data', 'data'), ('converters', 'converters')],
    hiddenimports=['reportlab.graphics.barcode.code128', 'reportlab.graphics.barcode.code39', 'reportlab.graphics.barcode.code93', 'reportlab.graphics.barcode.code11', 'reportlab.graphics.barcode.usps', 'reportlab.graphics.barcode.usps4s', 'reportlab.graphics.barcode.i2of5', 'reportlab.graphics.barcode.code39extended', 'reportlab.graphics.barcode.qr', 'reportlab.graphics.barcode.aztec', 'reportlab.graphics.barcode.ecc200datamatrix'],
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
    name='FlexConverter',
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
    icon=['data\\logo.ico'],
)
