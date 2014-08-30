# -*- mode: python -*-

block_cipher = None


a = Analysis(['Tortazo11.py'],
             pathex=['/home/adastra/Escritorio/Tortazo'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          Tree('db', prefix='db'),
	  Tree('templates', prefix='templates'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Tortazo',
          debug=False,
          strip=None,
          upx=True,
          console=True )
