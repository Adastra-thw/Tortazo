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
from core.tortazo.pluginManagement.socks import Socks5Error
from prettytable import PrettyTable
from collections import Counter
import config

class deepWebStemmingPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes):
        BasePlugin.__init__(self, torNodes, 'deepWebPlugin')
        self.setSocksProxy()
        #self.prepocessor = Preprocessor()
        #self.matrix = Matrix()
        #self.metric = Metrics()
        self.info("[*] deepWebStemmingPlugin Initialized!")
        self.webPorts = [80,443,8080]

    def __del__(self):
        self.debug("[*] deepWebStemmingPlugin Destroyed!")

    def simpleStemmingAllRelays(self, queryTerms, httpMethod="GET", portNumber=None):
        import requests

        for node in self.torNodes:
            if portNumber is not None and portNumber in node.openPorts:
                response = requests.get(node.host+":"+port, timeout=config.timeOutRequests)
                self.validateResponse(response, queryTerms)
            else:
                for port in node.openPorts:
                    if port.port in self.webPorts:
                        try:
                            print port.port
                            if httpMethod == "GET":
                                response = requests.get("http://"+node.host+":"+str(port.port), timeout=config.timeOutRequests)
                                self.validateResponse(response, queryTerms)
                            else:
                                response = requests.post("http://"+node.host+":"+str(port.port), timeout=config.timeOutRequests)
                                self.validateResponse(response, queryTerms)
                        except requests.ConnectionError:
                            pass
                        except requests.Timeout:
                            pass
                        except Socks5Error:
                            pass

    def stemmingWebSite(self, webSite, queryTerms):
        import requests
        response = requests.get(webSite, timeout=config.timeOutRequests)
        self.validateResponse(response, queryTerms)


    def validateResponse(self, response, queryTerms):
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
            '''for doc in mx.docs:
                distance = metric.euclid_vectors(doc['terms'], q_vector)
                print distance
            '''
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
        print "[*] Functions availaible available in the Plugin..."
        tableHelp = PrettyTable(["Function", "Description", "Example"])
        tableHelp.padding_width = 1
        tableHelp.add_row(['help', 'Help Banner', 'self.help()'])
        tableHelp.add_row(['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'])
        tableHelp.add_row(['simpleStemmingAllRelays', 'Stemming with all the specified terms along the relays loaded in the plugins. Search for web sites in common ports, like 80,8080,443 or in a specific port', 'self.simpleStemmingAllRelays("drugs kill killer")'])
        tableHelp.add_row(['stemmingWebSite', 'Stemming with all the specified terms in the website specified.', 'self.stemmingWebSite("http://torlinkbgs6aabns.onion/", "drugs kill killer")'])
        print tableHelp