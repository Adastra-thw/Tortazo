# -*- mode: python -*-
a = Analysis(['Tortazo.py'],
             pathex=['/media/MyPassword/Subigo Inimicus/Projects/THW/ACTUAL/Presentation/GITRepo-Adastra-thw/TortazoV1.1/Tortazo'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Tortazo',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='Tortazo')
