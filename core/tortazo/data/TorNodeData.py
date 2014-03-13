# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

BotMachine.py

BotMachine is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

BotMachine is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

class TorNodeData:
    '''
    Tor Structure to save the Node information.
    '''
    def __init__(self):
        self.host = None
        self.state = None
        self.reason = None
        self.openPorts = [] #List of TorNodePort objects
        self.closedFilteredPorts = [] #List of TorNodePort objects
        self.nickName = None

class TorNodePort:
    '''
    Information about the scanned port.
    '''
    def __init__(self):
        self.state = None
        self.reason = None
        self.port = None
        self.name = None
        self.version = None