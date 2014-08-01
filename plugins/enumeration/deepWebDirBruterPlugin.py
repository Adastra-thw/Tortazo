# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

deepWebDirBruterPlugin.py

deepWebDirBruterPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

deepWebDirBruterPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from requests.exceptions import InvalidURL
import os
from plugins.texttable import Texttable

class deepWebDirBruterPlugin(BasePlugin):

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'deepWebDirBruterPlugin')
        self.setPluginDetails('deepWebDirBruterPlugin', 'Find directories in the specified onion url.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] deepWebDirBruterPlugin Initialized!")
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
            self.debug("[*] deepWebDirBruterPlugin Destroyed!")



        print "[+] Starting DirBruter plugin against %s ... This could take some time. Be patient."

    def dirBruterOnRelay(self, site, dictFile='', proxy=False):
        print "\n[+] Trying to find directories in the webserver %s " %(site)
        print "[+] Verifying if the path %s is reachable ... " %(site)
        try:
            if proxy:
                initialResponse = self.serviceConnector.performHTTPConnectionHiddenService(site)
            else:
                initialResponse = self.serviceConnector.performHTTPConnection(site)

            if initialResponse.status_code in range(400, 499) or initialResponse.status_code in range(500, 599):
                print "[-] The web server responded with an HTTP error Code ... HTTP %s " %(str(initialResponse.status_code))
            else:
                if dictFile == '':
                    print "[+] No specified 'dictFile'. Using FuzzDB Project to execute the attack."
                    print "[+] Starting the attack using the FuzzDB Files ... This could take some time."
                    dirList = self.fuzzDBReader.getDirListFromFuzzDB()
                    for dir in dirList:
                        try:
                            resource = dir.replace('//','/')
                            if proxy:
                                response= self.serviceConnector.performHTTPConnectionHiddenService(site+resource)
                            else:
                                response= self.serviceConnector.performHTTPConnection(site+resource)

                            if response.status_code in range(200,299):
                                    print "[+] Resource found!  %s  in %s" %(dir, site+resource)
                        except InvalidURL:
                            continue

                else:
                    print "[+] Using the 'dictFile' stored in %s. Verifing the file. " %(dictFile,self.separator)
                    if os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
                        print "[-] The dictFile selected doesn't exists or is a directory."
                        return
                    else:
                        print "Executing the dictionary attack. Be patient."
                        for resource in open(dictFile, "r").readlines():
                            try:
                                if proxy:
                                    response= self.serviceConnector.performHTTPConnectionHiddenService(site+resource)
                                else:
                                    response= self.serviceConnector.performHTTPConnection(site+resource)
                                if response.status_code in range(200,299):
                                    print "[+] Resource found!  %s  in %s" %(dir, site+resource)
                            except InvalidURL:
                                continue
        except ConnectionError:
            print "[-] Seems that the webserver in path %s is not reachable. Aborting the attack..." %(site)
        except Timeout:
            print "[-] Seems that the webserver in path %s is not reachable. Aborting the attack..." %(site)




    def dirBruterOnAllRelays(self, port=80, dictFile=''):
        for relay in self.bruteForceData:
            self.dirBruterOnRelay("http://"+relay, proxy=False)

    def dirBruterOnHiddenService(self, hiddenService, dictFile=''):
        self.dirBruterOnRelay(hiddenService, dictFile=dictFile, proxy=True)


    def help(self):
        print "[*] Functions availaible available in the Plugin...\n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ["dirBruterOnRelay", 'Try to discover web resources in the relay specified. If the dictionary is not specified, Tortazo will use FuzzDB.', "self.dirBruterOnRelay('89.34.51.116', dictFile='/home/user/dictFile.txt')"],
                         ['dirBruterOnAllRelays', 'Try to discover web resources in the relays stored in database. If the dictionary is not specified, Tortazo will use FuzzDB.', "self.dirBruterOnAllRelays(port=8080,dictFile='/home/user/dictFile.txt')"],
                         ['dirBruterOnHiddenService', 'Try to discover web resources in the specified hidden service. If the dictionary is not specified, Tortazo will use FuzzDB.', 'self.dirBruterOnHiddenService("http://awjrc4y7j9po3ke3.onion")']
                        ])
        print table.draw() + "\\n"
