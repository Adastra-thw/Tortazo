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
from config import config
from pynessus.rest.client.NessusClient import NessusClient
from pynessus.rest.data.NessusStructure import NessusConverter
from plugins.texttable import Texttable
import requests
import sys
from core.tortazo.exceptions.PluginException import PluginException
from plugins.utils.validations.Validator import *

class nessusPlugin(BasePlugin):
    '''
    This class uses PyNessus to connect and execute scans with nessus.
    '''

    #http://static.tenable.com/documentation/nessus_5.0_XMLRPC_protocol_guide.pdf

    def __init__(self,torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'nessusPlugin')
        self.setPluginDetails('NessusPlugin', 'Plugin developed to interact with the REST API of Nessus. Uses pynessus-rest library', '1.0', 'Adastra: @jdaanial')
        self.info("[*] NessusPlugin Initialized!")
        self.pluginConfigs= {"nessusUser":config.nessusUser, "nessusPassword":config.nessusPass,
                               "nessusHost":config.nessusHost, "nessusPort":config.nessusPort}


    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)
        self.__login()

    def __login(self):
        try:
            self.nessusClient = NessusClient(self.pluginConfigs["nessusHost"], self.pluginConfigs["nessusPort"])
            contents = self.nessusClient.login(self.pluginConfigs["nessusUser"], self.pluginConfigs["nessusPassword"])
            if contents['reply']['status'] != 'OK':
                pluginException = PluginException(message="Autentication Failed. The credentials used were: user=%s and password=%s. Please, check those values. " %(self.pluginConfigs["nessusUser"], self.pluginConfigs["nessusPassword"]),
                                      trace="Autentication Failed.",
                                      plugin="nessus",
                                      method="__login")
                if self.runFromInterpreter:
                    showTrace(pluginException)
                    return
                else:
                    raise pluginException 
        except requests.exceptions.ConnectionError:
            pluginException = PluginException(message="Connection error with the Nessus server. The server specified was: %s:%s. Please, check those values. " %(self.pluginConfigs["nessusHost"], self.pluginConfigs["nessusPort"]),
                                  trace="Connection error with the Nessus server.",
                                  plugin="nessus",
                                  method="__login")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                raise pluginException



    def __del__(self):
        if len(self.torNodes) > 0:
            self.debug("[*] NessusPlugin Destroyed!")
            self.nessusClient.logout()

    def feed(self):
        nessusConverter = NessusConverter(self.nessusClient.feed(method="POST"))
        nessusConverter.feedToStructure()

        print "[*] Basic Feed Information"
        tableBasicFeed = Texttable()
        tableBasicFeed.set_cols_align(["l", "l", "l", "l", "l", "l"])
        tableBasicFeed.set_cols_valign(["m", "m", "m","m", "m", "m"])
        tableBasicFeed.set_cols_width([20,20,20,20,20,20])
        rows = [["Feed", "Plugin Rules", "Expiration", "UI Version", "Server Version", "WebServer Version"],
                [nessusConverter.nessusStructure.feed.feed, nessusConverter.nessusStructure.feed.pluginRules,nessusConverter.nessusStructure.feed.expiration,
                 nessusConverter.nessusStructure.feed.uiVersion,nessusConverter.nessusStructure.feed.serverVersion, nessusConverter.nessusStructure.feed.webServerVersion]]
        tableBasicFeed.add_rows(rows)
        print tableBasicFeed.draw()+"\n"
        
        print "\n[*] Other Information"
        tableOtherFeed = Texttable()
        tableOtherFeed.set_cols_align(["l", "l", "l", "l", "l", "l", "l", "l"])
        tableOtherFeed.set_cols_valign(["m", "m", "m","m", "m", "m","m","m"])
        tableOtherFeed.set_cols_width([20,20,20,20,20,20,20,20])
        rowsOther = [["Nessus Type", "Diff","Expiration Time","Report Email", "Tags", "MSP", "Multi-Scanner","Loaded PluginSet"],
                [nessusConverter.nessusStructure.feed.nessusType, nessusConverter.nessusStructure.feed.diff,nessusConverter.nessusStructure.feed.expirationTime,
                 nessusConverter.nessusStructure.feed.reportEmail, nessusConverter.nessusStructure.feed.tags, nessusConverter.nessusStructure.feed.msp,
                 nessusConverter.nessusStructure.feed.multiScanner, nessusConverter.nessusStructure.feed.loadedPluginSet]
                ]
        tableOtherFeed.add_rows(rowsOther)
        print tableOtherFeed.draw()+"\n"

    def serverSecureSettingsList(self):
        nessusConverter = NessusConverter(self.nessusClient.securesettingsList(method="POST"))
        nessusConverter.secureSettingsListToStructure()

        print "[*] Nessus Secure Settings"
        tableNessusSecureSettings = Texttable()
        tableNessusSecureSettings.set_cols_align(["l", "l", "l", "l", "l", "l"])
        tableNessusSecureSettings.set_cols_valign(["m", "m", "m", "m", "m", "m"])
        tableNessusSecureSettings.set_cols_width([20,20,20,20,20,20])
        
        rows = [["Proxy Password", "Proxy Port", "Custom Host", "Proxy Username", "User Agent", "Proxy"],
                [nessusConverter.nessusStructure.secureSettings.proxyPassword, nessusConverter.nessusStructure.secureSettings.proxyPort,
                 nessusConverter.nessusStructure.secureSettings.customHost,nessusConverter.nessusStructure.secureSettings.proxyUserName,
                 nessusConverter.nessusStructure.secureSettings.userAgent,nessusConverter.nessusStructure.secureSettings.proxy]
                ]
        tableNessusSecureSettings.add_rows(rows)
        print tableNessusSecureSettings.draw()+"\n"

    def serverSecureSettings(self):
        nessusConverter = NessusConverter(self.nessusClient.securesettings())
        nessusConverter.secureSettingsListToStructure()
        print "[*] Nessus Secure Settings Updated"
        tableNessusSecureSettings = Texttable()
        tableNessusSecureSettings.set_cols_align(["l"])
        tableNessusSecureSettings.set_cols_valign(["m"])
        tableNessusSecureSettings.set_cols_width([55])
        rows = [["Preferences"],[nessusConverter.nessusStructure.secureSettings.preferences]]
        tableNessusSecureSettings.add_rows(rows)
        print tableNessusSecureSettings.draw()+"\n"

    def serverUpdate(self):
        nessusConverter = NessusConverter(self.nessusClient.serverUpdate())
        nessusConverter.serverUpdateToStructure()

        print "[*] Server Update"
        tableNessusServerUpdate = Texttable()
        tableNessusServerUpdate.set_cols_align(["l"])
        tableNessusServerUpdate.set_cols_valign(["m"])
        tableNessusServerUpdate.set_cols_width([55])
        rows = [["Server Update"],[nessusConverter.nessusStructure.serverUpdate]]
        tableNessusServerUpdate.add_rows(rows)
        print tableNessusServerUpdate.draw()+"\n"

    def serverRegister(self, nessusCode):
        if nessusCode = '' or nessusCode is None:
            
            pluginException = PluginException(message="The 'nessus code' specified is invalid. %s " %(nessusCode),
                                  trace="The 'nessus code' specified is invalid.",
                                  plugin="nessus",
                                  method="serverRegister")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.serverRegister(nessusCode))
        nessusConverter.serverUpdateToStructure()

        print "[*] Server Register"
        tableNessusServerRegister = Texttable()
        tableNessusServerRegister.set_cols_align(["l"])
        tableNessusServerRegister.set_cols_valign(["m"])
        tableNessusServerRegister.set_cols_width([55])
        rows = [["Server Register"],[nessusConverter.nessusStructure.serverRegistration]]
        tableNessusServerRegister.add_rows(rows)
        print tableNessusServerRegister.draw()+"\n"

    def serverLoad(self):
        nessusConverter = NessusConverter(self.nessusClient.serverLoad(method="POST"))
        nessusConverter.serverLoadToStructure()

        print "[*] Server Load"
        tableNessusServerLoad = Texttable()
        tableNessusServerLoad.set_cols_align(["l","l","l","l","l","l"])
        tableNessusServerLoad.set_cols_valign(["m","m","m","m","m","m"])
        tableNessusServerLoad.set_cols_width([20,20,20,20,20,20])
        rows = [["Scans", "Sessions","Hosts","TCP Sessions", "Load AVG", "Platform"],
                [nessusConverter.nessusStructure.serverLoad.numScans,nessusConverter.nessusStructure.serverLoad.numSessions,
                 nessusConverter.nessusStructure.serverLoad.numHosts,nessusConverter.nessusStructure.serverLoad.numTcpSessions,
                 nessusConverter.nessusStructure.serverLoad.loadAvg,nessusConverter.nessusStructure.serverLoad.platform]
               ]
        tableNessusServerLoad.add_rows(rows)
        print tableNessusServerLoad.draw()+"\n"


    def serverUuid(self):
        nessusConverter = NessusConverter(self.nessusClient.serverUuid())
        nessusConverter.serverUuidToStructure()

        tableNessusServerUuid = Texttable()
        tableNessusServerUuid.set_cols_align(["l"])
        tableNessusServerUuid.set_cols_valign(["m"])
        tableNessusServerUuid.set_cols_width([55])
        rows = [["UUID"],[nessusConverter.nessusStructure.uuid]]
        tableNessusServerUuid.add_rows(rows)
        print tableNessusServerUuid.draw()+"\n"

    def userAdd(self, userName, password, admin=1):
        if userName == '' or userName is None:
            pluginException = PluginException(message='The username specified is invalid.',
                                  trace="userAdd with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="userAdd")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The username specified is invalid. "
                raise pluginException

        if password == '' or password is None:
            pluginException = PluginException(message='The password specified is invalid.',
                                  trace="userAdd with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="userAdd")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The password specified is invalid. "
                raise pluginException

        if str(admin).isdigit() == False or admin not in [0,1]:
            pluginException = PluginException(message='The admin flag specified is invalid. Should be 1 (admin) or 0 (regular user)',
                                  trace="userAdd with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="userAdd")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The admin flag specified is invalid. "
                raise pluginException          
            
        administrator = False
        if admin == 1:
            administrator = True
        nessusConverter = NessusConverter(self.nessusClient.usersAdd(userName,password,administrator, method="POST"))
        nessusConverter.userToStructure()

        print "[*] User Created"
        tableUsers = Texttable()
        tableUsers.set_cols_align(["l","l","l","l"])
        tableUsers.set_cols_valign(["m","m","m","m"])
        tableUsers.set_cols_width([20,20,20,20])
        
        rows = [["Name", "Admin", "Idx", "Last-Login"],
                [nessusConverter.nessusStructure.nessusUser.name,nessusConverter.nessusStructure.nessusUser.admin,
                 nessusConverter.nessusStructure.nessusUser.idx,nessusConverter.nessusStructure.nessusUser.lastLogin]
               ]
        tableUsers.add_rows(rows)
        print tableUsers.draw()+"\n"

    def userEdit(self, userName, password, admin=1):
        if userName == '' or userName is None:
            pluginException = PluginException(message='The username specified is invalid.',
                                  trace="userEdit with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="userEdit")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The username specified is invalid. "
                raise pluginException

        if password == '' or password is None:
            pluginException = PluginException(message='The password specified is invalid.',
                                  trace="userEdit with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="userEdit")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The password specified is invalid. "
                raise pluginException

        if str(admin).isdigit() == False or admin not in [0,1]:
            pluginException = PluginException(message='The admin flag specified is invalid. Should be 1 (admin) or 0 (regular user)',
                                  trace="userEdit with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="userEdit")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The admin flag specified is invalid. "
                raise pluginException

            
        administrator = False
        if admin == 1:
            administrator = True
        nessusConverter = NessusConverter(self.nessusClient.usersEdit(userName,password,administrator))
        nessusConverter.userToStructure()

        print "[*] User Edited"
        tableUsers = Texttable()
        tableUsers.set_cols_align(["l","l","l","l"])
        tableUsers.set_cols_valign(["m","m","m","m"])
        tableUsers.set_cols_width([20,20,20,20])
        rows = [["Name", "Admin", "Idx", "Last-Login"],
                [nessusConverter.nessusStructure.nessusUser.name,
                 nessusConverter.nessusStructure.nessusUser.admin,
                 nessusConverter.nessusStructure.nessusUser.idx,
                 nessusConverter.nessusStructure.nessusUser.lastLogin]
               ]
        tableUsers.add_rows(rows)
        print tableUsers.draw()+"\n"

    def userDelete(self, userName):
        if userName == '' or userName is None:
            pluginException = PluginException(message='The username specified is invalid.',
                                  trace="userDelete with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="userDelete")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The username specified is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.usersDelete(userName))
        nessusConverter.userToStructure()

        print "[*] User Removed"
        tableUsers = Texttable()
        tableUsers.set_cols_align(["l","l","l","l"])
        tableUsers.set_cols_valign(["m","m","m","m"])
        tableUsers.set_cols_width([20,20,20,20])
        rows = [["Name", "Admin", "Idx", "Last-Login"],
                [nessusConverter.nessusStructure.nessusUser.name,
                 nessusConverter.nessusStructure.nessusUser.admin,
                 nessusConverter.nessusStructure.nessusUser.idx,
                 nessusConverter.nessusStructure.nessusUser.lastLogin]
               ]
        tableUsers.add_rows(rows)
        print tableUsers.draw()+"\n"

    def userChpasswd(self, userName, password):
        if userName == '' or userName is None:
            pluginException = PluginException(message='The username specified is invalid.',
                                  trace="userChpasswd with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="userChpasswd")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return 
            else:
                print "[-] The username specified is invalid. "
                raise pluginException

        if password == '' or password is None:
            pluginException = PluginException(message='The password specified is invalid.',
                                  trace="userChpasswd with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="userChpasswd")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The password specified is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.usersChpasswd(userName,password))
        nessusConverter.userToStructure()

        print "[*] User Password Changed"
        tableUsers = Texttable()
        tableUsers.set_cols_align(["l","l","l","l"])
        tableUsers.set_cols_valign(["m","m","m","m"])
        tableUsers.set_cols_width([20,20,20,20])
        rows = [["Name", "Admin", "Idx", "Last-Login"],
                [nessusConverter.nessusStructure.nessusUser.name,
                 nessusConverter.nessusStructure.nessusUser.admin,
                 nessusConverter.nessusStructure.nessusUser.idx,
                 nessusConverter.nessusStructure.nessusUser.lastLogin]
               ]
        tableUsers.add_rows(rows)
        print tableUsers.draw()+"\n"

    def usersList(self):
        nessusConverter = NessusConverter(self.nessusClient.usersList())
        nessusConverter.userToStructure()

        print "[*] User List"
        tableUsers = Texttable()
        tableUsers.set_cols_align(["l","l","l","l"])
        tableUsers.set_cols_valign(["m","m","m","m"])
        tableUsers.set_cols_width([20,20,20,20])
        rows = [["Name", "Admin", "Idx", "Last-Login"]]
                
        for nessusUser in nessusConverter.nessusStructure.nessusUsers:
            rows.append([nessusUser.name,nessusUser.admin,nessusUser.idx,nessusUser.lastLogin])
        tableUsers.add_rows(rows)
        print tableUsers.draw()+"\n"


    def pluginsList(self):
        nessusConverter = NessusConverter(self.nessusClient.pluginsList())
        nessusConverter.pluginsListToStructure()

        print "[*] Plugins List"
        tableUsers = Texttable()
        tableUsers.set_cols_align(["l","l"])
        tableUsers.set_cols_valign(["m","m"])
        tableUsers.set_cols_width([40,40])
        
        rows = [["Family Member", "Family Name"]]
        for nessusPlugin in nessusConverter.nessusStructure.pluginsList:
            rows.append([nessusPlugin.familyMembers, nessusPlugin.familyName])
        tableUsers.add_rows(rows)
        print tableUsers.draw()+"\n"

    def pluginAttributesList(self):
        nessusConverter = NessusConverter(self.nessusClient.pluginsAttributesList())
        nessusConverter.pluginsAttributesToStructure()
        print "[*] Plugins Attributes List"
        tablePluginsAttributes = Texttable()
        tablePluginsAttributes.set_cols_align(["l","l","l"])
        tablePluginsAttributes.set_cols_valign(["m","m","m"])
        tablePluginsAttributes.set_cols_width([30,30,30])
        
        rows = [["Readable Name", 'Readable Regex', 'List']]
        
        for pluginsAttribute in nessusConverter.nessusStructure.pluginsAttributes:
            rows.append([pluginsAttribute.readableName, pluginsAttribute.control.readableRegex,pluginsAttribute.control.list])
        tablePluginsAttributes.add_rows(rows)
        print tablePluginsAttributes.draw()+"\n"

    def pluginListsFamily(self, familyName):
        if familyName == '' or familyName is None:
            pluginException = PluginException(message='The familyName specified is invalid.',
                                  trace="pluginListsFamily with args username=%s , password=%s , admin=%s " %(userName, password, str(admin)),
                                  plugin="nessus", method="pluginListsFamily")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The familyName specified is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.pluginsListFamily(familyName))
        nessusConverter.pluginListFamilyToStructure()
        print "[*] Plugins List Family"
        tablePluginsListFamily = Texttable()
        tablePluginsListFamily.set_cols_align(["l","l","l","l"])
        tablePluginsListFamily.set_cols_valign(["m","m","m","m"])
        tablePluginsListFamily.set_cols_width([20,20,20,20])


        rows = [["Plugin ID", "Plugin Name", "Plugin Family", 'Plugin FileName']]
        for pluginFamily in nessusConverter.nessusStructure.pluginsListFamily:
            rows.append([pluginFamily.pluginId,pluginFamily.pluginName,pluginFamily.pluginFamily,pluginFamily.pluginFileName])
        tablePluginsListFamily.add_rows(rows)
        print tablePluginsListFamily.draw()+"\n"

    def pluginDescription(self, fileNamePlugin):
        if fileNamePlugin is None or fileNamePlugin == '':
            pluginException = PluginException(message='The fileNamePlugin specified is invalid.',
                                  trace="pluginDescription with args fileNamePlugin=%s " %(fileNamePlugin),
                                  plugin="nessus", method="pluginDescription")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The fileNamePlugin specified is invalid. "
                raise pluginException
        nessusConverter = NessusConverter(self.nessusClient.pluginsDescription(fileNamePlugin))
        nessusConverter.pluginsDescriptionToStructure()
        print "[*] Plugin Description"
        tablePluginDescription = Texttable()
        tablePluginDescription.set_cols_align(["l","l","l"])
        tablePluginDescription.set_cols_valign(["m","m","m"])
        tablePluginDescription.set_cols_width([20,20,20])

        
        rowsPluginDescription = [ ["Plugin ID", "Plugin Name", "Plugin Family"],
                                  [nessusConverter.nessusStructure.pluginsDescription.pluginId,nessusConverter.nessusStructure.pluginsDescription.pluginName,
                                   nessusConverter.nessusStructure.pluginsDescription.pluginFamily,]
                                ]
        tablePluginDescription.add_rows(rowsPluginDescription)
        print tablePluginDescription.draw()+"\n"
        print "\n"
        print "[*] Plugin Attributes"
        tablePluginAttributes = Texttable()
        tablePluginAttributes.set_cols_align(["l","l","l","l","l","l","l","l","l"])
        tablePluginAttributes.set_cols_valign(["m","m","m","m","m","m","m","m","m"])
        tablePluginAttributes.set_cols_width([10,10,10,10,10,10,10,10,10])
        
        rowsPluginAttributes = [["Vuln Date", "Risk Factor", "CVSS", 'Type', 'Patch Date', 'CVSS Score', 'CVE', 'BID', 'CPE']]
        if nessusConverter.nessusStructure.pluginsDescription is not None:
            rowsPluginAttributes.append([nessusConverter.nessusStructure.pluginsDescription.vulnPublicationDate,
                                        nessusConverter.nessusStructure.pluginsDescription.riskFactor,
                                        nessusConverter.nessusStructure.pluginsDescription.cvssBaseScore,
                                        nessusConverter.nessusStructure.pluginsDescription.pluginType,
                                        nessusConverter.nessusStructure.pluginsDescription.pluginPatchDate,
                                        nessusConverter.nessusStructure.pluginsDescription.cvssBaseScore,
                                        nessusConverter.nessusStructure.pluginsDescription.cve,
                                        nessusConverter.nessusStructure.pluginsDescription.bid,
                                        nessusConverter.nessusStructure.pluginsDescription.cpe,])
        tablePluginAttributes.add_rows(rowsPluginAttributes)
        print tablePluginAttributes.draw()+"\n"



    def pluginsAttributesFamilySearch(self, filter0Quality, filterSearchType, filter0Value, filter0Filter):
        nessusConverter = NessusConverter(self.nessusClient.pluginsAttributesFamilySearch(filter0Quality,filterSearchType,filter0Value,filter0Filter))
        nessusConverter.pluginsAttributeFamilySearchToStructure()
        print "[*] Family Search"
        tablePluginAttributes = Texttable()
        tablePluginAttributes.set_cols_align(["l"])
        tablePluginAttributes.set_cols_valign(["m"])
        tablePluginAttributes.set_cols_width([55])
        tablePluginAttributes.add_rows([["Family"], [nessusConverter.nessusStructure.pluginsAttributeFamilySearch]])
        print tablePluginAttributes.draw()+"\n"



    def pluginsAttributesPluginSearch(self, filter0quality, filterSearchType, filter0Value, filter0Filter, family):
        nessusConverter = NessusConverter(self.nessusClient.pluginsAttributesPluginSearch(filter0quality,filterSearchType,filter0Value,filter0Filter, family))
        nessusConverter.pluginsAttributePluginSearchToStructure()
        print "[*] Plugin Search"
        tablePluginAttributes = Texttable()
        tablePluginAttributes.set_cols_align(["l","l","l"])
        tablePluginAttributes.set_cols_valign(["m","m","m"])
        tablePluginAttributes.set_cols_width([30,30,30])
        
        rows = [["Family", "FileName", "Plugin ID", "Plugin Name"]]
        
        if nessusConverter.nessusStructure.pluginsAttributePluginSearch is not None:
            rows.append([nessusConverter.nessusStructure.pluginsAttributePluginSearch.pluginFamily,
                         nessusConverter.nessusStructure.pluginsAttributePluginSearch.pluginFileName,
                         nessusConverter.nessusStructure.pluginsAttributePluginSearch.pluginId,
                         nessusConverter.nessusStructure.pluginsAttributePluginSearch.pluginName])
        tablePluginAttributes.add_rows(rows)
        print tablePluginAttributes.draw()+"\n"

    def pluginsMd5(self):
        nessusConverter = NessusConverter(self.nessusClient.pluginsMd5())
        nessusConverter.md5StructureToStructure()
        print "[*] Plugins MD5"
        tableMD5 = Texttable()
        tableMD5.set_cols_align(["l","l"])
        tableMD5.set_cols_valign(["m","m"])
        tableMD5.set_cols_width([55,55])
        
        rows = [["FileName", "MD5 Hash"]]
        for md5 in nessusConverter.nessusStructure.md5Structure:
            rows.append([md5.fileName, md5.md5])
        tableMD5.add_rows(rows)
        print tableMD5.draw()+"\n"

    def policyPreferencesList(self):
        nessusConverter = NessusConverter(self.nessusClient.policyPreferencesList())
        nessusConverter.serverPolicyPreferenceToStructure()
        print "[*] Policy Preferences List"
        tablePreference = Texttable()
        tablePreference.set_cols_align(["l","l"])
        tablePreference.set_cols_valign(["m","m"])
        tablePreference.set_cols_width([55,55])
        
        rows = [["Name", "Value"]]
        for preference in nessusConverter.nessusStructure.policyPreferences:
            rows.append([preference.name, preference.value])
        tablePreference.add_rows(rows)
        print tablePreference.draw()+"\n"


    def policyList(self):
        nessusConverter = NessusConverter(self.nessusClient.policyList())
        nessusConverter.policyStructureToStructure()
        print "[*] Policy List"
        tablePolicies = Texttable()
        tablePolicies.set_cols_align(["l","l","l","l"])
        tablePolicies.set_cols_valign(["m","m","m","m"])
        tablePolicies.set_cols_width([30,30,30,30])
        
        rows = [["Id", "Name","Owner","Visibility"]]
        for policy in nessusConverter.nessusStructure.nessusPolicies:
            rows.append([policy.policyId, policy.policyName, policy.policyOwner, policy.policyVisibility])
        tablePolicies.add_rows(rows)
        print tablePolicies.draw()+"\n"

    def policyDelete(self, policyId):
        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="policyDelete with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="policyDelete")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.policyDelete(policyId))
        nessusConverter.policyDeletedToStructure()
        print "[*] Policy Deleted"
        tablePolicies = Texttable()
        tablePolicies.set_cols_align(["l"])
        tablePolicies.set_cols_valign(["m"])
        tablePolicies.set_cols_width([55])
        
        rows = [["Policy Deleted"]]
        for policy in nessusConverter.nessusStructure.nessusPolicies:
            rows.append([nessusConverter.nessusStructure.policyDeleted])
        tablePolicies.add_rows(rows)
        print tablePolicies.draw()+"\n"

    def policyCopy(self, policyId):
        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="policyCopy with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="policyCopy")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.policyCopy(policyId))
        nessusConverter.policyStructureToStructure()
        print "[*] Policy Copy"
        tablePolicies = Texttable()
        tablePolicies.set_cols_align(["l","l","l","l"])
        tablePolicies.set_cols_valign(["m","m","m","m"])
        tablePolicies.set_cols_width([30,30,30,30])
        
        rows = [["Id", "Name","Owner","Visibility"]]
        for policy in nessusConverter.nessusStructure.nessusPolicies:
            rows.append([policy.policyId, policy.policyName, policy.policyOwner, policy.policyVisibility])
        tablePolicies.add_rows(rows)
        print tablePolicies.draw()+"\n"


    def policyDownload(self, policyId, fileName):
        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="policyDownload with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="policyDownload")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException
        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="policyDownload with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="policyDownload")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.policyDownload(policyId))
        nessusConverter.policyDownloadedToStructure()
        try:
            fileDescriptor = open(fileName, "w")
            fileDescriptor.write(str(nessusConverter.nessusStructure.policyDownloaded))
            fileDescriptor.close()
            print "[+] Policy's file downloaded successfully."
        except:
            pluginException = PluginException(message='Error downloading the policy. Check the file name specified.',
                                  trace=sys.exc_info()[0],
                                  plugin="nessus", method="policyDownload")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] Error downloading the policy. Check the file name specified."
                raise pluginException
            



    def scanAllRelays(self, policyId, scanName):
        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="scanAllRelays with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="scanAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException

        if scanName == '' or scanName is None:
            pluginException = PluginException(message='The scan name specified is invalid.',
                                  trace="scanAllRelays with args scanName=%s " %(str(scanName)),
                                  plugin="nessus", method="scanAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The scan name specified is invalid. "
                raise pluginException
            
            
        targets = ''
        for node in self.torNodes:
            targets +=node.host+"\n"
        nessusConverter = NessusConverter(self.nessusClient.scanNew(targets, policyId, scanName, method="POST"))
        nessusConverter.scanToStructure()

        tableScan = Texttable()
        tableScan.set_cols_align(["l","l","l","l","l","l","l","l"])
        tableScan.set_cols_valign(["m","m","m","m","m","m","m","m"])
        tableScan.set_cols_width([20,20,20,20,20,20,20,20])

        rows = [["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"],
                [nessusConverter.nessusStructure.scan.owner,
                 nessusConverter.nessusStructure.scan.scanName,
                 nessusConverter.nessusStructure.scan.startTime,
                 nessusConverter.nessusStructure.scan.uuid,
                 nessusConverter.nessusStructure.scan.readableName,
                 nessusConverter.nessusStructure.scan.status,
                 nessusConverter.nessusStructure.scan.completionCurrent,
                 nessusConverter.nessusStructure.scan.completionTotal]
               ]
        tableScan.add_rows(rows)
        print tableScan.draw()+"\n"


    def scanByRelay(self, policyId, scanName, relay):
        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="scanByRelay with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="scanByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException

        if scanName == '' or scanName is None:
            pluginException = PluginException(message='The scan name specified is invalid.',
                                  trace="scanByRelay with args scanName=%s " %(str(scanName)),
                                  plugin="nessus", method="scanByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The scan name specified is invalid. "
                raise pluginException

        if is_valid_ipv4_address(relay) == False and is_valid_ipv6_address(relay) == False and is_valid_domain(relay) == False:
            pluginException = PluginException(message='[-] The relay specified is invalid. %s ' %(relay),
                                              trace="scanByRelay with args relay=%s " %(relay),
                                              plugin="nessus", method="scanByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print '[-] The relay specified is invalid. %s ' %(relay)
                raise pluginException
            
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
            tableScan = Texttable()
            tableScan.set_cols_align(["l","l","l","l","l","l","l","l"])
            tableScan.set_cols_valign(["m","m","m","m","m","m","m","m"])
            tableScan.set_cols_width([20,20,20,20,20,20,20,20])
            rows = [["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"],
                    [nessusConverter.nessusStructure.scan.owner,
                     nessusConverter.nessusStructure.scan.scanName,
                     nessusConverter.nessusStructure.scan.startTime,
                     nessusConverter.nessusStructure.scan.uuid,
                     nessusConverter.nessusStructure.scan.readableName,
                     nessusConverter.nessusStructure.scan.status,
                     nessusConverter.nessusStructure.scan.completionCurrent,
                     nessusConverter.nessusStructure.scan.completionTotal]
                    ]
            tableScan.add_rows(rows)
            print tableScan.draw()+"\n"
        else:
            print ["[-] The relay specified is not found."]

    def scanStop(self, scanUuid):
        if scanUuid == '' or scanUuid is None:
            pluginException = PluginException(message='The scan uuid specified is invalid.',
                                  trace="scanStop with args scanUuid=%s " %(str(scanUuid)),
                                  plugin="nessus", method="scanStop")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The scan uuid specified is invalid. "
                raise pluginException
        
        nessusConverter = NessusConverter(self.nessusClient.scanStop(scanUuid))
        nessusConverter.scanToStructure()
        print "[*] Nessus scan stopped."
        tableScan = Texttable()
        tableScan.set_cols_align(["l","l","l","l","l","l","l","l"])
        tableScan.set_cols_valign(["m","m","m","m","m","m","m","m"])
        tableScan.set_cols_width([20,20,20,20,20,20,20,20])

        rows = [["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"],
                [nessusConverter.nessusStructure.scan.owner,
                 nessusConverter.nessusStructure.scan.scanName,
                 nessusConverter.nessusStructure.scan.startTime,
                 nessusConverter.nessusStructure.scan.uuid,
                 nessusConverter.nessusStructure.scan.readableName,
                 nessusConverter.nessusStructure.scan.status,
                 nessusConverter.nessusStructure.scan.completionCurrent,
                 nessusConverter.nessusStructure.scan.completionTotal]
               ]
        tableScan.add_rows(rows)
        print tableScan.draw()+"\n"

    def scanResume(self, scanUuid):
        if scanUuid == '' or scanUuid is None:
            pluginException = PluginException(message='The scan uuid specified is invalid.',
                                  trace="scanResume with args scanUuid=%s " %(str(scanUuid)),
                                  plugin="nessus", method="scanResume")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The scan uuid specified is invalid. "
                raise pluginException
        nessusConverter = NessusConverter(self.nessusClient.scanResume(scanUuid))
        nessusConverter.scanToStructure()
        print "[*] Nessus scan Resumed."
        tableScan = Texttable()
        tableScan.set_cols_align(["l","l","l","l","l","l","l","l"])
        tableScan.set_cols_valign(["m","m","m","m","m","m","m","m"])
        tableScan.set_cols_width([20,20,20,20,20,20,20,20])

        rows = [["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"],
                [nessusConverter.nessusStructure.scan.owner,
                 nessusConverter.nessusStructure.scan.scanName,
                 nessusConverter.nessusStructure.scan.startTime,
                 nessusConverter.nessusStructure.scan.uuid,
                 nessusConverter.nessusStructure.scan.readableName,
                 nessusConverter.nessusStructure.scan.status,
                 nessusConverter.nessusStructure.scan.completionCurrent,
                 nessusConverter.nessusStructure.scan.completionTotal]
               ]
        tableScan.add_rows(rows)
        print tableScan.draw()+"\n"

    def scanPause(self, scanUuid):
        if scanUuid == '' or scanUuid is None:
            pluginException = PluginException(message='The scan uuid specified is invalid.',
                                  trace="scanPause with args scanUuid=%s " %(str(scanUuid)),
                                  plugin="nessus", method="scanPause")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The scan uuid specified is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.scanPause(scanUuid))
        nessusConverter.scanToStructure()
        print "[*] Nessus scan Paused."
        tableScan = Texttable()
        tableScan.set_cols_align(["l","l","l","l","l","l","l","l"])
        tableScan.set_cols_valign(["m","m","m","m","m","m","m","m"])
        tableScan.set_cols_width([20,20,20,20,20,20,20,20])

        rows = [["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"],
                [nessusConverter.nessusStructure.scan.owner,
                 nessusConverter.nessusStructure.scan.scanName,
                 nessusConverter.nessusStructure.scan.startTime,
                 nessusConverter.nessusStructure.scan.uuid,
                 nessusConverter.nessusStructure.scan.readableName,
                 nessusConverter.nessusStructure.scan.status,
                 nessusConverter.nessusStructure.scan.completionCurrent,
                 nessusConverter.nessusStructure.scan.completionTotal]
               ]
        tableScan.add_rows(rows)
        print tableScan.draw()+"\n"

    def scanList(self):
        nessusConverter = NessusConverter(self.nessusClient.scanList(method="POST"))
        nessusConverter.scanListToStructure()
        print "[*] Nessus scan List."
        tableScan = Texttable()
        tableScan.set_cols_align(["l","l","l","l","l","l","l","l"])
        tableScan.set_cols_valign(["m","m","m","m","m","m","m","m"])
        tableScan.set_cols_width([20,20,20,20,20,20,20,20])

        rows = [["Owner", "Scan Name", "Start Time", "UUID", "Readable Name", "Status", "Completion Current","Completion Total"]]
        if len(nessusConverter.nessusStructure.scanList) > 0:
            for scan in nessusConverter.nessusStructure.scanList:
                rows.append([scan.owner, scan.scanName, scan.startTime, scan.uuid,
                             scan.readablename, scan.status,
                             scan.completionCurrent, scan.completionTotal])
        tableScan.add_rows(rows)
        print tableScan.draw()+"\n"

    def scanTemplateAllRelays(self, policyId, templateName):
        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="scanTemplateAllRelays with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="scanTemplateAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException

        if templateName == '' or templateName is None:
            pluginException = PluginException(message='The template name specified is invalid.',
                                  trace="scanTemplateAllRelays with args templateName=%s " %(str(templateName)),
                                  plugin="nessus", method="scanTemplateAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The template name specified is invalid. "
                raise pluginException
            
        targets = ''
        for node in self.torNodes:
            targets +=node.host+"\n"
        nessusConverter = NessusConverter(self.nessusClient.scanTemplateNew(policyId,targets,templateName))
        nessusConverter.scanTemplateToStructure()
        print "[*] Nessus scan Template New."
        tableTemplate = Texttable()
        tableTemplate.set_cols_align(["l","l","l","l","l"])
        tableTemplate.set_cols_valign(["m","m","m","m","m"])
        tableTemplate.set_cols_width([20,20,20,20,20])
        
        rows = [["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"],
                [nessusConverter.nessusStructure.nessusScanTemplate.owner,
                               nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                               nessusConverter.nessusStructure.nessusScanTemplate.target,
                               nessusConverter.nessusStructure.nessusScanTemplate.name,
                               nessusConverter.nessusStructure.nessusScanTemplate.policyId]]
        
        tableTemplate.add_rows(rows)
        print tableTemplate.draw()+"\n"

    def scanTemplateByRelay(self,policyId,relay,templateName):
        if is_valid_ipv4_address(relay) == False and is_valid_ipv6_address(relay) == False and is_valid_domain(relay) == False:
            pluginException = PluginException(message='[-] The relay specified is invalid. %s ' %(relay),
                                              trace="scanTemplateByRelay with args relay=%s " %(relay),
                                              plugin="nessus", method="scanTemplateByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print '[-] The relay specified is invalid. %s ' %(relay)
                raise pluginException

        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="scanTemplateByRelay with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="scanTemplateByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException

        if templateName == '' or templateName is None:
            pluginException = PluginException(message='The template name specified is invalid.',
                                  trace="scanTemplateByRelay with args templateName=%s " %(str(templateName)),
                                  plugin="nessus", method="scanTemplateByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The template name specified is invalid. "
                raise pluginException

            
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
            tableTemplate = Texttable()
            tableTemplate.set_cols_align(["l","l","l","l","l"])
            tableTemplate.set_cols_valign(["m","m","m","m","m"])
            tableTemplate.set_cols_width([20,20,20,20,20])
            rows = [["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"],
                    [nessusConverter.nessusStructure.nessusScanTemplate.owner,
                     nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                     nessusConverter.nessusStructure.nessusScanTemplate.target,
                     nessusConverter.nessusStructure.nessusScanTemplate.name,
                     nessusConverter.nessusStructure.nessusScanTemplate.policyId]]
            tableTemplate.add_rows(rows)
            print tableTemplate.draw()+"\n"


    def scanTemplateEditAllRelays(self, templateEdit, templateNewName, policyId):
        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="scanTemplateEditAllRelays with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="scanTemplateEditAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException

        if templateEdit == '' or templateEdit is None:
            pluginException = PluginException(message='The template name specified to edit is invalid.',
                                  trace="scanTemplateEditAllRelays with args templateEdit=%s " %(str(templateEdit)),
                                  plugin="nessus", method="scanTemplateEditAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The template name specified to edit is invalid. "
                raise pluginException

        if templateNewName == '' or templateNewName is None:
            pluginException = PluginException(message='The template name specified to create is invalid.',
                                  trace="scanTemplateEditAllRelays with args templateNewName=%s " %(str(templateNewName)),
                                  plugin="nessus", method="scanTemplateEditAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The template name specified to create is invalid. "
                raise pluginException
            
        targets = ''
        for node in self.torNodes:
            targets +=node.host+"\n"
        nessusConverter = NessusConverter(self.nessusClient.scanTemplateEdit(templateEdit,templateNewName,policyId,targets))
        nessusConverter.scanTemplateToStructure()
        print "[*] Nessus scan Template Edit."
        tableTemplate = Texttable()
        tableTemplate.set_cols_align(["l","l","l","l","l"])
        tableTemplate.set_cols_valign(["m","m","m","m","m"])
        tableTemplate.set_cols_width([20,20,20,20,20])
        rows = [["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"]]
        if nessusConverter.nessusStructure.nessusScanTemplate is not  None:
            rows.append([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                         nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                         nessusConverter.nessusStructure.nessusScanTemplate.target,
                         nessusConverter.nessusStructure.nessusScanTemplate.name,
                         nessusConverter.nessusStructure.nessusScanTemplate.policyId])
            
        tableTemplate.add_rows(rows)
        print tableTemplate.draw()+"\n"

        
        

    def scanTemplateEditByRelay(self,templateEdit, templateNewName, policyId, relay):
        if str(policyId).isdigit() == False or policyId is None:
            pluginException = PluginException(message='The policy identifier specified is invalid.',
                                  trace="scanTemplateEditByRelay with args policyId=%s " %(str(policyId)),
                                  plugin="nessus", method="scanTemplateEditByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The policy identifier specified is invalid. "
                raise pluginException

        if templateEdit == '' or templateEdit is None:
            pluginException = PluginException(message='The template name specified to edit is invalid.',
                                  trace="scanTemplateEditByRelay with args templateEdit=%s " %(str(templateEdit)),
                                  plugin="nessus", method="scanTemplateEditByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The template name specified to edit is invalid. "
                raise pluginException

        if templateNewName == '' or templateNewName is None:
            pluginException = PluginException(message='The template name specified to create is invalid.',
                                  trace="scanTemplateEditByRelay with args templateNewName=%s " %(str(templateNewName)),
                                  plugin="nessus", method="scanTemplateEditByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The template name specified to create is invalid. "
                raise pluginException
            
        if is_valid_ipv4_address(relay) == False and is_valid_ipv6_address(relay) == False and is_valid_domain(relay) == False:
            pluginException = PluginException(message='[-] The relay specified is invalid. %s ' %(relay),
                                              trace="scanTemplateByRelay with args relay=%s " %(relay),
                                              plugin="nessus", method="scanTemplateEditByRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print '[-] The relay specified is invalid. %s ' %(relay)
                raise pluginException
            
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
            tableTemplate = Texttable()
            tableTemplate.set_cols_align(["l","l","l","l","l"])
            tableTemplate.set_cols_valign(["m","m","m","m","m"])
            tableTemplate.set_cols_width([20,20,20,20,20])
            rows = [["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"]]

            if nessusConverter.nessusStructure.nessusScanTemplate is not None:
                rows.append([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                             nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                             nessusConverter.nessusStructure.nessusScanTemplate.target,
                             nessusConverter.nessusStructure.nessusScanTemplate.name,
                             nessusConverter.nessusStructure.nessusScanTemplate.policyId])
            tableTemplate.add_rows(rows)
            print tableTemplate.draw()+"\n"

    def scanTemplateDelete(self, templateUuid):
        if templateUuid == '' or templateUuid is None:
            pluginException = PluginException(message='The template uuid specified is invalid.',
                                  trace="scanTemplateDelete with args templateUuid=%s " %(str(templateUuid)),
                                  plugin="nessus", method="scanTemplateDelete")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The template uuid specified is invalid. "
                raise pluginException

            
        nessusConverter = NessusConverter(self.nessusClient.scanTemplateDelete(templateUuid))
        nessusConverter.scanTemplateToStructure()
        print "[*] Nessus scan Template Deleted."
        tableTemplate = Texttable()
        tableTemplate.set_cols_align(["l","l","l","l","l"])
        tableTemplate.set_cols_valign(["m","m","m","m","m"])
        tableTemplate.set_cols_width([20,20,20,20,20])
        rows = [["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"]]
        
        if nessusConverter.nessusStructure.nessusScanTemplate is not None:
            rows.append([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                         nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                         nessusConverter.nessusStructure.nessusScanTemplate.target,
                         nessusConverter.nessusStructure.nessusScanTemplate.name,
                         nessusConverter.nessusStructure.nessusScanTemplate.policyId])
        tableTemplate.add_rows(rows)
        print tableTemplate.draw()+"\n"

    def scanTemplateLaunch(self, templateName):
        
        if templateName == '' or templateName is None:
            pluginException = PluginException(message='The template name specified to launch is invalid.',
                                  trace="scanTemplateLaunch with args templateName=%s " %(str(templateName)),
                                  plugin="nessus", method="scanTemplateLaunch")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The template name specified to lauch is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.scanTemplateLaunch(templateName))
        #Nessus will return an scan structure.
        nessusConverter.scanToStructure()
        print "[*] Nessus scan Template Launch."
        tableTemplate = Texttable()
        tableTemplate.set_cols_align(["l","l","l","l","l"])
        tableTemplate.set_cols_valign(["m","m","m","m","m"])
        tableTemplate.set_cols_width([20,20,20,20,20])
        rows = [["Owner", "Readable Name", "Target", "Scan Name", "Policy ID"]]
        
        if nessusConverter.nessusStructure.nessusScanTemplate is not None:
            rows.append([nessusConverter.nessusStructure.nessusScanTemplate.owner,
                         nessusConverter.nessusStructure.nessusScanTemplate.readablename,
                         nessusConverter.nessusStructure.nessusScanTemplate.target,
                         nessusConverter.nessusStructure.nessusScanTemplate.name,
                         nessusConverter.nessusStructure.nessusScanTemplate.policyId])
        tableTemplate.add_rows(rows)
        print tableTemplate.draw()+"\n"

    def reportList(self):
        nessusConverter = NessusConverter(self.nessusClient.reportList())
        nessusConverter.reportToStructure()
        print "[*] Nessus Report List."
        tableReport = Texttable()
        tableReport.set_cols_align(["l","l","l","l"])
        tableReport.set_cols_valign(["m","m","m","m"])
        tableReport.set_cols_width([20,20,20,20])
        rows = [["Status","Readable Name", "UUID", "Timestamp"]]
        
        if nessusConverter.nessusStructure.reportList is not None:
            for report in nessusConverter.nessusStructure.reportList:
                rows.append([report.status,
                             report.readablename,
                             report.name,
                             report.timestamp])
        tableReport.add_rows(rows)
        print tableReport.draw()+"\n"

    def reportDelete(self, reportUuid):
        if reportUuid == '' or reportUuid is None:
            pluginException = PluginException(message='The report uuid specified is invalid.',
                                  trace="reportDelete with args reportUuid=%s " %(str(reportUuid)),
                                  plugin="nessus", method="reportDelete")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The report uuid specified is invalid. "
                raise pluginException


        nessusConverter = NessusConverter(self.nessusClient.reportDelete(reportUuid))
        nessusConverter.reportToStructure()
        if nessusConverter.nessusStructure.report:
            print "[*] Report %s deleted." %(reportUuid)

    def reportHosts(self,reportUuid):
        if reportUuid == '' or reportUuid is None:
            pluginException = PluginException(message='The report uuid specified is invalid.',
                                  trace="reportDelete with args reportUuid=%s " %(str(reportUuid)),
                                  plugin="nessus", method="reportDelete")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The report uuid specified is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.reportHosts(reportUuid))
        nessusConverter.reportHostToStructure()
        print "[*] Nessus Report Hosts List."
        tableReport = Texttable()
        tableReport.set_cols_align(["l","l","l","l","l","l"])
        tableReport.set_cols_valign(["m","m","m","m","m","m"])
        tableReport.set_cols_width([20,20,20,20,20,20])
        
        rows = [["Hostname","Num. Checks", "Total Checks", "Scan Progress Current", "Scan Progress Total", "Severity"]]
        
        if nessusConverter.nessusStructure.reportHosts is not None:
            for reportHost in nessusConverter.nessusStructure.reportHosts:
                rows.append([reportHost.hostname,
                             reportHost.numchecksconsidered,
                             reportHost.totalchecksconsidered,
                             reportHost.scanprogresscurrent,
                             reportHost.scanprogresstotal,
                             reportHost.severity])
        tableReport.add_rows(rows)
        print tableReport.draw()+"\n"

    def reportPorts(self, reportUuid, hostname):
        if reportUuid == '' or reportUuid is None:
            pluginException = PluginException(message='The report uuid specified is invalid.',
                                  trace="reportDelete with args reportUuid=%s " %(str(reportUuid)),
                                  plugin="nessus", method="reportDelete")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The report uuid specified is invalid. "
                raise pluginException
            
        if hostname == '' or hostname is None:
            pluginException = PluginException(message='The hostname is invalid.',
                                  trace="reportPorts with args hostname=%s " %(str(hostname)),
                                  plugin="nessus", method="reportPorts")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The hostname is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.reportPorts(reportUuid, hostname))
        nessusConverter.reportPortToStructure()
        print "[*] Nessus Report Ports."
        tableReport = Texttable()
        tableReport.set_cols_align(["l","l","l","l"])
        tableReport.set_cols_valign(["m","m","m","m"])
        tableReport.set_cols_width([20,20,20,20])
        
        rows = [["Port Number","Protocol", "Severity", "SVC Name"]]
        if nessusConverter.nessusStructure.reportPortList is not None:
            for reportPort in nessusConverter.nessusStructure.reportPortList:
                rows.append([reportPort.portNumber,
                             reportPort.protocol,
                             reportPort.severity,
                             reportPort.svcName])
        tableReport.add_rows(rows)
        print tableReport.draw()+"\n"

    def reportDetails(self,reportUuid, hostname,port,protocol):
        if reportUuid == '' or reportUuid is None:
            pluginException = PluginException(message='The report uuid specified is invalid.',
                                  trace="reportDetails with args reportUuid=%s " %(str(reportUuid)),
                                  plugin="nessus", method="reportDetails")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The report uuid specified is invalid. "
                raise pluginException
            
        if hostname == '' or hostname is None:
            pluginException = PluginException(message='The hostname is invalid.',
                                  trace="reportDetails with args hostname=%s " %(str(hostname)),
                                  plugin="nessus", method="reportDetails")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The hostname is invalid. "
                raise pluginException

        if protocol == '' or protocol is None:
            pluginException = PluginException(message='The protocol is invalid.',
                                  trace="reportDetails with args protocol=%s " %(str(protocol)),
                                  plugin="nessus", method="reportDetails")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The protocol is invalid. "
                raise pluginException
            
        if is_valid_port(port) == False:
            pluginException = PluginException(message='The port is invalid.',
                                  trace="reportDetails with args port=%s " %(str(port)),
                                  plugin="nessus", method="reportDetails")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The protocol is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.reportDetails(reportUuid,hostname,port,protocol))
        nessusConverter.reportPortDetailToStructure()
        print "[*] Nessus Report Details."
        tableReport = Texttable()
        tableReport.set_cols_align(["l","l","l","l","l","l","l","l","l","l","l","l"])
        tableReport.set_cols_valign(["m","m","m","m","m","m","m","m","m","m","m","m"])
        tableReport.set_cols_width([10,10,10,10,10,10,10,10,10,10,10,10])
        
        rows = [["ItemId", "Port", "Severity", "Plugin Id", "Plugin Name", "BID", "CPE","CVE","CVSS Base Score","CVSS Temporal Score","Description", "FName"]]
        if nessusConverter.nessusStructure.reportPortDetail is not None:
            for reportPort in nessusConverter.nessusStructure.reportPortDetail:
                rows.append([reportPort.itemId,
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
        tableReport.add_rows(rows)
        print tableReport.draw()+"\n"

    def reportTags(self, reportUuid, hostname):
        if reportUuid == '' or reportUuid is None:
            pluginException = PluginException(message='The report uuid specified is invalid.',
                                  trace="reportTags with args reportUuid=%s " %(str(reportUuid)),
                                  plugin="nessus", method="reportTags")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The report uuid specified is invalid. "
                raise pluginException
            
        if hostname == '' or hostname is None:
            pluginException = PluginException(message='The hostname is invalid.',
                                  trace="reportTags with args hostname=%s " %(str(hostname)),
                                  plugin="nessus", method="reportTags")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The hostname is invalid. "
                raise pluginException


        nessusConverter = NessusConverter(self.nessusClient.reportTags(reportUuid, hostname))
        nessusConverter.tagToNessusStructure()
        print "[*] Nessus Tags."
        tableReport = Texttable()
        tableReport.set_cols_align(["l","l"])
        tableReport.set_cols_valign(["m","m"])
        tableReport.set_cols_width([55,55])
        
        rows = [["Tag Name","Tag Value"]]
        if nessusConverter.nessusStructure.nessusTags is not None:
            for tag in nessusConverter.nessusStructure.nessusTags:
                rows.append([tag.name, tag.value])
        else:
            print "[*] No results."

        tableReport.add_rows(rows)
        print tableReport.draw()+"\n"

    def reportAttributesList(self,reportUuid):
        if reportUuid == '' or reportUuid is None:
            pluginException = PluginException(message='The report uuid specified is invalid.',
                                  trace="reportAttributesList with args reportUuid=%s " %(str(reportUuid)),
                                  plugin="nessus", method="reportAttributesList")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The report uuid specified is invalid. "
                raise pluginException
            
        nessusConverter = NessusConverter(self.nessusClient.reportAttributesList(reportUuid))
        nessusConverter.reportAttributesToStructure()
        print "[*] Nessus Report Attributes."
        tableReport = Texttable()
        tableReport.set_cols_align(["l","l","l","l"])
        tableReport.set_cols_valign(["m","m","m","m"])
        tableReport.set_cols_width([30,30,30,30])
        
        rows = [["Name","Readable Name","Readable Regex", "Operators"]]
        if nessusConverter.nessusStructure.nessusReportAttributes is not None:
            for reportAttribute in nessusConverter.nessusStructure.nessusReportAttributes:
                rows.append([reportAttribute.name,
                                     reportAttribute.readableName,
                                     reportAttribute.nessusControl.readableRegex,
                                     reportAttribute.operators])
        tableReport.add_rows(rows)
        print tableReport.draw()+"\n"

        

    def help(self):
        print "[*] Functions availaible available in the Plugin...\n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'],
                         ['feed', 'Return the Nessus Feed', 'self.feed()'],
                         ['serverSecureSettingsList', 'List of Server Secure Settings', 'self.serverSecureSettingsList()'],
                         ['serverRegister', 'Registers the Nessus server with Tenable Network Security', "self.serverRegister('FEED_CODE')"],
                         ['serverLoad', 'Server Load and Platform Type', "self.serverLoad()"],
                         ['serverUuid', 'Server UUID', "self.serverUuid()"],
                         ['userAdd', 'Create a new user', "self.userAdd('adastra','adastra',0)"],
                         ['userEdit', 'Edit the user specified', "self.userEdit('adastra','new_password',1)"],
                         ['userDelete', 'Delete the user specified', "self.userDelete('adastra')"],
                         ['userChpasswd', 'Change the password for the user specified', "self.userChpasswd('adastra','new_password')"],
                         ['usersList', 'List of users.', "self.usersList()"],
                         ['pluginsList', 'List of plugins.', "self.pluginsList()"],
                         ['pluginAttributesList', 'List of plugins attributes for plugin filtering.', "self.pluginListsFamily('AIX Local Security Checks')"],
                         ['pluginDescription', 'Returns the entire description of a given plugin.', "self.pluginDescription('ping_host.nasl')"],
                         ['pluginsAttributesFamilySearch', 'Filters against the family of plugins.', "self.pluginsAttributesFamilySearch('match','or','modicon','description')"],
                         ['pluginsAttributesPluginSearch', 'Returns the plugins in a family that match a given filter criteria.', "self.pluginsAttributesPluginSearch('match','or','modicon','description','FTP')"],
                         ['pluginsMd5', 'List of plugin file names and corresponding MD5 hashes.', "self.pluginsMd5()"],
                         ['policyList', 'List of available policies, policy settings and default values.', "self.policyList()"],
                         ['policyDelete', 'Delete the policy specified.', "self.policyDelete(POLICY_ID)"],
                         ['policyCopy', 'Copies an existing policy to a new policy.', "self.policyCopy(POLICY_ID)"],
                         ['policyDownload', 'Download the policy from the server to the local system.', "self.policyDownload(POLICY_ID, '/home/user/policy.nessus')"],
                         #['scanAllRelays', 'Create a new scan with all relays loaded.', "self.scanAllRelays(<POLICY_ID>, 'newScan')"],
                         #['scanByRelay', 'Create a new scan with the specified relay.', "self.scanAllRelays(<POLICY_ID>, 'newScan', <IP_OR_NICKNAME>)"],
                         ['scanStop', 'Stops the specified started scan.', "self.scanStop(<SCAN_UUID>)"],
                         ['scanResume', 'Resumes the specified paused scan.', "self.scanResume(<SCAN_UUID>)"],
                         ['scanPause', 'Pauses the specified actived scan.', "self.scanPause(<SCAN_UUID>)"],
                         ['scanList', 'List of finished scans.', "self.scanList()"],
                         ['scanTemplateAllRelays', 'Create a new scan template (scheduled) with all relays loaded.', "self.scanTemplateAllRelays(<POLICY_ID>,<TEMPLATE_NAME>)"],
                         ['scanTemplateByRelay', 'Create a new scan template (scheduled) with the specified relay.', "self.scanTemplateByRelay(<POLICY_ID>,<TEMPLATE_NEW_NAME>,<IP_OR_NICKNAME>)"],
                         ['scanTemplateEditAllRelays', 'Edit the scan template specified with all relays loaded.', "self.scanTemplateEditAllRelays(<POLICY_ID>,<TEMPLATE_NEW_NAME>)"],
                         ['scanTemplateEditByRelay', 'Edit the scan template specified with the specified relay.', "self.scanTemplateEditByRelay(<TEMPLATE_UUID>,<TEMPLATE_NEW_NAME>,<POLICY_ID>,<IP_OR_NICKNAME>)"],
                         ['scanTemplateDelete', 'Delete the scan template specified.', "self.scanTemplateDelete(<TEMPLATE_UUID>)"],
                         ['scanTemplateLaunch', 'Launch the scan template specified.', "self.scanTemplateLaunch(<TEMPLATE_UUID>)"],
                         ['reportList', 'List of available scan reports.', "self.reportList()"],
                         ['reportDelete', 'Delete the specified report.', "self.reportDelete(<REPORT_UUID>)"],
                         ['reportHosts', 'List of hosts contained in a specified report.', "self.reportHosts(<REPORT_UUID>)"],
                         ['reportPorts', 'List of ports and the number of findings on each port.', "self.reportPorts(<REPORT_UUID>,<HOSTNAME>)"],
                         ['reportDetails', 'Details of a scan for a given host.', "self.reportDetails(<REPORT_UUID>,<HOSTNAME>,<PORT>,<PROTOCOL>)"],
                         ['reportTags', 'Tags of a scan for a given host.', "self.reportTags(<REPORT_UUID>, <HOSTNAME>)"],
                         ['reportAttributesList', 'List of filter attributes associated with a given report.', "self.reportAttributesList(<REPORT_UUID>)"]
                        ])
        print table.draw() + "\\n"
