# -*- mode: python ; coding: utf-8 -*-

import os
import pulp

block_cipher = None

# Get the path to PuLP's solver directory
pulp_path = os.path.dirname(pulp.__file__)
cbc_solver_path = os.path.join(pulp_path, 'solverdir', 'cbc', 'win', 'i64', 'cbc.exe')

a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=[
        # Include the CBC solver binary
        (cbc_solver_path, 'pulp/solverdir/cbc/win/i64/'),
    ],
    datas=[
        # Include the solver directory structure
        (os.path.join(pulp_path, 'solverdir'), 'pulp/solverdir'),
    ],
    hiddenimports=[
        'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 
        'tkinter.simpledialog', 'tkinter.filedialog',
        'pulp', 'pulp.apis', 'pulp.apis.coin_api', 
        'tabulate', 'json', 'os', 'pathlib'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Only exclude things that definitely cause problems
        'matplotlib', 'numpy', 'scipy', 'pandas', 'PIL', 'PyQt5', 'PyQt6'
    ],
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
    name='ContainerAllocator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
