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
from core.tortazo.exceptions.PluginException import PluginException

class nessusPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = nessusPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    

    def test_serverRegister(self):
        print "Testing serverRegister with args: nessusCode=%s " %(None)
        self.assertRaises(PluginException, self.plugin.serverRegister, nessusCode=None)

        print "Testing serverRegister with args: nessusCode=%s " %(unittests.nessus_codeInvalid)
        self.assertRaises(PluginException, self.plugin.serverRegister, nessusCode=unittests.nessus_codeInvalid)

    
    def test_userAdd(self):
        print "Testing userAdd with args: userName=%s , password=%s , admin=%s" %(unittests.nessus_userNameInvalid, '', '')
        self.assertRaises(PluginException, self.plugin.userAdd, userName=unittests.nessus_userNameInvalid, password='', admin='')

        print "Testing userAdd with args:  userName=%s , password=%s , admin=%s" %(None, None, None)
        self.assertRaises(PluginException, self.plugin.userAdd, userName=None, password=None, admin=None )

    def test_userEdit(self):
        print "Testing userEdit with args: userName=%s , password=%s , admin=%s " %(unittests.nessus_userNameInvalid, '', '')
        self.assertRaises(PluginException, self.plugin.userEdit, userName=unittests.nessus_userNameInvalid, password='', admin='')

        print "Testing userEdit with args: userName=%s , password=%s , admin=%s " %(None, None, None)
        self.assertRaises(PluginException, self.plugin.userEdit, userName=None, password=None, admin=None )

    def test_userDelete(self):
        print "Testing userDelete with args: userName=%s  " %('')
        self.assertRaises(PluginException, self.plugin.userDelete, userName='')

        print "Testing userDelete with args: userName=%s " %(None)
        self.assertRaises(PluginException, self.plugin.userDelete, userName=None)


    def test_userChpasswd(self):
        print "Testing userChpasswd with args: userName=%s , password=%s " %(unittests.nessus_userNameInvalid, '')
        self.assertRaises(PluginException, self.plugin.userChpasswd, userName=unittests.nessus_userNameInvalid, password='')

        print "Testing userChpasswd with args: userName=%s , password=%s " %(None, None)
        self.assertRaises(PluginException, self.plugin.userChpasswd, userName=None, password=None )


    def test_pluginListsFamily(self):
        print "Testing pluginListsFamily with args: familyName=%s" %('')
        self.assertRaises(PluginException, self.plugin.pluginListsFamily, familyName='')

        print "Testing pluginListsFamily with args: familyName=%s" %(None)
        self.assertRaises(PluginException, self.plugin.pluginListsFamily, familyName=None )


    def test_pluginDescription(self):
        print "Testing pluginDescription with args: fileNamePlugin=%s" %('')
        self.assertRaises(PluginException, self.plugin.pluginDescription, fileNamePlugin='')

        print "Testing pluginDescription with args: fileNamePlugin=%s" %(None)
        self.assertRaises(PluginException, self.plugin.pluginDescription, fileNamePlugin=None )

    def test_policyDelete(self):
        print "Testing policyDelete with args: policyId=%s" %(str(unittests.nessus_policyId))
        self.assertRaises(PluginException, self.plugin.policyDelete, policyId=unittests.nessus_policyId)

        print "Testing policyDelete with args: policyId=%s" %(None)
        self.assertRaises(PluginException, self.plugin.policyDelete, policyId=None )

    def test_policyCopy(self):
        print "Testing policyCopy with args: policyId=%s" %(str(unittests.nessus_policyId))
        self.assertRaises(PluginException, self.plugin.policyCopy, policyId=unittests.nessus_policyId)

        print "Testing policyCopy with args: policyId=%s" %(None)
        self.assertRaises(PluginException, self.plugin.policyCopy, policyId=None )


    def test_policyDownload(self):
        print "Testing policyDownload with args: policyId=%s , fileName=%s" %(str(unittests.nessus_policyId), '')
        self.assertRaises(PluginException, self.plugin.policyDownload, policyId=unittests.nessus_policyId, fileName=None)

        print "Testing policyDownload with args: policyId=%s , fileName=%s" %(None,None)
        self.assertRaises(PluginException, self.plugin.policyDownload, policyId=None, fileName=None)


    def test_scanAllRelays(self):
        print "Testing scanAllRelays with args: policyId=%s , scanName=%s" %(str(unittests.nessus_policyId), '')
        self.assertRaises(PluginException, self.plugin.scanAllRelays, policyId=unittests.nessus_policyId, scanName='')

        print "Testing scanAllRelays with args: policyId=%s , scanName=%s" %(None,None)
        self.assertRaises(PluginException, self.plugin.scanAllRelays, policyId=None, scanName=None)


    def test_scanByRelay(self):
        print "Testing scanByRelay with args: policyId=%s , scanName=%s , relay=%s" %(str(unittests.nessus_policyId), '', unittests.nessus_relayInvalid)
        self.assertRaises(PluginException, self.plugin.scanByRelay, policyId=unittests.nessus_policyId, scanName='', relay=unittests.nessus_relayInvalid)

        print "Testing scanByRelay with args: policyId=%s , scanName=%s , relay=%s" %(None,None,None)
        self.assertRaises(PluginException, self.plugin.scanByRelay, policyId=None, scanName=None, relay=None)
    
    def test_scanStop(self):
        print "Testing scanStop with args: scanUuid=%s" %('')
        self.assertRaises(PluginException, self.plugin.scanStop, scanUuid='')

        print "Testing scanStop with args: scanUuid=%s" %(None)
        self.assertRaises(PluginException, self.plugin.scanStop, scanUuid=None )

    def test_scanResume(self):
        print "Testing scanResume with args: scanUuid=%s" %('')
        self.assertRaises(PluginException, self.plugin.scanResume, scanUuid='')

        print "Testing scanResume with args: scanUuid=%s" %(None)
        self.assertRaises(PluginException, self.plugin.scanResume, scanUuid=None )

    def test_scanPause(self):
        print "Testing scanPause with args: scanUuid=%s" %('')
        self.assertRaises(PluginException, self.plugin.scanPause, scanUuid='')

        print "Testing scanPause with args: scanUuid=%s" %(None)
        self.assertRaises(PluginException, self.plugin.scanPause, scanUuid=None )

    def test_scanTemplateAllRelays(self):
        print "Testing scanTemplateAllRelays with args: policyId=%s , templateName=%s" %(str(unittests.nessus_policyId), '')
        self.assertRaises(PluginException, self.plugin.scanTemplateAllRelays, policyId=unittests.nessus_policyId, templateName='')

        print "Testing scanTemplateAllRelays with args: policyId=%s , templateName=%s" %(None,None)
        self.assertRaises(PluginException, self.plugin.scanTemplateAllRelays, policyId=None, templateName=None)


    def test_scanTemplateByRelay(self):
        print "Testing scanTemplateByRelay with args: policyId=%s , templateName=%s , relay=%s" %(str(unittests.nessus_policyId), '', unittests.nessus_relayInvalid)
        self.assertRaises(PluginException, self.plugin.scanTemplateByRelay, policyId=unittests.nessus_policyId, templateName='', relay=unittests.nessus_relayInvalid)

        print "Testing scanTemplateByRelay with args: policyId=%s , templateName=%s , relay=%s" %(None,None,None)
        self.assertRaises(PluginException, self.plugin.scanTemplateByRelay, policyId=None, templateName=None, relay=None)



    def test_scanTemplateEditAllRelays(self):
        print "Testing scanTemplateEditAllRelays with args: templateEdit=%s , templateNewName=%s , policyId=%s" %('','',str(unittests.nessus_policyId))
        self.assertRaises(PluginException, self.plugin.scanTemplateEditAllRelays, templateEdit='', templateNewName='', policyId=unittests.nessus_policyId)

        print "Testing scanTemplateEditAllRelays with args: templateEdit=%s , templateNewName=%s , policyId=%s" %(None,None,None)
        self.assertRaises(PluginException, self.plugin.scanTemplateEditAllRelays, templateEdit=None , templateNewName=None, policyId=None)

    def test_scanTemplateEditByRelay(self):
        print "Testing scanTemplateEditByRelay with args: templateEdit=%s , templateNewName=%s , policyId=%s , relay=%s" %('','',str(unittests.nessus_policyId), unittests.nessus_relayInvalid)
        self.assertRaises(PluginException, self.plugin.scanTemplateEditByRelay, templateEdit='', templateNewName='', policyId=unittests.nessus_policyId,  relay=unittests.nessus_relayInvalid)

        print "Testing scanTemplateEditByRelay with args: templateEdit=%s , templateNewName=%s , policyId=%s , relay=%s" %(None,None,None,None)
        self.assertRaises(PluginException, self.plugin.scanTemplateEditByRelay, templateEdit=None , templateNewName=None, policyId=None, relay=None)

    def test_scanTemplateDelete(self):
        print "Testing scanTemplateDelete with args: templateUuid=%s" %('')
        self.assertRaises(PluginException, self.plugin.scanTemplateDelete, templateUuid='')

        print "Testing scanTemplateDelete with args: templateUuid=%s" %(None)
        self.assertRaises(PluginException, self.plugin.scanTemplateDelete, templateUuid=None )


    def test_scanTemplateLaunch(self):
        print "Testing scanTemplateLaunch with args: templateName=%s" %('')
        self.assertRaises(PluginException, self.plugin.scanTemplateLaunch, templateName='')

        print "Testing scanTemplateLaunch with args: templateName=%s" %(None)
        self.assertRaises(PluginException, self.plugin.scanTemplateLaunch, templateName=None )

    def test_reportDelete(self):
        print "Testing reportDelete with args: reportUuid=%s" %('')
        self.assertRaises(PluginException, self.plugin.reportDelete, reportUuid='')

        print "Testing reportDelete with args: reportUuid=%s" %(None)
        self.assertRaises(PluginException, self.plugin.reportDelete, reportUuid=None )

    def test_reportHosts(self):
        print "Testing reportHosts with args: reportUuid=%s" %('')
        self.assertRaises(PluginException, self.plugin.reportHosts, reportUuid='')

        print "Testing reportHosts with args: reportUuid=%s" %(None)
        self.assertRaises(PluginException, self.plugin.reportHosts, reportUuid=None )

    def test_reportPorts(self):
        print "Testing reportPorts with args: reportUuid=%s, hostname=%s" %('','')
        self.assertRaises(PluginException, self.plugin.reportPorts, reportUuid='', hostname='')

        print "Testing reportPorts with args: reportUuid=%s, hostname=%s" %(None,None)
        self.assertRaises(PluginException, self.plugin.reportPorts, reportUuid=None , hostname=None)


    def test_reportDetails(self):
        print "Testing reportDetails with args: reportUuid=%s, hostname=%s, port=%s , protocol=%s" %('','',unittests.nessus_portInvalid,'')
        self.assertRaises(PluginException, self.plugin.reportDetails, reportUuid='', hostname='', port=unittests.nessus_portInvalid , protocol='')

        print "Testing reportDetails with args: reportUuid=%s, hostname=%s, port=%s , protocol=%s" %(None,None,None,None)
        self.assertRaises(PluginException, self.plugin.reportDetails, reportUuid=None , hostname=None, port=None, protocol=None)


    def test_reportTags(self):
        print "Testing reportTags with args: reportUuid=%s, hostname=%s" %('','')
        self.assertRaises(PluginException, self.plugin.reportTags, reportUuid='', hostname='')

        print "Testing reportTags with args: reportUuid=%s, hostname=%s" %(None,None)
        self.assertRaises(PluginException, self.plugin.reportTags, reportUuid=None , hostname=None)


    def test_reportAttributesList(self):
        print "Testing reportAttributesList with args: reportUuid=%s" %('')
        self.assertRaises(PluginException, self.plugin.reportAttributesList, reportUuid='')

        print "Testing reportAttributesList with args: reportUuid=%s" %(None)
        self.assertRaises(PluginException, self.plugin.reportAttributesList, reportUuid=None )

if __name__ == '__main__':
    unittest.main()