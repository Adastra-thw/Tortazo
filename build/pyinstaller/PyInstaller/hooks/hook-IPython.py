#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


from hookutils import collect_data_files


# IPython (tested with 0.13) requires the following files:
#   ./site-packages/IPython/config/profile/README_STARTUP
datas = collect_data_files('IPython')
