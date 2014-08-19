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
from collections import Counter
from config import config
from plugins.texttable import Texttable
from core.tortazo.exceptions.PluginException import PluginException

class deepWebStemmingPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'deepWebStemmingPlugin')
        self.setPluginDetails('DeepWebStemmingPlugin', 'Basic stemming tasks against hidden services in the TOR network. Uses IRL library to find terms in hidden services in the TOR network.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.serviceConnector.setSocksProxy()
            #self.prepocessor = Preprocessor()
            #self.matrix = Matrix()
            #self.metric = Metrics()
            self.info("[*] deepWebStemmingPlugin Initialized!")
            self.webPorts = [80,443,8080]
        self.pluginConfigs= {"timeOutRequests":config.timeOutRequests}


    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)


    def __del__(self):
        if len(self.torNodes) > 0:
            self.debug("[*] deepWebStemmingPlugin Destroyed!")

    def simpleStemmingAllRelays(self, queryTerms, httpMethod="GET", portNumber=None):
        import requests

        for node in self.torNodes:
            if portNumber is not None and portNumber in node.openPorts:
                response = requests.get(node.host+":"+port, timeout=self.pluginConfigs['timeOutRequests'])
                self.__validateResponse(response, queryTerms)
            else:
                for port in node.openPorts:
                    if port.port in self.webPorts:
                        try:
                            response = self.serviceConnector.performHTTPConnection("http://"+node.host+":"+str(port.port), method=httpMethod)
                            self.validateResponse(response, queryTerms)
                        except requests.ConnectionError:
                            continue
                        except requests.Timeout:
                            continue

    def stemmingHiddenService(self, webSite, queryTerms):
        response = self.serviceConnector.performHTTPConnectionHiddenService(webSite, method="GET")
        self.__validateResponse(response, queryTerms)


    def __validateResponse(self, response, queryTerms):
        from bs4 import BeautifulSoup

        if response.status_code == 200:
            soup = BeautifulSoup(response.text)
            from irlib.preprocessor import Preprocessor
            from irlib.matrix import Matrix
            from irlib.metrics import Metrics
            prep = Preprocessor()
            mx = Matrix()
            metric = Metrics()
            terms = prep.ngram_tokenizer(text=soup.get_text())
            mx.add_doc( doc_id=response.url,doc_terms=terms,frequency=True,do_padding=True)
            cnt = Counter()

            for word in terms:
                cnt[word] += 1
            tableTerms = PrettyTable(["Term", "Frequency"])
            for word in sorted(cnt, key=cnt.get, reverse=True):
                if word.lower() in queryTerms.lower().split():
                    tableTerms.add_row([word, cnt[word]])
            print tableTerms
        else:
            print "[-] Response for %s is %s " %(response.url, response.status_code)


    def help(self):
        print "[*] Functions availaible available in the Plugin...\n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'],
                         ['simpleStemmingAllRelays', 'Stemming with all the specified terms along the relays loaded in the plugin. Search for web sites in common ports, like 80,8080,443 or in a specific port', 'self.simpleStemmingAllRelays("drugs kill killer hitman")'],
                         ['stemmingHiddenService', 'Stemming with all the specified terms in the website specified.', 'self.stemmingWebSite("http://torlinkbgs6aabns.onion/", "drugs kill killer")']
                        ])
        print table.draw() + "\\n"
