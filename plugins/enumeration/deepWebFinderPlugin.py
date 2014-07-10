# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

deepWebStemmingPlugin.py

deepWebStemmingPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

deepWebStemmingPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from prettytable import PrettyTable
import requests


class deepWebFinderPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'deepWebFinderPlugin')
        self.setPluginDetails('deepWebFinderPlugin', 'Basic pentesting tasks against hidden services in the TOR network', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.setSocksProxy()
            self.info("[*] deepWebFinderPlugin Initialized!")

    def __del__(self):
        if len(self.torNodes) > 0:
            self.debug("[*] DeepWebPlugin Destroyed!")

    def compareRelaysWithHiddenWebSite(self, hiddenWebSite):
        for node in self.torNodes:
            responseHidden = self.serviceConnector.performHTTPConnectionHiddenService(hiddenWebSite,method="GET")
            if responseHidden.status_code == 200:
                responseRelay = self.serviceConnector.performHTTPConnection('http://'+node.host, method="GET")
                requestRelay = requests.get(node.host)
    
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



    def crawlContentsHiddenWebSite(self, hiddenWebSite, outputDir='./', storeBD=False):
        pass

    def crawlLinksHiddenWebSite(self, hiddenWebSite, outputDir='./', storeBD=False):
        pass
		
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