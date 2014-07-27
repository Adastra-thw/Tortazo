# coding=utf-8
'''
Created on 22/01/2013
@author: Adastra
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

class BotMachine:
    '''
    Bot Structure.
    '''
    def __init__(self, hostId, user, password, host, nickname, port):
        '''
            Settings to perform the SSH Connection with a remote host.
        '''
        self.nickname = nickname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.hostId = hostId
        self.results = {}
