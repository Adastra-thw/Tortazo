'''
Created on 20/06/2014

#Author: Adastra.
#twitter: @jdaanial

deepWebCrawlerPluginTest.py

deepWebCrawlerPluginTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

deepWebCrawlerPluginTest is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from plugins.texttable import Texttable
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
import urllib
import  sys
import unittest

class deepWebCrawlerPluginTest(unittest.TestCase):

    def __init__(self):
        self.plugin = heartBleedPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        reference.setPluginArguments(self.pluginArgs)
        reference.processPluginArguments()

    def setExtractorRulesAllow(self, extractorRulesAllow):
        pass
    
    def setExtractorRulesDeny(self, extractorRulesDeny):
        pass

    def setCrawlRulesLinks(self, crawlRulesLinks):
        pass

    def setCrawlRulesImages(self, crawlRulesImages):
        pass

    def setDictForBruter(self, dictFile):
        pass

    def compareWebSiteWithHiddenWebSite(self, webSite, hiddenWebSite):
        pass

    def compareRelaysWithHiddenWebSite(self, hiddenWebSite):
        pass

    def crawlOnionWebSite(self, hiddenWebSite, hiddenWebSitePort=80,
                         socatTcpListenPort=8765,
                         crawlImages=False, crawlLinks=True,
                         crawlContents=True, crawlFormData=False,
                         useRandomUserAgents=True, deepLinks=None,
                         bruterOnProtectedResource=False):
        pass
