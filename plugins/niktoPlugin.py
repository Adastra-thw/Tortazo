# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

niktoPlugin.py

niktoPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

niktoPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from prettytable import PrettyTable
import subprocess

class niktoPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes):
        BasePlugin.__init__(self, torNodes, 'niktoPrinter')
        self.info("[*] NiktoPlugin Initialized!")

    def __del__(self):
        self.debug("[*] NiktoPlugin Destroyed!")

    def executeAll(self, switches):
        for torNode in self.torNodes:
            for torNodePort in torNode.openPorts:
                if torNodePort.port == '80':
                    subprocess.call("nikto.pl -H "+torNode.host+" "+ switches, shell=True)

    def executeAllOnPort(self, port, switches):
        for torNode in self.torNodes:
            for torNodePort in torNode.openPorts:
                if torNodePort.port == port:
                    subprocess.call("nikto.pl -H "+torNode.host+" "+ switches, shell=True)

    def executeByNickname(self, nickname, switches):
        for torNode in self.torNodes:
            for torNodePort in torNode.openPorts:
                if torNodePort.port == '80' and torNode.nickName == nickname:
                    subprocess.call("nikto.pl -H "+torNode.host+" "+ switches, shell=True)

    def executeByIP(self, ipAddress, switches):
        for torNode in self.torNodes:
            for torNodePort in torNode.openPorts:
                if torNodePort.port == '80' and torNode.host == ipAddress:
                    subprocess.call("nikto.pl -H "+torNode.host+" "+ switches, shell=True)

    def executeByIPOnPort(self, ipAddress, port, switches):
        for torNode in self.torNodes:
            for torNodePort in torNode.openPorts:
                if torNodePort.port == port and torNode.host == ipAddress:
                    subprocess.call("nikto.pl -H "+torNode.host+" "+ switches, shell=True)

    def help(self):
        print "[*] Functions availaible available in the Plugin..."
        tableHelp = PrettyTable(["Function", "Description", "Example"])
        tableHelp.padding_width = 1
        tableHelp.add_row(['help', 'Help Banner', 'self.help()'])
        tableHelp.add_row(['executeAll', 'Execute Nikto against all TOR relays found (by default, against port 80)', 'self.executeAll("nikto_switches")'])
        tableHelp.add_row(['executeAllOnPort', 'Execute Nikto against all TOR relays found on the specified port.', 'self.executeAllOnPort(8080, "nikto_switches")'])
        tableHelp.add_row(['executeByNickname', 'Execute Nikto against the relay specified by NickName (by default, against port 80)', "self.executeByNickname('TorNodeNickName','nikto_switches')"])
        tableHelp.add_row(['executeByIP', 'Execute Nikto against the relay specified by Ip Address (by default, against port 80)', "self.executeByIP('80.80.80.80','nikto_switches')"])
        tableHelp.add_row(['executeByIPOnPort', 'Execute Nikto against the relay specified by Ip Address on the specified port', "self.executeByIPOnPort('80.80.80.80', 8080, 'nikto_switches')"])
        print tableHelp
