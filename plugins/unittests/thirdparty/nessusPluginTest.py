# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

nessusPluginTest.py

nessusPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

nessusPluginTest is distributed in the hope that it will be useful,
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
from plugins.thirdparty.nessusPlugin import nessusPlugin
from config import unittests
from config import config

class nessusPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = nessusPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    

    def serverRegister(self, nessusCode):
        pass

    
    def userAdd(self, userName, password, admin=1):
        pass        

    def userEdit(self, userName, password, admin=1):
        pass

    def userDelete(self, userName):
        pass

    def userChpasswd(self, userName, password):
        pass

    def pluginListsFamily(self, familyName):
        pass

    def pluginDescription(self, fileNamePlugin):
        pass

    def policyDelete(self, policyId):
        pass

    def policyCopy(self, policyId):
        pass

    def policyDownload(self, policyId, fileName):
        pass

    def scanAllRelays(self, policyId, scanName):
        pass

    def scanByRelay(self, policyId, scanName, relay):
        pass
    
    def scanStop(self, scanUuid):
        pass

    def scanResume(self, scanUuid):
        pass

    def scanPause(self, scanUuid):
        pass

    def scanTemplateAllRelays(self, policyId, templateName):
        pass

    def scanTemplateByRelay(self,policyId,relay,templateName):
        pass


    def scanTemplateEditAllRelays(self, templateEdit, templateNewName, policyId):
        pass            

    def scanTemplateEditByRelay(self,templateEdit, templateNewName, policyId, relay):
        pass

    def scanTemplateDelete(self, templateUuid):
        pass

    def scanTemplateLaunch(self, templateName):
        pass

    def reportDelete(self, reportUuid):
        pass

    def reportHosts(self,reportUuid):
        pass

    def reportPorts(self, reportUuid, hostname):
        pass

    def reportDetails(self,reportUuid, hostname,port,protocol):
        pass

    def reportTags(self, reportUuid, hostname):
        pass

    def reportAttributesList(self,reportUuid):
        pass

if __name__ == '__main__':
    unittest.main()
