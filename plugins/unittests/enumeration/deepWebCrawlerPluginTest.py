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
from core.tortazo.exceptions.PluginException import PluginException

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
        print "Testing setCrawlRulesLinks with args: crawlRulesLinks=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setCrawlRulesLinks, crawlRulesLinks=None)

        print "Testing setCrawlRulesLinks with args: crawlRulesLinks=%s " %(unittests.crawlerPlugin_regexInvalid)
        self.assertRaises(PluginException, self.plugin.setCrawlRulesLinks, crawlRulesLinks=unittests.crawlerPlugin_regexInvalid)
        

    def test_setCrawlRulesImages(self):
        print "Testing setCrawlRulesImages with args: crawlRulesImages=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setCrawlRulesImages, crawlRulesImages=None)

        print "Testing setCrawlRulesImages with args: crawlRulesImages=%s " %(unittests.crawlerPlugin_regexInvalid)
        self.assertRaises(PluginException, self.plugin.setCrawlRulesImages, crawlRulesImages=unittests.crawlerPlugin_regexInvalid)
        

    def test_setDictForBruter(self):
        print "Testing setDictForBruter with args: dictFile=%s " %(None)
        self.assertRaises(PluginException, self.plugin.setDictForBruter, dictFile=None)

        print "Testing setDictForBruter with args: dictFile=%s " %(unittests.crawlerPlugin_dictFileInvalid)
        self.assertRaises(PluginException, self.plugin.setDictForBruter, dictFile=unittests.crawlerPlugin_dictFileInvalid)


    def test_compareWebSiteWithHiddenWebSite(self):
        print "Testing compareWebSiteWithHiddenWebSite with args: webSite=%s , hiddenWebSite=%s" %(unittests.crawlerPlugin_urlSite, unittests.crawlerPlugin_onionserviceInvalid)
        self.assertRaises(PluginException, self.plugin.compareWebSiteWithHiddenWebSite, webSite=unittests.crawlerPlugin_urlSite, hiddenWebSite=unittests.crawlerPlugin_onionserviceInvalid)

        print "Testing compareWebSiteWithHiddenWebSite with args: webSite=%s , hiddenWebSite=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.compareWebSiteWithHiddenWebSite, webSite=None, hiddenWebSite=None)

        print "Testing compareWebSiteWithHiddenWebSite with args: webSite=%s , hiddenWebSite=%s" %(unittests.crawlerPlugin_urlSite, None)
        self.assertRaises(PluginException, self.plugin.compareWebSiteWithHiddenWebSite, webSite=unittests.crawlerPlugin_urlSite, hiddenWebSite=None)

        print "Testing compareWebSiteWithHiddenWebSite with args: webSite=%s , hiddenWebSite=%s" %(None, unittests.crawlerPlugin_onionserviceInvalid)
        self.assertRaises(PluginException, self.plugin.compareWebSiteWithHiddenWebSite, webSite=None, hiddenWebSite=unittests.crawlerPlugin_onionserviceInvalid)

    def test_compareRelaysWithHiddenWebSite(self):
        print "Testing compareRelaysWithHiddenWebSite with args: hiddenWebSite=%s" %(unittests.crawlerPlugin_onionserviceInvalid)
        self.assertRaises(PluginException, self.plugin.compareRelaysWithHiddenWebSite, hiddenWebSite=unittests.crawlerPlugin_onionserviceInvalid)

        print "Testing compareRelaysWithHiddenWebSite  with args: hiddenWebSite=%s" %(None)
        self.assertRaises(PluginException, self.plugin.compareRelaysWithHiddenWebSite, hiddenWebSite=None)


    def test_crawlOnionWebSite(self):
        print "Testing crawlOnionWebSite with args: hiddenWebSite=%s" %(unittests.crawlerPlugin_onionserviceInvalid )
        self.assertRaises(PluginException, self.plugin.crawlOnionWebSite, hiddenWebSite=unittests.crawlerPlugin_onionserviceInvalid)

        print "Testing crawlOnionWebSite  with args: hiddenWebSite=%s" %(None)
        self.assertRaises(PluginException, self.plugin.crawlOnionWebSite, hiddenWebSite=None)

        print "Testing crawlOnionWebSite with args: hiddenWebSite=%s , hiddenWebSitePort=%s " %(unittests.crawlerPlugin_onionserviceInvalid, str(unittests.crawlerPlugin_portInvalid))
        self.assertRaises(PluginException, self.plugin.crawlOnionWebSite, hiddenWebSite=unittests.crawlerPlugin_onionserviceInvalid, )

        print "Testing crawlOnionWebSite  with args: hiddenWebSite=%s , hiddenWebSitePort=%s " %(None, None)
        self.assertRaises(PluginException, self.plugin.crawlOnionWebSite, hiddenWebSite=None, hiddenWebSitePort=None)

        print "Testing crawlOnionWebSite with args: hiddenWebSite=%s , socatTcpListenPort=%s" %(unittests.crawlerPlugin_onionserviceInvalid, str(unittests.crawlerPlugin_portInvalid))
        self.assertRaises(PluginException, self.plugin.crawlOnionWebSite, hiddenWebSite=unittests.crawlerPlugin_onionserviceInvalid, socatTcpListenPort=unittests.crawlerPlugin_portInvalid)

        print "Testing crawlOnionWebSite  with args: hiddenWebSite=%s , socatTcpListenPort=%s" %(None, None)
        self.assertRaises(PluginException, self.plugin.crawlOnionWebSite, hiddenWebSite=None, socatTcpListenPort=None)

if __name__ == '__main__':
    unittest.main()
