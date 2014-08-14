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

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from config import config
from pynessus.rest.client.NessusClient import NessusClient
from pynessus.rest.data.NessusStructure import NessusConverter
from plugins.texttable import Texttable
import requests
import sys
import unittest

class nessusPluginTest(unittest.TestCase):

    def __init__(self):
        self.plugin = heartBleedPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        reference.setPluginArguments(self.pluginArgs)
        reference.processPluginArguments()

    def feed(self):
        pass

    def serverSecureSettingsList(self):
        pass

    def serverSecureSettings(self):
        pass

    def serverUpdate(self):
        pass

    def serverRegister(self, nessusCode):
        pass

    def serverLoad(self):
        pass

    def serverUuid(self):
        pass

    def userAdd(self, userName, password, admin=1):
        pass        

    def userEdit(self, userName, password, admin=1):
        pass

    def userDelete(self, userName):
        pass

    def userChpasswd(self, userName, password):
        pass

    def usersList(self):
        pass

    def pluginsList(self):
        pass

    def pluginAttributesList(self):
        pass

    def pluginListsFamily(self, familyName):
        pass

    def pluginDescription(self, fileNamePlugin):
        pass

    def pluginsAttributesFamilySearch(self, filter0Quality, filterSearchType, filter0Value, filter0Filter):
        pass

    def pluginsAttributesPluginSearch(self, filter0quality, filterSearchType, filter0Value, filter0Filter, family):
        pass

    def pluginsMd5(self):
        pass
    
    def policyPreferencesList(self):
        pass

    def policyList(self):
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

    def scanList(self):
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

    def reportList(self):
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
