# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

w3afPluginTest.py

w3afPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3afPluginTest is distributed in the hope that it will be useful,
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
from plugins.thirdparty.w3afPlugin import w3afPlugin
from config import unittests
from config import config
from core.tortazo.exceptions.PluginException import PluginException


class w3afPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = w3afPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    def test_showPluginsByType(self):
        print "Testing showPluginsByType with args: pluginType=%s " %(None)
        self.assertRaises(PluginException, self.plugin.showPluginsByType, pluginType=None)

        print "Testing showPluginsByType with args: pluginType=%s " %(unittests.w3af_invalidPluginType)
        self.assertRaises(PluginException, self.plugin.showPluginsByType, pluginType=unittests.w3af_invalidPluginType)


    def test_getEnabledPluginsByType(self):
        print "Testing getEnabledPluginsByType with args: pluginType=%s " %(None)
        self.assertRaises(PluginException, self.plugin.getEnabledPluginsByType, pluginType=None)

        print "Testing getEnabledPluginsByType with args: pluginType=%s " %(unittests.w3af_invalidPluginType)
        self.assertRaises(PluginException, self.plugin.getEnabledPluginsByType, pluginType=unittests.w3af_invalidPluginType)


    def test_getPluginTypeDescription(self):
        print "Testing getPluginTypeDescription with args: pluginType=%s " %(None)
        self.assertRaises(PluginException, self.plugin.getPluginTypeDescription, pluginType=None)

        print "Testing getPluginTypeDescription with args: pluginType=%s " %(unittests.w3af_invalidPluginType)
        self.assertRaises(PluginException, self.plugin.getPluginTypeDescription, pluginType=unittests.w3af_invalidPluginType)


    def test_enablePlugin(self):
        print "Testing enablePlugin with args: pluginType=%s , pluginName=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.enablePlugin, pluginType=None, pluginName=None)

        print "Testing enablePlugin with args: pluginType=%s , pluginName=%s" %(unittests.w3af_invalidPluginType , unittests.w3af_invalidPluginName)
        self.assertRaises(PluginException, self.plugin.enablePlugin, pluginType=unittests.w3af_invalidPluginType, pluginName=unittests.w3af_invalidPluginName)

    def test_disablePlugin(self):
        print "Testing disablePlugin with args: pluginType=%s , pluginName=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.disablePlugin, pluginType=None, pluginName=None)

        print "Testing disablePlugin with args: pluginType=%s , pluginName=%s" %(unittests.w3af_invalidPluginType , unittests.w3af_invalidPluginName)
        self.assertRaises(PluginException, self.plugin.disablePlugin, pluginType=unittests.w3af_invalidPluginType, pluginName=unittests.w3af_invalidPluginName)


    def test_enableAllPlugins(self):
        print "Testing enableAllPlugins with args: pluginType=%s " %(None)
        self.assertRaises(PluginException, self.plugin.enableAllPlugins, pluginType=None)

        print "Testing enableAllPlugins with args: pluginType=%s " %(unittests.w3af_invalidPluginType)
        self.assertRaises(PluginException, self.plugin.enableAllPlugins, pluginType=unittests.w3af_invalidPluginType)


    def test_disableAllPlugins(self):
        print "Testing disableAllPlugins with args: pluginType=%s " %(None)
        self.assertRaises(PluginException, self.plugin.disableAllPlugins, pluginType=None)

        print "Testing disableAllPlugins with args: pluginType=%s " %(unittests.w3af_invalidPluginType)
        self.assertRaises(PluginException, self.plugin.disableAllPlugins, pluginType=unittests.w3af_invalidPluginType)


    def test_getPluginOptions(self):
        print "Testing getPluginOptions with args: pluginType=%s , pluginName=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.getPluginOptions, pluginType=None, pluginName=None)

        print "Testing getPluginOptions with args: pluginType=%s , pluginName=%s" %(unittests.w3af_invalidPluginType , unittests.w3af_invalidPluginName)
        self.assertRaises(PluginException, self.plugin.getPluginOptions, pluginType=unittests.w3af_invalidPluginType, pluginName=unittests.w3af_invalidPluginName)


    def test_setPluginOptions(self):
        print "Testing getPluginOptions with args: pluginType=%s , pluginName=%s , pluginSettingType=%s, pluginSetting=%s, pluginSettingValue=%s" %(None, None, None, None, None)
        self.assertRaises(PluginException, self.plugin.setPluginOptions, pluginType=None, pluginName=None, pluginSettingType=None, pluginSetting=None, pluginSettingValue=None)

        print "Testing getPluginOptions with args: pluginType=%s , pluginName=%s" %(unittests.w3af_invalidPluginType , unittests.w3af_invalidPluginName)
        self.assertRaises(PluginException, self.plugin.setPluginOptions, pluginType=unittests.w3af_invalidPluginType,
                                                                         pluginName=unittests.w3af_invalidPluginName,
                                                                         pluginSettingType=unittests.w3af_invalidSettingType,
                                                                         pluginSetting=unittests.w3af_invalidSetting,
                                                                         pluginSettingValue=unittests.w3af_invalidSettingValue)


    def test_getPluginStatus(self):
        print "Testing getPluginStatus with args: pluginType=%s , pluginName=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.getPluginStatus, pluginType=None, pluginName=None)

        print "Testing getPluginStatus with args: pluginType=%s , pluginName=%s" %(unittests.w3af_invalidPluginType , unittests.w3af_invalidPluginName)
        self.assertRaises(PluginException, self.plugin.getPluginStatus, pluginType=unittests.w3af_invalidPluginType, pluginName=unittests.w3af_invalidPluginName)


    def test_setTarget(self):
        print "Testing setTarget with args: url=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setTarget, url=None)

        print "Testing setTarget with args: url=%s" %(unittests.w3af_urlSite)
        self.assertRaises(PluginException, self.plugin.setTarget, url=unittests.w3af_urlSite)

    def test_setTargetDeepWeb(self):
        print "Testing setTargetDeepWeb with args: url=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setTargetDeepWeb, url=None)

        print "Testing setTargetDeepWeb with args: url=%s" %(unittests.w3af_onionserviceInvalid)
        self.assertRaises(PluginException, self.plugin.setTargetDeepWeb, url=unittests.w3af_onionserviceInvalid)


    def test_setMiscConfig(self):
        print "Testing setMiscConfig with args: setting=%s , value=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.setMiscConfig, setting=None , value=None)

        print "Testing setMiscConfig with args: setting=%s , value=%s" %(unittests.w3af_invalidSetting, unittests.w3af_invalidSettingValue)
        self.assertRaises(PluginException, self.plugin.setMiscConfig, setting=unittests.w3af_invalidSetting , value=unittests.w3af_invalidSettingValue)

    def test_useProfile(self):
        print "Testing useProfile with args: profileName=%s " %(None)
        self.assertRaises(PluginException, self.plugin.useProfile, profileName=None)

        print "Testing useProfile with args: profileName=%s" %(unittests.w3af_invalidProfile)
        self.assertRaises(PluginException, self.plugin.useProfile, profileName=unittests.w3af_invalidProfile)


    def test_createProfileWithCurrentConfig(self):
        print "Testing createProfileWithCurrentConfig with args: profileName=%s , profileDescription=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.createProfileWithCurrentConfig, profileName=None, profileDescription=None)

        print "Testing createProfileWithCurrentConfig with args: profileName=%s , profileDescription=%s" %("", None)
        self.assertRaises(PluginException, self.plugin.createProfileWithCurrentConfig, profileName="", profileDescription="")


    def test_modifyProfileWithCurrentConfig(self):
        print "Testing modifyProfileWithCurrentConfig with args: profileName=%s , profileDescription=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.modifyProfileWithCurrentConfig, profileName=None, profileDescription=None)

        print "Testing modifyProfileWithCurrentConfig with args: profileName=%s , profileDescription=%s" %(unittests.w3af_invalidProfile, None)
        self.assertRaises(PluginException, self.plugin.modifyProfileWithCurrentConfig, profileName=unittests.w3af_invalidProfile, profileDescription="")

    
    def removeProfile(self,profileName):
        print "Testing removeProfile with args: profileName=%s" %(None)
        self.assertRaises(PluginException, self.plugin.removeProfile, profileName=None)

        print "Testing removeProfile with args: profileName=%s " %(unittests.w3af_invalidProfile)
        self.assertRaises(PluginException, self.plugin.removeProfile, profileName=unittests.w3af_invalidProfile)


    def test_executeCommand(self):
        print "Testing removeProfile with args: shellId=%s , command=%s , params=%s" %(None, None, None)
        self.assertRaises(PluginException, self.plugin.executeCommand, shellId=None, command=None, params=None)

        print "Testing removeProfile with args: shellId=%s , command=%s , params=%s" %(unittests.w3af_invalidId1, "", None)
        self.assertRaises(PluginException, self.plugin.executeCommand, shellId=unittests.w3af_invalidId1, command="", params=None)

        print "Testing removeProfile with args: shellId=%s , command=%s , params=%s" %(unittests.w3af_invalidId2, "", None)
        self.assertRaises(PluginException, self.plugin.executeCommand, shellId=unittests.w3af_invalidId2, command="", params=None)

    def test_exploitAllVulns(self):
        print "Testing exploitAllVulns with args: pluginExploit=%s " %(None)
        self.assertRaises(PluginException, self.plugin.exploitAllVulns, pluginExploit=None)

        print "Testing exploitAllVulns with args: pluginExploit=%s" %(unittests.w3af_invalidPluginName)
        self.assertRaises(PluginException, self.plugin.exploitAllVulns, pluginExploit=unittests.w3af_invalidPluginName)



    def test_exploitVuln(self):
        print "Testing exploitVuln with args: pluginExploit=%s , vulnId=%s " %(None,None)
        self.assertRaises(PluginException, self.plugin.exploitVuln, pluginExploit=None, vulnId=None)

        print "Testing exploitVuln with args: pluginExploit=%s , vulnId=%s" %(unittests.w3af_invalidPluginName , unittests.w3af_invalidId1)
        self.assertRaises(PluginException, self.plugin.exploitVuln, pluginExploit=unittests.w3af_invalidPluginName , vulnId=unittests.w3af_invalidId1)

        print "Testing exploitVuln with args: pluginExploit=%s , vulnId=%s" %(unittests.w3af_invalidPluginName , unittests.w3af_invalidId2)
        self.assertRaises(PluginException, self.plugin.exploitVuln, pluginExploit=unittests.w3af_invalidPluginName , vulnId=unittests.w3af_invalidId2)

if __name__ == '__main__':
    unittest.main()