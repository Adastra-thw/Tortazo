# coding=utf-8
'''
Created on 14/14/2014

#Author: Adastra.
#twitter: @jdaanial

feedOnionRepositoryPlugin.py

FeedOnionRepositoryPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

FeedOnionRepositoryPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from plugins.texttable import Texttable
from core.tortazo.exceptions.PluginException import PluginException

class feedOnionRepositoryPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'feedOnionRepositoryPlugin')
        self.setPluginDetails('feedOnionRepositoryPlugin', 'Try to search for hidden services in searchers of deep web like TorCH or AhMIA. The information gathered will be validated and then inserted in the onion repository tables.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] feedOnionRepositoryPlugin Initialized!")
        self.pluginConfigs= {}


    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)


    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] feedOnionRepositoryPlugin Destroyed!")

    def torCH(self, searchWords):
        pass

    def ahmia(self, searchWords):
        pass

    def search(self, searchWords):
        pass



    def help(self):
        print "[*] Functions availaible available in the Plugin...\n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([25,20,20])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'],
                         ['torCH', 'Search the specified keyworks in TorCH.', 'self.torCH("anonymous networks")']
                         ['ahmia', 'Search the specified keyworks in AhMIA.', 'self.ahmia("anonymous networks")']
                         ['ahmia', 'Search the specified keyworks in TorCH, AhMIA, etc.', 'self.ahmia("anonymous networks")']
                        ])
        print table.draw() + "\\n"        
