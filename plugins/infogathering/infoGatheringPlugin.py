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
from plugins.texttable import Texttable
from core.tortazo.exceptions.PluginException import PluginException

class infoGatheringPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'infoGatheringPlugin')
        self.setPluginDetails('infoGatheringPlugin', 'Information Gathering of Tor relays.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] infoGatheringPlugin Initialized!")
        self.pluginConfigs= {}


    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)


    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] infoGatheringPlugin Destroyed!")

    def printRelaysFound(self):
        #tableRelays = PrettyTable(["Host", "State", "Reason", "NickName", "Open Ports"])
        table = Texttable()
        table.set_cols_align(["l", "l", "l", "l", "l"])
        table.set_cols_valign(["m", "m", "m","m", "m", "m"])
        table.set_cols_width([20,20,20,20,20])

        rows = [["NickName", "Host", "State", "Reason", "Open Ports"]]
        openPorts = None

        for torNode in self.torNodes:
            for port in torNode.openPorts:
                openPorts = ''
                openPorts += str(port.reason)+':'+str(port.port)

            if openPorts is None:
                rows.append([torNode.nickName,torNode.host,torNode.state,torNode.reason,'No open ports found'])
            else:
                rows.append([torNode.nickName,torNode.host,torNode.state,torNode.reason,openPorts])
            openPorts = None


    def checkOutdateRelays(self, torVersion='0.2.3.0'):
        print "Checking relays with TOR version equals or less to %s " %(torVersion)
        for torNode in self.torNodes:
            if torNode.torVersion < Version(torVersion):
                print "[*] Older version of TOR detected: %s Nickname of the Relay %s IP Address reported %s" %(torNode.torVersion,torNode.nickName,torNode.host)




    def help(self):
        print "[*] Functions availaible available in the Plugin...\n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()']
                        ])
        print table.draw() + "\\n"        
