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
import config
from pynessus.rest.client.NessusClient import NessusClient
import pprint

class nessusPlugin(BasePlugin):
    '''
    This class uses PyNessus to connect and execute scans with nessus.
    '''

    #http://static.tenable.com/documentation/nessus_5.0_XMLRPC_protocol_guide.pdf

    def __init__(self):
        BasePlugin.__init__(self)
        self.NESSUS_FUNCTIONS = ["feed", "serverSecureSettingsList", "serverSecureSettings", "serverPreferencesList",
                                 "serverPreferences", "serverUpdate", "serverRegister", "serverRestart", "serverLoad",
                                 "serverUuid", "serverGetCert", "serverPluginsProcess",
                                 "usersAdd", "usersEdit", "usersDelete", "usersChpasswd", "usersList",
                                 "pluginsList","pluginsAttributesList", "pluginsListsFamily", "pluginsDescription",
                                 "pluginsPreferences", "pluginsAttributesFamilySearch",
                                 "pluginsAttributesPluginSearch", "pluginsMd5", "pluginsDescriptions",
                                 "listPlugins", "listPolicies", "listReports",
                                 "policyPreferencesList", "policyList", "policyDelete", "policyCopy",
                                 "policyAdd", "policyEdit", "policyDownload","policyFileUpload", "policyFileImport",
                                 'scanNew','scanStop','scanResume','scanPause','scanList',
                                 'scanTimeZones','scanTemplateNew','scanTemplateEdit',
                                 'scanTemplateDelete','scanTemplateLaunch',
                                 'reportList','reportDelete','reportHosts','report2HostsPlugin','report2Hosts',
                                 'reportPorts','report2Ports','reportDetails','report2DetailsPlugin',
                                 'report2Details','reportTags','reportHasAuditTrail','reportAttributesList',
                                 'reportErrors','reportHasKB','reportCanDeleteItems','report2DeleteItem',
                                 'reportTrailDetails','report2Vulnerabilities','reportChapterList',
                                 'reportChapter','reportFileImport','reportFileDownload',
                                 'reportFileXsltList','reportFileXslt','reportFileXsltDownload'
                                 ]
        self.nessusClient = NessusClient(config.nessusHost, config.nessusPort)
        self.nessusClient.login(config.nessusUser, config.nessusPass)

    def __del__(self):
        pass
        self.debug("[*] nessusPlugin Destroyed!")
        self.nessusClient.logout()


    def runPlugin(self):
        '''
        The most simplest plugin! Just prints the tor data structure.
        '''
        for argumentName, argumentValue in self.pluginArguments.iteritems():
            print argumentName +":"+ argumentValue
            if argumentValue in self.NESSUS_FUNCTIONS:
                nessusFunction = getattr(self, argumentValue)
                if callable(nessusFunction):
                    nessusFunction()

    def feed(self):
        pass

    def serverSecureSettingsList(self):
        pass

    def serverSecureSettings(self):
        pass

    def serverPreferencesList(self):
        pass

    def serverPreferences(self):
        pass

    def serverUpdate(self):
        pass

    def serverRegister(self):
        pass

    def serverRestart(self):
        pass

    def serverLoad(self):
        pass

    def serverUuid(self):
        pass

    def serverGetCert(self):
        pass

    def serverPluginsProcess(self):
        pass

    def usersAdd(self):
        pass

    def usersEdit(self):
        pass

    def usersDelete(self):
        pass

    def usersChpasswd(self):
        pass

    def usersList(self):
        pass

    def pluginsList(self):
        pprint.pprint(self.nessusClient.pluginsList())

    def pluginsAttributesList(self):
        pass

    def pluginsListsFamily(self):
        pass

    def pluginsDescription(self):
        pass

    def pluginsPreferences(self):
        pass

    def pluginsAttributesFamilySearch(self):
        pass

    def pluginsAttributesPluginSearch(self):
        pass

    def pluginsMd5(self):
        pass

    def pluginsDescriptions(self):
        pass

    def policyPreferencesList(self):
        pass

    def policyList(self):
        pass

    def policyDelete(self):
        pass

    def policyCopy(self):
        pass

    def policyAdd(self):
        pass

    def policyEdit(self):
        pass

    def policyDownload(self):
        pass

    def policyFileUpload(self):
        pass

    def policyFileImport(self):
        pass

    def scanNew(self):
        pass

    def scanStop(self):
        pass

    def scanResume(self):
        pass

    def scanPause(self):
        pass

    def scanList(self):
        pass

    def scanTimeZones(self):
        pass

    def scanTemplateNew(self):
        pass

    def scanTemplateEdit(self):
        pass

    def scanTemplateDelete(self):
        pass

    def scanTemplateLaunch(self):
        pass

    def reportList(self):
        pass

    def reportDelete(self):
        pass

    def reportHosts(self):
        pass

    def report2HostsPlugin(self):
        pass

    def report2Hosts(self):
        pass

    def reportPorts(self):
        pass

    def report2Ports(self):
        pass

    def reportDetails(self):
        pass

    def report2DetailsPlugin(self):
        pass

    def report2Details(self):
        pass

    def reportTags(self):
        pass

    def reportHasAuditTrail(self):
        pass

    def reportAttributesList(self):
        pass

    def reportErrors(self):
        pass

    def reportHasKB(self):
        pass

    def reportCanDeleteItems(self):
        pass

    def report2DeleteItem(self):
        pass

    def reportTrailDetails(self):
        pass

    def report2Vulnerabilities(self):
        pass

    def reportChapterList(self):
        pass

    def reportChapter(self):
        pass

    def reportFileImport(self):
        pass

    def reportFileDownload(self):
        pass

    def reportFileXsltList(self):
        pass

    def reportFileXslt(self):
        pass

    def reportFileXsltDownload(self):
        pass





    def help(self):
        self.info("[*] Help for plugin nessusPlugin: \n")
        self.info("[*][*]  Important: Some settings are readed from config.py. Change this file for your own needs.  \n")
        self.info("[*][*] Available Functions and arguments: \n")
        self.info("[*][*]   feed: Feed for the Nessus Server. Arguments: None. \n")
        self.info("[*][*]   feed: Feed for the Nessus Server. Arguments: None. \n")

        self.info("[*][*]   listPlugins: List of plugins loaded. Arguments: None. \n")
        self.info("[*][*]   listPolicies: List of policies loaded. Arguments: None. \n")
        self.info("[*][*]   getPolicyByName: Get Policy ID by Name. Arguments: PolicyName.  \n")
        self.info("[*][*]   listReports: List of reports loaded.  \n")
        self.info("[*][*]   singleScan: scan a single TOR Node. Arguments: ScanName, IP-Address or DomainName of the target and Policy ID \n")
        self.info("[*][*]   scan: Scans the full list of TOR Nodes found. Arguments: ScanName and Policy ID \n")
        self.info("[*][*]   multiScan: Scans a sublist of the TOR Nodes found. Arguments: ScanName, sublist of TOR Nodes (IP-Addresses or DomainNames separated by '|') and Policy ID \n")
        self.info("[*][*]   downloadReport: Download a Report. Arguments: Report UUID \n")
        self.info("[*][*]   findVulnerabilities: . Arguments: Target, Risk Factor, Plugin Family \n")


