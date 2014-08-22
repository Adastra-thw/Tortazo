# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

w3afPlugin.py

w3afPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3afPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from w3af.core.data.parsers.url import URL as URL_KLASS
from plugins.texttable import Texttable
from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from w3af.core.controllers.w3afCore import w3afCore
from w3af.core.data.options.option_list import OptionList
from w3af.core.data.options.opt_factory import opt_factory
from w3af.core.data.kb.knowledge_base import kb
from w3af.core.controllers.misc_settings import MiscSettings
import w3af.core.data.kb.config as cf
from core.tortazo.exceptions.PluginException import PluginException
from plugins.utils.validations.Validator import *

class w3afPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'w3afPlugin')
        self.setPluginDetails('w3afPlugin', 'Plugin to load the W3AF context in Tortazo. You can execute W3AF against the TOR deep web.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] w3afPlugin Initialized!")
            self.w3afCorePlugin = w3afCore()
            self.w3afCorePlugin.plugins.init_plugins()
            self.w3afCorePlugin.plugins.zero_enabled_plugins()
            self.miscSettings = MiscSettings()
        self.pluginConfigs= {}


    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)

    
    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] w3afPlugin Destroyed!")


    '''
    PLUGIN MANAGEMENT FUNCTIONS.
    '''
    def showPluginsByType(self, pluginType):
        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="showPluginsByType with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="showPluginsByType")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException
        pluginByType = self.w3afCorePlugin.plugins.get_plugin_list(pluginType)
        tablePlugins = Texttable()
        tablePlugins.set_cols_align(["l"])
        tablePlugins.set_cols_valign(["m"])
        tablePlugins.set_cols_width([55])
        rows = [ ["[*] Plugins for %s "%(pluginType)] ]
        for plugin in pluginByType:
            rows.append([plugin])
            
        tablePlugins.add_rows(rows)
        print tablePlugins.draw() + "\n"


    def showPluginTypes(self):
        types = self.w3afCorePlugin.plugins.get_plugin_types()

        tableTypes = Texttable()
        tableTypes.set_cols_align(["l"])
        tableTypes.set_cols_valign(["m"])
        tableTypes.set_cols_width([55])
        rows = [ ["[*] Plugins Types"] ]
        for plugintype in types:
            rows.append([plugintype])
        tableTypes.add_rows(rows)       
        print tableTypes.draw() + "\n"

    def getEnabledPluginsByType(self, pluginType):
        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="getEnabledPluginsByType with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="getEnabledPluginsByType")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException
            
        enabled = self.w3afCorePlugin.plugins.get_enabled_plugins(pluginType)
        tablePluginsEnabled = Texttable()
        tablePluginsEnabled.set_cols_align(["l"])
        tablePluginsEnabled.set_cols_valign(["m"])
        tablePluginsEnabled.set_cols_width([55])
        rows = [ ["[*] Enabled plugins by type %s" %(pluginType)] ]
        for plugin in enabled:
            rows.append([plugin])
        tablePluginsEnabled.add_rows(rows)       
        print tablePluginsEnabled.draw() + "\n"

    def getPluginTypeDescription(self, pluginType):
        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="getPluginTypeDescription with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="getPluginTypeDescription")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException
            
        tablePluginsEnabled = Texttable()
        tablePluginsEnabled.set_cols_align(["l"])
        tablePluginsEnabled.set_cols_valign(["m"])
        tablePluginsEnabled.set_cols_width([55])
        
        rows = [ ["[*] Type %s" %(pluginType)],
                 [self.w3afCorePlugin.plugins.get_plugin_type_desc(pluginType)] ]
        
        tablePluginsEnabled.add_rows(rows)
        print tablePluginsEnabled.draw() + "\n"

    def getAllEnabledPlugins(self):
        enabledPlugins = self.w3afCorePlugin.plugins.get_all_enabled_plugins()
        tableTypes = Texttable()
        tableTypes.set_cols_align(["l", "l"])
        tableTypes.set_cols_valign(["m", "m"])
        tableTypes.set_cols_width([40, 55])
        rows = [ ["Type", "Plugins" ] ]
        
        for type in enabledPlugins.keys():
            rows.append([type,enabledPlugins[type]])

        tableTypes.add_rows(rows)
        print tableTypes.draw() + "\n"


    def enablePlugin(self, pluginName, pluginType):
        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="enablePlugin with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="enablePlugin")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException

        if pluginName == '' or pluginName is None:
            pluginException = PluginException(message='The plugin name specified is invalid.',
                                  trace="enablePlugin with args pluginName=%s " %(str(pluginName)),
                                  plugin="w3af", method="enablePlugin")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin name specified is invalid. "
                raise pluginException

            
        enabled = [pluginName, ]
        enabledPlugins = self.w3afCorePlugin.plugins.get_all_enabled_plugins()
        for plugin in enabledPlugins[pluginType]:
            enabled.append(plugin)
        self.w3afCorePlugin.plugins.set_plugins(enabled, pluginType)
        self.getEnabledPluginsByType(pluginType)

    def disablePlugin(self,pluginName,pluginType):
        if pluginName == '' or pluginName is None:
            pluginException = PluginException(message='The plugin name specified is invalid.',
                                  trace="disablePlugin with args pluginName=%s " %(str(pluginName)),
                                  plugin="w3af", method="disablePlugin")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin name specified is invalid. "
                raise pluginException

        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="disablePlugin with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="disablePlugin")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException       

        
            
        enabled = self.w3afCorePlugin.plugins.get_enabled_plugins(pluginType)
        if pluginName in enabled:
            enabled.remove(pluginName)
        print "[*] Plugin Disabled"
        self.w3afCorePlugin.plugins.set_plugins(enabled, pluginType)
        self.getEnabledPluginsByType(pluginType)


    def enableAllPlugins(self, pluginType):
        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="enableAllPlugins with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="enableAllPlugins")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException
            
        plugins = self.w3afCorePlugin.plugins.get_plugin_list(pluginType)
        self.w3afCorePlugin.plugins.set_plugins(plugins, pluginType)
        print "[*] All plugins of type %s has been enabled..." %(pluginType)
        self.getAllEnabledPlugins()


    def disableAllPlugins(self, pluginType):
        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="disableAllPlugins with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="disableAllPlugins")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException
            
        self.w3afCorePlugin.plugins.set_plugins([], pluginType)
        print "[*] All plugins of type %s has been disabled..." %(pluginType)
        self.getAllEnabledPlugins()

    def getPluginOptions(self, pluginType, pluginName):
        if pluginName == '' or pluginName is None:
            pluginException = PluginException(message='The plugin name specified is invalid.',
                                  trace="getPluginOptions with args pluginName=%s " %(str(pluginName)),
                                  plugin="w3af", method="getPluginOptions")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin name specified is invalid. "
                raise pluginException

        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="getPluginOptions with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="getPluginOptions")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException
            
        optList = self.w3afCorePlugin.plugins.get_plugin_options(pluginType,pluginName)
        print "[*] Plugin Options for %s " %(pluginName)

        tablePluginOptions = Texttable()
        tablePluginOptions.set_cols_align(["l", "l", "l"])
        tablePluginOptions.set_cols_valign(["m", "m", "m"])
        tablePluginOptions.set_cols_width([40, 55, 55])
        rows = [ ["Name","Value", "Type"] ]
        
        for item in optList._internal_opt_list:
            rows.append([item.get_name(),item.get_value(),item.get_type()])        

        tablePluginOptions.add_rows(rows)
        print tablePluginOptions.draw() + "\n"


    def setPluginOptions(self, pluginType, pluginName, pluginSettingType, pluginSetting, pluginSettingValue):
        if pluginName == '' or pluginName is None:
            pluginException = PluginException(message='The plugin name specified is invalid.',
                                  trace="getPluginStatus with args pluginName=%s " %(str(pluginName)),
                                  plugin="w3af", method="getPluginStatus")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin name specified is invalid. "
                raise pluginException

        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="setPluginOptions with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="setPluginOptions")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException

        if pluginSettingType == '' or pluginSettingType is None:
            pluginException = PluginException(message='The plugin setting type specified is invalid.',
                                  trace="setPluginOptions with args pluginSettingType=%s " %(str(pluginSettingType)),
                                  plugin="w3af", method="setPluginOptions")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin setting type specified is invalid. "
                raise pluginException

        if pluginSetting == '' or pluginSetting is None:
            pluginException = PluginException(message='The plugin setting specified is invalid.',
                                  trace="setPluginOptions with args pluginSetting=%s " %(str(pluginSetting)),
                                  plugin="w3af", method="setPluginOptions")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin setting specified is invalid. "
                raise pluginException

        if pluginSettingValue == '' or pluginSettingValue is None:
            pluginException = PluginException(message='The plugin setting value specified is invalid.',
                                  trace="setPluginOptions with args pluginSettingValue=%s " %(str(pluginSettingValue)),
                                  plugin="w3af", method="setPluginOptions")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin setting value specified is invalid. "
                raise pluginException
        
        opt_list = OptionList()
        opt_list.add( opt_factory(pluginSetting, pluginSettingValue, "Plugin Setting", pluginSettingType) )
        print "[*] Setting %s with value %s on Plugin %s ..." %(pluginSetting,pluginSettingValue,pluginName)
        self.w3afCorePlugin.plugins._plugins_options[pluginType][pluginName] = opt_list
        print "[*] Done!"


    def getPluginStatus(self, pluginType, pluginName):
        if pluginName == '' or pluginName is None:
            pluginException = PluginException(message='The plugin name specified is invalid.',
                                  trace="getPluginStatus with args pluginName=%s " %(str(pluginName)),
                                  plugin="w3af", method="getPluginStatus")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin name specified is invalid. "
                raise pluginException

        if pluginType == '' or pluginType is None:
            pluginException = PluginException(message='The plugin type specified is invalid.',
                                  trace="getPluginStatus with args pluginType=%s " %(str(pluginType)),
                                  plugin="w3af", method="getPluginStatus")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The plugin type specified is invalid. "
                raise pluginException
            
        enabledPlugins = self.w3afCorePlugin.plugins.get_all_enabled_plugins()
        enabled = False
        for type in enabledPlugins.keys():
            if type in pluginType and pluginName in enabledPlugins[type]:
                enabled = True
        if enabled:
            print "[*] The plugin %s status is: ENABLED" %(pluginName)
        else:
            print "[*] The plugin %s status is: DISABLED" %(pluginName)

    '''
    ATTACK MANAGEMENT FUNCTIONS.
    '''
    def setTarget(self, url):
        if is_valid_url(url) == False:
            pluginException = PluginException(message='The URL specified is invalid.',
                                  trace="setTarget with args url=%s " %(str(url)),
                                  plugin="w3af", method="setTarget")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The URL specified is invalid. "
                raise pluginException
            
            
        if self.w3afCorePlugin.target._verify_url(URL_KLASS(url)):
            options = self.w3afCorePlugin.target.get_options()
            options['target'].set_value(url)
            self.w3afCorePlugin.target.set_options(options)
            print "[*] Target %s configured." %(url)


    def setTargetDeepWeb(self, url):
        if is_valid_onion_address(url) == False:
            pluginException = PluginException(message='The Onion address specified is invalid.',
                                  trace="setTargetDeepWeb with args url=%s " %(str(url)),
                                  plugin="w3af", method="setTargetDeepWeb")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The Onion address specified is invalid. "
                raise pluginException
            
        self.serviceConnector.setSocksProxy()
        #if self.w3afCorePlugin.target._verify_url(URL_KLASS(url)):
        options = self.w3afCorePlugin.target.get_options()
        options['target'].set_value(url)
        self.w3afCorePlugin.target.set_options(options)
        print "[*] Target %s configured." %(url)

    def startAttack(self):
        print "[*] W3AF Attack Starting..."
        #print '[*] Starting Attack against: '+str(cf.cf['targets'])
        self.w3afCorePlugin.plugins.init_plugins()
        self.w3afCorePlugin.verify_environment()
        self.w3afCorePlugin.start()
        #self.w3afCorePlugin.plugins.create_instances()
        #self.w3afCorePlugin.start()
        print "[*] W3AF Attack Finished! Check the results using the right functions in this plugin."

    '''
    MISC CONFIGURATION FUNCTIONS
    '''
    def listMiscConfigs(self):
        optList = self.miscSettings.get_options()
        print "[*] MiscSettings List"

        tableMiscOptions = Texttable()
        tableMiscOptions.set_cols_align(["l", "l", "l"])
        tableMiscOptions.set_cols_valign(["m", "m", "m"])
        tableMiscOptions.set_cols_width([40, 55, 55])
        rows = [ ["Name","Value", "Type"] ]
        
        for item in optList._internal_opt_list:
            rows.append([item.get_name(),item.get_value(),item.get_type()])
        tableMiscOptions.add_rows(rows)
        print tableMiscOptions.draw() + "\n"

    def setMiscConfig(self,setting,value):
        if setting == '' or setting is None:
            pluginException = PluginException(message='The setting specified is invalid.',
                                  trace="setMiscConfig with args setting=%s " %(str(setting)),
                                  plugin="w3af", method="setMiscConfig")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The setting specified is invalid. "
                raise pluginException

        if value == '' or value is None:
            pluginException = PluginException(message='The value specified is invalid.',
                                  trace="setMiscConfig with args value=%s " %(str(value)),
                                  plugin="w3af", method="setMiscConfig")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The value specified is invalid. "
                raise pluginException
            
        opt_list = OptionList()
        opt_list.add( opt_factory(setting, value, "Misc Setting", "string") )
        print "[*] Setting %s with value %s on MiscsSettings ..." %(setting,value)
        if cf.cf.has_key(setting):
            cf.cf.save(setting, value)
            print "[*] Done!"
            self.listMiscConfigs()
        else:
            print "[-] Invalid setting. Check the available settings with the function self.listMiscConfigs()"

    '''
    PROFILE MANAGEMENT FUNCTIONS
    '''
    def listProfiles(self):
        valid_profiles, invalid_profiles = self.w3afCorePlugin.profiles.get_profile_list()
        print "[*] List of profiles."
        print "\n"

        tableProfiles = Texttable()
        tableProfiles.set_cols_align(["l", "l", "l"])
        tableProfiles.set_cols_valign(["m", "m", "m"])
        tableProfiles.set_cols_width([40, 55, 55])
        rows = [ ["Description", "Profile File", "Name"] ]

        for profile in valid_profiles:
            rows.append([profile.get_desc(),
                         profile.get_profile_file(),
                         profile.get_name()])
        tableProfiles.add_rows(rows)
        print tableProfiles.draw() +"\n"



    def useProfile(self,profileName):
        if profileName == '' or profileName is None:
            pluginException = PluginException(message='The profile name specified is invalid.',
                                  trace="useProfile with args profileName=%s " %(str(profileName)),
                                  plugin="w3af", method="useProfile")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The profile name specified is invalid. "
                raise pluginException        
        print "[*] Loading profile %s " %(profileName)
        self.w3afCorePlugin.profiles.use_profile(profileName)
        print "[*] Done!"

    def createProfileWithCurrentConfig(self, profileName, profileDescription):
        if profileName == '' or profileName is None:
            pluginException = PluginException(message='The profile name specified is invalid.',
                                  trace="createProfileWithCurrentConfig with args profileName=%s " %(str(profileName)),
                                  plugin="w3af", method="createProfileWithCurrentConfig")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The profile name specified is invalid. "
                raise pluginException
            
        print "[*] Creating profile %s " %(profileName)
        profile = self.w3afCorePlugin.profiles.save_current_to_new_profile(profileName, profileDescription)

        tableProfiles = Texttable()
        tableProfiles.set_cols_align(["l", "l", "l"])
        tableProfiles.set_cols_valign(["m", "m", "m"])
        tableProfiles.set_cols_width([40, 55, 55])
        rows = [ ["Description", "Profile File", "Name"],
                 [profile.get_desc(),profile.get_profile_file(),profile.get_name()] ]
        
        tableProfiles.add_rows(rows)
        print tableProfiles.draw()+"\n"


    def modifyProfileWithCurrentConfig(self, profileName, profileDescription):
        if profileName == '' or profileName is None:
            pluginException = PluginException(message='The profile name specified is invalid.',
                                  trace="modifyProfileWithCurrentConfig with args profileName=%s " %(str(profileName)),
                                  plugin="w3af", method="modifyProfileWithCurrentConfig")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The profile name specified is invalid. "
                raise pluginException
            
        print "[*] Updating profile %s with the current configuration" %(profileName)
        profile = self.w3afCorePlugin.profiles.save_current_to_profile(profileName,profileDescription)

        tableProfiles = Texttable()
        tableProfiles.set_cols_align(["l", "l", "l", "l"])
        tableProfiles.set_cols_valign(["m", "m", "m", "m"])
        tableProfiles.set_cols_width([40, 55, 55, 55])
        rows = [["Profile File", "Name", "Target", "Description"]]
        
        rows.append([profile.get_profile_file(),
                     profile.get_name(),
                     profile.get_target(),
                     profile.get_desc()])
        tableProfiles.add_rows(rows)
        print tableProfiles.draw()+"\n"

    def removeProfile(self,profileName):
        if profileName == '' or profileName is None:
            pluginException = PluginException(message='The profile name specified is invalid.',
                                  trace="removeProfile with args profileName=%s " %(str(profileName)),
                                  plugin="w3af", method="removeProfile")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The profile name specified is invalid. "
                raise pluginException
        removed = self.w3afCorePlugin.profiles.remove_profile(profileName)
        if removed:
            print "[*] Profile %s removed successfully." %(profileName)
        else:
            print "[-] Error removing the profile %s. The profile, already Exists?" %(profileName)

    '''
    SHELLS MANAGEMENT FUNCTIONS
    '''

    def listShells(self):
        shells = kb.get_all_shells()
        print "[*] List of shells."

        tableShells = Texttable()
        tableShells.set_cols_align(["l", "l", "l", "l", "l"])
        tableShells.set_cols_valign(["m", "m", "m", "m", "m"])
        tableShells.set_cols_width([40, 55, 55, 55, 55])
        
        rows = [ ["Id","OS","System","User","System Name"] ]
        for shell in shells:
            rows.append([shell.id,
                         shell.get_remote_os(),
                         shell.get_remote_system(),
                         shell.get_remote_user(),
                         shell.get_remote_system_name()])
        tableShells.add_rows(rows)
        print tableShells.draw()+"\n"


    def executeCommand(self,shellId, command,params):
        #TODO: There's any way to get the list of current supported commands? Check the code of W3AF.
        if command == '' or command is None:
            pluginException = PluginException(message='The command specified is invalid.',
                                  trace="executeCommand with args command=%s " %(str(command)),
                                  plugin="w3af", method="executeCommand")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The command specified is invalid. "
                raise pluginException
            
        if str(shellId).isdigit() == False or shellId < 0:
            pluginException = PluginException(message='The shell identifier specified is invalid.',
                                  trace="executeCommand with args shellId=%s " %(str(shellId)),
                                  plugin="w3af", method="executeCommand")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The shell identifier specified is invalid. "
                raise pluginException
            
        shells = kb.get_all_shells()
        response = None
        for shell in shells:
            if shell.id == shellId and command is not None:
                response = shell.generic_user_input(command,params)
        if response is not None:
            print "[*] Response: %s" %(response)
        else:
            print "[-] No response received. Check the shell that you've entered. Exists?"


    '''
    VULNS AND INFO MANAGEMENT FUNCTIONS
    '''
    def listAttackPlugins(self):
        self.showPluginsByType('attack')

    def listInfos(self):
        infos = kb.get_all_infos()
        print "[*] List of Infos."

        tableInfos = Texttable()
        tableInfos.set_cols_align(["l", "l", "l", "l", "l"])
        tableInfos.set_cols_valign(["m", "m", "m", "m", "m"])
        tableInfos.set_cols_width([40, 55, 55, 55, 55])
        rows = [["Id","Name","Method","Description","Plugin Name"]]
        for info in infos:
            rows.append([info.get_id(),
                         info.get_name(),
                         info.get_method(),
                         info.get_desc(),
                         info.get_plugin_name()])
        tableInfos.add_rows(rows)
        print tableInfos.draw()+"\n"

    def listVulnerabilities(self):
        vulns = kb.get_all_vulns()
        print "[*] List of Vulns."
        tableVulns = Texttable()
        tableVulns.set_cols_align(["l", "l"])
        tableVulns.set_cols_valign(["m", "m"])
        tableVulns.set_cols_width([40, 55])
        
        rows = [["Severity","Description"]]
        for vuln in vulns:
            rows.append([vuln.get_severity(),vuln.get_desc()])
        tableVulns.add_rows(rows)
        print tableVulns.draw()+"\n"

    def exploitAllVulns(self,pluginExploit):
        if pluginExploit == '' or pluginExploit is None:
            pluginException = PluginException(message='The attack plugin  specified is invalid.',
                                  trace="exploitAllVulns with args pluginExploit=%s " %(str(pluginExploit)),
                                  plugin="w3af", method="exploitAllVulns")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The attack plugin  specified is invalid. "
                raise pluginException
            
        print "[*] Checking the vulnerability and plugin to exploit..."
        pluginAttack = self.w3afCorePlugin.plugins.get_plugin_inst('attack',pluginExploit)
        for vuln in kb.get_all_vulns():
            if vuln.get_id() is not None:
                shells = pluginAttack.exploit(vuln.get_id())
                for shell in shells:
                    print "Shell Generated %s " %(shell.id)

        print "[*] Exploit vulnerability finished."

    def exploitVuln(self,pluginExploit,vulnId):
        if pluginExploit == '' or pluginExploit is None:
            pluginException = PluginException(message='The attack plugin  specified is invalid.',
                                  trace="exploitVuln with args pluginExploit=%s " %(str(pluginExploit)),
                                  plugin="w3af", method="exploitVuln")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The attack plugin  specified is invalid. "
                raise pluginException

        if str(vulnId).isdigit() == False or vulnId < 0:
            pluginException = PluginException(message='The vuln identifier specified is invalid.',
                                  trace="exploitVuln with args vulnId=%s " %(str(vulnId)),
                                  plugin="w3af", method="exploitVuln")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The shell identifier specified is invalid. "
                raise pluginException
            
            
        print "[*] Checking the vulnerability and plugin to exploit..."
        pluginAttack = self.w3afCorePlugin.plugins.get_plugin_inst('attack',pluginExploit)
        for vuln in kb.get_all_vulns():
            if vuln.get_id() is not None:
                if int(vulnId) in vuln.get_id():
                    shells = pluginAttack.exploit(vuln.get_id())
                    for shell in shells:
                        print "Shell Generated %s " %(shell.id)
        print "[*] Exploit vulnerability finished."

    def help(self):
        print "[*] Functions availaible in the Plugin...\n"
        print "[*] Plugin Management Functions"
        tablePlugins = Texttable()
        tablePlugins.set_cols_align(["l", "l", "c"])
        tablePlugins.set_cols_valign(["m", "m", "m"])
        tablePlugins.set_cols_width([40,55,55])
        tablePlugins.add_rows([ ["Function", "Description", "Example"],
                                ['help', 'Help Banner', 'self.help()'],
                                ['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'],
                                ['showPluginsByType', 'List of available plugins filtered by type.', 'self.showPluginsByType("audit")'],
                                ['showPluginTypes', 'List of available plugin types.', 'self.showPluginTypes()'],
                                ['getEnabledPluginsByType', 'Enabled plugins by types.', 'self.getEnabledPluginsByType("audit")'],
                                ['getPluginTypeDescription', 'Description for the plugin type specified.', 'self.getPluginTypeDescription("audit")'],
                                ['getAllEnabledPlugins', 'List of enabled plugins.', 'self.getAllEnabledPlugins()'],
                                ['enablePlugin', 'Enable a plugin.', 'self.enablePlugin("blind_sqli","audit")'],
                                ['disablePlugin', 'Disable a plugin.', 'self.disablePlugin("blind_sqli","audit")'],
                                ['enableAllPlugins', 'Enable all plugins.', 'self.enableAllPlugins("audit")'],
                                ['disableAllPlugins', 'Disable all plugins.', 'self.disableAllPlugins("audit")'],
                                ['getPluginOptions', 'Get Options for the plugin specified.', 'self.getPluginOptions("audit","blind_sqli")'],
                                ['setPluginOptions', 'Set Options for the plugin specified.', 'self.setPluginOptions("audit","eval","boolean","use_time_delay","False")'],
                                ['getPluginStatus', 'Check if the specified plugin is enabled.', 'self.getPluginStatus("audit","eval")']                                
                              ])
        
        print tablePlugins.draw() + "\n"

        print "[*] Attack Functions..."
        tableAttack = Texttable()
        tableAttack.set_cols_align(["l", "l", "c"])
        tableAttack.set_cols_valign(["m", "m", "m"])
        tableAttack.set_cols_width([40,55,55])
        tableAttack.add_rows([ ["Function", "Description", "Example"],
                               ['setTarget', 'Sets the target for the attack (clear web)', 'self.setTarget("http://www.target.com")'],
                               ['setTargetDeepWeb', 'Sets the target in the DeepWeb of TOR.', 'self.setTarget("http://torlongonionpath.onion")'],
                               ['startAttack', 'Starts the attack.', 'self.startAttack()']
                              ])
        
        print tableAttack.draw() + "\n"

        print "[*] Misc Settings Functions..."
        tableMisc = Texttable()
        tableMisc.set_cols_align(["l", "l", "c"])
        tableMisc.set_cols_valign(["m", "m", "m"])
        tableMisc.set_cols_width([40,55,55])
        tableMisc.add_rows([ ["Function", "Description", "Example"],
                               ['listMiscConfigs', 'List of Misc Settings', 'self.listMiscConfigs()'],
                               ['setMiscConfig', 'Sets a Misc Settings', 'self.setMiscConfig("msf_location","/opt/msf")']                             
                              ])
        
        print tableMisc.draw() + "\n"

        print "[*] Profile Management Functions"
        tableProfile = Texttable()
        tableProfile.set_cols_align(["l", "l", "c"])
        tableProfile.set_cols_valign(["m", "m", "m"])
        tableProfile.set_cols_width([40,55,55])
        tableProfile.add_rows([["Function", "Description", "Example"],
                               ['listProfiles', 'List of Profiles', 'self.listProfiles()'],
                               ['useProfile', 'Use a Profile', 'self.useProfile("profileName")'],
                               ['createProfileWithCurrentConfig', 'Creates a new Profile with the current settings', 'self.createProfileWithCurrentConfig("profileName", "Profile Description")'],
                               ['modifyProfileWithCurrentConfig', 'Modifies an existing profile with the current settings', 'self.modifyProfileWithCurrentConfig("profileName", "Profile Description")'],
                               ['removeProfile', 'Removes an existing profile', 'self.removeProfile("profileName")']
                              ])
        
        print tableProfile.draw() + "\n"

        print "[*] Shell Management Functions"
        tableShell = Texttable()
        tableShell.set_cols_align(["l", "l", "c"])
        tableShell.set_cols_valign(["m", "m", "m"])
        tableShell.set_cols_width([40,55,55])
        tableShell.add_rows([   ["Function", "Description", "Example"],
                                ['listShells', 'List of Shells', 'self.listShells()'],
                                ['executeCommand', 'Executes a command in the specified shell', 'self.executeCommand(1,"lsp")']                                
                              ])
        print tableShell.draw() + "\n"

        print "[*] Vulns and Info Management Functions"
        tableVulns = Texttable()
        tableVulns.set_cols_align(["l", "l", "c"])
        tableVulns.set_cols_valign(["m", "m", "m"])
        tableVulns.set_cols_width([40,55,55])
        tableVulns.add_rows([   ["Function", "Description", "Example"],
                                ['listAttackPlugins', 'List of attack plugins.', 'self.listAttackPlugins()'],
                                ['executeCommand', 'Executes a command in the specified shell', 'self.executeCommand(1,"lsp")'],
                                ['listInfos', 'List of Infos in the Knowledge Base of W3AF', 'self.listInfos()'],
                                ['listVulnerabilities', 'List of Vulns in the Knowledge Base of W3AF', 'self.listVulnerabilities()'],
                                ['exploitAllVulns', 'Exploits all vulns in the Knowledge Base of W3AF', 'self.exploitVulns("sqli")'],
                                ['exploitVuln', 'Exploits the specified Vuln in the Knowledge Base of W3AF', 'self.exploitVulns("sqli",18)']
                              ])
        print tableVulns.draw() + "\n"    
