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

class BasePlugin():
    '''
    Every plugin in Tortazo should inher
    '''

    def __init__(self):
        '''
        Constructor for the Base plugin class.
        '''
        self.logger = log
        self.torNodes = []
        self.pluginArguments = {}
        self.logger.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)

    def info(self, message):
         self.logger.info(term.format(message, term.Color.YELLOW))

    def error(self, message):
        self.logger.warn(term.format(message, term.Color.RED))

    def debug(self, message):
        self.logger.debug(term.format(message, term.Color.GREEN))


    def setNodes(self, torNodes):
        '''
        Function used to set the Tor Nodes scanned.
        '''
        self.torNodes = torNodes

    def setPluginArguments(self, pluginArguments):
        '''
        Arguments passed from command-line to the plugin.
        '''
        self.pluginArguments = pluginArguments

    def runPlugin(self):
        pass

    def help(self):
        self.info("[*] Help for the plugin... You should overwrite this method in your own plugin class")