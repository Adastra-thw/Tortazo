#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


# Compare attributes of ElementTree (cElementTree) module from frozen executable
# with ElementTree (cElementTree) module from standard python.


import copy
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
import xml.etree.cElementTree as cET


if hasattr(sys, 'frozen'):
    # In frozen mode current working dir is the path with final executable.
    _pyexe_file = os.path.join('..', '..', 'python_exe.build')
else:
    _pyexe_file = 'python_exe.build'

_lines = open(_pyexe_file).readlines()
_pyexe = _lines[0].strip()
_env_path = _lines[2].strip()


def exec_python(pycode):
    """
    Wrap running python script in a subprocess.

    Return stdout of the invoked command.
    """
    # Environment variable 'PATH' has to be defined on Windows.
    # Otherwise dynamic library pythonXY.dll cannot be found by
    # Python executable.
    env = copy.deepcopy(os.environ)
    env['PATH'] = _env_path
    out = subprocess.Popen([_pyexe, '-c', pycode], env=env,
        stdout=subprocess.PIPE, shell=False).stdout.read()

    return out.strip()


def compare(test_name, expect, frozen):
    # PyInstaller sets attribute '__lodader'. Remove this attribute from the
    # module properties.
    frozen.remove('__loader__')
    frozen = str(frozen)

    print(test_name)
    print('  Attributes expected: ' + expect)
    print('  Attributes current:  ' + frozen)
    print('')
    # Compare attributes of frozen module with unfronzen module.
    if not frozen == expect:
        raise SystemExit('Frozen module has no same attribuses as unfrozen.')


## Pure Python module.
_expect = exec_python('import xml.etree.ElementTree as ET; print dir(ET)')
_frozen = dir(ET)
compare('ElementTree', _expect, _frozen)


## C-extension Python module.
_expect = exec_python('import xml.etree.cElementTree as cET; print dir(cET)')
_frozen = dir(cET)
compare('cElementTree', _expect, _frozen)
