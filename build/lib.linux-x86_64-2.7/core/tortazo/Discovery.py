# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

Discovery.py

Discovery is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

Discovery is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from stem.descriptor.remote import DescriptorDownloader
from stem import CircStatus
from stem.control import Controller
from stem.connection import MissingPassword, AuthenticationFailure
from getpass import getpass
from stem.util import term
from core.tortazo.data.TorNodeData import TorNodeData, TorNodePort, TorNodeScan
from core.tortazo.data.ShodanHost import ShodanHost
import zlib
import nmap
import shodan
import urllib2
from config import config as tortazoConfiguration

class Discovery:
    '''
		Class used to list the current "exit-nodes" from the TOR network and perform the nmap scanning to discover the open ports.
	'''
    executor = None
    scan = None

    def __init__(self, executor, database):
        '''
        Constructor.
        '''
        self.tortazoExecutor = executor
        self.database = database
        self.exitNodes = []

    def __excludeFingerPrint(self, exit_fingerprint):
        if self.tortazoExecutor.excludeFingerprints.value != None:
            self.tortazoExecutor.logger.debug(term.format("[+] Excluding the following Fingerprints: "+str(self.tortazoExecutor.excludeFingerprints.value), term.Color.GREEN))
            listFingers = self.tortazoExecutor.excludeFingerprints.value.split(',')
            if exit_fingerprint in listFingers:
                self.tortazoExecutor.logger.debug(term.format("[+] The fingerprint %s has been excluded from the scanning. " %(str(exit_fingerprint)), term.Color.GREEN))
                return True
        return False
        
    def listAuthorityExitNodes(self):
        '''
			List the Exit Nodes using the filters specified by command-line.
		'''
        self.tortazoExecutor.logger.debug(term.format("[+] Try to listing the current Exit-Nodes of TOR.", term.Color.GREEN))
        if self.tortazoExecutor.exitNodeFingerprint.value != None:
            self.tortazoExecutor.logger.debug(term.format("[+] Using the fingerprint: %s " % (self.tortazoExecutor.exitNodeFingerprint.value), term.Color.GREEN))
        self.tortazoExecutor.logger.debug(term.format("[+] Filter by platform: %s." % (self.tortazoExecutor.mode.value), term.Color.GREEN))
        self.tortazoExecutor.logger.debug(term.format("[+] Retrieving the first %d records in the Descriptors." % (self.tortazoExecutor.serversToAttack.value),
                             term.Color.GREEN))

        if self.tortazoExecutor.useMirrors.value == True:
            self.tortazoExecutor.logger.info(term.format("[+] Using the Directory Mirrors to get the descriptors", term.Color.YELLOW))
        downloader = DescriptorDownloader(use_mirrors=self.tortazoExecutor.useMirrors.value)
        if self.tortazoExecutor.exitNodeFingerprint.value != None:
            descriptors = downloader.get_server_descriptors(fingerprints=[self.tortazoExecutor.exitNodeFingerprint.value])
        else:
            descriptors = downloader.get_server_descriptors()
        try:
            listDescriptors = descriptors.run()
        except zlib.error:
            self.tortazoExecutor.logger.error(term.format("[-] Error fetching the TOR descriptors. This is something quite common... Try again in a few seconds.",term.Color.RED))
            return
        except urllib2.HTTPError:
            self.tortazoExecutor.logger.error(term.format("[-] Figerprint not found... It's not registered in the last valid server descriptor.",term.Color.RED))
            return
        return self.filterNodes(listDescriptors)

    def listCircuitExitNodes(self):
        '''
        Use the descriptors downloaded by the TOR client and list the exit nodes.
        '''
        listDescriptors = []
        self.tortazoExecutor.logger.info(term.format(
            "[+] Trying to get a list of exit nodes from the already downloaded descriptors from the TOR Client instead of using the directory authorities",
            term.Color.YELLOW))
        if self.tortazoExecutor.controllerPort.value and self.tortazoExecutor.controllerPort.value.isdigit():
            try:
                controllerPass = getpass("Enter the password for the Local Controller (Empty if the instance doesn't need a password): ")
                controller = Controller.from_port(port=int(self.tortazoExecutor.controllerPort.value))
                if controllerPass:
                    controller.authenticate(controllerPass)
                else:
                    controller.authenticate()
                self.tortazoExecutor.logger.debug(term.format("[+] TOR Controller Authentication Successful.", term.Color.GREEN))
                for circuit in controller.get_circuits():
                    if circuit.status != CircStatus.BUILT:
                        continue
                    exit_fingerprint, exit_nickname = circuit.path[-1]
                    
                    '''As of Tor version 0.2.3.25 relays no longer get server descriptors by default. It's advised that you use microdescriptors instead, but if you really need server descriptors then you can get them by setting UseMicrodescriptors 0.	'''
                    exitNode = controller.get_server_descriptor(exit_fingerprint, None)
                    if self.tortazoExecutor.exitNodeFingerprint.value != None:
                        self.tortazoExecutor.logger.debug(term.format("[+] Filtering by Fingerprint: "+str(self.tortazoExecutor.exitNodeFingerprint.value), term.Color.GREEN))
                    
                    if self.__excludeFingerPrint(exit_fingerprint):
                        continue
                        
                    if exitNode:
                        if self.tortazoExecutor.exitNodeFingerprint.value is None:
                            listDescriptors.append(exitNode)
                        elif self.tortazoExecutor.exitNodeFingerprint.value == exitNode.fingerprint:
                            self.tortazoExecutor.logger.debug(term.format("[+] The Fingerprint specified has been found (%s , %s) ." %(exitNode.nickname, exitNode.fingerprint), term.Color.GREEN))
                            listDescriptors.append(exitNode)
                        else:
                            self.tortazoExecutor.logger.debug(term.format("[+] Server found but there's no match with the Fingerprint specified (%s , %s) ." %(exitNode.nickname, exitNode.fingerprint), term.Color.GREEN))
                    return self.filterNodes(listDescriptors)
                    #exit_address = exit_desc.address if exit_desc else 'unknown'
                    #print "Exit relay"
                    #print "  fingerprint: %s" % exit_fp
                    #print "  nickname: %s" % exit_nickname
                    #print "  address: %s" % exit_address
                    #print
            except MissingPassword:
                self.tortazoExecutor.logger.warn(term.format("[-] Expected password in the AUTH process... This should not be empty", term.Color.RED))
            except AuthenticationFailure:
                self.tortazoExecutor.logger.warn(term.format("[-] The password specified is invalid.", term.Color.RED))
        else:
            self.tortazoExecutor.logger.warn(term.format("[-] The control port specified is invalid.", term.Color.RED))

    def filterNodes(self, listDescriptors):
        '''
        List the Exit Nodes using the filters specified by command-line.
        '''
        nodesAlreadyScanned = []
        nm = nmap.PortScanner()
        #Creating a "TorScan" with the information about the current scan.
        torScan = TorNodeScan()
        
        if tortazoConfiguration.dbPostgres == True:
            import psycopg2
            from datetime import datetime
            nowTime = datetime.now()
            torScan.scanDate = psycopg2.Timestamp(nowTime.year, nowTime.month, nowTime.day, nowTime.hour, nowTime.minute, nowTime.second)    
        else:
            torScan.scanDate = datetime.now().time()
        
        for descriptor in listDescriptors[0:self.tortazoExecutor.serversToAttack.value]:
        #for descriptor in parse_file(open("/home/adastra/Escritorio/tor-browser_en-US-Firefox/Data/Tor/cached-consensus")):
            if descriptor.operating_system is not None and \
               self.tortazoExecutor.mode.value.lower() in descriptor.operating_system.lower() and \
               descriptor.exit_policy.is_exiting_allowed():
                #SEARCH FILTERING BY FINGERPRINT
                #Conditions: Fingerprint specified in command-line AND
                #Relay Fingerprint equals to the Fingerprint specified in command-line. AND
                #Relay's Operative System equals to the Operative System (option mode) specified in command-line AND
                #The Relay is a Exit Node.
                                    
                if self.__excludeFingerPrint(descriptor.fingerprint):
                    continue
                
                if descriptor.address not in nodesAlreadyScanned:
                    self.tortazoExecutor.logger.info(term.format("[+] %s System has been found... Nickname: %s - OS Version: %s - Fingerprint: %s - TOR Version: %s " % (descriptor.operating_system, descriptor.nickname, descriptor.operating_system, descriptor.fingerprint, descriptor.tor_version), term.Color.YELLOW))
                    self.tortazoExecutor.logger.debug(term.format("[+] Starting the NMap Scan with the following options: ", term.Color.GREEN))
                    self.tortazoExecutor.logger.debug(term.format("[+][+] Scan Address: %s " % (descriptor.address), term.Color.GREEN))
                    self.tortazoExecutor.logger.debug(term.format("[+][+] Scan Arguments: %s " % (self.tortazoExecutor.scanArguments.value), term.Color.GREEN))
                    self.tortazoExecutor.logger.debug(term.format("[+][+] Scan Ports: %s " % (self.tortazoExecutor.listScanPorts.value), term.Color.GREEN))
                    try:
                        if self.tortazoExecutor.scanArguments.value != None:
                            nm.scan(descriptor.address, arguments=self.tortazoExecutor.scanArguments.value )
                            self.tortazoExecutor.logger.debug(term.format("[+][+] Nmap command: %s " % (nm.command_line()), term.Color.GREEN))
                        else:
                            nm.scan(descriptor.address, self.tortazoExecutor.listScanPorts.value)
                            self.tortazoExecutor.logger.debug(term.format("[+][+] Nmap command: %s " % (nm.command_line()), term.Color.GREEN))
                    except nmap.nmap.PortScannerError as scannerError:
                        self.tortazoExecutor.logger.warn(term.format("[-] Error scanning the host: %s scanning the next host in the list" % (descriptor.address), term.Color.GREEN))
                        continue
                    self.recordNmapScan(nm, descriptor)
                    self.tortazoExecutor.logger.info(term.format('[+] Scan Ended for %s .' % (descriptor.nickname), term.Color.YELLOW))
                    nodesAlreadyScanned.append(descriptor.address)
        if len(self.exitNodes) == 0:
            self.tortazoExecutor.logger.warn(term.format("[+] In the first %d records searching for the %s Operating System, there's no results (machines with detected open ports)" %(self.tortazoExecutor.serversToAttack.value, self.tortazoExecutor.mode.value.lower()), term.Color.RED))
            self.tortazoExecutor.logger.warn(term.format("[+] Also, if you see scans above, maybe the relays that you see were scanned before and therefore, not included in the final list of scanned relays in the current scan", term.Color.RED))
        else:
            torScan.numNodes = len(self.exitNodes) 
            torScan.tortazoCommand = self.tortazoExecutor.torCommand
            
            if tortazoConfiguration.dbPostgres == True:
                import psycopg2
                from datetime import datetime
                nowTime = datetime.now()
                torScan.scanFinished = psycopg2.Timestamp(nowTime.year, nowTime.month, nowTime.day, nowTime.hour, nowTime.minute, nowTime.second)    
            else:
                torScan.scanFinished = datetime.now().time()


            torScan.nodes = self.exitNodes
            self.database.initDatabase()
            self.tortazoExecutor.logger.debug(term.format("[+] Inserting in database the relays found and retrieving the GeoLocation references ...", term.Color.GREEN))
            self.database.insertExitNode(torScan)
        return self.exitNodes

    def shodanSearchByHost(self, shodanKey, ip):
        '''
        Search in Shodan by host. This function needs the shodanKey and the IP address of the host.
        '''
        self.tortazoExecutor.logger.debug(term.format("[+] Using Shodan against %s " %(ip), term.Color.GREEN))
        try:
            self.shodanApi = shodan.Shodan(shodanKey)
            self.results = self.shodanApi.host(ip)
            shodanHost = ShodanHost()
            shodanHost.keyInfo = self.shodanApi.info()
            shodanHost.host = ip
            self.extract(self.results, shodanHost.results)
            return shodanHost

        except shodan.APIError:
            self.tortazoExecutor.logger.error(term.format("[-] There's no information about %s in the Shodan Database." %(ip), term.Color.RED))
            pass

    def recordNmapScan(self, scan, descriptor):
        #Performs the NMap scan using python-nmap library. Returns the exitnodes with the open ports found in the scanning process.
        for host in scan.all_hosts():
            torNode = TorNodeData()
            torNode.host = host
            torNode.nickName = descriptor.nickname
            torNode.fingerprint = descriptor.fingerprint
            torNode.torVersion = descriptor.tor_version
            torNode.operatingSystem = descriptor.operating_system
            if descriptor.contact is not None:
                torNode.contactData = descriptor.contact.decode("utf-8", "replace")
            if scan[host].has_key('status'):
                torNode.state = scan[host]['status']['state']
                torNode.reason = scan[host]['status']['reason']
                for protocol in ["tcp", "udp", "icmp"]:
                    if scan[host].has_key(protocol):
                        ports = scan[host][protocol].keys()
                        for port in ports:
                            torNodePort = TorNodePort()
                            torNodePort.port = port
                            torNodePort.state = scan[host][protocol][port]['state']
                            if scan[host][protocol][port].has_key('reason'):
                                torNodePort.reason = scan[host][protocol][port]['reason']
                            if scan[host][protocol][port].has_key('name'):
                                torNodePort.name = scan[host][protocol][port]['name']
                            if scan[host][protocol][port].has_key('version'):
                                torNodePort.version = scan[host][protocol][port]['version']
                            if 'open' in (scan[host][protocol][port]['state']):
                                torNode.openPorts.append(torNodePort)
                            else:
                                torNode.closedFilteredPorts.append(torNodePort)
                        self.exitNodes.append(torNode)
            else:
                self.tortazoExecutor.logger.warn(term.format("[-] There's no match in the Nmap scan with the specified protocol %s" %(protocol), term.Color.RED))

    def extract(self, DictIn, Dictout):
        for key, value in DictIn.iteritems():
            if isinstance(value, dict): # If value itself is dictionary
                self.extract(value, Dictout)
            elif isinstance(value, list): # If value itself is list
                for i in value:
                    if type(i) == dict:
                        self.extract(i, Dictout)
                    else:
                        if value is not None and isinstance(value, str):
                            Dictout[i] = value.decode('utf-8')
                        else:
                            Dictout[i] = value

            else:
                if value is not None and isinstance(value, str):
                    Dictout[key] = value.decode('utf-8')
                else:
                    Dictout[key] = value