# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# SPECPATH 由 PyInstaller 注入，指向 .spec 文件所在目录（即项目根目录），
# 这样打包配置就不会绑定到某台机器的绝对路径。
project_root = os.path.abspath(SPECPATH)

a = Analysis(
    ['run.py'],  # 入口文件
    pathex=[project_root],  # 项目根目录
    binaries=[],
    datas=[
        # 静态资源和模板目录（相对路径，与入口文件同目录）
        ('game/static', 'game/static'),
        ('game/templates', 'game/templates'),
    ],
    hiddenimports=[
        'config',
        'game.models.user',
        'game.models.NPC',
        'game.routes.login',
        'game.routes.play',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='run',  # 可执行文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用UPX压缩（可选，需安装UPX）
    console=True,  # 显示控制台（调试用，发布时可设为False）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run',  # 输出目录名（与exe名一致）
)