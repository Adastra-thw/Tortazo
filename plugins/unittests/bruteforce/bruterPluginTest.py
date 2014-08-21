# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

bruterPluginTest.py

bruterPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

bruterPluginTest is distributed in the hope that it will be useful,
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

from plugins.bruteforce.bruterPlugin import bruterPlugin
from core.tortazo.exceptions.PluginException import PluginException
import unittest
from config import unittests
from config import config
import os.path
from config import unittests

class bruterPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = bruterPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SSH BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def test_sshBruterOnRelay(self):
        print "Testing sshBruterOnRelay with args: relay=%s, port=%s, dictFile=%s, force=%s " %(unittests.bruterPlugin_relayInvalid, str(unittests.bruterPlugin_portSSH), unittests.bruterPlugin_dictFile, "False")
        self.assertRaises(PluginException, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_relayInvalid, port=unittests.bruterPlugin_portSSH,dictFile=unittests.bruterPlugin_dictFile, force=False)

        print "Testing sshBruterOnRelay with args: relay=%s, port=%s, dictFile=%s, force=%s " %(unittests.bruterPlugin_relayInvalid, str(unittests.bruterPlugin_portInvalid), unittests.bruterPlugin_dictFile, "False")
        self.assertRaises(PluginException, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portInvalid,dictFile=unittests.bruterPlugin_dictFile, force=False)

        print "Testing sshBruterOnRelay with args: relay=%s, port=%s, dictFile=%s, force=%s " %(unittests.bruterPlugin_portSSH, str(unittests.bruterPlugin_portInvalid), unittests.bruterPlugin_dictFileInvalid, "False")
        self.assertFalse(self.plugin.sshBruterOnRelay(relay=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSSH,dictFile=unittests.bruterPlugin_dictFileInvalid, force=False))

        print "Testing sshBruterOnRelay with args: relay=%s, port=%s, dictFile=%s, force=%s " %(None, None, None, None)
        self.assertRaises(PluginException, self.plugin.sshBruterOnRelay, relay=None, port=None,dictFile=None, force=None)

        print "Testing sshBruterOnRelay with args: relay=%s, port=%s, dictFile=%s, force=%s " %(unittests.bruterPlugin_Relay, None, None, None)
        self.assertRaises(PluginException, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_Relay, port=None,dictFile=None, force=None)

        print "Testing sshBruterOnRelay with args: relay=%s, port=%s, dictFile=%s, force=%s " %(unittests.bruterPlugin_Relay, str(unittests.bruterPlugin_portSSH), None, None)
        self.assertRaises(PluginException, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSSH,dictFile=None, force=None)

            
    def test_sshBruterOnAllRelays(self):
        print "Testing sshBruterOnAllRelays with args: port=%s, dictFile=%s, force=%s " %(str(unittests.bruterPlugin_portInvalid), unittests.bruterPlugin_dictFile, "False")
        self.assertRaises(PluginException, self.plugin.sshBruterOnAllRelays, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile, force=False)

        print "Testing sshBruterOnAllRelays with args: port=%s, dictFile=%s, force=%s " %(str(unittests.bruterPlugin_portSSH), unittests.bruterPlugin_dictFileInvalid, "False")
        self.assertFalse(self.plugin.sshBruterOnAllRelays(port=unittests.bruterPlugin_portSSH, dictFile=unittests.bruterPlugin_dictFileInvalid, force=False))

        print "Testing sshBruterOnAllRelays with args: port=%s, dictFile=%s, force=%s " %(None, None, None)
        self.assertRaises(PluginException, self.plugin.sshBruterOnAllRelays, port=None,dictFile=None, force=None)

        print "Testing sshBruterOnAllRelays with args: port=%s, dictFile=%s, force=%s " %(unittests.bruterPlugin_portSSH, None, None)
        self.assertRaises(PluginException, self.plugin.sshBruterOnAllRelays, port=unittests.bruterPlugin_portSSH, dictFile=None, force=None)


    def test_sshBruterOnHiddenService(self):
        print "Testing sshBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_onionserviceInvalid, str(unittests.bruterPlugin_portSSH), unittests.bruterPlugin_dictFile)
        self.assertRaises(PluginException, self.plugin.sshBruterOnHiddenService, onionService=unittests.bruterPlugin_onionserviceInvalid, port=unittests.bruterPlugin_portSSH, dictFile=unittests.bruterPlugin_dictFile)

        print "Testing sshBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_onionservice, str(ittests.bruterPlugin_portInvalid), unittests.bruterPlugin_dictFile)
        self.assertRaises(PluginException, self.plugin.sshBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)

        print "Testing sshBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_onionservice, str(ittests.bruterPlugin_portInvalid), unittests.bruterPlugin_dictFileInvalid)
        self.assertFalse(self.plugin.sshBruterOnHiddenService(onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portSSH, dictFile=unittests.bruterPlugin_dictFileInvalid))

        print "Testing sshBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(None, None, None)
        self.assertRaises(PluginException, self.plugin.sshBruterOnHiddenService, onionService=None, port=None,dictFile=None

        print "Testing sshBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_onionservice, None, None))
        self.assertRaises(PluginException, self.plugin.sshBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=None, dictFile=None)





    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM FTP BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def test_ftpBruterOnRelay(self):
        print "Testing ftpBruterOnRelay with args: host=%s, port=%s, dictFile=%s, proxy=%s " %(unittests.bruterPlugin_relayInvalid, str(unittests.bruterPlugin_portFTP), unittests.bruterPlugin_dictFile, "False")
        self.assertRaises(PluginException, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_relayInvalid, port=unittests.bruterPlugin_portFTP,dictFile=unittests.bruterPlugin_dictFile, proxy=False)

        print "Testing ftpBruterOnRelay with args: host=%s, port=%s, dictFile=%s, proxy=%s " %(unittests.bruterPlugin_Relay, str(unittests.bruterPlugin_portInvalid), unittests.bruterPlugin_dictFile, "False")        
        self.assertRaises(PluginException, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portInvalid,dictFile=unitte

        print "Testing ftpBruterOnRelay with args: host=%s, port=%s, dictFile=%s, proxy=%s " %(None, None, None, None)        
        self.assertRaises(PluginException, self.plugin.ftpBruterOnRelay, host=None, port=None,dictFile=None, proxy=None)

        print "Testing ftpBruterOnRelay with args: host=%s, port=%s, dictFile=%s, proxy=%s " %(unittests.bruterPlugin_Relay, None, None, None)       
        self.assertRaises(PluginException, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=None,dictFile=None, proxy=None)

    def test_ftpBruterOnAllRelays(self):
        print "Testing ftpBruterOnAllRelays with args: port=%s, dictFile=%s " %(str(unittests.bruterPlugin_portInvalid), unittests.bruterPlugin_dictFile)       
        self.assertRaises(PluginException, self.plugin.ftpBruterOnAllRelays, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)

        print "Testing ftpBruterOnAllRelays with args: port=%s, dictFile=%s " %(None, None)      
        self.assertRaises(PluginException, self.plugin.ftpBruterOnAllRelays, port=None,dictFile=None)

        

    def test_ftpBruterOnHiddenService(self, onionService, port=21, dictFile=None):
        print "Testing ftpBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_onionserviceInvalid, unittests.bruterPlugin_portFTP, unittests.bruterPlugin_dictFile)      
        self.assertRaises(PluginException, self.plugin.ftpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionserviceInvalid, port=unittests.bruterPlugin_portFTP, dictFile=unittests.bruterPlugin_dictFile)

        print "Testing ftpBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_onionservice, unittests.bruterPlugin_portInvalid, unittests.bruterPlugin_dictFile)                                
        self.assertRaises(PluginException, self.plugin.ftpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)

        print "Testing ftpBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(None, None, None)                                
        self.assertRaises(PluginException, self.plugin.ftpBruterOnHiddenService, onionService=None, port=None,dictFile=None)

        print "Testing ftpBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_onionservice, None, None)                                                          
        self.assertRaises(PluginException, self.plugin.ftpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=None, dictFile=None)

        print "Testing ftpBruterOnHiddenService with args: onionService=%s, port=%s, dictFile=%s " %(None, unittests.bruterPlugin_portFTP, None)                                                          
        self.assertRaises(PluginException, self.plugin.ftpBruterOnHiddenService, onionService=None, port=unittests.bruterPlugin_portFTP, dictFile=None)



    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SNMP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def test_snmpBruterOnRelay(self):
        print "Testing snmpBruterOnRelay with args: host=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_relayInvalid, unittests.bruterPlugin_portSNMP, unittests.bruterPlugin_dictFile)
        self.assertRaises(PluginException, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_relayInvalid, port=unittests.bruterPlugin_portSNMP,dictFile=unittests.bruterPlugin_dictFile)

        print "Testing snmpBruterOnRelay with args: host=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_Relay, unittests.bruterPlugin_portInvalid, unittests.bruterPlugin_dictFile)
        self.assertRaises(PluginException, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portInvalid,dictFile=unittests.bruterPlugin_dictFile)

        print "Testing snmpBruterOnRelay with args: host=%s, port=%s, dictFile=%s " %(None, None, None)
        self.assertRaises(PluginException, self.plugin.snmpBruterOnRelay, host=None, port=None,dictFile=None)

        print "Testing snmpBruterOnRelay with args: host=%s, port=%s, dictFile=%s " %(unittests.bruterPlugin_Relay, None, None)                          
        self.assertRaises(PluginException, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=None,dictFile=None)


    def test_snmpBruterOnAllRelays(self):
        print "Testing snmpBruterOnAllRelays with args: port=%s, dictFile=%s " %(unittests.bruterPlugin_portInvalid, unittests.bruterPlugin_dictFile)                                                    
        self.assertRaises(PluginException, self.plugin.snmpBruterOnAllRelays, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)

        print "Testing snmpBruterOnAllRelays with args: port=%s, dictFile=%s " %(None, None)                                                    
        self.assertRaises(PluginException, self.plugin.snmpBruterOnAllRelays, port=None,dictFile=None)



    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SMB BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def test_smbBruterOnRelay(self):
        print "Testing smbBruterOnRelay with args: host=%s, port=%s " %(unittests.bruterPlugin_relayInvalid, str(unittests.bruterPlugin_portSMB))
        self.assertRaises(PluginException, self.plugin.smbBruterOnRelay, host=unittests.bruterPlugin_relayInvalid, port=unittests.bruterPlugin_portSMB)

        print "Testing smbBruterOnRelay with args: host=%s, port=%s " %(unittests.bruterPlugin_Relay, str(unittests.bruterPlugin_portInvalid))
        self.assertRaises(PluginException, self.plugin.smbBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portInvalid)

        print "Testing smbBruterOnRelay with args: host=%s, port=%s " %(None, None)
        self.assertRaises(PluginException, self.plugin.snmpBruterOnRelay, host=None, port=None)

        print "Testing smbBruterOnRelay with args: host=%s, port=%s " %(unittests.bruterPlugin_Relay, None)                          
        self.assertRaises(PluginException, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=None)

        print "Testing smbBruterOnRelay with args: host=%s, port=%s " %(None, str(unittests.bruterPlugin_portSMB))                                                    
        self.assertRaises(PluginException, self.plugin.snmpBruterOnRelay, host=None, port=unittests.bruterPlugin_portSMB)

            
    def test_smbBruterOnAllRelays(self):
        print "Testing smbBruterOnAllRelays with args: port=%s " %(str(unittests.bruterPlugin_portInvalid))
        self.assertRaises(PluginException, self.plugin.smbBruterOnAllRelays, port=unittests.bruterPlugin_portInvalid)

        print "Testing smbBruterOnAllRelays with args: port=%s " %(None)
        self.assertRaises(PluginException, self.plugin.smbBruterOnAllRelays, port=None)


    def test_smbBruterOnHiddenService(self):
        print "Testing smbBruterOnHiddenService with args: onionService=%s, servicePort=%s, localPort=%s " %(unittests.bruterPlugin_onionserviceInvalid, str(unittests.bruterPlugin_portSMB), str(unittests.bruterPlugin_localportSMB))
        self.assertRaises(PluginException, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionserviceInvalid, servicePort=unittests.bruterPlugin_portSMB, localPort=unittests.bruterPlugin_localportSMB)

        print "Testing smbBruterOnHiddenService with args: onionService=%s, servicePort=%s, localPort=%s " %(unittests.bruterPlugin_onionservice, str(unittests.bruterPlugin_portInvalid), str(unittests.bruterPlugin_localportSMB))
        self.assertRaises(PluginException, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, servicePort=unittests.bruterPlugin_portInvalid, localPort=unittests.bruterPlugin_localportSMB)

        print "Testing smbBruterOnHiddenService with args: onionService=%s, servicePort=%s, localPort=%s " %(unittests.bruterPlugin_onionservice, str(unittests.bruterPlugin_portSMB), str(unittests.bruterPlugin_portInvalid))
        self.assertRaises(PluginException, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, servicePort=unittests.bruterPlugin_portSMB, localPort=unittests.bruterPlugin_portInvalid)

        print "Testing smbBruterOnHiddenService with args: onionService=%s, servicePort=%s, localPort=%s " %(None, None, None)                          
        self.assertRaises(PluginException, self.plugin.smbBruterOnHiddenService, onionService=None, servicePort=None, localPort=None)

        print "Testing smbBruterOnHiddenService with args: onionService=%s, servicePort=%s, localPort=%s " %(onionService=unittests.bruterPlugin_onionservice, None, None)                                                    
        self.assertRaises(PluginException, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, servicePort=None, localPort=None)

        print "Testing smbBruterOnHiddenService with args: onionService=%s, servicePort=%s, localPort=%s " %(unittests.bruterPlugin_onionservice, str(unittests.bruterPlugin_portSMB), None)                                                    
        self.assertRaises(PluginException, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, servicePort=unittests.bruterPlugin_portSMB, localPort=None)

        print "Testing smbBruterOnHiddenService with args: onionService=%s, servicePort=%s, localPort=%s " %(unittests.bruterPlugin_onionservice, None, unittests.bruterPlugin_localportSMB)                                                    
        self.assertRaises(PluginException, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, None, localPort=unittests.bruterPlugin_localportSMB)
        

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM HTTP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def test_httpBruterOnSite(self):
        print "Testing httpBruterOnSite with args: url=%s " %(unittests.bruterPlugin_urlSite)
        self.assertRaises(PluginException, self.plugin.httpBruterOnSite, url=unittests.bruterPlugin_urlSite)

        print "Testing httpBruterOnSite with args: url=%s " %(None)
        self.assertRaises(PluginException, self.plugin.httpBruterOnSite, url=None)



    def test_httpBruterOnHiddenService(self):
        print "Testing httpBruterOnHiddenService with args: url=%s " %(unittests.bruterPlugin_onionserviceInvalid)                          
        self.assertRaises(PluginException, self.plugin.httpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionserviceInvalid)

        print "Testing httpBruterOnHiddenService with args: url=%s " %(None)                          
        self.assertRaises(PluginException, self.plugin.httpBruterOnHiddenService, onionService=None)
        

if __name__ == '__main__':
    unittest.main()
