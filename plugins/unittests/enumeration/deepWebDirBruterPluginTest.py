# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

deepWebDirBruterPluginTest.py

deepWebDirBruterPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

deepWebDirBruterPluginTest is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from requests.exceptions import InvalidURL
import os
from plugins.texttable import Texttable
import unittest

class deepWebDirBruterPluginTest(unittest.TestCase):

    def __init__(self):
        self.plugin = heartBleedPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        reference.setPluginArguments(self.pluginArgs)
        reference.processPluginArguments()

    def dirBruterOnRelay(self, site, dictFile='', proxy=False):
        pass

    def dirBruterOnAllRelays(self, port=80, dictFile=''):
        pass

    def dirBruterOnHiddenService(self, hiddenService, dictFile=''):
        pass
