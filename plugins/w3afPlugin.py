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
from prettytable import PrettyTable
from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from w3af.core.controllers.w3afCore import w3afCore
from w3af.core.data.options.option_list import OptionList
from w3af.core.data.options.opt_factory import opt_factory
from w3af.core.data.kb.knowledge_base import kb
from w3af.core.controllers.misc_settings import MiscSettings
import w3af.core.data.kb.config as cf

class w3afPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes):
        BasePlugin.__init__(self, torNodes, 'w3afPlugin')
        self.info("[*] w3afPlugin Initialized!")
        self.w3afCorePlugin = w3afCore()
        self.w3afCorePlugin.plugins.init_plugins()
        self.w3afCorePlugin.plugins.zero_enabled_plugins()
        self.miscSettings = MiscSettings()

    def __del__(self):
        self.info("[*] w3afPlugin Destroyed!")


    '''
    PLUGIN MANAGEMENT FUNCTIONS.
    '''
    def showPluginsByType(self, type):
        pluginByType = self.w3afCorePlugin.plugins.get_plugin_list(type)
        tablePlugins = PrettyTable(["[*] Plugins for %s "%(type)])
        for plugin in pluginByType:
            tablePlugins.add_row([plugin])
        print tablePlugins

    def showPluginTypes(self):
        types = self.w3afCorePlugin.plugins.get_plugin_types()
        tableTypes = PrettyTable(["[*] Plugin Types"])
        for plugin in types:
            tableTypes.add_row([plugin])
        print tableTypes

    def getEnabledPluginsByType(self, type):
        enabled = self.w3afCorePlugin.plugins.get_enabled_plugins(type)
        tableTypes = PrettyTable(["[*] Enabled plugins by type %s" %(type)])
        for plugin in enabled:
            tableTypes.add_row([plugin])
        print tableTypes

    def getPluginTypeDescription(self, type):
        tableTypes = PrettyTable(["[*] Type %s" %(type)])
        tableTypes.add_row([self.w3afCorePlugin.plugins.get_plugin_type_desc(type)])
        print tableTypes

    def getAllEnabledPlugins(self):
        enabledPlugins = self.w3afCorePlugin.plugins.get_all_enabled_plugins()
        tableTypes = PrettyTable(["Type", "Plugins" ])
        for type in enabledPlugins.keys():
            tableTypes.add_row([type,enabledPlugins[type]])
        print tableTypes


    def enablePlugin(self, pluginName, type):
        enabled = [pluginName, ]
        self.w3afCorePlugin.plugins.set_plugins(enabled, type)
        self.getEnabledPluginsByType(type)

    def disablePlugin(self,pluginName,type):
        enabled = self.w3afCorePlugin.plugins.get_enabled_plugins(type)
        if pluginName in enabled:
            enabled.remove(pluginName)
        print "[*] Plugin Disabled"
        self.w3afCorePlugin.plugins.set_plugins(enabled, type)
        self.getEnabledPluginsByType(type)


    def enableAllPlugins(self, pluginType):
        plugins = self.w3afCorePlugin.plugins.get_plugin_list(pluginType)
        self.w3afCorePlugin.plugins.set_plugins(plugins, pluginType)
        print "[*] All plugins of type %s has been enabled..." %(pluginType)
        self.getAllEnabledPlugins()


    def disableAllPlugins(self, pluginType):
        self.w3afCorePlugin.plugins.set_plugins([], pluginType)
        print "[*] All plugins of type %s has been disabled..." %(pluginType)
        self.getAllEnabledPlugins()

    def getPluginOptions(self, pluginType, pluginName):
        optList = self.w3afCorePlugin.plugins.get_plugin_options(pluginType,pluginName)
        print "[*] Plugin Options for %s " %(pluginName)
        tablePluginOptions = PrettyTable(["Name","Value", "Type"])
        for item in optList._internal_opt_list:
            tablePluginOptions.add_row([item.get_name(),item.get_value(),item.get_type()])
        print tablePluginOptions


    def setPluginOptions(self, pluginType, pluginName, pluginSettingType, pluginSetting, pluginSettingValue):
        opt_list = OptionList()
        opt_list.add( opt_factory(pluginSetting, pluginSettingValue, "Plugin Setting", pluginSettingType) )
        print "[*] Setting %s with value %s on Plugin %s ..." %(pluginSetting,pluginSettingValue,pluginName)
        self.w3afCorePlugin.plugins._plugins_options[pluginType][pluginName] = opt_list
        print "[*] Done!"


    def getPluginStatus(self, pluginType, pluginName):
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
        if self.w3afCorePlugin.target._verify_url(URL_KLASS(url)):
            options = self.w3afCorePlugin.target.get_options()
            options['target'].set_value(url)
            self.w3afCorePlugin.target.set_options(options)
            print "[*] Target %s configured." %(url)


    def setTargetDeepWeb(self, url):
        self.setSocksProxy()
        #if self.w3afCorePlugin.target._verify_url(URL_KLASS(url)):
        options = self.w3afCorePlugin.target.get_options()
        options['target'].set_value(url)
        self.w3afCorePlugin.target.set_options(options)
        print "[*] Target %s configured." %(url)

    def startAttack(self):
        print "[*] W3AF Attack Starting..."
        print '[*] Starting Attack against: '+str(cf.cf['targets'])
        self.w3afCorePlugin.plugins.create_instances()
        self.w3afCorePlugin.start()
        print "[*] W3AF Attack Finished! Check the results using the right functions in this plugin."

    '''
    MISC CONFIGURATION FUNCTIONS
    '''
    def listMiscConfigs(self):
        optList = self.miscSettings.get_options()
        print "[*] MiscSettings List"
        tableMiscOptions = PrettyTable(["Name","Value", "Type"])
        for item in optList._internal_opt_list:
            tableMiscOptions.add_row([item.get_name(),item.get_value(),item.get_type()])
        print tableMiscOptions

    def setMiscConfig(self,setting,value):
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
        tableProfiles = PrettyTable(["Description","Profile File", "Name", "Target"])
        for profile in valid_profiles:
            tableProfiles.add_row([profile.get_desc(),
                                   profile.get_profile_file(),
                                   profile.get_name(),
                                   profile.get_target().get("target")])
        tableProfiles["Description"].align="l"
        tableProfiles["Profile File"].align="l"
        tableProfiles["Name"].align="l"
        tableProfiles["Target"].align="l"
        print tableProfiles



    def useProfile(self,profileName):
        print "[*] Loading profile %s " %(profileName)
        self.w3afCorePlugin.profiles.use_profile(profileName)
        print "[*] Done!"

    def createProfileWithCurrentConfig(self, profileName, profileDescription):
        print "[*] Creating profile %s " %(profileName)
        profile = self.w3afCorePlugin.profiles.save_current_to_new_profile(profileName, profileDescription)
        tableProfiles = PrettyTable(["Description","Profile File", "Name", "Target"])
        tableProfiles.add_row([profile.get_desc(),profile.get_profile_file(),profile.get_name(),profile.get_target().get("target")])
        tableProfiles["Description"].align="l"
        tableProfiles["Profile File"].align="l"
        tableProfiles["Name"].align="l"
        tableProfiles["Target"].align="l"
        print tableProfiles


    def modifyProfileWithCurrentConfig(self, profileName, profileDescription):
        print "[*] Updating profile %s with the current configuration" %(profileName)
        profile = self.w3afCorePlugin.profiles.save_current_to_profile(profileName,profileDescription)
        tableProfile = PrettyTable(["Profile File", "Name", "Target", "Description"])
        tableProfile.add_row([profile.get_profile_file(),
                               profile.get_name(),
                               profile.get_target(),
                               profile.get_desc()])
        print tableProfile

    def removeProfile(self,profileName):
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
        tableShells = PrettyTable(["Id","OS","System","User","System Name"])
        for shell in shells:
            tableShells.add_row([shell.id,
                                 shell.get_remote_os(),
                                 shell.get_remote_system(),
                                 shell.get_remote_user(),
                                 shell.get_remote_system_name()])
        print tableShells

    def executeCommand(self,shellId, command,params):
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
        tableInfos = PrettyTable(["Id","Name","Method","Description","Plugin Name"])
        for info in infos:
            tableInfos.add_row([info.get_id(),
                                 info.get_name(),
                                 info.get_method(),
                                 info.get_desc(),
                                 info.get_plugin_name()])
        print tableInfos

    def listVulnerabilities(self):
        vulns = kb.get_all_vulns()
        print "[*] List of Vulns."
        tableVulns = PrettyTable(["Severity","Description"])
        for vuln in vulns:
            tableVulns.add_row([vuln.get_severity(),vuln.get_desc()])
        print tableVulns

    def exploitVulns(self,pluginExploit,vulnId):
        print "[*] Checking the vulnerabily and plugin to exploit..."
        pluginAttack = self.w3afCorePlugin.plugins.get_plugin_inst('attack',pluginExploit)
        for vuln in kb.get_all_vulns():
            if vuln.get_id() is not None:
                if int(vulnId) in vuln.get_id():
                    print pluginAttack.exploit(vuln.get_id())
        print "[*] Exploit vulnerability finished."
        self.listShells()


    def help(self):
        print "[*] Functions availaible in the Plugin..."
        print "[*] Plugin Management Functions"
        tableHelpPlugins = PrettyTable(["Function", "Description", "Example"])
        tableHelpPlugins.padding_width = 1
        tableHelpPlugins.add_row(['help', 'Help Banner', 'self.help()'])
        tableHelpPlugins.add_row(['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'])
        tableHelpPlugins.add_row(['showPluginsByType', 'List of available plugins filtered by type.', 'self.showPluginsByType("audit")'])
        tableHelpPlugins.add_row(['showPluginTypes', 'List of available plugin types.', 'self.showPluginTypes()'])
        tableHelpPlugins.add_row(['getEnabledPluginsByType', 'Enabled plugins by types.', 'self.getEnabledPluginsByType("audit")'])
        tableHelpPlugins.add_row(['getPluginTypeDescription', 'Description for the plugin type specified.', 'self.getPluginTypeDescription("audit")'])
        tableHelpPlugins.add_row(['getAllEnabledPlugins', 'List of enabled plugins.', 'self.getAllEnabledPlugins()'])
        tableHelpPlugins.add_row(['enablePlugin', 'Enable a plugin.', 'self.enablePlugin("blind_sqli","audit")'])
        tableHelpPlugins.add_row(['disablePlugin', 'Disable a plugin.', 'self.disablePlugin("blind_sqli","audit")'])
        tableHelpPlugins.add_row(['enableAllPlugins', 'Enable all plugins.', 'self.enableAllPlugins("audit")'])
        tableHelpPlugins.add_row(['disableAllPlugins', 'Disable all plugins.', 'self.disableAllPlugins("audit")'])
        tableHelpPlugins.add_row(['getPluginOptions', 'Get Options for the plugin specified.', 'self.getPluginOptions("audit","blind_sqli")'])
        tableHelpPlugins.add_row(['setPluginOptions', 'Set Options for the plugin specified.', 'self.setPluginOptions("audit","eval","boolean","use_time_delay","False")'])
        tableHelpPlugins.add_row(['getPluginStatus', 'Check if the specified plugin is enabled.', 'self.getPluginStatus("audit","eval")'])
        print tableHelpPlugins

        print "\n"
        print "[*] Attack Functions"
        tableHelpAttack = PrettyTable(["Function", "Description", "Example"])
        tableHelpAttack.add_row(['setTarget', 'Sets the target for the attack (clear web)', 'self.setTarget("http://www.target.com")'])
        tableHelpAttack.add_row(['setTargetDeepWeb', 'Sets the target in the DeepWeb of TOR.', 'self.setTarget("http://torlongonionpath.onion")'])
        tableHelpAttack.add_row(['startAttack', 'Starts the attack.', 'self.startAttack()'])
        print tableHelpAttack

        print "\n"
        print "[*] Misc Settings Functions"
        tableHelpMiscSettings = PrettyTable(["Function", "Description", "Example"])
        tableHelpMiscSettings.add_row(['listMiscConfigs', 'List of Misc Settings', 'self.listMiscConfigs()'])
        tableHelpMiscSettings.add_row(['setMiscConfig', 'Sets a Misc Settings', 'self.setMiscConfig("msf_location","/opt/msf")'])
        print tableHelpMiscSettings

        print "\n"
        print "[*] Profile Management Functions"
        tableHelpMiscSettings = PrettyTable(["Function", "Description", "Example"])
        tableHelpMiscSettings.add_row(['listProfiles', 'List of Profiles', 'self.listProfiles()'])
        tableHelpMiscSettings.add_row(['useProfile', 'Use a Profile', 'self.useProfile("profileName")'])
        tableHelpMiscSettings.add_row(['createProfileWithCurrentConfig', 'Creates a new Profile with the current settings', 'self.createProfileWithCurrentConfig("profileName", "Profile Description")'])
        tableHelpMiscSettings.add_row(['modifyProfileWithCurrentConfig', 'Modifies an existing profile with the current settings', 'self.modifyProfileWithCurrentConfig("profileName", "Profile Description")'])
        tableHelpMiscSettings.add_row(['removeProfile', 'Removes an existing profile', 'self.removeProfile("profileName")'])
        print tableHelpMiscSettings

        print "\n"
        print "[*] Shell Management Functions"
        tableHelpShells = PrettyTable(["Function", "Description", "Example"])
        tableHelpShells.add_row(['listShells', 'List of Shells', 'self.listShells()'])
        tableHelpShells.add_row(['executeCommand', 'Executes a command in the specified shell', 'self.executeCommand(1,"lsp")'])
        print tableHelpShells

        print "\n"
        print "[*] Vulns and Info Management Functions"
        tableHelpShells = PrettyTable(["Function", "Description", "Example"])
        tableHelpShells.add_row(['listAttackPlugins', 'List of attack plugins.', 'self.listAttackPlugins()'])
        tableHelpShells.add_row(['listInfos', 'List of Infos in the Knowledge Base of W3AF', 'self.listInfos()'])
        tableHelpShells.add_row(['listVulnerabilities', 'List of Vulns in the Knowledge Base of W3AF', 'self.listVulnerabilities()'])
        tableHelpShells.add_row(['exploitVulns', 'Exploits the specified Vuln in the Knowledge Base of W3AF', 'self.exploitVulns("sqli",18)'])
        print tableHelpShells



'''
    def runPlugin(self):
        target = w3af_core_target()
        core = w3af.core.controllers.w3afCore.w3afCore()

        print core.target._verify_url(URL_KLASS('http://www.google.com/'))
        core.plugins.init_plugins()

        plugin_types = core.plugins.get_plugin_types()
        print plugin_types
        plugin_list = core.plugins.get_plugin_list('audit')
        print plugin_list

        plugin_inst = core.plugins.get_plugin_inst('audit', 'sqli')
        print plugin_inst

        for plugin_name in core.plugins.get_plugin_list('audit'):
            plugin_inst = core.plugins.get_plugin_inst('audit', plugin_name)
            print plugin_inst.get_name()

        enabled = ['sqli', ]
        core.plugins.set_plugins(enabled, 'audit')
        retrieved = core.plugins.get_enabled_plugins('audit')
        print retrieved
'''