# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

nessusPlugin.py

nessusPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

nessusPlugin is distributed in the hope that it will be useful,
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
from pynessus.rest.data.NessusStructure import NessusConverter
from prettytable import PrettyTable
import sys

class nessusPlugin(BasePlugin):
    '''
    This class uses PyNessus to connect and execute scans with nessus.
    '''

    #http://static.tenable.com/documentation/nessus_5.0_XMLRPC_protocol_guide.pdf

    def __init__(self,torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'nessusPlugin')
        self.setPluginDetails('NessusPlugin', 'Plugin developed to interact with the REST API of Nessus. Uses pynessus-rest library', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.nessusClient = NessusClient(config.nessusHost, config.nessusPort)
            self.nessusClient.login(config.nessusUser, config.nessusPass)
            self.info("[*] NessusPlugin Initialized!")



    def __del__(self):
        if len(self.torNodes) > 0:
            self.debug("[*] NessusPlugin Destroyed!")
            self.nessusClient.logout()

    def feed(self):
        nessusConverter = NessusConverter(self.nessusClient.feed(method="POST"))
        nessusConverter.feedToStructure()

        print "[*] Basic Feed Information"
        tableBasicFeed = PrettyTable(["Feed", "Plugin Rules", "Expiration", "UI Version", "Server Version", "WebServer Version"])
        tableBasicFeed.padding_width = 1
        tableBasicFeed.add_row([nessusConverter.nessusStructure.feed.feed,
                                nessusConverter.nessusStructure.feed.pluginRules,
                                nessusConverter.nessusStructure.feed.expiration,
                                nessusConverter.nessusStructure.feed.uiVersion,
                                nessusConverter.nessusStructure.feed.serverVersion,
                                nessusConverter.nessusStructure.feed.webServerVersion])
        print tableBasicFeed
        print "\n[*] Other Information"
        tableOtherFeed = PrettyTable(["Nessus Type", "Diff","Expiration Time","Report Email", "Tags", "MSP", "Multi-Scanner","Loaded PluginSet"])
        tableOtherFeed.padding_width = 1
        tableOtherFeed.add_row([nessusConverter.nessusStructure.feed.nessusType,
                                nessusConverter.nessusStructure.feed.diff,
                                nessusConverter.nessusStructure.feed.expirationTime,
                                nessusConverter.nessusStructure.feed.reportEmail,
                                nessusConverter.nessusStructure.feed.tags,
                                nessusConverter.nessusStructure.feed.msp,
                                nessusConverter.nessusStructure.feed.multiScanner,
                                nessusConverter.nessusStructure.feed.loadedPluginSet])
        print tableOtherFeed

    def serverSecureSettingsList(self):
        nessusConverter = NessusConverter(self.nessusClient.securesettingsList(method="POST"))
        nessusConverter.secureSettingsListToStructure()

        print "[*] Nessus Secure Settings"

        tableNessusSecureSettings = PrettyTable(["Proxy Password", "Proxy Port", "Custom Host", "Proxy Username", "User Agent", "Proxy"])
        tableNessusSecureSettings.padding_width = 1
        tableNessusSecureSettings.add_row([nessusConverter.nessusStructure.secureSettings.proxyPassword,
                                nessusConverter.nessusStructure.secureSettings.proxyPort,
                                nessusConverter.nessusStructure.secureSettings.customHost,
                                nessusConverter.nessusStructure.secureSettings.proxyUserName,
                                nessusConverter.nessusStructure.secureSettings.userAgent,
                                nessusConverter.nessusStructure.secureSettings.proxy])
        print tableNessusSecureSettings

    def serverSecureSettings(self):
        nessusConverter = NessusConverter(self.nessusClient.securesettings())
        nessusConverter.secureSettingsListToStructure()
        print "[*] Nessus Secure Settings Updated"
        tableNessusSecureSettings = PrettyTable(["Preferences"])
        tableNessusSecureSettings.padding_width = 1
        tableNessusSecureSettings.add_row([nessusConverter.nessusStructure.secureSettings.preferences])
        print tableNessusSecureSettings

    def serverUpdate(self):
        nessusConverter = NessusConverter(self.nessusClient.serverUpdate())
        nessusConverter.serverUpdateToStructure()

        print "[*] Server Update"
        tableNessusSecureSettings = PrettyTable(["Server Update"])
        tableNessusSecureSettings.padding_width = 1
        tableNessusSecureSettings.add_row([nessusConverter.nessusStructure.serverUpdate])
        print tableNessusSecureSettings

    def serverRegister(self, nessusCode):
        nessusConverter = NessusConverter(self.nessusClient.serverRegister(nessusCode))
        nessusConverter.serverUpdateToStructure()

        print "[*] Server Register"
        tableNessusServerRegister = PrettyTable(["Server Register"])
        tableNessusServerRegister.padding_width = 1
        tableNessusServerRegister.add_row([nessusConverter.nessusStructure.serverRegistration])
        print tableNessusServerRegister

    def serverLoad(self):
        nessusConverter = NessusConverter(self.nessusClient.serverLoad(method="POST"))
        nessusConverter.serverLoadToStructure()

        print "[*] Server Load"
        tableNessusServerLoad = PrettyTable(["Scans", "Sessions","Hosts","TCP Sessions", "Load AVG", "Platform"])
        tableNessusServerLoad.padding_width = 1
        tableNessusServerLoad.add_row([nessusConverter.nessusStructure.serverLoad.numScans,
                                       nessusConverter.nessusStructure.serverLoad.numSessions,
                                       nessusConverter.nessusStructure.serverLoad.numHosts,
                                       nessusConverter.nessusStructure.serverLoad.numTcpSessions,
                                       nessusConverter.nessusStructure.serverLoad.loadAvg,
                                       nessusConverter.nessusStructure.serverLoad.platform])
        print tableNessusServerLoad


    def serverUuid(self):
        nessusConverter = NessusConverter(self.nessusClient.serverUuid())
        nessusConverter.serverUuidToStructure()

        tableUuid = PrettyTable(["UUID"])
        tableUuid.padding_width = 1
        tableUuid.add_row([nessusConverter.nessusStructure.uuid])
        print tableUuid

    def userAdd(self, userName, password, admin=1):
        administrator = False
        if admin == 1:
            administrator = True
        nessusConverter = NessusConverter(self.nessusClient.usersAdd(userName,password,administrator, method="POST"))
        nessusConverter.userToStructure()

        print "[*] User Created"
        tableUsers = PrettyTable(["Name", "Admin", "Idx", "Last-Login"])
        tableUsers.padding_width = 1
        tableUsers.add_row([nessusConverter.nessusStructure.nessusUser.name,
                            nessusConverter.nessusStructure.nessusUser.admin,
                            nessusConverter.nessusStructure.nessusUser.idx,
                            nessusConverter.nessusStructure.nessusUser.lastLogin])
        print tableUsers

    def userEdit(self, userName, password, admin=1):
        administrator = False
        if admin == 1:
            administrator = True
        nessusConverter = NessusConverter(self.nessusClient.usersEdit(userName,password,administrator))
        nessusConverter.userToStructure()

        print "[*] User Edited"
        tableUsers = PrettyTable(["Name", "Admin", "Idx", "Last-Login"])
        tableUsers.padding_width = 1
        tableUsers.add_row([nessusConverter.nessusStructure.nessusUser.name,
                            nessusConverter.nessusStructure.nessusUser.admin,
                            nessusConverter.nessusStructure.nessusUser.idx,
                            nessusConverter.nessusStructure.nessusUser.lastLogin])
        print tableUsers

    def userDelete(self, userName):
        nessusConverter = NessusConverter(self.nessusClient.usersDelete(userName))
        nessusConverter.userToStructure()

        print "[*] User Removed"
        tableUsers = PrettyTable(["Name", "Admin", "Idx", "Last-Login"])
        tableUsers.padding_width = 1
        tableUsers.add_row([nessusConverter.nessusStructure.nessusUser.name,
                            nessusConverter.nessusStructure.nessusUser.admin,
                            nessusConverter.nessusStructure.nessusUser.idx,
                            nessusConverter.nessusStructure.nessusUser.lastLogin])
        print tableUsers

    def userChpasswd(self, userName, password):
        nessusConverter = NessusConverter(self.nessusClient.usersChpasswd(userName,password))
        nessusConverter.userToStructure()

        print "[*] User Password Changed"
        tableUsers = PrettyTable(["Name", "Admin", "Idx", "Last-Login"])
        tableUsers.padding_width = 1
        tableUsers.add_row([nessusConverter.nessusStructure.nessusUser.name,
                            nessusConverter.nessusStructure.nessusUser.admin,
                            nessusConverter.nessusStructure.nessusUser.idx,
                            nessusConverter.nessusStructure.nessusUser.lastLogin])
        print tableUsers

    def usersList(self):
        nessusConverter = NessusConverter(self.nessusClient.usersList())
        nessusConverter.userToStructure()

        print "[*] User List"
        tableUsers = PrettyTable(["Name", "Admin", "Idx", "Last-Login"])
        tableUsers.padding_width = 1
        for nessusUser in nessusConverter.nessusStructure.nessusUsers:
            tableUsers.add_row([nessusUser.name,nessusUser.admin,nessusUser.idx,nessusUser.lastLogin])
        print tableUsers


    def pluginsList(self):
        nessusConverter = NessusConverter(self.nessusClient.pluginsList())
        nessusConverter.pluginsListToStructure()

        print "[*] Plugins List"
        tablePlugins = PrettyTable(["Family Member", "Family Name"])
        tablePlugins.padding_width = 1
        for nessusPlugin in nessusConverter.nessusStructure.pluginsList:
            tablePlugins.add_row([nessusPlugin.familyMembers, nessusPlugin.familyName])
        print tablePlugins

    def pluginAttributesList(self):
        nessusConverter = NessusConverter(self.nessusClient.pluginsAttributesList())
        nessusConverter.pluginsAttributesToStructure()
        print "[*] Plugins Attributes List"
        tablePluginsAttributes = PrettyTable(["Readable Name", 'Readable Regex', 'List'])
        for pluginsAttribute in nessusConverter.nessusStructure.pluginsAttributes:
            tablePluginsAttributes.add_row([pluginsAttribute.readableName, pluginsAttribute.control.readableRegex,
                                            pluginsAttribute.control.list ])

        print tablePluginsAttributes

    def pluginListsFamily(self, familyName):
        nessusConverter = NessusConverter(self.nessusClient.pluginsListFamily(familyName))
        nessusConverter.pluginListFamilyToStructure()
        print "[*] Plugins List Family"
        tablePluginsListFamily = PrettyTable(["Plugin ID", "Plugin Name", "Plugin Family", 'Plugin FileName'])
        for pluginFamily in nessusConverter.nessusStructure.pluginsListFamily:
            tablePluginsListFamily.add_row([pluginFamily.pluginId,
                                            pluginFamily.pluginName,
                                            pluginFamily.pluginFamily,
                                            pluginFamily.pluginFileName])
        print tablePluginsListFamily

    def pluginDescription(self, fileNamePlugin):
        nessusConverter = NessusConverter(self.nessusClient.pluginsDescription(fileNamePlugin))
        nessusConverter.pluginsDescriptionToStructure()
        print "[*] Plugin Description"
        tablePluginDescription = PrettyTable(["Plugin ID", "Plugin Name", "Plugin Family"])
        tablePluginDescription.add_row([nessusConverter.nessusStructure.pluginsDescription.pluginId,
                                        nessusConverter.nessusStructure.pluginsDescription.pluginName,
                                        nessusConverter.nessusStructure.pluginsDescription.pluginFamily,])
        print tablePluginDescription
        print "\n"
        print "[*] Plugin Attributes"
        tablePluginAttributes = PrettyTable(["Vuln Date", "Risk Factor", "CVSS", 'Type', 'Patch Date', 'CVSS Score', 'CVE', 'BID', 'CPE'])
        if nessusConverter.nessusStructure.pluginsDescription is not None:
            tablePluginAttributes.add_row([nessusConverter.nessusStructure.pluginsDescription.vulnPublicationDate,
                                        nessusConverter.nessusStructure.pluginsDescription.riskFactor,
                                        nessusConverter.nessusStructure.pluginsDescription.cvssBaseScore,
                                        nessusConverter.nessusStructure.pluginsDescription.pluginType,
                                        nessusConverter.nessusStructure.pluginsDescription.pluginPatchDate,
                                        nessusConverter.nessusStructure.pluginsDescription.cvssBaseScore,
                                        nessusConverter.nessusStructure.pluginsDescription.cve,
                                        nessusConverter.nessusStructure.pluginsDescription.bid,
                                        nessusConverter.nessusStructure.pluginsDescription.cpe,])
        print tablePluginAttributes



    def pluginsAttributesFamilySearch(self, filter0Quality, filterSearchType, filter0Value, filter0Filter):
        nessusConverter = NessusConverter(self.nessusClient.pluginsAttributesFamilySearch(filter0Quality,filterSearchType,filter0Value,filter0Filter))
        nessusConverter.pluginsAttributeFamilySearchToStructure()
        print "[*] Family Search"
        tablePluginAttributes = PrettyTable(["Family"])
        tablePluginAttributes.add_row([nessusConverter.nessusStructure.pluginsAttributeFamilySearch])
        print tablePluginAttributes



    def pluginsAttributesPluginSearch(self, filter0quality, filterSearchType, filter0Value, filter0Filter, family):
        nessusConverter = NessusConverter(self.nessusClient.pluginsAttributesPluginSearch(filter0quality,filterSearchType,filter0Value,filter0Filter, family))
        nessusConverter.pluginsAttributePluginSearchToStructure()
        print "[*] Plugin Search"
        tablePluginAttributes = PrettyTable(["Family", "FileName", "Plugin ID", "Plugin Name"])
        if nessusConverter.nessusStructure.pluginsAttributePluginSearch is not None:
            tablePluginAttributes.add_row([nessusConverter.nessusStructure.pluginsAttributePluginSearch.pluginFamily,
                                       nessusConverter.nessusStructure.pluginsAttributePluginSearch.pluginFileName,
                                       nessusConverter.nessusStructure.pluginsAttributePluginSearch.pluginId,
                                       nessusConverter.nessusStructure.pluginsAttributePluginSearch.pluginName])
        print tablePluginAttributes

    def pluginsMd5(self):
        nessusConverter = NessusConverter(self.nessusClient.pluginsMd5())
        nessusConverter.md5StructureToStructure()
        print "[*] Plugins MD5"
        tableMD5 = PrettyTable(["FileName", "MD5 Hash"])
        for md5 in nessusConverter.nessusStructure.md5Structure:
            tableMD5.add_row([md5.fileName, md5.md5])
        print tableMD5

    def policyPreferencesList(self):
        nessusConverter = NessusConverter(self.nessusClient.policyPreferencesList())
        nessusConverter.serverPolicyPreferenceToStructure()
        print "[*] Policy Preferences List"
        tablePreference = PrettyTable(["Name", "Value"])
        for preference in nessusConverter.nessusStructure.policyPreferences:
            tablePreference.add_row([preference.name, preference.value])
        print tablePreference


    def policyList(self):
        nessusConverter = NessusConverter(self.nessusClient.policyList())
        nessusConverter.policyStructureToStructure()
        print "[*] Policy List"
        tablePolicies = PrettyTable(["Id", "Name","Owner","Visibility"])
        for policy in nessusConverter.nessusStructure.nessusPolicies:
            tablePolicies.add_row([policy.policyId, policy.policyName, policy.policyOwner, policy.policyVisibility])
        print tablePolicies

    def policyDelete(self, policyId):
        nessusConverter = NessusConverter(self.nessusClient.policyDelete(policyId))
        nessusConverter.policyDeletedToStructure()
        print "[*] Policy Deleted"
        tablePolicies = PrettyTable(["Policy Deleted"])
        for policy in nessusConverter.nessusStructure.nessusPolicies:
            tablePolicies.add_row([nessusConverter.nessusStructure.policyDeleted])
        print tablePolicies

    def policyCopy(self, policyId):
        nessusConverter = NessusConverter(self.nessusClient.policyCopy(policyId))
        nessusConverter.policyStructureToStructure()
        print "[*] Policy Copy"
        tablePolicies = PrettyTable(["Id", "Name","Owner","Visibility"])
        for policy in nessusConverter.nessusStructure.nessusPolicies:
            tablePolicies.add_row([policy.name, policy.value])
        print tablePolicies


    def policyDownload(self, policyId, fileName):
        nessusConverter = NessusConverter(self.nessusClient.policyDownload(policyId))
        nessusConverter.policyDownloadedToStructure()
        try:
            fileDescriptor = open(fileName, "w")
            fileDescriptor.write(str(nessusConverter.nessusStructure.policyDownloaded))
            fileDescriptor.close()
            print "[+] Policy's file downloaded successfully."
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print "[-] Error downloading the policy. Check the file name specified."


    def scanAllRelays(self, policyId, scanName):
        targets = ''
        for node in self.torNodes:
            targets +=node.host+"\n"
        nessusConverter = NessusConverter(self.nessusClient.scanNew(targets, policyId, scanName, method="POST"))
        nessusConverter.scanToStructure()
        tableScan = PrettyTable(["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"])
        tableScan.add_row([nessusConverter.nessusStructure.scan.owner,
                           nessusConverter.nessusStructure.scan.scanName,
                           nessusConverter.nessusStructure.scan.startTime,
                           nessusConverter.nessusStructure.scan.uuid,
                           nessusConverter.nessusStructure.scan.readableName,
                           nessusConverter.nessusStructure.scan.status,
                           nessusConverter.nessusStructure.scan.completionCurrent,
                           nessusConverter.nessusStructure.scan.completionTotal])
        print tableScan


    def scanByRelay(self, policyId, scanName, relay):
        found = False
        for node in self.torNodes:
            if relay is not None:
                if relay == node.host or relay.lower() == node.nickName.lower():
                    found = True
                    break
        if found:
            nessusConverter = NessusConverter(self.nessusClient.scanNew(relay, policyId, scanName, method="POST"))
            nessusConverter.scanToStructure()
            print "[*] Nessus scan using the relay %s " %(relay)
            tableScan = PrettyTable(["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"])
            tableScan.add_row([nessusConverter.nessusStructure.scan.owner,
                               nessusConverter.nessusStructure.scan.scanName,
                               nessusConverter.nessusStructure.scan.startTime,
                               nessusConverter.nessusStructure.scan.uuid,
                               nessusConverter.nessusStructure.scan.readableName,
                               nessusConverter.nessusStructure.scan.status,
                               nessusConverter.nessusStructure.scan.completionCurrent,
                               nessusConverter.nessusStructure.scan.completionTotal])
            print tableScan
        else:
            print ["[-] The relay specified is not found."]

    def scanStop(self, scanUuid):
        nessusConverter = NessusConverter(self.nessusClient.scanStop(scanUuid))
        nessusConverter.scanToStructure()
        print "[*] Nessus scan stopped."
        tableScan = PrettyTable(["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"])
        tableScan.add_row([nessusConverter.nessusStructure.scan.owner,
                           nessusConverter.nessusStructure.scan.scanName,
                           nessusConverter.nessusStructure.scan.startTime,
                           nessusConverter.nessusStructure.scan.uuid,
                           nessusConverter.nessusStructure.scan.readableName,
                           nessusConverter.nessusStructure.scan.status,
                           nessusConverter.nessusStructure.scan.completionCurrent,
                           nessusConverter.nessusStructure.scan.completionTotal])
        print tableScan

    def scanResume(self, scanUuid):
        nessusConverter = NessusConverter(self.nessusClient.scanResume(scanUuid))
        nessusConverter.scanToStructure()
        print "[*] Nessus scan Resumed."
        tableScan = PrettyTable(["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"])
        tableScan.add_row([nessusConverter.nessusStructure.scan.owner,
                           nessusConverter.nessusStructure.scan.scanName,
                           nessusConverter.nessusStructure.scan.startTime,
                           nessusConverter.nessusStructure.scan.uuid,
                           nessusConverter.nessusStructure.scan.readableName,
                           nessusConverter.nessusStructure.scan.status,
                           nessusConverter.nessusStructure.scan.completionCurrent,
                           nessusConverter.nessusStructure.scan.completionTotal])
        print tableScan

    def scanPause(self, scanUuid):
        nessusConverter = NessusConverter(self.nessusClient.scanPause(scanUuid))
        nessusConverter.scanToStructure()
        print "[*] Nessus scan Paused."
        tableScan = PrettyTable(["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"])
        tableScan.add_row([nessusConverter.nessusStructure.scan.owner,
                           nessusConverter.nessusStructure.scan.scanName,
                           nessusConverter.nessusStructure.scan.startTime,
                           nessusConverter.nessusStructure.scan.uuid,
                           nessusConverter.nessusStructure.scan.readableName,
                           nessusConverter.nessusStructure.scan.status,
                           nessusConverter.nessusStructure.scan.completionCurrent,
                           nessusConverter.nessusStructure.scan.completionTotal])
        print tableScan

    def scanList(self):
        nessusConverter = NessusConverter(self.nessusClient.scanList(method="POST"))
        nessusConverter.scanListToStructure()
        print "[*] Nessus scan List."
        tableScan = PrettyTable(["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"])
        if len(nessusConverter.nessusStructure.scanList) > 0:
            for scan in nessusConverter.nessusStructure.scanList:
                tableScan.add_row([scan.owner, scan.scanName, scan.startTime, scan.uuid,
                                   scan.readablename, scan.status,
                                   scan.completionCurrent, scan.completionTotal])
        print tableScan

    def scanTemplateAllRelays(self, policyId, templateName):
        targets = ''
        for node in self.torNodes:
            targets +=node.host+"\n"
        nessusConverter = NessusConverter(self.nessusClient.scanTemplateNew(policyId,targets,templateName))
        nessusConverter.scanTemplateToStructure()
        print "[*] Nessus scan Template New."
        tableTemplate = PrettyTable(["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"])
        tableTemplate.add_row([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                               nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                               nessusConverter.nessusStructure.nessusScanTemplate.target,
                               nessusConverter.nessusStructure.nessusScanTemplate.name,
                               nessusConverter.nessusStructure.nessusScanTemplate.policyId])
        print tableTemplate

    def scanTemplateByRelay(self,policyId,relay,templateName):
        found = False
        for node in self.torNodes:
            if relay is not None:
                if relay == node.host or relay.lower() == node.nickName.lower():
                    found = True
                    break
        if found:
            nessusConverter = NessusConverter(self.nessusClient.scanTemplateNew(policyId,relay,templateName))
            nessusConverter.scanTemplateToStructure()
            print "[*] Nessus scan Template New."
            tableTemplate = PrettyTable(["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"])
            tableTemplate.add_row([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                               nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                               nessusConverter.nessusStructure.nessusScanTemplate.target,
                               nessusConverter.nessusStructure.nessusScanTemplate.name,
                               nessusConverter.nessusStructure.nessusScanTemplate.policyId])
            print tableTemplate


    def scanTemplateEditAllRelays(self, templateEdit, templateNewName, policyId):
        targets = ''
        for node in self.torNodes:
            targets +=node.host+"\n"
        nessusConverter = NessusConverter(self.nessusClient.scanTemplateEdit(templateEdit,templateNewName,policyId,targets))
        nessusConverter.scanTemplateToStructure()
        print "[*] Nessus scan Template Edit."
        tableTemplate = PrettyTable(["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"])
        if nessusConverter.nessusStructure.nessusScanTemplate is not  None:
            tableTemplate.add_row([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                               nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                               nessusConverter.nessusStructure.nessusScanTemplate.target,
                               nessusConverter.nessusStructure.nessusScanTemplate.name,
                               nessusConverter.nessusStructure.nessusScanTemplate.policyId])
        print tableTemplate

    def scanTemplateEditByRelay(self,templateEdit, templateNewName, policyId, relay):
        found = False
        for node in self.torNodes:
            if relay is not None:
                if relay == node.host or relay.lower() == node.nickName.lower():
                    found = True
                    break
        if found:
            nessusConverter = NessusConverter(self.nessusClient.scanTemplateEdit(templateEdit,templateNewName,policyId,relay))
            nessusConverter.scanTemplateToStructure()
            print "[*] Nessus scan Template Edit."
            tableTemplate = PrettyTable(["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"])
            if nessusConverter.nessusStructure.nessusScanTemplate is not None:
                tableTemplate.add_row([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                                   nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                                   nessusConverter.nessusStructure.nessusScanTemplate.target,
                                   nessusConverter.nessusStructure.nessusScanTemplate.name,
                                   nessusConverter.nessusStructure.nessusScanTemplate.policyId])
            print tableTemplate

    def scanTemplateDelete(self, templateUuid):
        nessusConverter = NessusConverter(self.nessusClient.scanTemplateDelete(templateUuid))
        nessusConverter.scanTemplateToStructure()
        print "[*] Nessus scan Template Deleted."
        tableTemplate = PrettyTable(["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"])
        if nessusConverter.nessusStructure.nessusScanTemplate is not None:
            tableTemplate.add_row([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                               nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                               nessusConverter.nessusStructure.nessusScanTemplate.target,
                               nessusConverter.nessusStructure.nessusScanTemplate.name,
                               nessusConverter.nessusStructure.nessusScanTemplate.policyId])
        print tableTemplate

    def scanTemplateLaunch(self, templateName):
        nessusConverter = NessusConverter(self.nessusClient.scanTemplateLaunch(templateName))
        #Nessus will return an scan structure.
        nessusConverter.scanToStructure()
        print "[*] Nessus scan Template Launch."
        tableTemplate = PrettyTable(["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"])
        if nessusConverter.nessusStructure.nessusScanTemplate is not None:
            tableTemplate.add_row([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                               nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                               nessusConverter.nessusStructure.nessusScanTemplate.target,
                               nessusConverter.nessusStructure.nessusScanTemplate.name,
                               nessusConverter.nessusStructure.nessusScanTemplate.policyId])
        print tableTemplate

    def reportList(self):
        nessusConverter = NessusConverter(self.nessusClient.reportList())
        nessusConverter.reportToStructure()
        print "[*] Nessus Report List."
        tableReport = PrettyTable(["Status","Readable Name", "UUID", "Timestamp"])
        if nessusConverter.nessusStructure.reportList is not None:
            for report in nessusConverter.nessusStructure.reportList:
                tableReport.add_row([report.status,
                                     report.readablename,
                                     report.name,
                                     report.timestamp])
        print tableReport

    def reportDelete(self, reportUuid):
        nessusConverter = NessusConverter(self.nessusClient.reportDelete(reportUuid))
        nessusConverter.reportToStructure()
        if nessusConverter.nessusStructure.report:
            print "[*] Report %s deleted." %(reportUuid)

    def reportHosts(self,reportUuid):
        nessusConverter = NessusConverter(self.nessusClient.reportHosts(reportUuid))
        nessusConverter.reportHostToStructure()
        print "[*] Nessus Report Hosts List."
        tableReport = PrettyTable(["Hostname","Num. Checks", "Total Checks", "Scan Progress Current", "Scan Progress Total", "Severity"])
        if nessusConverter.nessusStructure.reportHosts is not None:
            for reportHost in nessusConverter.nessusStructure.reportHosts:
                tableReport.add_row([reportHost.hostname,
                                     reportHost.numchecksconsidered,
                                     reportHost.totalchecksconsidered,
                                     reportHost.scanprogresscurrent,
                                     reportHost.scanprogresstotal,
                                     reportHost.severity])
        print tableReport

    def reportPorts(self, reportUuid, hostname):
        nessusConverter = NessusConverter(self.nessusClient.reportPorts(reportUuid, hostname))
        nessusConverter.reportPortToStructure()
        print "[*] Nessus Report Ports."
        tableReport = PrettyTable(["Port Number","Protocol", "Severity", "SVC Name"])
        if nessusConverter.nessusStructure.reportPortList is not None:
            for reportPort in nessusConverter.nessusStructure.reportPortList:
                tableReport.add_row([reportPort.portNumber,
                                     reportPort.protocol,
                                     reportPort.severity,
                                     reportPort.svcName])
        print tableReport

    def reportDetails(self,reportUuid, hostname,port,protocol):
        nessusConverter = NessusConverter(self.nessusClient.reportDetails(reportUuid,hostname,port,protocol))
        nessusConverter.reportPortDetailToStructure()
        print "[*] Nessus Report Details."
        tableReport = PrettyTable(["Port", "Severity", "Plugin Id", "Plugin Name", "BID", "CPE","CVE","CVSS Base Score","CVSS Temporal Score","Description", "FName"])
        if nessusConverter.nessusStructure.reportPortDetail is not None:
            for reportPort in nessusConverter.nessusStructure.reportPortDetail:
                tableReport.add_row([reportPort.itemId,
                                     reportPort.port,
                                     reportPort.severity,
                                     reportPort.pluginId,
                                     reportPort.pluginName,
                                     reportPort.bid,
                                     reportPort.cpe,
                                     reportPort.cve,
                                     reportPort.cvss_base_score,
                                     reportPort.cvss_temporal_score,
                                     reportPort.description,
                                     reportPort.fname])
        else:
            print "[*] No results."

        print tableReport

    def reportTags(self, reportUuid, hostname):
        nessusConverter = NessusConverter(self.nessusClient.reportTags(reportUuid, hostname))
        nessusConverter.tagToNessusStructure()
        print "[*] Nessus Tags."
        tableReport = PrettyTable(["Tag Name","Tag Value"])
        if nessusConverter.nessusStructure.nessusTags is not None:
            for tag in nessusConverter.nessusStructure.nessusTags:
                tableReport.add_row([tag.name, tag.value])
        else:
            print "[*] No results."
        print tableReport

    def reportAttributesList(self,reportUuid):
        nessusConverter = NessusConverter(self.nessusClient.reportAttributesList(reportUuid))
        nessusConverter.reportAttributesToStructure()
        print "[*] Nessus Report Attributes."
        tableReport = PrettyTable(["Name","Readable Name","Readable Regex", "Operators"])
        if nessusConverter.nessusStructure.nessusReportAttributes is not None:
            for reportAttribute in nessusConverter.nessusStructure.nessusReportAttributes:
                tableReport.add_row([reportAttribute.name,
                                     reportAttribute.readableName,
                                     reportAttribute.nessusControl.readableRegex,
                                     reportAttribute.operators])
        tableReport.align["Operators"] = "l"

        print tableReport

    def help(self):
        print "[*] Functions availaible available in the Plugin..."
        tableHelp = PrettyTable(["Function", "Description", "Example"])
        tableHelp.padding_width = 1
        tableHelp.add_row(['help', 'Help Banner', 'self.help()'])
        tableHelp.add_row(['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'])
        tableHelp.add_row(['feed', 'Return the Nessus Feed', 'self.feed()'])
        tableHelp.add_row(['serverSecureSettingsList', 'List of Server Secure Settings', 'self.serverSecureSettingsList()'])
        tableHelp.add_row(['serverRegister', 'Registers the Nessus server with Tenable Network Security', "self.serverRegister('FEED_CODE')"])
        tableHelp.add_row(['serverLoad', 'Server Load and Platform Type', "self.serverLoad()"])
        tableHelp.add_row(['serverUuid', 'Server UUID', "self.serverUuid()"])
        tableHelp.add_row(['userAdd', 'Create a new user', "self.userAdd('adastra','adastra',0)"])
        tableHelp.add_row(['userEdit', 'Edit the user specified', "self.userEdit('adastra','new_password',1)"])
        tableHelp.add_row(['userDelete', 'Delete the user specified', "self.userDelete('adastra')"])
        tableHelp.add_row(['userChpasswd', 'Change the password for the user specified', "self.userChpasswd('adastra','new_password')"])
        tableHelp.add_row(['usersList', 'List of users.', "self.usersList()"])
        tableHelp.add_row(['pluginsList', 'List of plugins.', "self.pluginsList()"])
        tableHelp.add_row(['pluginAttributesList', 'List of plugins attributes for plugin filtering.', "self.pluginListsFamily('AIX Local Security Checks')"])
        tableHelp.add_row(['pluginDescription', 'Returns the entire description of a given plugin.', "self.pluginDescription('ping_host.nasl')"])
        tableHelp.add_row(['pluginsAttributesFamilySearch', 'Filters against the family of plugins.', "self.pluginsAttributesFamilySearch('match','or','modicon','description')"])
        tableHelp.add_row(['pluginsAttributesPluginSearch', 'Returns the plugins in a family that match a given filter criteria.', "self.pluginsAttributesPluginSearch('match','or','modicon','description','FTP')"])
        tableHelp.add_row(['pluginsMd5', 'List of plugin file names and corresponding MD5 hashes.', "self.pluginsMd5()"])
        tableHelp.add_row(['policyList', 'List of available policies, policy settings and default values.', "self.policyList()"])
        tableHelp.add_row(['policyDelete', 'Delete the policy specified.', "self.policyDelete(POLICY_ID)"])
        tableHelp.add_row(['policyCopy', 'Copies an existing policy to a new policy.', "self.policyCopy(POLICY_ID)"])
        tableHelp.add_row(['policyDownload', 'Download the policy from the server to the local system.', "self.policyDownload(POLICY_ID, /home/user/policy.nessus)"])
        tableHelp.add_row(['scanAllRelays', 'Create a new scan with all relays loaded.', "self.scanAllRelays(<POLICY_ID>, 'newScan')"])
        tableHelp.add_row(['scanByRelay', 'Create a new scan with the specified relay.', "self.scanAllRelays(<POLICY_ID>, 'newScan', <IP_OR_NICKNAME>)"])
        tableHelp.add_row(['scanStop', 'Stops the specified started scan.', "self.scanStop(<SCAN_UUID>)"])
        tableHelp.add_row(['scanResume', 'Resumes the specified paused scan.', "self.scanResume(<SCAN_UUID>)"])
        tableHelp.add_row(['scanPause', 'Pauses the specified actived scan.', "self.scanPause(<SCAN_UUID>)"])
        tableHelp.add_row(['scanList', 'List of scans.', "self.scanList()"])
        tableHelp.add_row(['scanTemplateAllRelays', 'Create a new scan template (scheduled) with all relays loaded.', "self.scanTemplateAllRelays(<POLICY_ID>,<TEMPLATE_NAME>)"])
        tableHelp.add_row(['scanTemplateByRelay', 'Create a new scan template (scheduled) with the specified relay.', "self.scanTemplateByRelay(<POLICY_ID>,<TEMPLATE_NEW_NAME>,<IP_OR_NICKNAME>)"])
        tableHelp.add_row(['scanTemplateEditAllRelays', 'Edit the scan template specified with all relays loaded.', "self.scanTemplateEditAllRelays(<POLICY_ID>,<TEMPLATE_NEW_NAME>)"])
        tableHelp.add_row(['scanTemplateEditByRelay', 'Edit the scan template specified with the specified relay.', "self.scanTemplateEditByRelay(<TEMPLATE_UUID>,<TEMPLATE_NEW_NAME>,<POLICY_ID>,<IP_OR_NICKNAME>)"])
        tableHelp.add_row(['scanTemplateDelete', 'Delete the scan template specified.', "self.scanTemplateDelete(<TEMPLATE_UUID>)"])
        tableHelp.add_row(['scanTemplateLaunch', 'Launch the scan template specified.', "self.scanTemplateLaunch(<TEMPLATE_UUID>)"])
        tableHelp.add_row(['reportList', 'List of available scan reports.', "self.reportList()"])
        tableHelp.add_row(['reportDelete', 'Delete the specified report.', "self.reportDelete(<REPORT_UUID>)"])
        tableHelp.add_row(['reportHosts', 'List of hosts contained in a specified report.', "self.reportHosts(<REPORT_UUID>)"])
        tableHelp.add_row(['reportPorts', 'List of ports and the number of findings on each port.', "self.reportPorts(<REPORT_UUID>,<HOSTNAME>)"])
        tableHelp.add_row(['reportDetails', 'Details of a scan for a given host.', "self.reportDetails(<REPORT_UUID>,<HOSTNAME>,<PORT>,<PROTOCOL>)"])
        tableHelp.add_row(['reportTags', 'Tags of a scan for a given host.', "self.reportTags(<REPORT_UUID>, <HOSTNAME>)"])
        tableHelp.add_row(['reportAttributesList', 'List of filter attributes associated with a given report.', "self.reportAttributesList(<REPORT_UUID>)"])


        tableHelp.align["Function"] = "l"
        tableHelp.align["Description"] = "l"
        tableHelp.align["Example"] = "l"
        print tableHelp