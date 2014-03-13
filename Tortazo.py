# coding=utf-8
'''
Created on 22/01/2014

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

from plumbum import cli, local
import logging as log
from time import gmtime, strftime
import ftplib
from core.tortazo.Discovery import Discovery
from core.tortazo.WorkerThread import WorkerThread
from core.tortazo.BotNet import BotNet
from core.tortazo.Reporting import Reporting
import Queue
from stem.util import term
import logging as log
import config


#  ████████╗ ██████╗ ██████╗ ████████╗ █████╗ ███████╗ ██████╗ 
#  ╚══██╔══╝██╔═══██╗██╔══██╗╚══██╔══╝██╔══██╗╚══███╔╝██╔═══██╗
#     ██║   ██║   ██║██████╔╝   ██║   ███████║  ███╔╝ ██║   ██║
#     ██║   ██║   ██║██╔══██╗   ██║   ██╔══██║ ███╔╝  ██║   ██║
#     ██║   ╚██████╔╝██║  ██║   ██║   ██║  ██║███████╗╚██████╔╝
#     ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝ 
#                                                              

#
#	Attack exit nodes of the TOR Network.
#	Author: Adastra.
#	http://thehackerway.com
#
#	DONE IN V1.0:
#   "{" and "}"  means Done :P
#
#   {-} In bruteforce mode, if there's no dictfile, then use FuzzDB to perform the bruteforce attack.
#   {-} Check the "open-shell" feature. Try with invalid values, a long list of bots, etc.
#   {-} Check the Fabric library for Botnet C&C
#   {-} Testing
#   {-} Docs.
#   {-} NMAP Scripting output! Include this in the final report and include the nickname of the scanned exitnode, not just the IP Address.
#   {-} When filter by fingerprint and use the local descriptors, the filter is not working as expected. Check it!
#
#   TODO IN V1.1:
#   {-} Upgrade the Shodan Library and use the new features. Move Shodan from "WorkerThread to Discovery" (validate the shodankey file, what happen if the file don't exists?)
#   - Testing Shodan Features and generate a report with jinja2.
#   - Plugins system: Just an directory with *.py files. The name of the "py" should define a class with a constructor which receives the "TorNodeData" structure, in this way, the developer can use the internal data representation of Exit Nodes of tor.
#   - Format reports for Nmap, Shodan, Nessus and SNMP. (Not just an .txt file, create an HTML, XML and probably JSON files)
#   - Report any issue to the administrator of the exitnode.
#   - PyNessus integration (develop as Plugin).
#   - Gather information about SNMP Devices.
#   - Upload and execute files to the compromised machines using SFTP and FTP.
#   - Check subterfuge: http://code.google.com/p/subterfuge/
#   - Allow 'windows', 'linux', 'bsd', and other filters. (Also, allow any type of OS.)
#   - Check what do bannergrab:  http://sourceforge.net/projects/bannergrab/
#   - GeoLocation, for example using: http://www.melissadata.com/lookups/iplocation.asp?ipaddress=46.17.138.212
#   - Use PyInstaller to generate an executable for Linux and Windows.
#   - Create setup.py for Tortazo.

#   TODO IN V1.2:
#   - Integration with W3AF
#   - Try to integrate with FOCA.


class Cli(cli.Application):
    '''
    Command-Line options received.
    '''
    PROGNAME = "TORTAZO"
    AUTHOR = "Adastra"
    VERSION = "1.0"
    SEPARATOR = ':' #Separator for the dictionary (bruteforce attacks) for each line in the file, the user and password must be separated by colon. For Instance -> user:password
    verbose = cli.Flag(["-v", '--verbose'], help="Verbose Mode.")
    brute = cli.Flag(["-b", '--brute'], help="Brute Force Mode. (Specify -f/--passwords-file option to select the passwords file. Every line should contain the the username and password to test separated with a colon <USER>:<PASSWORD>)")
    useMirror = cli.Flag(["-d", '--use-mirrors'], help="Use the mirror directories of TOR. This will help to not overwhelm the official directories")
    useShodan = cli.Flag(["-s", '--use-shodan'], help="Use ShodanHQ Service. (Specify -k/--shodan-key to set up the file where's stored your shodan key.)")
    useCircuitExitNodes = cli.Flag(["-c", "--use-circuit-nodes"], help="Use the exit nodes selected for a local instance of TOR.")
    openShell = cli.Flag(["-o", "--open-shell"], excludes=["--mode"], requires=["--zombie-mode"],  help="Open a shell on the specified host. example: '--open-shell 1' will spawn a new shell on the host defined in line 1 of the 'tortazo_botnet.bot' file")

    threads = 1 #Execution Threads.
    # mode = None #Mode: Windows/Linux
    dictFile = None #Dict. file for brute-force attacks.
    exitNodesToAttack = 10 #Number of default exit-nodes to filter from the Server Descriptor file.
    shodanKey = None #ShodanKey file.
    scanPorts = "21,22,23,53,69,80,88,110,139,143,161,162,389,443,445,1079,1080,1433,3306,5432,8080,9050,9051,5800" #Default ports used to scan with nmap.
    scanArguments = None #Scan Arguments passed to nmap.
    exitNodeFingerprint = None #Fingerprint of the exit-node to attack.
    queue = Queue.Queue() #Queue with the host/open-port found in the scanning.
    controllerPort = '9151'
    zombieMode = None
    mode = None
    runCommand = None
    pluginManagement = None



    @cli.switch(["-n", "--servers-to-attack"], int, help="Number of TOR exit-nodes to attack. Default = 10")
    def servers_to_attack(self, exitNodesToAttack):
        '''
        Number of "exit-nodes" to attack received from command-line
        '''
        self.exitNodesToAttack = exitNodesToAttack

    @cli.switch(["-t", "--threads"], cli.Range(1, 20), help='Number of threads to use.')
    def number_threads(self, threads):
        '''
        Number of threads to create when the scanning process has been done.
        '''
        self.threads = threads

    @cli.switch(["-m", "--mode"], cli.Set("windows", "linux", case_sensitive=False),  excludes=["--zombie-mode"] , help="Filter the platform of exit-nodes to attack.")
    def server_mode(self, mode):
        '''
        Server Mode: Search for Windows or Linux machines.
        '''
        self.mode = mode

    @cli.switch(["-f", "--passwords-file"], str, help="Passwords File in the Bruteforce mode.", requires=["--brute"])
    def passwords_file(self, dictFile):
        '''
        User's file. Used to perform bruteforce attacks.
        '''
        self.dictFile = dictFile

    @cli.switch(["-k", "--shodan-key"], str, help="Development Key to use Shodan API.", requires=["--use-shodan"])
    def shodan_key(self, shodanKey):
        '''
        This option is used to specify the file where the shodan development key is stored
        '''
        self.shodanKey = shodanKey

    @cli.switch(["-l", "--list-ports"], str, help="Comma-separated List of ports to scan with Nmap. Don't use spaces")
    def list_ports(self, scanPorts):
        '''
        List of ports used to perform the nmap scan.
        '''
        self.scanPorts = scanPorts

    @cli.switch(["-a", "--scan-arguments"], str, help='Arguments to Nmap. Use "" to specify the arguments. For example: "-sSV -A -Pn"')
    def scan_arguments(self, scanArguments):
        '''
        Arguments used to perform the nmap scan.
        '''
        self.scanArguments = scanArguments

    @cli.switch(["-e", "--exit-node-fingerprint"], str, help="ExitNode's Fingerprint to attack.")
    def exitNode_Fingerprint(self, exitNodeFingerprint):
        '''
        If we want to perform a single attack against an known "exit-node", We can specify the fingerprint of the exit-node to perform the attack.
        '''
        self.exitNodeFingerprint = exitNodeFingerprint

    @cli.switch(["-i", "--controller-port"], str, help="Controller's port of the local instance of TOR. (Default=9151)", requires=["--use-circuit-nodes"])
    def controller_port(self, controllerPort):
        '''
        Controller's Port. Default=9151
        '''
        self.controllerPort = controllerPort

    @cli.switch(["-z", "--zombie-mode"], str, help="This option reads the tortazo_botnet.bot file generated from previous successful attacks. With this option you can select the Nicknames that will be excluded. (Nicknames included in the tortazo_botnet.bot). For instance, '-z Nickname1,Nickname2' or '-z all' to include all nicknames.")
    def zombie_mode(self, zombieMode):
        '''
        Zombie mode to execute commands across the compromised hosts.
        '''
        if zombieMode == None:
            self.zombieMode = ""
        self.zombieMode = zombieMode

    @cli.switch(["-r", "--run-command"], str, excludes=["--mode"], requires=["--zombie-mode"],  help='Execute a command across the hosts of the botnet. Requieres the -z/--zombie-mode. example: --run-command "uname -a; uptime" ')
    def run_command(self, runCommand):
        '''
        Command to execute across the compromised hosts.
        '''
        self.runCommand = runCommand

    @cli.switch(["-P", "--use-plugins"], str, help='Execute a plugin (or list) included in the plugins directory. for instance: "-P simplePlugin:simplePrinter,argName1=arg1,argName2=arg2,argNameN=argN;anotherSimplePlugin:anotherSimpleExecutor,argName1=arg1,argName2=arg2,argNameN=argN" where simplePlugin is the module, simplePrinter is a class which inherites from BasePlugin class and argName1=argValue1,argName2=argValue2,argNameN=argValueN are arguments used for this plugin. Multiple plugins should be separated by ";" Check the documentation for more detailed information')
    def plugin_management(self, pluginManagement):
        '''
        Plugin Management.
        '''
        self.pluginManagement = pluginManagement

    def main(self):
        '''
        Initialization of logger system.
        '''

        self.logger = log
        if self.verbose:
            self.logger.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
            self.logger.debug(term.format("[+] Verbose mode activated.", term.Color.GREEN))
        else:
            self.logger.basicConfig(format="%(levelname)s: %(message)s")
        self.logger.info(term.format("[+] Process started at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()), term.Color.YELLOW))

        #self.loadAndExecute(self,"simplePlugin:simplePrinter")
        '''
        Simple Tests for V1.0

        exitNode = [('127.0.0.1', 'descriptor'), [22,33,44,55,66]]
        self.queue.put(exitNode)
        worker = WorkerThread(self.queue, 0, self)
        worker.setDaemon(True)
        worker.start()
        self.queue.join()
        '''

        '''
            List and Scan the exit nodes. The function will return an dictionary with the exitnodes found and the open ports.
            THIS PROCESS IS VERY SLOW AND SOMETIMES THE CONNECTION WITH THE DIRECTORY AUTHORITIES IS NOT AVAILABLE.
        '''

        if self.zombieMode:
            '''
            In zombie mode, The program should read the file named "tortazo_botnet.bot".
            In that file, every line have this format: host:user:password:nickname
            Extract every host and then, create a list of bots.
            '''
            botnet = BotNet(self)
            botnet.start()


        elif self.mode is not None:
            discovery = Discovery(self)
            exitNodes = []
            if self.useCircuitExitNodes:
                exitNodes = discovery.listCircuitExitNodes()
            else:
                exitNodes = discovery.listAuthorityExitNodes() #Returns a list of TorNodeData objects

            if exitNodes is not None and len(exitNodes) > 0:
                reporter = Reporting(self)
                reporter.generateNmapReport(exitNodes, config.NmapOutputFile)
                for torNode in exitNodes:
                    if self.brute:
                        self.queue.put(torNode)
                    #If shodan is activated, let's try to gather some information for every node found.
                    if self.useShodan == True:
                        #Using Shodan to search information about this machine in shodan database.
                        self.logger.info(term.format("[+] Shodan Activated. About to read the Development Key. ", term.Color.YELLOW))
                        if self.shodanKey == None:
                            #If the key is None, we can't use shodan.
                            self.logger.warn(term.format("[-] Shodan Key's File has not been specified. We can't use shodan without a valid key", term.Color.RED))
                        else:
                            #Read the shodan key and create the Shodan object.
                            try:
                                shodanKeyString = open(self.shodanKey).readline().rstrip('\n')
                                shodanHost = discovery.shodanSearchByHost(shodanKeyString, torNode.host)
                                reporter.generateShodanReport(shodanHost, config.ShodanOutputFile)
                            except IOError, ioerr:
                                self.logger.warn(term.format("[-] Shodan's key File: %s not Found." %(self.shodanKey), term.Color.RED))

                #Check if there's any plugin to execute!
                if self.pluginManagement != None:
                    self.loadAndExecute(self.pluginManagement, exitNodes)

                #Block until the queue is empty.
                if self.brute:
                    for thread in range(self.threads): #Creating the number of threads specified by command-line.
                        worker = WorkerThread(self.queue, thread, self)
                        worker.setDaemon(True)
                        worker.start()
                    self.queue.join()
        else:
            self.logger.info(term.format("[-] The option -m/mode is mandatory (values: windows | linux)", term.Color.RED))
        self.logger.info((term.format("[+] Process finished at "+ strftime("%Y-%m-%d %H:%M:%S", gmtime()), term.Color.YELLOW)))

    def loadAndExecute(self, listPlugins, torNodesFound):
        '''
        Load and execute external rutines (plugins)
        '''
        #simplePlugin:simplePrinter,argName1=arg1,argName2=arg2,argNameN=argN;anotherSimplePlugin:anotherSimpleExecutor,argName1=arg1,argName2=arg2,argNameN=argN
        if listPlugins is None:
            self.logger.warn((term.format("[-] You should specify a list of plugins with the option -P/--use-plugins", term.Color.YELLOW)))
            return
        plugins = listPlugins.split(";")
        for plugin in plugins:
            pluginModule, pluginClass = plugin.split(":")
            if pluginModule is None or pluginClass is None:
                self.logger.info((term.format("[-] Format "+ listPlugins +" invalid. Check the documentation to use plugins in Tortazo", term.Color.YELLOW)))
                return
            try:
                module = __import__("plugins."+pluginModule)
                pluginArguments = pluginClass.split(',')
                pluginClassName = pluginArguments[0]
                pluginArguments.remove(0)
                components = ("plugins."+pluginModule+"."+pluginClassName).split('.')
                self.logger.debug((term.format("[+] Loading plugin...", term.Color.GREEN)))
                for comp in components[1:]:
                    module = getattr(module, comp)
                reference = module()
                reference.setNodes(torNodesFound)
                self.logger.debug((term.format("[+] Done!", term.Color.GREEN)))
                self.logger.debug((term.format("[+] Parsing the arguments for the plugin...", term.Color.GREEN)))
                pluginArguments = {}
                for argument in pluginArguments:
                    argumentName, argumentValue = argument.split('=')
                    pluginArguments[argumentName] = argumentValue
                reference.setPluginArguments(pluginArguments)
                reference.runPlugin()
            except ImportError, importErr:
                self.logger.warn((term.format("[-] Error loading the class. Your plugin class should be located in 'plugins' package. Check if "+pluginModule+"."+pluginClass+" exists", term.Color.RED)))


if __name__ == "__main__":
    '''
    Start the main program.
    '''
    Cli.run()
