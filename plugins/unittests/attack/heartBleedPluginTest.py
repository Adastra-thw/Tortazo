# coding=utf-8
'''
Created on 13/08/2014

#Author: Adastra.
#twitter: @jdaanial

heartBleedPluginTest.py

heartBleedPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

heartBleedPluginTest is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from plugins.attack.heartBleedPlugin import heartBleedPlugin
from config import config
from config import unittests 
import unittest
from core.tortazo.exceptions.PluginException import PluginException

class heartBleedPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = heartBleedPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    def test_setTarget(self):
        print "Testing setTarget with args: relayIp=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setTarget, relayIp=None)
        print "Testing setTarget with args: relayIp=%s " %("INVALID_IP")
        self.assertRaises(PluginException, self.plugin.setTarget, relayIp='INVALID_IP')
        print "Testing setTarget with args: relayIp=%s " %('87.11.2.145')
        self.assertTrue(self.plugin.setTarget(relayIp='87.11.2.145'))
        print "Testing startAttack "
        self.assertTrue(self.plugin.startAttack() )

    def test_setTargetWithPort(self):
        print "Testing setTargetWithPort with args: relayIp=%s , relayPort=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.setTargetWithPort, None, None)
        print "Testing setTargetWithPort with args: relayIp=%s , relayPort=%s" %('INVALID_IP', 'INVALID PORT')
        self.assertRaises(PluginException, self.plugin.setTargetWithPort, 'INVALID_IP', 'INVALID PORT')
        print "Testing setTargetWithPort with args: relayIp=%s , relayPort=%s" %('INVALID_IP', "80")
        self.assertRaises(Exception, self.plugin.setTargetWithPort, 'INVALID_IP', 80)
        print "Testing setTargetWithPort with args: relayIp=%s , relayPort=%s" %('87.11.2.145', 'INVALID_PORT')
        self.assertRaises(Exception, self.plugin.setTargetWithPort, '87.11.2.145', 'INVALID_PORT')
        print "Testing setTargetWithPort with args: relayIp=%s , relayPort=%s" %('87.11.2.145', '80')
        self.assertTrue(self.plugin.setTargetWithPort('87.11.2.145', 80))
        print "Testing startAttackAllRelays "
        self.assertTrue(self.plugin.startAttackAllRelays() )

if __name__ == '__main__':
    unittest.main()
