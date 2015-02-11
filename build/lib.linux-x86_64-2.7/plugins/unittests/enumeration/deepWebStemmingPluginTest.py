# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

deepWebStemmingPluginTest.py

deepWebStemmingPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

deepWebStemmingPluginTest is distributed in the hope that it will be useful,
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
from plugins.enumeration.deepWebStemmingPlugin import deepWebStemmingPlugin
from config import unittests
from config import config
from core.tortazo.exceptions.PluginException import PluginException

class deepWebStemmingPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = deepWebStemmingPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    def test_simpleStemmingAllRelays(self):
        print "Testing simpleStemmingAllRelays with args: queryTerms=%s , port=%s " %(unittests.stemming_queryTerms, str(unittests.stemming_portInvalid))
        self.assertRaises(PluginException, self.plugin.simpleStemmingAllRelays, queryTerms=unittests.stemming_queryTerms ,port=unittests.stemming_portInvalid)

        print "Testing simpleStemmingAllRelays with args: queryTerms=%s , port=%s " %(None, None)
        self.assertRaises(PluginException, self.plugin.simpleStemmingAllRelays, queryTerms=None, port=None)

    
    def test_stemmingHiddenService(self):
        print "Testing stemmingHiddenService with args: queryTerms=%s , onionSite=%s " %(unittests.stemming_queryTerms , unittests.stemming_onionserviceInvalid)
        self.assertRaises(PluginException, self.plugin.stemmingHiddenService, queryTerms=unittests.stemming_queryTerms , onionSite=unittests.stemming_onionserviceInvalid)

        print "Testing stemmingHiddenService with args: queryTerms=%s , onionSite=%s " %(None , None)
        self.assertRaises(PluginException, self.plugin.stemmingHiddenService, queryTerms=None , onionSite=None)


if __name__ == '__main__':
    unittest.main()
