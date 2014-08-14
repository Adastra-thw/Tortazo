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

from plugins.attack.heartBleedPlugin import heartBleedPlugin
from config import config
from config import unittests 
import unittest

class heartBleedPluginTest(unittest.TestCase):

    def __init__(self):
        self.plugin = heartBleedPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        reference.setPluginArguments(self.pluginArgs)
        reference.processPluginArguments()

    def test_setTarget(self):
        self.assertRaises(Exception, self.plugin.setTarget, None)
        self.assertRaises(Exception, self.plugin.setTarget, 'INVALID_IP')
        self.assertRaises(Exception, self.plugin.setTarget, '87.11.2.145')

    def test_setTargetWithPort(self):
        self.assertRaises(Exception, self.plugin.setTargetWithPort, None, None)
        self.assertRaises(Exception, self.plugin.setTargetWithPort, 'INVALID_IP', 'INVALID PORT')
        self.assertRaises(Exception, self.plugin.setTargetWithPort, 'INVALID_IP', 80)
        self.assertRaises(Exception, self.plugin.setTargetWithPort, '87.11.2.145', 'INVALID_PORT')
        self.assertRaises(Exception, self.plugin.setTargetWithPort, '87.11.2.145', 80)

    def test_startAttack(self):
        self.assertRaises(Exception, self.plugin.startAttack, )

    def test_startAttackAllRelays(self):
        self.assertRaises(Exception, self.plugin.startAttackAllRelays, )

if __name__ == '__main__':
    unittest.main()
