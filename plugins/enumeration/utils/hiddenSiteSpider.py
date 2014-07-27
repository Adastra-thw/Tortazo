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

class HiddenSiteSpider(CrawlSpider):

    def __init__(self, localTunnel, onionSite, extractorAllowRules=[r'^/*'], extractorDenyRules=['']):
        self.name="TortazoSpider"
        self.onionSite = onionSite
        self.localTunnel = localTunnel
        self.start_urls=[localTunnel]
        self.visitedLinks=[]
        #self._rules = [Rule(LinkExtractor(allow=extractorAllowRules), deny=extractorDenyRules, follow=True, callback=self.parse),]
        self._rules = [Rule(LinkExtractor(allow=extractorAllowRules), follow=True, callback=self.parse),]

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

    def parse(self, response):
        if response.url in self.visitedLinks:
            return
        else:
            self.visitedLinks.append(response.url)
        #if response.status == 401:
            #Request authentication.

        item = HiddenSitePage()
        selector = Selector(response)
        item['title'] = selector.xpath('//title/text()').extract()[0]
        item['url']  =  response.url
        if self.contents:
            item['body']  =  response.body
            onion = response.url
            onion = onion.replace(self.localTunnel,self.onionSite)
            onion = onion.replace('http://', '')
            onion = onion.replace(':','')
            indexResource = onion.rfind('/')
            dirStructure = onion[:indexResource]
            resource = onion[indexResource:].replace('/','')
            if os.path.exists(config.deepWebCrawlerOutdir+dirStructure) == False:
                os.makedirs(config.deepWebCrawlerOutdir+dirStructure)
            if resource == '':
                open(config.deepWebCrawlerOutdir+dirStructure+"/index.html", 'wb').write(response.body)
            else:
                open(config.deepWebCrawlerOutdir+dirStructure+"/"+resource, 'wb').write(response.body)

        headers = ''
        for header, value in response.headers.iteritems():
            headers = str(header)+" : "+str(value)+"\n"+headers
        item['headers']  =  headers
        if self.images:
            item['imagesSrc'] = selector.xpath('//img/@src').extract()
        if self.forms:
            if len(selector.xpath('//form').extract()) > 0:
                browser = mechanize.Browser()
                browser.open(response.url)
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
                except AttributeError:
                        pass




        if response.meta.has_key('item'):
            parent = response.meta.get('item')
            item['pageParent'] = parent

        if self.links:
            linksFound = response.xpath('//a/@href').extract()
            for url in linksFound:
                if len(self.userAgents) > 0:
                    userAgent = random.choice(self.userAgents)
                    newRequest = Request(urljoin(response.url, url), callback=self.parse,errback=lambda _: item,meta=dict(item=item))
                    newRequest.headers.setdefault('User-Agent', userAgent)
                    yield newRequest
                else:
                    yield Request(urljoin(response.url, url), callback=self.parse,errback=lambda _: item,meta=dict(item=item))
        yield item