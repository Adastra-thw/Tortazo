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
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from plugins.enumeration.utils.hiddenSitePage import HiddenSitePage
from scrapy import Request
from urlparse import urljoin
import mechanize

class HiddenSiteSpider(CrawlSpider):

    def __init__(self, onionSite, extractorRules=[r'^/*']):
        self.name="TortazoSpider"
        self.start_urls=[onionSite]
        self._rules = [Rule(SgmlLinkExtractor(allow=extractorRules), follow=True, callback=self.parse),]

    def setImages(self, images):
        self.images = images

    def setLinks(self, links):
        self.links = links

    def setContents(self, contents):
        self.contents = contents

    def setForms(self, forms):
        self.forms = forms


    def setCrawlRules(self, crawlRules):
        self.crawlRules = crawlRules


    def parse(self, response):
        item = HiddenSitePage()
        selector = Selector(response)
        item['title'] = selector.xpath('//title/text()').extract()[0]
        item['url']  =  response.url
        item['body']  =  response.body

        headers = ''
        for header, value in response.headers.iteritems():
            headers = str(header)+" : "+str(value)+"\n"+headers
        item['headers']  =  headers
        if self.images:
            item['images'] = selector.xpath('//img/@src').extract()
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
                            print control
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
                yield Request(urljoin(response.url, url), callback=self.parse,errback=lambda _: item,meta=dict(item=item))
        yield item
'''
    def processPage(self, response):
        #http://doc.scrapy.org/en/latest/topics/request-response.html
        #print 'link parseado %s' %response.url
        print "[+] Parent Page: %s " %response.url
        self.items = []
        selector = Selector(response)
        item = HiddenSitePage()
        item['title'] = selector.xpath('//title/text()').extract()
        item['url']  =  response.url
        if self.images:
            item['images'] = selector.xpath('//img/@src').extract()
        if self.forms:
            item['forms'] =  selector.xpath('//form').extract()

        if self.links:
            linksPage = selector.xpath('//a/@href').extract()
            for link in linksPage:
                print "[+][+] Child Page: %s " %(urljoin(response.url, link))
                #yield Request(urljoin(response.url, link),callback=self.parse_link,errback=lambda _: item,meta=dict(item=item),)

                #request = Request("http://127.0.0.1:8765/testing/"+link,callback=self.processChildPage)
                #request.meta['item'] = item
                #return  request

        return item # Retornando el Item.

    def parse_link(self, response):
        child = HiddenSitePage()
        item = response.meta.get('item')
        child['pageParent'] = item
        return child


    def processChildPage(self, response):
        parentPage = response.meta['item']
        selector = Selector(response)
        child = HiddenSitePage()
        child['title'] = selector.xpath('//title/text()').extract()
        child['url']  =  response.url
        if self.images:
            child['images'] = selector.xpath('//img/@src').extract()
        if self.forms:
            child['forms'] =  selector.xpath('//form').extract()

        child['pageParent'] = parentPage
        if self.links:
            linksPage = selector.xpath('//a/@href').extract()
            for link in linksPage:
                request = Request("http://127.0.0.1:8765/testing/"+link,callback=self.processChildPage)
                request.meta['item'] = child
                return request
'''


