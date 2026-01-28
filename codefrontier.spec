# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for CodeFrontier

import os
from pathlib import Path

block_cipher = None

# Diretório raiz do projeto
ROOT_DIR = Path(SPECPATH)

# Coletar todos os arquivos de assets
assets_data = []
assets_path = ROOT_DIR / 'assets'

for root, dirs, files in os.walk(assets_path):
    for file in files:
        src = os.path.join(root, file)
        # Caminho relativo a partir do diretório do projeto
        rel_path = os.path.relpath(root, ROOT_DIR)
        assets_data.append((src, rel_path))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=assets_data,
    hiddenimports=['pygame', 'pygame.mixer', 'pygame.font'],
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
    name='CodeFrontier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem console (aplicação windowed)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/images/icons/star.png' if os.path.exists('assets/images/icons/star.png') else None,
)
