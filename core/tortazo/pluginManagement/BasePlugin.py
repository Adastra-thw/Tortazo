# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

WorkerThread.py

WorkerThread is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

WorkerThread is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

class BasePlugin():
    '''
    Every plugin in Tortazo should inher
    '''

    def __init__(self):
        '''
        Constructor for the Base plugin class.
        '''
        self.torNodes = []
        self.pluginArguments = {}

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