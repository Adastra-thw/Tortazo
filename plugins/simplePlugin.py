# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

simplePlugin.py

simplePlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

simplePlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from IPython.config.loader import Config
from IPython.terminal.embed import InteractiveShellEmbed

class simplePrinter(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self):
        BasePlugin.__init__(self)

    def __del__(self):
        pass

    def runPlugin(self):
        '''
        The most simplest plugin! Just prints the tor data structure.
        '''
        try:
            get_ipython
        except NameError:
            nested = 0
            cfg = Config()
            prompt_config = cfg.PromptManager
            prompt_config.in_template = 'Tortazo Plugin <\\#>: '
            prompt_config.in2_template = '   .\\D.: '
            prompt_config.out_template = '<\\#>: '
        else:
            cfg = Config()
            nested = 1
        tortazoShell = InteractiveShellEmbed(config=cfg,banner1 = 'Loading Tortazo plugin interpreter...',banner2="simplePlugin Help:", exit_msg = 'Leaving Tortazo plugin interpreter.')
        tortazoShell()

    def printRelaysFound(self):
        for torNode in self.torNodes:
            print "=========================="
            print "Host: %s " %(torNode.host)
            print "State: %s " %(torNode.state)
            print "Host: %s " %(torNode.reason)
            print "Host: %s " %(torNode.nickName)
            for port in torNode.openPorts:
                print "Open Port!"
                print "     State: %s " %(port.state)
                print "     Reason: %s " %(port.reason)
                print "     Port: %s " %(port.port)
                print "     Name: %s " %(port.name)
                print "     Version: %s " %(port.version)
            for port in torNode.closedFilteredPorts:
                print "Closed|Filtered Port!"
                print "     State: %s " %(port.state)
                print "     Reason: %s " %(port.reason)
                print "     Port: %s " %(port.port)
                print "     Name: %s " %(port.name)
                print "     Version: %s " %(port.version)
            print "=========================="
            print "\n"
