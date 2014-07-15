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
from plugins.enumeration.utils.hiddenSiteItem import HiddenSiteItem

class HiddenSiteSpider(CrawlSpider):

    def __init__(self, onionSite, extractorRules=[r'^/*']):
        self.name="TortazoSpider"
        self.start_urls=[onionSite]
        self._rules = [Rule(SgmlLinkExtractor(allow=extractorRules), follow=True, callback=self.parseResponse),]

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

    def parseResponse(self, response):
        print 'link parseado %s' %response.url
        selector = Selector(response)
        item = HiddenSiteItem()
        item['title'] = selector.xpath('//title/text()').extract()
        item['link']  =  response.url
        if self.links:
            item['links'] = selector.xpath('//a/@href').extract()
        if self.images:
            item['images'] = selector.xpath('//img/@src').extract()
        if self.forms:
            item['forms'] =  selector.xpath('//form').extract()
        return item # Retornando el Item.

