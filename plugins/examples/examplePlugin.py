# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

examplePlugin.py

examplePlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

examplePlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from plugins.texttable import Texttable


class examplePlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'examplePlugin')
        self.setPluginDetails('examplePlugin', 'Example of a plugin in Tortazo.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] examplePlugin Initialized!")
        self.validPluginArgs= []

    def processPluginArguments(self):
        pass


    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] examplePlugin Destroyed!")

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
