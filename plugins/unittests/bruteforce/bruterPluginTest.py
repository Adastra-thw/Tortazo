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

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from plugins.texttable import Texttable
from plugins.bruteforce.bruterPlugin import bruterPlugin
import socket
import os
import sys
import time
from socket import error as socket_error
import signal
import paramiko
import unittest
from config import unittests

class bruterPluginTest(unittest.TestCase):

    def __init__(self):
        self.plugin = bruterPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        reference.setPluginArguments(self.pluginArgs)
        reference.processPluginArguments()

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SSH BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def test_sshBruterOnRelay(self):
        self.assertRaises(Exception, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSSH,dictFile=unittests.bruterPlugin_dictFile, force=False)
        self.assertRaises(Exception, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_relayInvalid, port=unittests.bruterPlugin_portSSH,dictFile=unittests.bruterPlugin_dictFile, force=False)
        self.assertRaises(Exception, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portInvalid,dictFile=unittests.bruterPlugin_dictFile, force=False)
        self.assertRaises(Exception, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSSH,dictFile=unittests.bruterPlugin_dictFileInvalid, force=False)

        self.assertRaises(Exception, self.plugin.sshBruterOnRelay, relay=None, port=None,dictFile=None, force=None)
        self.assertRaises(Exception, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_Relay, port=None,dictFile=None, force=None)
        self.assertRaises(Exception, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSSH,dictFile=None, force=None)
        self.assertRaises(Exception, self.plugin.sshBruterOnRelay, relay=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSSH,dictFile=unittests.bruterPlugin_dictFile, force=None)

            
    def test_sshBruterOnAllRelays(self):
        self.assertRaises(Exception, self.plugin.sshBruterOnAllRelays, port=unittests.bruterPlugin_portSSH, dictFile=unittests.bruterPlugin_dictFile, force=False)
        self.assertRaises(Exception, self.plugin.sshBruterOnAllRelays, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile, force=False)
        self.assertRaises(Exception, self.plugin.sshBruterOnAllRelays, port=unittests.bruterPlugin_portSSH, dictFile=unittests.bruterPlugin_dictFileInvalid, force=False)
        
        self.assertRaises(Exception, self.plugin.sshBruterOnAllRelays, port=None,dictFile=None, force=None)
        self.assertRaises(Exception, self.plugin.sshBruterOnAllRelays, port=unittests.bruterPlugin_portSSH, dictFile=None, force=None)
        self.assertRaises(Exception, self.plugin.sshBruterOnAllRelays, port=unittests.bruterPlugin_portSSH, dictFile=unittests.bruterPlugin_dictFile, force=None)


    def test_sshBruterOnHiddenService(self):
        self.assertRaises(Exception, self.plugin.sshBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portSSH, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.sshBruterOnHiddenService, onionService=unittests.bruterPlugin_onionserviceInvalid, port=unittests.bruterPlugin_portSSH, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.sshBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.sshBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portSSH, dictFile=unittests.bruterPlugin_dictFileInvalid)
        
        self.assertRaises(Exception, self.plugin.sshBruterOnHiddenService, onionService=None, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.sshBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=None, dictFile=None)
        self.assertRaises(Exception, self.plugin.sshBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portSSH, dictFile=None)




    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM FTP BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def test_ftpBruterOnRelay(self):
        self.assertRaises(Exception, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portFTP,dictFile=unittests.bruterPlugin_dictFile, proxy=False)
        self.assertRaises(Exception, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_relayInvalid, port=unittests.bruterPlugin_portFTP,dictFile=unittests.bruterPlugin_dictFile, proxy=False)
        self.assertRaises(Exception, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portInvalid,dictFile=unittests.bruterPlugin_dictFile, proxy=False)
        self.assertRaises(Exception, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portFTP,dictFile=unittests.bruterPlugin_dictFileInvalid, proxy=False)

        self.assertRaises(Exception, self.plugin.ftpBruterOnRelay, host=None, port=None,dictFile=None, proxy=None)
        self.assertRaises(Exception, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=None,dictFile=None, proxy=None)
        self.assertRaises(Exception, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portFTP,dictFile=None, proxy=None)
        self.assertRaises(Exception, self.plugin.ftpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portFTP,dictFile=unittests.bruterPlugin_dictFile, proxy=None)

        

    def test_ftpBruterOnAllRelays(self):
        self.assertRaises(Exception, self.plugin.ftpBruterOnAllRelays, port=unittests.bruterPlugin_portFTP, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.ftpBruterOnAllRelays, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.ftpBruterOnAllRelays, port=unittests.bruterPlugin_portFTP, dictFile=unittests.bruterPlugin_dictFileInvalid)
        
        self.assertRaises(Exception, self.plugin.ftpBruterOnAllRelays, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.ftpBruterOnAllRelays, port=unittests.bruterPlugin_portFTP, dictFile=None)


        

    def test_ftpBruterOnHiddenService(self, onionService, port=21, dictFile=None):
        self.assertRaises(Exception, self.plugin.ftpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portFTP, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.ftpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionserviceInvalid, port=unittests.bruterPlugin_portFTP, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.ftpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.ftpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portFTP, dictFile=unittests.bruterPlugin_dictFileInvalid)
        
        self.assertRaises(Exception, self.plugin.ftpBruterOnHiddenService, onionService=None, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.ftpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=None, dictFile=None)
        self.assertRaises(Exception, self.plugin.ftpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portFTP, dictFile=None)
        


    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SNMP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def test_snmpBruterOnRelay(self, host, port=161, dictFile=None):
        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSNMP,dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_relayInvalid, port=unittests.bruterPlugin_portSNMP,dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portInvalid,dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSNMP,dictFile=unittests.bruterPlugin_dictFileInvalid)

        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=None, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSNMP,dictFile=None)


    def test_snmpBruterOnAllRelays(self, port=161, dictFile=None):
        self.assertRaises(Exception, self.plugin.snmpBruterOnAllRelays, port=unittests.bruterPlugin_portSNMP, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.snmpBruterOnAllRelays, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.snmpBruterOnAllRelays, port=unittests.bruterPlugin_portSNMP, dictFile=unittests.bruterPlugin_dictFileInvalid)
        
        self.assertRaises(Exception, self.plugin.snmpBruterOnAllRelays, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.snmpBruterOnAllRelays, port=unittests.bruterPlugin_portSNMP, dictFile=None)



    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SMB BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def test_smbBruterOnRelay(self, host, port=139, dictFile=None):
        self.assertRaises(Exception, self.plugin.smbBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSMB,dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.smbBruterOnRelay, host=unittests.bruterPlugin_relayInvalid, port=unittests.bruterPlugin_portSMB,dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.smbBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portInvalid,dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.smbBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSMB,dictFile=unittests.bruterPlugin_dictFileInvalid)

        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=None, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.snmpBruterOnRelay, host=unittests.bruterPlugin_Relay, port=unittests.bruterPlugin_portSMB,dictFile=None)

            
    def test_smbBruterOnAllRelays(self, port=139, dictFile=None):
        self.assertRaises(Exception, self.plugin.smbBruterOnAllRelays, port=unittests.bruterPlugin_portSNB, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.smbBruterOnAllRelays, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.smbBruterOnAllRelays, port=unittests.bruterPlugin_portSMB, dictFile=unittests.bruterPlugin_dictFileInvalid)
        
        self.assertRaises(Exception, self.plugin.smbBruterOnAllRelays, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.smbBruterOnAllRelays, port=unittests.bruterPlugin_portSMB, dictFile=None)

    def test_smbBruterOnHiddenService(self, onionService, servicePort=139, localPort=139, dictFile=None):
        self.assertRaises(Exception, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portFTP, dictFile=unittests.bruterPlugin_dictFile, localPort=unittests.bruterPlugin_localportSMB)
        self.assertRaises(Exception, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionserviceInvalid, port=unittests.bruterPlugin_portSMB, dictFile=unittests.bruterPlugin_dictFile, localPort=unittests.bruterPlugin_localportSMB)
        self.assertRaises(Exception, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile, localPort=unittests.bruterPlugin_localportSMB)
        self.assertRaises(Exception, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portSMB, dictFile=unittests.bruterPlugin_dictFileInvalid, localPort=unittests.bruterPlugin_localportSMB)
        self.assertRaises(Exception, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portFTP, dictFile=unittests.bruterPlugin_dictFile, localPort=unittests.bruterPlugin_portInvalid)
        
        self.assertRaises(Exception, self.plugin.smbBruterOnHiddenService, onionService=None, port=None,dictFile=None, localPort=None)
        self.assertRaises(Exception, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=None, dictFile=None)
        self.assertRaises(Exception, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portSMB, dictFile=None)
        self.assertRaises(Exception, self.plugin.smbBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portSMB, localPort=None)
        

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM HTTP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def test_httpBruterOnSite(self, url, dictFile=None, proxy=False):
        self.assertRaises(Exception, self.plugin.httpBruterOnSite, url=unittests.bruterPlugin_urlSite, port=unittests.bruterPlugin_portHTTP,dictFile=unittests.bruterPlugin_dictFile, proxy=False)
        self.assertRaises(Exception, self.plugin.httpBruterOnSite, url=unittests.bruterPlugin_urlSite, port=unittests.bruterPlugin_portHTTP,dictFile=unittests.bruterPlugin_dictFile, proxy=False)
        self.assertRaises(Exception, self.plugin.httpBruterOnSite, url=unittests.bruterPlugin_urlSite, port=unittests.bruterPlugin_portInvalid,dictFile=unittests.bruterPlugin_dictFile, proxy=False)
        self.assertRaises(Exception, self.plugin.httpBruterOnSite, url=unittests.bruterPlugin_urlSite, port=unittests.bruterPlugin_portHTTP,dictFile=unittests.bruterPlugin_dictFileInvalid, proxy=False)

        self.assertRaises(Exception, self.plugin.httpBruterOnSite, url=None, port=None,dictFile=None, proxy=None)
        self.assertRaises(Exception, self.plugin.httpBruterOnSite, url=unittests.bruterPlugin_urlSite, port=None,dictFile=None, proxy=None)
        self.assertRaises(Exception, self.plugin.httpBruterOnSite, url=unittests.bruterPlugin_urlSite, port=unittests.bruterPlugin_portHTTP,dictFile=None, proxy=None)
        self.assertRaises(Exception, self.plugin.httpBruterOnSite, url=unittests.bruterPlugin_urlSite, port=unittests.bruterPlugin_portHTTP,dictFile=unittests.bruterPlugin_dictFile, proxy=None)



    def test_httpBruterOnHiddenService(self, onionService, dictFile=None):
        self.assertRaises(Exception, self.plugin.httpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portHTTP, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.httpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionserviceInvalid, port=unittests.bruterPlugin_portHTTP, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.httpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portInvalid, dictFile=unittests.bruterPlugin_dictFile)
        self.assertRaises(Exception, self.plugin.httpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portHTTP, dictFile=unittests.bruterPlugin_dictFileInvalid)
        
        self.assertRaises(Exception, self.plugin.httpBruterOnHiddenService, onionService=None, port=None,dictFile=None)
        self.assertRaises(Exception, self.plugin.httpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=None, dictFile=None)
        self.assertRaises(Exception, self.plugin.httpBruterOnHiddenService, onionService=unittests.bruterPlugin_onionservice, port=unittests.bruterPlugin_portHTTP, dictFile=None)
        
