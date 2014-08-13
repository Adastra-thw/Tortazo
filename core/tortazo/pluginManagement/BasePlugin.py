# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

BasePlugin.py

BasePlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

BasePlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import logging as log

from stem.util import term
from IPython.config.loader import Config
from IPython.terminal.embed import InteractiveShellEmbed

from core.tortazo.pluginManagement.utils.FuzzDBReader import FuzzDBReader
from core.tortazo.databaseManagement.TortazoDatabase import TortazoDatabase
from core.tortazo.utils.ServiceConnector import ServiceConnector
from plugins.texttable import Texttable
from distutils.util import strtobool
import sys

class BasePlugin():
    '''
    Every plugin in Tortazo should inher
    '''

    def __init__(self, torNodes, pluginLoaded):
        '''
        Constructor for the Base plugin class.
        '''
        self.db = TortazoDatabase()
        self.logger = log
        self.torNodes = []
        self.pluginArguments = {}
        self.logger.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        self.torNodes = torNodes
        self.pluginLoaded = pluginLoaded
        self.name = None
        self.desc = None
        self.version = None
        self.author = None
        self.cli = None
        self.serviceConnector = ServiceConnector(self.cli)
        self.fuzzDBReader = FuzzDBReader()
        self.numberOnionSitesRegistered = self.db.countOnionRepositoryResponses()


    def info(self, message):
         self.logger.info(term.format(message, term.Color.YELLOW))

    def error(self, message):
        self.logger.warn(term.format(message, term.Color.RED))

    def debug(self, message):
        self.logger.debug(term.format(message, term.Color.GREEN))

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


    def printOnionRepository(self, start=1, maxResults=30):
        #Start-1. Indexes in database starts from 0.
        start = start-1
        onionAddresses = self.db.searchOnionRepository(start,maxResults)
        table = Texttable()
        table.set_cols_align(["l", "l", "l", "l" , "l", "l"])
        table.set_cols_valign(["m", "m", "m", "m", "m", "m"])
        table.set_cols_width([5,35,55,15,15, 55])
        rows = [ ["#", "Onion Adress", "Description", "Service Type", "Response", "Headers"], ]
        for rowid, address in enumerate(onionAddresses):
            (onionAddress, responseCode, responseHeaders, onionDescription, serviceType) = address
            rows.append( [rowid, onionAddress, onionDescription, serviceType, responseCode, responseHeaders] )
        table.add_rows(rows)
        print table.draw() + "\n"

        if start+maxResults <=  self.numberOnionSitesRegistered:
            sys.stdout.write('%s [y/n]\n' %('Print more onion addresses?'))
            while True:
                try:
                    input = raw_input
                    if strtobool(input().lower()) == True:
                        break
                    else:
                        return
                except NameError:
                    pass
                except ValueError:
                    sys.stdout.write('Please respond with \'y\' or \'n\'.\n')
            self.printOnionRepository(start+maxResults, maxResults)






    def runPlugin(self):
        '''
        Runs the plugin.
        '''
        try:
            get_ipython
        except NameError:
            nested = 0
            cfg = Config()
            prompt_config = cfg.PromptManager
            prompt_config.in_template = 'Tortazo Plugin <%s> : ' %(self.pluginLoaded)
            prompt_config.in2_template = "Type 'self.help()' to get information about the functions available in this plugin :"
        else:
            cfg = Config()
            nested = 1
        self.tortazoShell = InteractiveShellEmbed(config=cfg, banner1 = 'Loading Tortazo plugin interpreter... ', banner2="Plugin %s loaded successfully! Type self.help() to get information about this plugin and exit() to finish the execution. "%(self.pluginLoaded), exit_msg = 'Leaving Tortazo plugin interpreter.')
        self.tortazoShell()

    def setPluginDetails(self,name,desc,version,author):
        self.name = name
        self.desc = desc
        self.version = version
        self.author = author

    def setPluginArguments(self, pluginArguments):
        self.pluginArguments = pluginArguments

    def processPluginArguments(self):
        for validConfig in self.pluginConfigs.keys():
            if validConfig in self.pluginArguments:
                self.pluginConfigs[validConfig] = self.pluginArguments[validConfig]
    def help(self):
        pass