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
import socket
import os
import sys
import time
from socket import error as socket_error
import signal
import paramiko
import unittest

class bruterPluginTest(unittest.TestCase):

    def __init__(self):
        self.plugin = heartBleedPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        reference.setPluginArguments(self.pluginArgs)
        reference.processPluginArguments()

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SSH BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def sshBruterOnRelay(self, relay, port=22, dictFile=None, force=False):
        pass

            
    def sshBruterOnAllRelays(self, port=22, dictFile=None, force=False):
        pass

    def sshBruterOnHiddenService(self, onionService, port=22, dictFile=None):
        pass



    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM FTP BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def ftpBruterOnRelay(self, host, port=21, dictFile=None, proxy=False):
        pass

    def ftpBruterOnAllRelays(self, port=21, dictFile=None):
        pass
        

    def ftpBruterOnHiddenService(self, onionService, port=21, dictFile=None):
        pass


    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SNMP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def snmpBruterOnRelay(self, host, port=161, dictFile=None):
        pass

    def snmpBruterOnAllRelays(self, port=161, dictFile=None):
        pass

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SMB BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def smbBruterOnRelay(self, host, port=139, dictFile=None):
        pass
            
    def smbBruterOnAllRelays(self, port=139, dictFile=None):
        pass

    def smbBruterOnHiddenService(self, onionService, servicePort=139, localPort=139, dictFile=None):
        pass

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM HTTP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def httpBruterOnSite(self, url, dictFile=None, proxy=False):
        pass


    def httpBruterOnHiddenService(self, onionService, dictFile=None):
        pass
