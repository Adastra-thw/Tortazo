# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

deepWebDirBruterPlugin.py

deepWebDirBruterPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

deepWebDirBruterPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from prettytable import PrettyTable
import os
import difflib
import signal
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from plugins.enumeration.utils.hiddenSiteSpider import HiddenSiteSpider
from twisted.internet import reactor
from time import sleep
import socket
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import config
import  sys

class deepWebDirBruterPlugin(BasePlugin):  

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'deepWebDirBruterPlugin')
        self.setPluginDetails('deepWebDirBruterPlugin', 'Find directories in the specified onion url.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] deepWebDirBruterPlugin Initialized!")

    def __del__(self):
        if len(self.torNodes) > 0:
            self.debug("[*] deepWebDirBruterPlugin Destroyed!")

    def findDirsInHiddenSite(self, onionSite, dictFile=''):
        print "[+] Starting DirBruter plugin against %s ... This could take some time. Be patient."
