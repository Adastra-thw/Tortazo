# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

shodanPluginTest.py

shodanPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

shodanPluginTest is distributed in the hope that it will be useful,
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
from plugins.infogathering.shodanPlugin import shodanPlugin
from config import unittests
from config import config
from core.tortazo.exceptions.PluginException import PluginException

class shodanPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = shodanPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()
        
    def test_setApiKey(self):
        print "Testing setApiKey with args: apiKey=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setApiKey, apiKey=None)

        print "Testing setApiKey with args: apiKey=%s " %(unittests.shodan_apiKeyInvalid)
        self.assertRaises(PluginException, self.plugin.setApiKey, apiKey=unittests.shodan_apiKeyInvalid)


    def test_setApiKeyFile(self):
        print "Testing setApiKeyFile with args: apiKeyFile=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setApiKeyFile, apiKeyFile=None)

        print "Testing setApiKeyFile with args: apiKeyFile=%s " %(unittests.shodan_apiKeyFileInvalid)
        self.assertRaises(PluginException, self.plugin.setApiKeyFile, apiKeyFile=unittests.shodan_apiKeyFileInvalid)


    def test_basicSearchQuery(self):
        print "Testing basicSearchQuery with args: basicSearch=%s , limit=%s " %(unittests.shodan_basicSearchInvalid, unittests.shodan_invalidLimit)
        self.assertRaises(PluginException, self.plugin.basicSearchQuery, basicSearch=unittests.shodan_basicSearchInvalid, limit=unittests.shodan_invalidLimit)

        print "Testing basicSearchQuery with args: basicSearch=%s , limit=%s " %(None, None)
        self.assertRaises(PluginException, self.plugin.basicSearchQuery, basicSearch=None, limit=None)


    def test_basicSearchAllRelays(self):
        print "Testing basicSearchAllRelays with args: basicSearch=%s " %(unittests.shodan_basicSearchInvalid)
        self.assertRaises(PluginException, self.plugin.basicSearchAllRelays, basicSearch=unittests.shodan_basicSearchInvalid)

        print "Testing basicSearchAllRelays with args: basicSearch=%s " %(None)
        self.assertRaises(PluginException, self.plugin.basicSearchAllRelays, basicSearch=None)


    def test_basicSearchByRelay(self):
        print "Testing basicSearchByRelay with args: basicSearch=%s relay=%s" %(unittests.shodan_basicSearchInvalid, unittests.shodan_relayInvalid)
        self.assertRaises(PluginException, self.plugin.basicSearchByRelay, basicSearch=unittests.shodan_basicSearchInvalid, relay=unittests.shodan_relayInvalid)

        print "Testing basicSearchByRelay with args: basicSearch=%s relay=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.basicSearchByRelay, basicSearch=None, relay=None)


    def test_basicSearchByNickname(self):
        print "Testing basicSearchByNickname with args: basicSearch=%s , nickname=%s " %(unittests.shodan_basicSearchInvalid, unittests.shodan_nickNameInvalid)
        self.assertRaises(PluginException, self.plugin.basicSearchByNickname, basicSearch=unittests.shodan_basicSearchInvalid, nickname=unittests.shodan_nickNameInvalid)

        print "Testing basicSearchByNickname with args: basicSearch=%s nickname=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.basicSearchByNickname, basicSearch=None, nickname=None)


if __name__ == '__main__':
    unittest.main()
