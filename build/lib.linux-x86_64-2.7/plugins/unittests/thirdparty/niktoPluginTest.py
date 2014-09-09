# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

niktoPluginTest.py

niktoPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

niktoPluginTest is distributed in the hope that it will be useful,
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
from plugins.thirdparty.niktoPlugin import niktoPlugin
from config import unittests
from config import config


class niktoPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = niktoPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    
    def executeByIP(self, ipAddress, switches):
        pass
    
    def executeAll(self, switches):
        pass

    def executeAllOnPort(self, port, switches):
        pass

    def executeByNickname(self, nickname, switches):
        pass

    def executeByIPOnPort(self, ipAddress, port, switches):
        pass

if __name__ == '__main__':
    unittest.main()
