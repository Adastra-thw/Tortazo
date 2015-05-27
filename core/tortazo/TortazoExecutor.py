# coding=utf-8
'''
Created on 21/12/2014

#Author: Adastra.
#twitter: @jdaanial

Tortazo.py

Tortazo is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

Tortazo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))


from core.tortazo.Discovery import Discovery
from core.tortazo.BotNet import BotNet
from core.tortazo.Reporting import Reporting
from core.tortazo.databaseManagement.TortazoServerDB import  TortazoSQLiteDB, TortazoPostgreSQL, TortazoMySQL
from core.tortazo.OnionRepository import  RepositoryGenerator
from core.tortazo.utils.ServiceConnector import ServiceConnector
from config import config as tortazoConfiguration
from stem.util import term
import stem.process
import logging as log
from plumbum import cli
from time import gmtime, strftime
from distutils.util import strtobool
import string
import random
from pyfiglet import Figlet
import time
from core.tortazo.exceptions.PluginException import PluginException

#
#  ████████╗ ██████╗ ██████╗ ████████╗ █████╗ ███████╗ ██████╗ 
#  ╚══██╔══╝██╔═══██╗██╔══██╗╚══██╔══╝██╔══██╗╚══███╔╝██╔═══██╗
#     ██║   ██║   ██║██████╔╝   ██║   ███████║  ███╔╝ ██║   ██║
#     ██║   ██║   ██║██╔══██╗   ██║   ██╔══██║ ███╔╝  ██║   ██║
#     ██║   ╚██████╔╝██║  ██║   ██║   ██║  ██║███████╗╚██████╔╝
#     ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ 
#                                                              

class TortazoSwitch:
    def __init__(self, shortSwitch, longSwitch, helpSwitch, callback=None,
                 value=None, composedValues=[], mandatory=False, 
                 requiresSwitches=[], excludesSwitches=[], typeSwitch=str, defaultValue=''):
        self.shortSwitch = shortSwitch
        self.longSwitch = longSwitch
        self.value = value
        self.composedValues=composedValues
        self.mandatory = mandatory
        self.requiresSwitches = requiresSwitches
        self.excludesSwitches = excludesSwitches
        self.helpSwitch = helpSwitch
        self.typeSwitch = typeSwitch
        self.defaultValue=defaultValue
        self.callback = callback

    def setValue(self, value):
        self.value = value



class TortazoExecutor:
    def __init__(self,logger):
        self.socksHost = None
        self.socksPort = None
        
        self.logger = logger
        self.__configureDatabaseInstance()

        self.verbose = TortazoSwitch(shortSwitch='-v', longSwitch='--verbose', callback=self.__activateVerbose, helpSwitch="Verbose Mode.")
        
        self.useMirrors = TortazoSwitch(shortSwitch='-d', longSwitch='--use-mirrors', helpSwitch="Use the mirror directories of TOR. This will help to not overwhelm the official directories") 
        self.useShodan = TortazoSwitch(shortSwitch='-s', longSwitch='--use-shodan', callback=self.__useShodan, helpSwitch="Use ShodanHQ Service. (Specify -k/--shodan-key to set up the file where's stored your shodan key.)")
        
        self.useCircuitExitNodes = TortazoSwitch(shortSwitch='-c', longSwitch='--use-circuit-nodes', callback=self.__useCircuitNodes, helpSwitch="Use the exit nodes selected for a local instance of TOR.")
        
        self.zombieMode = TortazoSwitch(shortSwitch='-z', longSwitch='--zombie-mode', callback=self.__zombieMode,  helpSwitch="This option reads the tortazo_botnet.bot file generated from previous successful attacks. With this option you can select the Nicknames that will be excluded. (Nicknames included in the tortazo_botnet.bot). For instance, '-z Nickname1,Nickname2' or '-z all' to include all nicknames.")
        
        self.mode = TortazoSwitch(shortSwitch='-m', longSwitch='--mode', callback=self.__mode, excludesSwitches=[self.zombieMode], composedValues=["windows", "linux", "darwin", "freebsd", "openbsd", "bitrig","netbsd"], helpSwitch="Filter the platform of exit-nodes to attack.")
        self.openShell = TortazoSwitch(shortSwitch='-o', longSwitch='--open-shell', excludesSwitches=[self.mode], requiresSwitches=[self.zombieMode],  helpSwitch="Open a shell on the specified host.")
        self.useDatabase = TortazoSwitch(shortSwitch='-D', longSwitch='--use-database', callback=self.__useDatabase,  helpSwitch="Tortazo will store the last results from the scanning process in a database. If you use this flag, Tortazo will omit the scan and just will try use the data stored from the last execution.")
        
        self.cleanDatabase = TortazoSwitch(shortSwitch='-C', longSwitch='--clean-database', callback=self.__cleanDatabase, helpSwitch="Tortazo will delete all records stored in database when finished executing. This option will delete every record stored, included the data from previous scans.")
        self.listPlugins = TortazoSwitch(shortSwitch='-L', longSwitch='--list-plugins', callback=self.__listPlugins, helpSwitch="List of plugins loaded.")
        
        self.useLocalTorInstance = TortazoSwitch(shortSwitch='-U', longSwitch='--use-localinstance',  helpSwitch="Use a local TOR instance started with the option -T/--tor-localinstance (Socks Proxy included) to execute requests from the plugins loaded. By default, if you don't start a TOR local instance and don't specify this option, the settings defined in 'config.py' will be used to perform requests to hidden services.")
        self.serversToAttack =  TortazoSwitch(shortSwitch='-n', longSwitch='--servers-to-attack', defaultValue=10, typeSwitch=int, helpSwitch="Number of TOR exit-nodes to attack. If this switch is used with --use-database, will recover information stored from the last 'n' scans. Default = 10")
        self.shodanKey =  TortazoSwitch(shortSwitch='-k', longSwitch='--shodan-key', helpSwitch="Development Key to use Shodan API.", requiresSwitches=[self.useShodan])
        self.listScanPorts = TortazoSwitch(shortSwitch='-l', longSwitch='--list-ports', defaultValue="21,22,23,53,69,80,88,110,139,143,161,162,389,443,445,1079,1080,1433,3306,5432,8080,9050,9051,5800", helpSwitch="Comma-separated List of ports to scan with Nmap. Don't use spaces") 
        self.excludeFingerprints = TortazoSwitch(shortSwitch='-X', longSwitch='--exclude-fingerprints', defaultValue="", helpSwitch="Comma-separated List of fingerprints to exclude from the Tortazo scan. Don't use spaces") 
        
        self.scanArguments = TortazoSwitch(shortSwitch='-a', longSwitch='--scan-arguments', helpSwitch='Arguments to Nmap. Use "" to specify the arguments. For example: "-sSV -A -Pn"') 
        self.exitNodeFingerprint = TortazoSwitch(shortSwitch='-e', longSwitch='--exit-node-fingerprint', helpSwitch="ExitNode's Fingerprint to attack.") 
        self.controllerPort = TortazoSwitch(shortSwitch='-i', longSwitch='--controller-port', defaultValue='9151', requiresSwitches=[self.useCircuitExitNodes], helpSwitch="Controller's port of the local instance of TOR. (Default=9151)") 
        self.runCommandBotnet = TortazoSwitch(shortSwitch='-r', longSwitch='--run-command', excludesSwitches=[self.mode], requiresSwitches=[self.zombieMode], helpSwitch='Execute a command across the hosts of the botnet. Requieres the -z/--zombie-mode. example: --run-command "uname -a; uptime" ') 
        self.usePlugin = TortazoSwitch(shortSwitch='-P', longSwitch='--use-plugin', callback=self.__loadAndExecute, helpSwitch='Execute a plugin. To see the available plugins, execute Tortazo with switch -L / --list-plugins') 
        self.pluginArguments = TortazoSwitch(shortSwitch='-A', longSwitch='--plugin-arguments', requiresSwitches=[self.usePlugin], helpSwitch='Args to execute the specified plugin with the switch -P / --use-plugin. List of key/value pairs separated by colon. Example= nessusHost=127.0.0.1,nessusPort=8843,nessusUser=adastra,nessusPassword=adastra') 
        
        self.torLocalInstance = TortazoSwitch(shortSwitch='-T', longSwitch="--tor-localinstance", callback=self.__torLocalInstance, helpSwitch='Start a new local TOR instance with the "torrc" file specified. DO NOT RUN TORTAZO WITH THIS OPTION AS ROOT!') 
        
        self.scanIdentifier = TortazoSwitch(shortSwitch='-S', longSwitch="--scan-identifier", typeSwitch=int, requiresSwitches=[self.useDatabase], helpSwitch="scan identifier in the Scan table. Tortazo will use the relays related with the scan identifier specified with this option.") 
        self.onionPartialAddress = TortazoSwitch(shortSwitch='-O', longSwitch="--onionpartial-address", helpSwitch="Partial address of a hidden service. Used in Onion repository mode.") 
        
        self.onionRepositoryMode = TortazoSwitch(shortSwitch='-R', longSwitch="--onion-repository", callback=self.__onionRepositoryMode, composedValues=["ssh", "ftp", "http", "onionup"], helpSwitch="Activate the Onion Repository mode and try to find hidden services in the TOR deep web.")
        
        self.workerThreadsRepository = TortazoSwitch(shortSwitch='-W', longSwitch="--workers-repository", defaultValue=10, typeSwitch=int, requiresSwitches=[self.onionRepositoryMode], helpSwitch="Number of threads used to process the ONION addresses generated.")
        self.validCharsRepository = TortazoSwitch(shortSwitch='-V', longSwitch="--validchars-repository", defaultValue='234567'+string.lowercase, helpSwitch="Valid characters to use in the generation process of onion addresses. Default: All characters between a-z and digits between 2-7")
        self.generateSimpleReport = TortazoSwitch(shortSwitch='-g', longSwitch="--generate-simple-nmapreport", callback=self.__generateSimpleReport, helpSwitch="Generate a report for each exit relay analized with Nmap and Shodan (if you use the switches for shodan). The reports will be generated in your home directory.")

        self.exportReport = TortazoSwitch(shortSwitch='-E', longSwitch="--export-report", callback=self.__exportReport, helpSwitch="Exports a JSON file with the results found by Tortazo. This feature is useful.")        


        self.discovery = Discovery(self, self.database)
        self.reporter = Reporting(self)

        self.switches = [self.verbose, self.useMirrors, self.useShodan, self.useCircuitExitNodes, self.useCircuitExitNodes, self.zombieMode, self.mode, self.openShell, self.useDatabase,
                        self.cleanDatabase, self.listPlugins, self.useLocalTorInstance, self.serversToAttack, self.shodanKey, self.listScanPorts, self.scanArguments, self.exitNodeFingerprint, 
                        self.controllerPort, self.runCommandBotnet, self.usePlugin, self.pluginArguments, self.torLocalInstance, self.scanIdentifier, self.onionPartialAddress, self.onionRepositoryMode, 
                        self.workerThreadsRepository, self.validCharsRepository, self.generateSimpleReport, self.excludeFingerprints]

        
        self.activatedSwitches=[]
        self.singleSwitches=[]

    def __logsTorInstance(self, log):
        '''
        Shows the Logs for the TOR startup.
        '''
        self.logger.debug(term.format(log, term.Color.GREEN))

    def __exportReport(self):
        if self.discovery is not None and self.discovery.torScan is not None:
            self.reporter.exportNmapReport(self.discovery.torScan, tortazoConfiguration.ExportNmapOutputFile)
            return True
        else:
            self.logger.warn(term.format("[-] No records found to generate the Nmap report." , term.Color.RED))        

    def __killTorProcess(self):
        #If TOR process has been started, it should be stopped.
        if hasattr(self, 'torProcess') and self.torProcess is not None:
            self.logger.info(term.format("[+] Killing TOR process with PID %s " %(self.torProcess.pid), term.Color.YELLOW))
            self.torProcess.kill()
        self.logger.info((term.format("[+] Process finished at "+ strftime("%Y-%m-%d %H:%M:%S", gmtime()), term.Color.YELLOW)))
        
    def __configureDatabaseInstance(self):
        if tortazoConfiguration.dbPostgres:
            self.database = TortazoPostgreSQL()
        elif tortazoConfiguration.dbMySQL:
            self.database = TortazoMySQL()
        else:
            self.database = TortazoSQLiteDB()
        return True

    def __cleanDatabase(self):
        self.logger.info(term.format("[+] Cleaning database... Deleting all records.", term.Color.YELLOW))
        self.database.initDatabase()
        self.database.cleanDatabaseState()
        return True

    def __activateVerbose(self):
        self.logger.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        self.logger.debug(term.format("[+] Verbose mode activated.", term.Color.GREEN))
        self.logger.info(term.format("[+] Process started at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()), term.Color.YELLOW))
        return True

    def __listPlugins(self):
        print "[*] Plugins list... "
        import pluginsDeployed
        for plugin in pluginsDeployed.plugins.keys():
            completeModulePath = pluginsDeployed.plugins.get(plugin)
            pluginModule = completeModulePath[:completeModulePath.rfind(".")]
            module = __import__(pluginModule)
            components = completeModulePath.split('.')
            for comp in components[1:]:
                module = getattr(module, comp)
            inst = module([])
            print "Plugin package: %s" %(completeModulePath)
            print "Plugin Name: %s" %(inst.name)
            print "Plugin Description: %s" %(inst.desc)
            print "Plugin Version: %s" %(inst.version)
            print "Plugin Author: %s" %(inst.author)
            print "Plugin Arguments Available: %s" %(inst.pluginConfigs.keys())
            print "\n"
        return True

    def __torLocalInstance(self):
        if os.path.exists(self.torLocalInstance.value) and os.path.isfile(self.torLocalInstance.value):
            torrcFile = open(self.torLocalInstance.value,'r')
            torConfig = {}
            import pwd
            if pwd.getpwuid(os.getuid()).pw_uid != 0:
                #Running TOR as non-root user. GOOD!
                for line in torrcFile:
                    if line.startswith("#", 0, len(line)) is False and len(line.split()) > 0:
                        torOptionName = line.split()[0]
                        if len(line.split()) > 1:
                            torOptionValue = line[len(torOptionName)+1 : ]
                            torConfig[torOptionName] = torOptionValue
                try:
                    self.logger.info(term.format("[+] Starting TOR Local instance with the following options: ", term.Color.YELLOW))
                    for config in torConfig.keys():
                        self.logger.info(term.format("[+] Config: %s value: %s " %(config, torConfig[config]), term.Color.YELLOW))
                    if os.path.exists(tortazoConfiguration.torExecutablePath):
                        self.torProcess = stem.process.launch_tor_with_config(config = torConfig, tor_cmd = tortazoConfiguration.torExecutablePath, init_msg_handler=self.__logsTorInstance)
                    else:
                        self.torProcess = stem.process.launch_tor_with_config(config = torConfig, init_msg_handler=self.__logsTorInstance)
                        
                    time.sleep(5)
                    if self.torProcess > 0:
                        #If SocksListenAddress or SocksPort properties are empty but the process has been started, the socks proxy will use the default values.
                        self.logger.debug(term.format("[+] TOR Process created. PID %s " %(self.torProcess.pid),  term.Color.GREEN))
                        if torConfig.has_key('SocksListenAddress'):
                            self.socksHost = torConfig['SocksListenAddress']
                        else:
                            self.socksHost = '127.0.0.1'
                        if torConfig.has_key('SocksPort'):
                            self.socksPort = torConfig['SocksPort']
                        else:
                            #Starting TOR from the command "tor". The default Socks port in that case is '9050'. If you run tor with tor bundle, the default socks port is '9150'
                            self.socksPort = '9050'
                except OSError, ose:
                    print sys.exc_info()
                    #OSError: Stem exception raised. Tipically, caused because the "tor" command is not in the path.
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.logger.warn(term.format("Exception raised during the startup of TOR Local instance.... "+str(ose), term.Color.RED))
                    self.logger.warn(term.format("Details Below: \n", term.Color.RED))
                    self.logger.warn(term.format("Type: %s " %(str(exc_type)), term.Color.RED))
                    self.logger.warn(term.format("Value: %s " %(str(exc_value)), term.Color.RED))
                    self.logger.warn(term.format("Traceback: %s " %(str(exc_traceback)), term.Color.RED))
            else:
                self.logger.warn(term.format("You cannot run TOR as root user! Please, use an account with limited privileges ", term.Color.RED))
                return False
        else:
            self.logger.warn(term.format("The specified torrc file is not valid: %s " %(str(self.torLocalInstance)), term.Color.RED))
        return True

    def __onionRepositoryMode(self):
        #Tortazo should start a process and the goes to sleep. In this mode should not be other actions to be performed.
        #This switch will invalidate the other switches, just repository mode should be started.
        # Setup and start the simulation
        try:
            serviceConnector = ServiceConnector(self)
            self.logger.info(term.format("[+] Entering in Onion Repository Mode. This process could take a lot of time depending what you know of the hidden service to discover...", term.Color.YELLOW))
            if tortazoConfiguration.loadKnownOnionSites:
                self.logger.info(term.format("[+] Reading the file of known hidden services located in 'db/knwonOnionSites.txt'. Tortazo will try to feed the local database with that information. If you want to avoid this behavior, set to False the property: 'loadKnownOnionSites' in the 'config/config.py' configuration file ...", term.Color.YELLOW))
            if self.onionPartialAddress.value.lower() == 'random':
                self.logger.info(term.format("[+] Random address generator selected ...", term.Color.YELLOW))
            else:
                self.logger.info(term.format("[+] Incremental address generator selected ...", term.Color.YELLOW))
                self.onionPartialAddress.setValue((self.onionPartialAddress.value.replace('http://', '')).replace('.onion', ''))
                if len(self.onionPartialAddress.value) == 0:
                    self.logger.warn(term.format("[+] Consider to use the switches -O / --onionpartial-address or -V / --validchars-repository to filter the results. ", term.Color.YELLOW))
                if len(self.onionPartialAddress.value) <= 10:
                    self.logger.warn(term.format("[+] You've entered an address with 10 or less characters [just %s chars]. The number of combinations will be very huge. You'll need a considerable process capacity in this machine and let run this process for hours, days or even weeks! If you're sure, let this process run" %(str(len(self.onionPartialAddress.value))), term.Color.YELLOW))
                    sys.stdout.write('%s [y/n]\n' %('Are you sure?'))
                    while True:
                        try:
                            input = raw_input
                            if strtobool(input().lower()) == True:
                                break
                            else:
                                return
                        except NameError:
                            pass
                        except ValueError:
                            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')
            if hasattr(self, "socksHost") and hasattr(self, "socksPort"):
                if self.socksPort is not None and self.socksPort.isdigit():
                    serviceConnector.setSocksProxySettings(self.socksHost, int(self.socksPort))
            self.logger.info(term.format("[+] Starting the Onion repository mode against "+self.onionRepositoryMode.value+" services...  " + strftime("%Y-%m-%d %H:%M:%S", gmtime()), term.Color.YELLOW))
            repository =  RepositoryGenerator(self.validCharsRepository.value, serviceConnector, self.database, self.onionPartialAddress.value, self.workerThreadsRepository.value)
            repository.startGenerator(tortazoConfiguration.loadKnownOnionSites, self.onionRepositoryMode.value)
            self.logger.info(term.format("[+] Onion repository finished...  " + strftime("%Y-%m-%d %H:%M:%S", gmtime()), term.Color.YELLOW))

        except KeyboardInterrupt:
            print "Interrupted!"
        except StandardError as standardExcept:
            self.logger.warn((term.format(standardExcept.message, term.Color.RED)))

        self.__killTorProcess()
        return True

    def __zombieMode(self):
        self.zombieMode.value.start()

    def __useDatabase(self):
        #There's a previous scan stored in database. We'll use that information!
        if self.scanIdentifier.value is None:
            self.logger.info(term.format("[+] Getting the last %s scans executed from database..."  %(self.serversToAttack.value),  term.Color.YELLOW))
            self.logger.debug(term.format("[+] Use -n/--servers-to-attack option to include more or less records from the scans recorded in database.",  term.Color.GREEN))
            self.exitNodes = self.database.searchExitNodes(self.serversToAttack.value, None)
        else:
            self.logger.info(term.format("[+] Getting the relays for the scan %d ..."  %(self.scanIdentifier.value),  term.Color.YELLOW))
            self.exitNodes = self.database.searchExitNodes(self.serversToAttack.value, self.scanIdentifier.value)

        if len(self.exitNodes) > 0:
            self.logger.info(term.format("[+] Done!" , term.Color.YELLOW))
        else:
            if self.scanIdentifier.value is None:
                self.logger.info(term.format("[+] No records found... You should execute an initial scan." , term.Color.YELLOW))
                self.logger.warn(term.format("[-] You've chosen to use the database records, however the database tables are empty because you have not run an initial scan." , term.Color.RED))
            else:
                self.logger.warn(term.format("[-] No records found with the scan identifier specified, check the database..." , term.Color.RED))
            return False
        return True

    def __useCircuitNodes(self):
        #Try to use a local instance of TOR to get information about the relays in the server descriptors.
        self.exitNodes = self.discovery.listCircuitExitNodes()
        return True

    def __mode(self):
        #Try to connect with the TOR directories to get information about the relays in the server descriptors.
        self.exitNodes = self.discovery.listAuthorityExitNodes() #Returns a list of TorNodeData objects
        return True

    def __useShodan(self):
        self.shodanHosts = []
        self.logger.info(term.format("[+] Shodan Activated. About to read the Development Key. ", term.Color.YELLOW))
        for torNode in self.exitNodes:
            if self.shodanKey.value == None:
                self.logger.warn(term.format("[-] Shodan Key's File has not been specified. We can't use shodan without a valid key", term.Color.RED))
            else:
                #Read the shodan key and create the Shodan object.
                try:
                    shodanKeyString = open(self.shodanKey).readline().rstrip('\n')
                    shodanHost = self.discovery.shodanSearchByHost(shodanKeyString, torNode.host)
                    self.shodanHosts.append(shodanHost)
                    if self.generateSimpleReport in self.activatedSwitches:
                        #Generate the report for Shodan if the switch for reporting is enabled.
                        if len(self.shodanHosts) > 0:
                            self.reporter.generateShodanReport(self.shodanHosts, tortazoConfiguration.ShodanOutputFile)
                except IOError, ioerr:
                    self.logger.warn(term.format("[-] Shodan's key File: %s not Found." %(str(self.shodanKey.value)), term.Color.RED))
        return True

    def __generateSimpleReport(self):
        if self.exitNodes is not None and len(self.exitNodes) > 0:
            self.reporter.generateNmapReport(self.exitNodes, tortazoConfiguration.NmapOutputFile)
            return True
        else:
            self.logger.warn(term.format("[-] No records found to generate the Nmap report." , term.Color.RED))

    def __loadAndExecute(self):
        if self.usePlugin.value is None:
            self.logger.warn((term.format("[-] You should specify a plugin with the option -P/--use-plugin", term.Color.YELLOW)))
            return False
        try:
            pluginArgs = {}
            if self.pluginArguments.value != None:
                arguments = self.pluginArguments.value.split(',')
                for argument in arguments:
                    key, value = argument.split('=')
                    print key, value
                    pluginArgs[key] = value
            import pluginsDeployed
            self.logger.debug((term.format("[+] Loading plugin...", term.Color.GREEN)))
            if pluginsDeployed.plugins.__contains__(self.usePlugin.value):
                completeModulePath = pluginsDeployed.plugins.get(self.usePlugin.value)
                pluginModule = completeModulePath[:completeModulePath.rfind(".")]
                module = __import__(pluginModule)
                components = completeModulePath.split('.')
                for comp in components[1:]:
                    module = getattr(module, comp)
                try:
                    if hasattr(self,'exitNodes') == False:
                        self.logger.warn((term.format("[-] You should select a set of exit nodes from database or an active scan. Use de Information Gathering mode (-m/--mode) or Database mode (-D/--use-database).", term.Color.RED)))
                        return False

                    if self.socksHost is not None and self.socksPort is not None and self.useLocalTorInstance:
                        self.logger.info((term.format("[+] You've started a TOR local instance and specified the -U/--use-localinstance option. The plugin loaded will use the following options to connect with TOR and Hidden Services in the deep web: " , term.Color.YELLOW)))
                        self.logger.info((term.format("[+] Host=%s , Port=%s" %(self.socksHost, self.socksPort), term.Color.YELLOW)))
                        reference = module(self.exitNodes)
                        reference.serviceConnector.setSocksProxySettings(self.socksHost, self.socksPort)
                        reference.setPluginArguments(pluginArgs)
                        reference.processPluginArguments()
                        reference.serviceConnector.cli = self
                        reference.cli = self
                    else:
                        self.logger.info((term.format("[+] If you want to connect with Hidden Services in the deep web using the loaded plugin, you must start a TOR local instance manually. The default configuration used to connect with the TOR Socks Server is: " , term.Color.YELLOW)))
                        self.logger.info((term.format("[+] Host=%s , Port=%s" %(tortazoConfiguration.socksHost, tortazoConfiguration.socksPort), term.Color.YELLOW)))
                        self.logger.info((term.format("[+] You can change this configuration editing the 'socksHost' and 'socksPort' properties in 'config.py' module. Also, you can use -T/--tor-localinstance with your 'torrc' file and Tortazo will start a TOR instance for you and then, if you use the -U/--use-localinstance Tortazo will use the TOR local instance started to connect with hidden services in the deep web.", term.Color.YELLOW)))
                        reference = module(self.exitNodes)
                        reference.serviceConnector.setSocksProxySettings(tortazoConfiguration.socksHost, tortazoConfiguration.socksPort)
                        reference.setPluginArguments(pluginArgs)
                        reference.processPluginArguments()
                        reference.serviceConnector.cli = self
                        reference.cli = self
                    if hasattr(self, 'database'):
                        reference.setDatabaseConnection(self.database)
                    reference.runPlugin()
                except StandardError as standarError:
                    self.logger.warn((term.format(standarError.message, term.Color.RED)))
                except PluginException as pluginExc:
                    self.logger.warn((term.format("[-] Exception raised executing the plugin. Please, check the arguments used in the function called. Details below.", term.Color.RED)))
                    self.logger.warn((term.format("Message: %s " %(pluginExc.getMessage()), term.Color.RED)))
                    self.logger.warn((term.format("Plugin: %s " %(pluginExc.getPlugin()), term.Color.RED)))
                    self.logger.warn((term.format("Method: %s " %(pluginExc.getMethod()), term.Color.RED)))
                    self.logger.warn((term.format("Trace: %s " %(pluginExc.getTrace()), term.Color.RED)))
                self.logger.debug((term.format("[+] Done!", term.Color.GREEN)))
            else:
                self.logger.warn((term.format("[-] The plugin specified is unknown... Check the available plugins with -L/--list-plugins option", term.Color.RED)))
        except ImportError, importErr:
            print "Unexpected error:", sys.exc_info()
            self.logger.warn((term.format("[-] Error loading the class. Your plugin class should be located in 'plugins' package and registered in pluginsDeployed.py. Check the available plugins with -L/--list-plugins option", term.Color.RED)))
        except AttributeError, attrErr:
            print "Unexpected error:", sys.exc_info()
            self.logger.warn((term.format("[-] Error loading the class. Your plugin class should be located in 'plugins' package and registered in pluginsDeployed.py. Check the available plugins with -L/--list-plugins option", term.Color.RED)))






    def run(self):
        if self.zombieMode not in self.activatedSwitches and self.usePlugin not in self.activatedSwitches and self.mode not in self.activatedSwitches and self.onionRepositoryMode not in self.activatedSwitches:
            self.logger.warn(term.format("Specify the execution mode. You should use Info Gathering (-m), Botnet Mode (-z) or Plugins Mode (-P) or Onion Repository (-R). Type '--help' to see the available options. ", term.Color.RED))
        else:
            self.torCommand = "python Tortazo.py "
            for singleSwitch in self.singleSwitches:
                if singleSwitch.value != None:
                    self.torCommand += "%s %s " %(str(singleSwitch.longSwitch) , str(singleSwitch.value) )
                else:
                    self.torCommand += "%s " %(str(singleSwitch.longSwitch)  )            
            
            for switch in self.activatedSwitches:
                if switch.value != None:
                    self.torCommand += "%s %s " %(str(switch.longSwitch) , str(switch.value) )
                else:
                    self.torCommand += "%s " %(str(switch.longSwitch)  )
                if not switch.callback():
                    break
        #If TOR process has been started, it should be stopped.
        self.__killTorProcess()
