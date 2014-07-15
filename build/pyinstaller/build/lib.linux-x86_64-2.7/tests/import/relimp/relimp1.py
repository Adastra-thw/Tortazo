#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


from __future__ import absolute_import

name = 'relimp.relimp1'

from . import relimp2 as upper
from . relimp import relimp2 as lower

assert upper.name == 'relimp.relimp2'
assert lower.name == 'relimp.relimp.relimp2'

if upper.__name__ == lower.__name__:
    raise SystemExit("Imported the same module")

if upper.__file__ == lower.__file__:
    raise SystemExit("Imported the same file")
