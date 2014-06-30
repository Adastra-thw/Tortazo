# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

deepWebStemmingPlugin.py

deepWebStemmingPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

deepWebStemmingPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from prettytable import PrettyTable
import requests


class deepWebFinderPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'deepWebFinderPlugin')
        self.setPluginDetails('deepWebFinderPlugin', 'Basic pentesting tasks against hidden services in the TOR network', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.setSocksProxy()
            self.info("[*] deepWebFinderPlugin Initialized!")

    def __del__(self):
        if len(self.torNodes) > 0:
            self.debug("[*] DeepWebPlugin Destroyed!")

    def compareAllRelaysWithHiddenService(self, hiddenWebSite):
        for node in self.torNodes:
            requestHidden = requests.get(hiddenWebSite)
            requestRelay = requests.get(node.host)





    def help(self):
        print "[*] Functions availaible available in the Plugin..."
        tableHelp = PrettyTable(["Function", "Description", "Example"])
        tableHelp.padding_width = 1
        tableHelp.add_row(['help', 'Help Banner', 'self.help()'])
        tableHelp.add_row(['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'])
        tableHelp.add_row(['compareRelayWithHiddenWebSite', 'Execute Nikto against all TOR relays found (by default, against port 80)', 'self.executeAll("nikto_switches")'])
        print tableHelp