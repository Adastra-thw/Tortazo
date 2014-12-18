# coding=utf-8
'''
Created on 12/07/2014

#Author: Adastra.
#twitter: @jdaanial

HiddenSiteSpider.py

HiddenSiteSpider is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

HiddenSiteSpider is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from plugins.enumeration.utils.hiddenSitePage import HiddenSitePage
from scrapy import Request
from urlparse import urljoin
import mechanize
from config import config
import os
import random
from plugins.bruteforce.bruterPlugin import bruterPlugin
import cookielib
from re import search

class HiddenSiteSpider(CrawlSpider):

    def __init__(self, localTunnel, onionSite, extractorAllowRules=[r'^/*'], extractorDenyRules=[], **kw):
        self.name="TortazoSpider"
        self.onionSite = onionSite
        self.localTunnel = localTunnel
        self.start_urls=[localTunnel]
        self.visitedLinks=[]
        handle_httpstatus_list = [401]
        self.deepLinks = None
        self.extractorAllowRules = extractorAllowRules
        self.extractorDenyRules = extractorDenyRules
        #self._rules = [Rule(LinkExtractor(allow=extractorAllowRules), deny=extractorDenyRules, follow=True, callback=self.parse),]
        self._rules = [Rule(LinkExtractor(allow=extractorAllowRules, deny=extractorDenyRules), follow=True, callback=self.parse),]
        self.crawlRulesLinks = "//a/@href"
        self.crawlRulesImages = '//img/@src'
        self.dictFile = None



    def setImages(self, images):
        self.images = images

    def setLinks(self, links):
        self.links = links

    def setContents(self, contents):
        self.contents = contents

    def setForms(self, forms):
        self.forms = forms

    def setUserAgents(self, userAgents):
        self.userAgents = userAgents

    def setDeepLinks(self, deepLinks):
        self.deepLinks = deepLinks

    def setCrawlRulesLinks(self, crawlRulesLinks):
        self.crawlRulesLinks = crawlRulesLinks

    def setCrawlRulesImages(self, crawlRulesImages):
        self.crawlRulesImages = crawlRulesImages

    def setDictForBruter(self, dictFile):
        self.dictFile = dictFile


    def setBruterOnProtectedResource(self, bruterOnProtectedResource):
        self.bruterOnProtectedResource = bruterOnProtectedResource

    def parse(self, response):
        onionDomain = response.url.replace(self.localTunnel, self.onionSite)
        #validation for onion domain with the regular expresions for Allowed domains and Disallowed domains.
        onionDir = onionDomain.replace("http://", "").replace("https://", "")

        for disallowed in self.extractorDenyRules:
            if disallowed is None or disallowed == '':
                continue
            matching = search(disallowed, onionDir)
            if matching != None:
                #The link is disallowed. We don't process this link.
                return

        for allowed in self.extractorAllowRules:
            if allowed is None or allowed == '':
                continue
            matching = search(allowed, onionDir)
            if matching == None:
                #The link doesn't follow the condition for valid links in the crawling process. We don't process this link.
                return

        if response.url in self.visitedLinks:
            #Link already visited in the current crawling process.
            return
        else:
            self.visitedLinks.append(response.url)
        if response.status == 401:
            #Request authentication.
            bruter = bruterPlugin(torNodes=[])
            if response.url.contains('.onion') and self.bruterOnProtectedResource:
                print "[+] HTTP Protected resource found in hiddenservice. As you've indicated, we're gonna start an HTTP Dictionary Attack."
                bruter.httpBruterOnHiddenService(response.url, dictFile=self.dictFile)
            elif response.url.contains('.onion') == False and self.bruterOnProtectedResource:
                print "[+] HTTP Protected resource found in clear web site. As you've indicated, we're gonna start an HTTP Dictionary Attack."
                bruter.httpBruterOnSite(response.url, dictFile=self.dictFile)



        item = HiddenSitePage()
        if self.contents:
            onion = response.url

            onion = onion.replace(self.localTunnel,self.onionSite)
            onion = onion.replace('http://', '')
            onion = onion.replace('https://', '')
            onion = onion.replace(':','')

            indexResource = onion.rfind('/')
            dirStructure = onion[:indexResource]
            resource = onion[indexResource:].replace('/','')
            try:
                if os.path.exists(config.deepWebCrawlerOutdir+dirStructure) == False:
                    os.makedirs(config.deepWebCrawlerOutdir+dirStructure)
                if resource == '':
                    open(config.deepWebCrawlerOutdir+dirStructure+"/index.html", 'wb').write(response.body)
                else:
                    open(config.deepWebCrawlerOutdir+dirStructure+resource, 'wb').write(response.body)
            except:
                pass

        if response.headers['Content-Type'].find('text/') <= -1:
            return
        else:
            item['body']  =  response.body


        selector = Selector(response)
        if len(selector.xpath('//title/text()').extract()) > 0:
            item['title'] = selector.xpath('//title/text()').extract()[0]
        else:
            item['title'] = 'No title'
        item['url']  =  response.url

        headers = ''
        for header, value in response.headers.iteritems():
            headers = str(header)+" : "+str(value)+"\n"+headers
        item['headers']  =  headers
        if self.images:
            item['imagesSrc'] = selector.xpath(self.crawlRulesImages).extract()
        if self.forms:
            if len(selector.xpath('//form').extract()) > 0:
                browser = mechanize.Browser()
                browser.open(response.url)
                cj = cookielib.LWPCookieJar()
                browser.set_cookiejar(cj)
                #some browser options.
                browser.set_handle_equiv(True)
                browser.set_handle_gzip(True)
                browser.set_handle_redirect(True)
                browser.set_handle_referer(True)
                browser.set_handle_robots(False)
                # User-Agent
                browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
                try:
                    pageForms = {}
                    formId = 0
                    for form in browser.forms():
                        if form.name is None:
                            form.name="form_"+str(formId)
                        controls = []
                        for control in form.controls:
                            controlName = control.name
                            controlType = control.type
                            controlValue = control.value
                            if controlName == None:
                                controlName = ""
                            if controlType == None:
                                controlType = ""
                            if controlValue == None:
                                controlValue = ""
                            controls.append( (str(controlName), str(controlType), str(controlValue)) )
                        formId = formId + 1
                        pageForms[form.name] = controls
                    item['forms'] = pageForms
                except:
                    pass




        if response.meta.has_key('item'):
            parent = response.meta.get('item')
            item['pageParent'] = parent

        if self.links and self.deepLinks is None:
            linksFound = response.xpath(self.crawlRulesLinks).extract()
            for url in linksFound:
                if len(self.userAgents) > 0:
                    userAgent = random.choice(self.userAgents)
                    newRequest = Request(urljoin(response.url, url), callback=self.parse,errback=lambda _: item,meta=dict(item=item))
                    newRequest.headers.setdefault('User-Agent', userAgent)
                    yield newRequest
                else:
                    yield Request(urljoin(response.url, url), callback=self.parse,errback=lambda _: item,meta=dict(item=item))


        if self.links and self.deepLinks is not None:
            linksFound = response.xpath(self.crawlRulesLinks).extract()
            for url in linksFound:
                if self.deepLinks > 0:
                    if len(self.userAgents) > 0:
                        userAgent = random.choice(self.userAgents)
                        newRequest = Request(urljoin(response.url, url), callback=self.parse,errback=lambda _: item,meta=dict(item=item))
                        newRequest.headers.setdefault('User-Agent', userAgent)
                        yield newRequest
                    else:
                        yield Request(urljoin(response.url, url), callback=self.parse,errback=lambda _: item,meta=dict(item=item))
                    self.deepLinks = self.deepLinks-1
                else:
                    break
        yield item
