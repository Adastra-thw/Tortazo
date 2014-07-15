#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


attrs = [('notamodule','')]
def hook(mod):
    import os, sys, marshal
    other = os.path.join(mod.__path__[0], '../pkg2/__init__.pyc')
    if os.path.exists(other):
        co = marshal.loads(open(other,'rb').read()[8:])
    else:
        co = compile(open(other[:-1],'rU').read()+'\n', other, 'exec')
    mod.__init__(mod.__name__, other, co)
    mod.__path__.append(os.path.join(mod.__path__[0], 'extra'))
    return mod
