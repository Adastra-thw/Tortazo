# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

simplePlugin.py

WorkerThread is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

WorkerThread is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from pynessus import pynessus
from pynessus.rest.client.NessusClient import NessusClient
import os

class nessusPlugin(BasePlugin):
    '''
    This class uses PyNessus to connect and execute scans with nessus.
    '''

    def __init__(self, torNodes):
        BasePlugin.__init__(self, torNodes, 'nessusPlugin')

    def __del__(self):
        self.debug("[*] nessusPlugin Destroyed!")
        self.nessusInstance.logout()

    def listPlugins(self):
        print self.nessusInstance.list_plugins()

    def listPolicies(self):
        pass

    def getPolicyByName(self, policyName):
        pass

    def listReports(self):
        pass

    def singleScan(self, scanName, target, policyId):
        pass

    def scan(self, scanName, policyId):
        pass

    def multiScan(self, scanName, targets, policyId):
        pass

    def downloadReport(self, reportId):
        pass

    def findVulnerabilities(self, target, pluginFamily, riskFactor):
        pass

    def help(self):
        print "[*] Functions availaible available in the Plugin..."
        tableHelp = PrettyTable(["Function", "Description", "Example"])
        tableHelp.padding_width = 1
        tableHelp.padding_width = 1
        tableHelp.add_row(['help', 'Help Banner', 'self.help()'])
        tableHelp.add_row(['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'])
        print tableHelp

        self.info("[*] Help for plugin nessusPlugin: \n")
        self.info("[*][*]  Important: Some settings are readed from config.py. Change this file for your own needs.  \n")
        self.info("[*][*] Available Options: \n")
        self.info("[*][*]   listPlugins: List of plugins loaded. Arguments: None. \n")
        self.info("[*][*]   listPolicies: List of policies loaded. Arguments: None. \n")
        self.info("[*][*]   getPolicyByName: Get Policy ID by Name. Arguments: PolicyName.  \n")
        self.info("[*][*]   listReports: List of reports loaded.  \n")
        self.info("[*][*]   singleScan: scan a single TOR Node. Arguments: ScanName, IP-Address or DomainName of the target and Policy ID \n")
        self.info("[*][*]   scan: Scans the full list of TOR Nodes found. Arguments: ScanName and Policy ID \n")
        self.info("[*][*]   multiScan: Scans a sublist of the TOR Nodes found. Arguments: ScanName, sublist of TOR Nodes (IP-Addresses or DomainNames separated by '|') and Policy ID \n")
        self.info("[*][*]   downloadReport: Download a Report. Arguments: Report UUID \n")
        self.info("[*][*]   findVulnerabilities: . Arguments: Target, Risk Factor, Plugin Family \n")