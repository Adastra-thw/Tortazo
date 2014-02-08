# coding=utf-8

from plumbum import cli, local
import logging as log
from time import gmtime, strftime
import ftplib
import os
from core.tortazo.CommandAndControl import CommandAndControl
from core.tortazo.Discovery import Discovery
from core.tortazo.WorkerThread import WorkerThread
import Queue

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
#	TODO:
#
#	- Use combinators if the passfile is not issued, check itertools module.
#	- Check the Fabric library for Botnet C&C
#	- Testing and Doc.
#   - NMAP Scripting output! Include this in the final report and include the nickname of the scanned exitnode, not just the IP Address.
#   - When filter by fingerprint and use the local descriptors, the filter is not working as expected. Check it!
#

class Cli(cli.Application):
    '''
	Command-Line options received.
	'''
    PROGNAME = "TORTAZO"
    AUTHOR = "Adastra"
    VERSION = "1.0"
    verbose = cli.Flag(["-v", '--verbose'], help="Verbose Mode.")
    brute = cli.Flag(["-b", '--brute'], help="Brute Force Mode. (Specify -f/--passwords-file option to select the passwords file. Every line should contain the the username and password to test separated with a colon <USER>:<PASSWORD>)")
    useMirror = cli.Flag(["-d", '--use-mirrors'], help="Use the mirror directories of TOR. This will help to not overwhelm the official directories")
    useShodan = cli.Flag(["-s", '--use-shodan'], help="Use ShodanHQ Service. (Specify -k/--shodan-key to set up the file where's stored your shodan key.)")
    useCircuitExitNodes = cli.Flag(["-c", "--use-circuit-nodes"], help="Use the exit nodes selected for a local instance of TOR.")
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
    zoombieMode = None
	
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

    @cli.switch(["-m", "--mode"], cli.Set("windows", "linux", case_sensitive=False), mandatory=True, excludes=["--zoombie-mode"] , help="Filter the platform of exit-nodes to attack.")
    def server_mode(self, mode):
        '''
        Server Mode: Search for Windows or Linux machines.
        '''
        self.mode = mode

    @cli.switch(["-f", "--passwords-file"], help="Passwords File in the Bruteforce mode.", requires=["--brute"])
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
	
    @cli.switch(["-z", "--zoombie-mode"], str, help="This option reads the commandandcontrol* files generated from previous scans. Allows to send commands parallely over all the compromised hosts.")
    def zoombie_mode(self, zoombieMode):
        '''
        Zoombie mode to execute commands across the compromised hosts.
        '''
        self.zoombieMode = zoombieMode

    def main(self):
        '''
            List and Scan the exit nodes. The function will return an dictionary with the exitnodes found and the open ports.
            THIS PROCESS IS VERY SLOW AND SOMETIMES THE CONNECTION WITH THE DIRECTORY AUTHORITIES IS NOT AVAILABLE.
        '''
        if self.zoombieMode:
            control = CommandAndControl(self)
            control.execute(self.zoombieMode)
        else:
            discovery = Discovery(self)
            exitNodes = []
            if self.useCircuitExitNodes:
                exitNodes = discovery.listCircuitExitNodes()
            else:
                exitNodes = discovery.listAuthorityExitNodes() #Returns a tuple with IP Addresses and open-ports.

            if exitNodes != None and len(exitNodes) > 0:
                for thread in range(self.threads): #Creating the number of threads specified by command-line.
                    worker = WorkerThread(self.queue, thread, self)
                    worker.setDaemon(True)
                    worker.start()

                for exitNode in exitNodes.items():
                    self.queue.put(exitNode)
                self.queue.join() #Blocks the main process until the queue is empty.

        log.info("[+] Process finished at "+ strftime("%Y-%m-%d %H:%M:%S", gmtime()))


if __name__ == "__main__":
    '''
    Start the main program.
    '''
    Cli.run()
