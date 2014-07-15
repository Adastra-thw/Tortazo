#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


import ctypes.util
import os

from PyInstaller.depend.utils import _resolveCtypesImports
from PyInstaller.compat import is_cygwin


# Include glob for library lookup in run-time hook.
hiddenimports = ['glob']


# This method will try to resolve your libusb libraries in the
# following orders:
#
#   libusb-1.0, libusb-0.1, openusb
#
# NOTE: Mind updating run-time hook when adding further libs.
libusb_candidates = (
    # libusb10
    'usb-1.0', 'usb', 'libusb-1.0',
    # libusb01
    'usb-0.1', 'libusb0',
    # openusb
    'openusb',
)


def hook(mod):
    for candidate in libusb_candidates:
        libname = ctypes.util.find_library(candidate)
        if libname is not None:
            break

    if libname is not None:
        # Use basename here because Python returns full library path
        # on Mac OSX when using ctypes.util.find_library.
        bins = [os.path.basename(libname)]
        mod.binaries.extend(_resolveCtypesImports(bins))
    elif is_cygwin:
        bins = ['cygusb-1.0-0.dll', 'cygusb0.dll']
        mod.binaries.extend(_resolveCtypesImports(bins)[0:1])

    return mod
