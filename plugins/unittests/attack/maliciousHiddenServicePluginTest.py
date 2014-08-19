# coding=utf-8
'''
Created on 13/08/2014

#Author: Adastra.
#twitter: @jdaanial

maliciousHiddenServicePluginTest.py

maliciousHiddenServicePluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

maliciousHiddenServicePluginTest is distributed in the hope that it will be useful,
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


from plugins.attack.maliciousHiddenServicePlugin import maliciousHiddenServicePlugin
from core.tortazo.exceptions.PluginException import PluginException
from config import unittests
from config import config
import unittest

class maliciousHiddenServicePluginTest(unittest.TestCase):
    
    def __init__(self):
        self.plugin = maliciousHiddenServicePlugin()
        self.pluginArgs = []        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()



    def test_startHTTPHiddenService(self):
        print "Testing startHTTPHiddenService with args: serviceDir=%s " %(None)
        self.assertRaises(PluginException, self.plugin.startHTTPHiddenService, serviceDir=None)



        self.assertRaises(Exception, self.plugin.startHTTPHiddenService, serviceDir=unittests.maliciousHiddenServicePlugin_serviceDir)
        self.assertRaises(Exception, self.plugin.startHTTPHiddenService, servicePort=None)
        self.assertRaises(Exception, self.plugin.startHTTPHiddenService, servicePort=unittests.maliciousHiddenServicePlugin_servicePort)
        self.assertRaises(Exception, self.plugin.startHTTPHiddenService, hiddenserviceDir=None)
        self.assertRaises(Exception, self.plugin.startHTTPHiddenService, hiddenserviceDir=unittests.maliciousHiddenServicePlugin_hsserviceDir)
        self.assertRaises(Exception, self.plugin.startHTTPHiddenService, hiddenservicePort=None)
        self.assertRaises(Exception, self.plugin.startHTTPHiddenService, hiddenservicePort=unittests.maliciousHiddenServicePlugin_hsservicePort)  
