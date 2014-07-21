# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

deepWebCrawlerPlugin.py

deepWebCrawlerPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

deepWebCrawlerPlugin is distributed in the hope that it will be useful,
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

class deepWebCrawlerPlugin(BasePlugin):

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'deepWebCrawlerPlugin')
        self.setPluginDetails('deepWebFinderPlugin', 'Basic crawling tasks against web sites in the TOR network', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] deepWebFinderPlugin Initialized!")
        self.extractorRules=[r'^/*']
        self.crawlRulesLinks = '//a/@href'
        self.crawlRulesImages = '//img/@src'

    def __del__(self):
        if len(self.torNodes) > 0:
            self.debug("[*] DeepWebPlugin Destroyed!")

    def setExtractorRules(self, extractorRules):
        self.extractorRules = extractorRules

    def setCrawlRulesLinks(self, crawlRulesLinks):
        self.crawlRulesLinks = crawlRulesLinks

    def setCrawlRulesImages(self, crawlRulesImages):
        self.crawlRulesImages = crawlRulesImages

    def compareWebSiteWithHiddenWebSite(self, webSite, hiddenWebSite):
        #CHECK THIS: https://docs.python.org/2/library/difflib.html#module-difflib
        responseHidden = self.serviceConnector.performHTTPConnectionHiddenService(hiddenWebSite,method="GET")
        if responseHidden.status_code == 200:
            responseRelay = self.serviceConnector.performHTTPConnection('http://'+webSite, method="GET")
            if responseRelay.status_code == 200:
                print "[+] Executing the matcher tool against the responses."
                ratio = difflib.SequenceMatcher(None,responseHidden.content,responseRelay.content).ratio()
                print "[+] Match ration between the web sites: %s " %(str(ratio))
            else:
                print "[-] The website returned an non HTTP 200 code. %s " %(str(responseRelay.status_code))
        else:
            print "[-] The Hidden website returned an non HTTP 200 code. %s " %(str(responseHidden.status_code))


    def compareRelaysWithHiddenWebSite(self, hiddenWebSite):
        #CHECK THIS: https://docs.python.org/2/library/difflib.html#module-difflib
        responseHidden = self.serviceConnector.performHTTPConnectionHiddenService(hiddenWebSite,method="GET")
        for node in self.torNodes:
            if responseHidden.status_code == 200:
                responseRelay = self.serviceConnector.performHTTPConnection('http://'+node.host, method="GET")
                if responseRelay.status_code == 200:
                    ratio = difflib.SequenceMatcher(None,responseHidden.content,responseRelay.content).ratio()
                    print str(ratio)
    
    def crawlImagesHiddenWebSite(self, hiddenWebSite, outputDir='./', storeBD=False):
        from bs4 import BeautifulSoup
        from PIL import Image
        from StringIO import StringIO

        response = self.serviceConnector.performHTTPConnectionHiddenService(hiddenWebSite)
        rootSite = BeautifulSoup(response.content)
        images = rootSite.find_all("img")
        for image in images:
            responseImage = self.onionHttpGetRequest(images.src)
            i = Image.open(StringIO(responseImage.content))


    def crawOnionWebSite(self, hiddenWebSite, hiddenWebSitePort=80,
                         socatTcpListenPort=8765,
                         crawlImages=True, crawlLinks=True,
                         crawlContents=True, crawlFormData=True):
        onionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        onionSocket.settimeout(1)
        result = onionSocket.connect_ex(('127.0.0.1',socatTcpListenPort))
        if result == 0:
            print "[-] The selected local port "+str(socatTcpListenPort)+" is being used by another process. Please, select an port available in this machine"
            return

        if hiddenWebSite.startswith('http://'):
            onionSite = hiddenWebSite.replace('http://', "")
        else:
            onionSite = hiddenWebSite

        extraPath = onionSite[onionSite.find('.onion') + 6:]
        #Extracts the Onion Site, everything before ".onion"
        onionSite = onionSite[:onionSite.find('.onion') + 6]

        try:
            print "[+] Starting a local proxy with Socat to forward requests to the hidden service through the local machine and the local Socks Proxy... "
            socatProcess = self.serviceConnector.startLocalSocatTunnel(socatTcpListenPort, onionSite,hiddenWebSitePort, socksPort=self.serviceConnector.socksPort)
            sleep(5)
            print "[+] Socat process started! PID: "+str(socatProcess.pid)
            self.__crawl(hiddenWebSite, socatTcpListenPort,extraPath, crawlImages=True, crawlLinks=True,crawlContents=True, crawlFormData=True,)
            os.killpg(socatProcess.pid, signal.SIGTERM)
            print "[+] Socat process killed."
        except:
            print "[+] The following exception was raised, however, shutting down the local Socat tunnel..."
            print sys.exc_info()
            os.killpg(socatProcess.pid, signal.SIGTERM)
            sleep(5)


    def __crawl(self, hiddenWebSite, localPort, extraPath='', crawlImages=True, crawlLinks=True,crawlContents=True, crawlFormData=True):
        def catch_item(sender, item, **kwargs):
            item['url'] = item['url'].replace('http://127.0.0.1:'+str(localPort)+extraPath, hiddenWebSite)
            print "[+]Processing URL %s ...  " %(item['url'])
            from core.tortazo.databaseManagement.TortazoDatabase import TortazoDatabase
            database = TortazoDatabase()
            database.initDatabaseDeepWebCrawlerPlugin()
            self.__processPage(item, database)

        # setup crawler
        dispatcher.connect(catch_item, signal=signals.item_passed)
        dispatcher.connect(reactor.stop, signal=signals.spider_closed)

        settings = get_project_settings()
        settings.set('ITEM_PIPELINES', {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}, priority='cmdline')
        settings.set('IMAGES_STORE', config.deepWebCrawlerOutdir+hiddenWebSite)

        crawler = Crawler(settings)
        crawler.configure()
        spider = HiddenSiteSpider("http://127.0.0.1:"+str(localPort)+extraPath, hiddenWebSite, self.extractorRules)
        spider.setImages(crawlImages)
        spider.setLinks(crawlLinks)
        spider.setContents(crawlContents)
        spider.setForms(crawlFormData)

        crawler.crawl(spider)
        print "\n[+] Starting scrapy engine... this process could take some time, depending on the crawling and extractor rules applied... \n"
        crawler.start()
        reactor.run()
        print "[+] Crawler finished."

    def __processPage(self, page, db):
        #Search the page in database. Maybe is already registered.
        if page.has_key('url'):
            exists = db.existsPageByUrl(page['url'])
            if exists == False:
                #The page was not found in database. Let's insert it.
                pageId = db.insertPage(page)
            else:
                #The page already exists in database. Let's get the primary key.
                pageId = db.searchPageByUrl(page['url'])

            if pageId is not None:
                db.insertImages(page, pageId)
                db.insertForms(page, pageId)
            else:
                print "[-] Seems that an error occurred while inserting or querying the page %s in database. Images and forms not saved." %(page['url'])

        
    def findGeoLocationByIP(self):
        pass


    def help(self):
        print "[*] Functions availaible available in the Plugin..."
        tableHelp = PrettyTable(["Function", "Description", "Example"])
        tableHelp.padding_width = 1
        tableHelp.add_row(['help', 'Help Banner', 'self.help()'])
        tableHelp.add_row(['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'])
        tableHelp.add_row(['compareRelaysWithHiddenWebSite', ''])
        tableHelp.add_row(['crawlImagesHiddenWebSite', ''])
        tableHelp.add_row(['crawlLinksHiddenWebSite', ''])
        tableHelp.add_row(['crawlContentsHiddenWebSite', ''])
        tableHelp.add_row(['findGeoLocationByIP', ''])
        print tableHelp
