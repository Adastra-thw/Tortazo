# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

deepWebDirBruterPluginTest.py

deepWebDirBruterPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

deepWebDirBruterPluginTest is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import os
import  sys
import unittest
from plugins.enumeration.deepWebDirBruterPlugin import deepWebDirBruterPlugin
from config import unittests
from config import config

class deepWebDirBruterPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = deepWebDirBruterPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    def dirBruterOnRelay(self, site, dictFile='', proxy=False):
        pass

    def dirBruterOnAllRelays(self, port=80, dictFile=''):
        pass

    def dirBruterOnHiddenService(self, hiddenService, dictFile=''):
        pass

if __name__ == '__main__':
    unittest.main()
