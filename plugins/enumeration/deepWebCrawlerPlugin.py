'''
Created on 20/06/2014

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
from core.tortazo.exceptions.PluginException import PluginException
from plugins.utils.validations.Validator import *

class deepWebCrawlerPlugin(BasePlugin):

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'deepWebCrawlerPlugin')
        self.setPluginDetails('deepWebFinderPlugin', 'Basic crawling tasks against web sites in the TOR network', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] deepWebFinderPlugin Initialized!")
        self.extractorRulesAllow=[r'^/*']
        self.extractorRulesDeny=['']
        self.crawlRulesLinks = '//a/@href'
        self.crawlRulesImages = '//img/@src'
        self.dictFile = None
        self.pluginConfigs= {}


    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)


    def __del__(self):
        if len(self.torNodes) > 0:
            self.debug("[*] DeepWebPlugin Destroyed!")

    def setExtractorRulesAllow(self, extractorRulesAllow):
        if is_valid_regex(extractorRulesAllow) == False:
            print '[-] The regular expresion specified is invalid. %s ' %(extractorRulesAllow)
            raise PluginException(message='The regular expresion specified is invalid. %s ' %(extractorRulesAllow),
                                  trace="deepWebCrawlerPlugin with args setExtractorRulesAllow=%s " %(str(extractorRulesAllow)),
                                  plugin="crawler", method="setExtractorRulesAllow")
        
        print "[+] Setting allow rules ... %s " %(extractorRulesAllow)
        self.extractorRulesAllow = extractorRulesAllow

    def setExtractorRulesDeny(self, extractorRulesDeny):
        if is_valid_regex(extractorRulesDeny) == False:
            print '[-] The regular expresion specified is invalid. %s ' %(extractorRulesDeny)
            raise PluginException(message='The regular expresion specified is invalid. %s ' %(extractorRulesDeny),
                                  trace="deepWebCrawlerPlugin with args extractorRulesDeny=%s " %(str(extractorRulesDeny)),
                                  plugin="crawler", method="setExtractorRulesDeny")
        
        print "[+] Setting deny rules ... %s " %(extractorRulesDeny)
        self.extractorRulesDeny = extractorRulesDeny

    def setCrawlRulesLinks(self, crawlRulesLinks):
        if is_valid_regex(crawlRulesLinks) == False:
            print '[-] The regular expresion specified is invalid. %s ' %(crawlRulesLinks)
            raise PluginException(message='The regular expresion specified is invalid. %s ' %(crawlRulesLinks),
                                  trace="deepWebCrawlerPlugin with args crawlRulesLinks=%s " %(str(crawlRulesLinks)),
                                  plugin="crawler", method="setCrawlRulesLinks")
        
        print "[+] Setting rules for the links extractor... %s " %(crawlRulesLinks)
        self.crawlRulesLinks = crawlRulesLinks

    def setCrawlRulesImages(self, crawlRulesImages):
        if is_valid_regex(crawlRulesImages) == False:
            print '[-] The regular expresion specified is invalid. %s ' %(crawlRulesImages)
            raise PluginException(message='The regular expresion specified is invalid. %s ' %(crawlRulesImages),
                                  trace="deepWebCrawlerPlugin with args crawlRulesImages=%s " %(str(crawlRulesImages)),
                                  plugin="crawler", method="setCrawlRulesImages")
        
        print "[+] Setting rules for the images extractor... %s " %(crawlRulesImages)
        self.crawlRulesImages = crawlRulesImages

    def setDictForBruter(self, dictFile):
        if dictFile == None or os.path.exists(dictFile) == False or os.path.isfile(dictFile) == False:
            print "[-] The file selected doesn't exists or is a directory."
            raise PluginException(message='The regular expresion specified is invalid. %s ' %(dictFile),
                                  trace="deepWebCrawlerPlugin with args dictFile=%s " %(str(dictFile)),
                                  plugin="crawler", method="setDictForBruter")
            
            
        print "[+] Setting Dictionary File ... %s " %(dictFile)
        self.dictFile = dictFile

    def compareWebSiteWithHiddenWebSite(self, webSite, hiddenWebSite):

        if webSite == '' or webSite is None:
            print "[-] The URL specified is invalid. %s " %(webSite)
            raise PluginException(message="The URL specified is invalid. %s " %(webSite),
                                  trace="compareWebSiteWithHiddenWebSite with args webSite=%s, hiddenWebSite=%s" %(webSite, hiddenWebSite),
                                  plugin="crawler", method="compareWebSiteWithHiddenWebSite")

        if hiddenWebSite == '' or hiddenWebSite is None:
            print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite)
            raise PluginException(message="Invalid Onion Adress %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite),
                                  trace="compareWebSiteWithHiddenWebSite with args webSite=%s, hiddenWebSite=%s" %(webSite, hiddenWebSite),
                                  plugin="crawler",
                                  method="compareWebSiteWithHiddenWebSite")

        if hiddenWebSite.startswith('http://') == False:
            hiddenWebSite = "http://"+hiddenWebSite
        if webSite.startswith('http://') == False:
            webSite = "http://"+webSite

        if is_valid_onion_address(hiddenWebSite) == False:
            print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite)
            raise PluginException(message="Invalid Onion Adress %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite),
                                  trace="compareWebSiteWithHiddenWebSite with args webSite=%s, hiddenWebSite=%s" %(webSite, hiddenWebSite),
                                  plugin="crawler",
                                  method="compareWebSiteWithHiddenWebSite")



        if is_valid_url(webSite) == False:
            print "[-] The URL specified is invalid. %s " %(webSite)
            raise PluginException(message="The URL specified is invalid. %s " %(webSite),
                                  trace="compareWebSiteWithHiddenWebSite with args webSite=%s, hiddenWebSite=%s" %(webSite, hiddenWebSite),
                                  plugin="crawler", method="compareWebSiteWithHiddenWebSite")

        try:
            responseHidden = self.serviceConnector.performHTTPConnectionHiddenService(hiddenWebSite,method="GET")
        except Exception as exc:
            print "[-] Exception connecting to the hidden service. Is the hidden service up and running? "+str(exc.message)
            return

        ratio = 0

        if responseHidden.status_code == 200:
            try:
                responseRelay = self.serviceConnector.performHTTPConnection(webSite, method="GET")
                if responseRelay.status_code == 200:
                    print "[+] Executing the matcher tool against the responses."
                    ratio = difflib.SequenceMatcher(None,responseHidden.content,responseRelay.content).ratio()
                    print "[+] Match ration between the web sites: %s " %(str(ratio))
                else:
                    print "[-] The website returned an non HTTP 200 code. %s " %(str(responseRelay.status_code))
            except Exception as exc:
                print "[-] Exception connecting to the web service. Is the web service up and running? "+str(exc.message)
                return

        else:
            print "[-] The Hidden website returned an non HTTP 200 code. %s " %(str(responseHidden.status_code))

        print "[+] The percentage of equivalence between the contents of web sites found in the relays and hidden services are: \n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])

        elements = [ ["Hidden Service", "WebSite", "Percentage"] ]
        elements.append( [ hiddenWebSite, webSite, str(ratio)  ] )
        table.add_rows( elements )
        print table.draw() + "\n"


    def compareRelaysWithHiddenWebSite(self, hiddenWebSite):
        if hiddenWebSite == '' or hiddenWebSite is None:
            print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite)
            raise PluginException(message="Invalid Onion Adress %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite),
                                  trace="compareRelaysWithHiddenWebSite with args hiddenWebSite=%s" %(hiddenWebSite),
                                  plugin="crawler",
                                  method="compareRelaysWithHiddenWebSite")

        if hiddenWebSite.startswith('http://') == False:
            hiddenWebSite = "http://"+hiddenWebSite

        if is_valid_onion_address(hiddenWebSite) == False:
            print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite)
            raise PluginException(message="Invalid Onion Adress %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite),
                                  trace="compareRelaysWithHiddenWebSite with args hiddenWebSite=%s" %(hiddenWebSite),
                                  plugin="crawler",
                                  method="compareRelaysWithHiddenWebSite")


        try:
            responseHidden = self.serviceConnector.performHTTPConnectionHiddenService(hiddenWebSite,method="GET")
        except Exception as exc:
            print "[-] Exception connecting to the hidden service. Is the hidden service up and running? "+str(exc.message)
            return
        ratios={}
        for node in self.torNodes:
            if responseHidden.status_code == 200:
                try:
                    responseRelay = self.serviceConnector.performHTTPConnection('http://'+node.host, method="GET")
                    if responseRelay.status_code == 200:
                        print "[+] Executing the matcher tool against the responses."
                        ratio = difflib.SequenceMatcher(None,responseHidden.content,responseRelay.content).ratio()
                        ratios[node.host] = str(ratio)
                except:
                    continue
        print "[+] The percentage of equivalence between the contents of web sites found in the relays and hidden services are: \n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])

        elements = [ ["Hidden Service", "Relay", "Percentage"]]
        for key in ratios.keys():
            elements.append( [ hiddenWebSite, str(key), str(ratios[key])  ] )

        table.add_rows( elements )
        print table.draw() + "\\n"



    def crawlOnionWebSite(self, hiddenWebSite, hiddenWebSitePort=80,
                         socatTcpListenPort=8765,
                         crawlImages=False, crawlLinks=True,
                         crawlContents=True, crawlFormData=False,
                         useRandomUserAgents=True, deepLinks=None,
                         bruterOnProtectedResource=False):
        if hiddenWebSite == '' or hiddenWebSite is None:
            print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite)
            raise PluginException(message="Invalid Onion Adress %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite),
                                  trace="crawlOnionWebSite with args hiddenWebSite=%s" %(hiddenWebSite),
                                  plugin="crawler",
                                  method="crawlOnionWebSite")
        if hiddenWebSite.startswith('http://'):
            onionSite = hiddenWebSite.replace('http://', "")
        else:
            onionSite = hiddenWebSite

        if is_valid_onion_address(onionSite) == False:
            print "[-] Invalid Onion Address %s must contain 16 characters. The TLD must be .onion" %(hiddenWebSite)
            raise PluginException(message="Invalid Onion Adress %s must contain 16 characters. The TLD must be .onion" %(onionSite),
                                  trace="crawlOnionWebSite with args hiddenWebSite=%s" %(hiddenWebSite),
                                  plugin="crawler",
                                  method="crawlOnionWebSite")


        if is_valid_port(hiddenWebSitePort) == False:
            print "[-] The port specified is invalid. "
            raise PluginException(message='[-] The port specified is invalid. %s ' %(str(hiddenWebSitePort)),
                                  trace="crawlOnionWebSite with args hiddenWebSitePort=%s , " %(str(hiddenWebSitePort)),
                                  plugin="crawler", method="crawlOnionWebSite")


        if is_valid_port(socatTcpListenPort) == False:
            print "[-] The port specified is invalid. "
            raise PluginException(message='[-] The port specified is invalid. %s ' %(str(socatTcpListenPort)),
                                  trace="crawlOnionWebSite with args hiddenWebSitePort=%s , " %(str(socatTcpListenPort)),
                                  plugin="crawler", method="crawlOnionWebSite")

        onionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        onionSocket.settimeout(1)
        result = onionSocket.connect_ex(('127.0.0.1',socatTcpListenPort))
        if result == 0:
            print "[-] The selected local port "+str(socatTcpListenPort)+" is being used by another process. Please, select an port available in this machine"
            raise PluginException(message="The selected local port "+str(socatTcpListenPort)+" is being used by another process. Please, select an port available in this machine",
                                  trace="crawlOnionWebSite with args socatTcpListenPort=%s , " %(str(socatTcpListenPort)),
                                  plugin="crawler", method="crawlOnionWebSite")

        extraPath = onionSite[onionSite.find('.onion') + 6:]
        #Extracts the Onion Site, everything before ".onion"
        onionSite = onionSite[:onionSite.find('.onion') + 6]

        try:
            print "[+] Starting a local proxy with Socat to forward requests to the hidden service through the local machine and the local Socks Proxy... "
            socatProcess = self.serviceConnector.startLocalSocatTunnel(socatTcpListenPort, onionSite,hiddenWebSitePort, socksPort=self.serviceConnector.socksPort)
            sleep(5)
            print "[+] Socat process started! PID: "+str(socatProcess.pid)
            self.__crawl(hiddenWebSite, socatTcpListenPort,
                         extraPath=extraPath, crawlImages=crawlImages,
                         crawlLinks=crawlLinks, crawlContents=crawlContents,
                         crawlFormData=crawlFormData, useRandomUserAgents=useRandomUserAgents, deepLinks=deepLinks, bruterOnProtectedResource=bruterOnProtectedResource)
            os.killpg(socatProcess.pid, signal.SIGTERM)
            print "[+] Socat process killed."
        except Exception as exce:
            print "[+] The following exception was raised, however, shutting down the local Socat tunnel..."
            print sys.exc_info()
            print exce
            os.killpg(socatProcess.pid, signal.SIGTERM)
            sleep(5)

    def __crawl(self, hiddenWebSite, localPort, extraPath='', crawlImages=True, crawlLinks=True,crawlContents=True, crawlFormData=True, useRandomUserAgents=True, deepLinks=None, bruterOnProtectedResource=False):
        def catch_item(sender, item, **kwargs):
            item['url'] = item['url'].replace('http://127.0.0.1:'+str(localPort)+extraPath, hiddenWebSite)
            print "[+] Processing URL %s ...  " %(item['url'])
            from core.tortazo.databaseManagement.TortazoDatabase import TortazoDatabase
            database = TortazoDatabase()
            database.initDatabaseDeepWebCrawlerPlugin()
            self.__processPage(item, database)

        # setup crawler
        dispatcher.connect(catch_item, signal=signals.item_passed)
        dispatcher.connect(reactor.stop, signal=signals.spider_closed)

        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.configure()

        try:
            httpcode = urllib.urlopen("http://127.0.0.1:"+str(localPort)+extraPath).getcode()
            if httpcode not in range(200,299):
                print "[-] Seems that the hidden service is not responding... detected HTTP Status code %s. The scrapper could fail." %(str(httpcode))
        except IOError as ioError:
            error, code,desc,detail = ioError
            if "http protocol" in error:
                print "[-] Seems that the hidden service is not responding... Detected HTTP Protocol error. The scrapper could fail."

        spider = HiddenSiteSpider("http://127.0.0.1:"+str(localPort)+extraPath, hiddenWebSite, self.extractorRulesAllow, self.extractorRulesDeny)
        spider.setImages(crawlImages)
        spider.setLinks(crawlLinks)
        spider.setContents(crawlContents)
        spider.setForms(crawlFormData)
        spider.setDeepLinks(deepLinks)
        if self.crawlRulesLinks != None:
            spider.setCrawlRulesLinks(self.crawlRulesLinks)
        if self.crawlRulesImages != None:
            spider.setCrawlRulesImages(self.crawlRulesImages)
        if self.dictFile != None:
            spider.setDictForBruter(self.dictFile)


        spider.setBruterOnProtectedResource(bruterOnProtectedResource)


        if useRandomUserAgents:
            spider.setUserAgents(self.fuzzDBReader.getUserAgentsFromFuzzDB())

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

        
    def help(self):
        print "[*] Functions availaible available in the Plugin...\n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ["setExtractorRulesAllow", 'Sets the XPATH rules to specify the allowed pages to visit and analyze. This value will be passed to the "allow" attribute of the class "scrapy.contrib.linkextractors.LinkExtractor".', "self.setExtractorRulesAllow('index\.php| index\.jsp')"],
                         ['setExtractorRulesDeny', 'Sets the XPATH rules to specify the disallowed pages to visit and analyze. This value will be passed to the "deny" attribute of the class "scrapy.contrib.linkextractors.LinkExtractor"', "self.setExtractorRulesDeny('index\.php| index\.jsp')"],
                         ['setCrawlRulesLinks', 'Sets the XPath rules to extract links from every webpage analyzed. Default value should be enough to almost every case, however you can use this function to overwrite this value. Default: "//a/@href"', "self.setCrawlRulesLinks('//a[contains(@href, 'confidential')]/@href')"],
                         ['setCrawlRulesImages', 'Sets the XPath rules to extract images from every webpage analyzed. Default value should be enough to almost every case, however you can use this function to overwrite this value. Default: "//img/@src"', "self.setCrawlRulesImages('//a[contains(@href, 'image')]/@href')" ],
                         ['setDictForBruter', 'Sets the Dictionary file for HTTP Bruteforce attacks on protected resources.', 'self.setDictForBruter("/home/user/dictFile.txt")'],
                         ['compareWebSiteWithHiddenWebSite', 'This function compares the contents of a website in clear web with the contents of a web site in TOR deep web. The return value will be a percent of correlation and similitude between both sites.', 'self.compareWebSiteWithHiddenWebSite("http://exit-relay-found.com/", "http://gai12dase4sw3f5a.onion/")'],
                         ['compareRelaysWithHiddenWebSite', 'This function will perform an HTTP connection against every relay found and if the response is a HTTP 200 status code, performs an HTTP connection against the hidden service specified and compares the contents of both responses.  The return value will be a percent of correlation and similitude between both sites.', 'self.compareRelaysWithHiddenWebSite("http://gai12dase4sw3f5a.onion/")'],
                         ['crawlOnionWebSite', 'This function executes a crawler against the specified hidden service. The following parameters allows to control the behaviour of the crawler:hiddenWebSite: The hidden site to crawl. This is a mandatory parameter. hiddenWebSitePort: Port for the hidden site to crawl. Default value: 80. socatTcpListenPort: Port for the Socat proxy. Default value: 8765. crawlImages: Search and download the images from every page. Default value is True. crawlLinks: Search and visit the links found in every page. Default value: True. crawlContents: Download and save in local file system the contents of every page found. deepLinks: Number of Links that the crawler will visit in deep. bruterOnProtectedResource: If true, when the spider found an HTTP protected resource, tries to execute an bruteforce attack using the specified dict file or FuzzDB. crawlFormData: Search the forms in every page and store that structure in database. useRandomUserAgents: Use a random list of User-Agents in every HTTP connection performed by the crawler. FuzzDB project is used to get a list of User-Agents reading the file fuzzdb/attack-payloads/http-protocol/user-agents.txt', '- self.crawlOnionWebSite("http://gai12dase4sw3f5a.onion/")\n - self.crawlOnionWebSite("http://gai12dase4sw3f5a.onion/", hiddenWebSitePort=8080, crawlImages=False)\n - self.crawlOnionWebSite("http://gai12dase4sw3f5a.onion/", crawlFormData=False)']
                        ])
        print table.draw() + "\\n"
