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

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import os
import  sys
import unittest
from plugins.enumeration.deepWebCrawlerPlugin import deepWebCrawlerPlugin
from config import unittests
from config import config

class deepWebCrawlerPluginTest(unittest.TestCase):

    def setUp(self):
        self.plugin = deepWebCrawlerPlugin()
        self.pluginArgs = []
        
        self.plugin.serviceConnector.setSocksProxySettings(config.socksHost, config.socksPort)
        self.plugin.setPluginArguments(self.pluginArgs)
        self.plugin.processPluginArguments()

    def test_setExtractorRulesAllow(self):
        print "Testing setExtractorRulesAllow with args: extractorRulesAllow=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setExtractorRulesAllow, extractorRulesAllow=None)

        print "Testing setExtractorRulesAllow with args: extractorRulesAllow=%s " %(unittests.crawlerPlugin_regexInvalid)
        self.assertRaises(PluginException, self.plugin.setExtractorRulesAllow, extractorRulesAllow=unittests.crawlerPlugin_regexInvalid)

        
    
    def test_setExtractorRulesDeny(self):
        print "Testing setExtractorRulesDeny with args: extractorRulesDeny=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setExtractorRulesDeny, extractorRulesDeny=None)

        print "Testing setExtractorRulesDeny with args: extractorRulesDeny=%s " %(unittests.crawlerPlugin_regexInvalid)
        self.assertRaises(PluginException, self.plugin.setExtractorRulesDeny, extractorRulesDeny=unittests.crawlerPlugin_regexInvalid)


    def test_setCrawlRulesLinks(self):
        print "Testing setCrawlRulesLinks with args: extractorRulesDeny=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setCrawlRulesLinks, crawlRulesLinks=None)

        print "Testing setCrawlRulesLinks with args: extractorRulesDeny=%s " %(unittests.crawlerPlugin_regexInvalid)
        self.assertRaises(PluginException, self.plugin.setCrawlRulesLinks, crawlRulesLinks=unittests.crawlerPlugin_regexInvalid)
        

    def test_setCrawlRulesImages(self):
        print "Testing setCrawlRulesImages with args: crawlRulesImages=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setCrawlRulesLinks, crawlRulesImages=None)

        print "Testing setCrawlRulesImages with args: crawlRulesImages=%s " %(unittests.crawlerPlugin_regexInvalid)
        self.assertRaises(PluginException, self.plugin.setCrawlRulesLinks, crawlRulesImages=unittests.crawlerPlugin_regexInvalid)
        

    def test_setDictForBruter(self, dictFile):
        print "Testing setDictForBruter with args: dictFile=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setDictForBruter, dictFile=None)

        print "Testing setDictForBruter with args: dictFile=%s " %(unittests.crawlerPlugin_dictFileInvalid)
        self.assertRaises(PluginException, self.plugin.setDictForBruter, dictFile=unittests.crawlerPlugin_dictFileInvalid)


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

if __name__ == '__main__':
    unittest.main()
