# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

infoGatheringPlugin.py

infoGatheringPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

infoGatheringPlugin is distributed in the hope that it will be useful,
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

class infoGatheringPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'infoGatheringPlugin')
        self.setPluginDetails('infoGatheringPlugin', 'Information Gathering of Tor relays.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] infoGatheringPlugin Initialized!")


    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] infoGatheringPlugin Destroyed!")

    def printRelaysFound(self):
        #tableRelays = PrettyTable(["Host", "State", "Reason", "NickName", "Open Ports"])
        tableRelays = PrettyTable(["NickName", "Host", "State", "Reason", "Open Ports"])
        tableRelays.padding_width = 1
        openPorts = None

        for torNode in self.torNodes:
            for port in torNode.openPorts:
                openPorts = ''
                openPorts += str(port.reason)+':'+str(port.port)

            if openPorts is None:
                tableRelays.add_row([torNode.nickName,torNode.host,torNode.state,torNode.reason,'No open ports found'])
            else:
                tableRelays.add_row([torNode.nickName,torNode.host,torNode.state,torNode.reason,openPorts])
            openPorts = None
        print tableRelays.get_string(sortby='NickName')

    def checkOutdateRelays(self, torVersion='0.2.3.0'):
        print "Checking relays with TOR version equals or less to %s " %(torVersion)
        for torNode in self.torNodes:
            if torNode.torVersion < Version('0.2.3.0'):
                print "[*] Older version of TOR detected: %s Nickname of the Relay %s IP Address reported %s" %(torNode.torVersion,torNode.nickName,torNode.host)




    def help(self):
        print "[*] Functions availaible available in the Plugin..."
        tableHelp = PrettyTable(["Function", "Description", "Example"])
        tableHelp.padding_width = 1
        tableHelp.padding_width = 1
        tableHelp.add_row(['help', 'Help Banner', 'self.help()'])
        tableHelp.add_row(['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'])
        print tableHelp