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
from core.tortazo.exceptions.PluginException import PluginException

class deepWebDirBruterPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = deepWebDirBruterPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    def test_dirBruterOnRelay(self):
        print "Testing dirBruterOnRelay with args: site=%s " %(unittests.dirBruter_urlSite)
        self.assertRaises(PluginException, self.plugin.dirBruterOnRelay, site=unittests.dirBruter_urlSite)

        print "Testing dirBruterOnRelay with args: site=%s " %(None)
        self.assertRaises(PluginException, self.plugin.dirBruterOnRelay, site=None)

    def test_dirBruterOnAllRelays(self):
        print "Testing dirBruterOnRelay with args: port=%s " %(str(unittests.dirBruter_portInvalid))
        self.assertRaises(PluginException, self.plugin.dirBruterOnAllRelays, port=unittests.dirBruter_portInvalid)

        print "Testing dirBruterOnRelay with args: port=%s " %(None)
        self.assertRaises(PluginException, self.plugin.dirBruterOnAllRelays, port=None)


    def test_dirBruterOnHiddenService(self):
        print "Testing dirBruterOnHiddenService with args: hiddenService=%s " %(unittests.dirBruter_onionserviceInvalid)
        self.assertRaises(PluginException, self.plugin.dirBruterOnHiddenService, hiddenService=unittests.dirBruter_onionserviceInvalid)

        print "Testing dirBruterOnHiddenService with args: hiddenService=%s " %(None)
        self.assertRaises(PluginException, self.plugin.dirBruterOnHiddenService, hiddenService=None)

if __name__ == '__main__':
    unittest.main()
