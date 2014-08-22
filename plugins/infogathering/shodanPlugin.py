# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

shodanPlugin.py

shodanPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

shodanPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from plugins.texttable import Texttable
import shodan
from core.tortazo.exceptions.PluginException import PluginException
import os
from plugins.utils.validations.Validator import *

class shodanPlugin(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'shodanPlugin')
        self.setPluginDetails('shodanPlugin', 'Plugin to gather information using the Shodan Database.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] shodanPlugin Initialized!")
        self.pluginConfigs= {}


    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)


    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] shodanPlugin Destroyed!")

    def setApiKey(self, apiKey):
        if apiKey == '' or apiKey is None:
            print "[-] The Shodan key specified is invalid. "
            raise PluginException(message='The Shodan key specified is invalid.',
                                  trace="setApiKey with args apiKey=%s " %(apiKey),
                                  plugin="shodan", method="setApiKey")
        self.apiKey = apiKey
        print "[*] Shodan Key established!"

    def setApiKeyFile(self, apiKeyFile):
        if apiKeyFile == '' or apiKeyFile is None:
            print "[-] The file specified is invalid. "
            raise PluginException(message='The file specified is invalid.',
                                  trace="setApiKeyFile with args apiKeyFile=%s " %(apiKeyFile),
                                  plugin="shodan", method="setApiKeyFile")

        if os.path.exists(apiKeyFile) == False or os.path.isfile(apiKeyFile) == False:
            print "[-] The file specified is invalid. "
            raise PluginException(message='The file specified is invalid.',
                                  trace="setApiKeyFile with args apiKeyFile=%s " %(apiKeyFile),
                                  plugin="shodan", method="setApiKeyFile")



        shodanKeyString = open(apiKeyFile).readline().rstrip('\n')
        self.apiKey = shodanKeyString
        print "[*] Shodan Key established!"

    def basicSearchQuery(self, basicSearch, limit=10):
        if limit == None or limit < 0:
            print "[-] The limit specified is invalid. "
            raise PluginException(message='The limit specified is invalid.',
                                  trace="basicSearchQuery with args basicSearch=%s , limit=%s " %(basicSearch, str(limit)),
                                  plugin="shodan", method="basicSearchQuery")

        if basicSearch == None or basicSearch == '':
            print "[-] The query specified is invalid. "
            raise PluginException(message='The query specified is invalid.',
                                  trace="basicSearchQuery with args basicSearch=%s , limit=%s " %(basicSearch, str(limit)),
                                  plugin="shodan", method="basicSearchQuery")



        if hasattr(self, 'apiKey') and self.apiKey is not None:
            shodanApi = shodan.Shodan(self.apiKey)
            results = shodanApi.search(basicSearch)
            count = 0
            table = Texttable()
            table.set_cols_align(["l"])
            table.set_cols_valign(["m"])
            table.set_cols_width([55])

            rows = [["Data"]]

            for service in results['matches']:
                if count == limit:
                    break
                else:
                    count += 1
                    rows.append([service['ip_str']+"\n"+service['data']])
            table.add_rows(rows)
            print table.draw() + "\n"

        else:
            print "[*] Shodan API key not set. This is mandatory to perform searches using Shodan"

    def basicSearchAllRelays(self,basicSearch):
        if basicSearch == None or basicSearch == '':
            print "[-] The query specified is invalid. "
            raise PluginException(message='The query specified is invalid.',
                                  trace="basicSearchAllRelays with args basicSearch=%s " %(basicSearch),
                                  plugin="shodan", method="basicSearchAllRelays")

        if hasattr(self, 'apiKey') and self.apiKey is not None:
            shodanApi = shodan.Shodan(self.apiKey)
            for node in self.torNodes:
                results = shodanApi.search(basicSearch+"net:"+node.host)

                table = Texttable()
                table.set_cols_align(["l"])
                table.set_cols_valign(["m"])
                table.set_cols_width([55])

                rows = [["Data"]]
                if len(results['matches']) > 0:
                    print results
                    print "[*] Data for: %s " %(node.host)
                    for service in results['matches']:
                        rows.append([service['ip_str']+"\n"+service['data']])
                    table.add_rows(rows)
                    print table.draw() + "\n"
                else:
                    print "[*] No results for: %s " %(node.host)
        else:
            print "[*] Shodan API key not set. This is mandatory to perform searches using Shodan"

    def basicSearchByRelay(self,basicSearch, relay):
        if basicSearch == None or basicSearch == '':
            print "[-] The query specified is invalid. "
            raise PluginException(message='The query specified is invalid.',
                                  trace="basicSearchAllRelays with args basicSearch=%s , relay=%s" %(basicSearch, relay),
                                  plugin="shodan", method="basicSearchAllRelays")


        if is_valid_ipv4_address(relay) == False and is_valid_ipv6_address(relay) == False and is_valid_domain(relay) == False:
            print '[-] The relay specified is invalid. %s ' %(relay)
            raise PluginException(message='The relay specified is invalid. %s ' %(relay),
                                  trace="basicSearchByRelay with args basicSearch=%s , relay=%s " %(basicSearch, relay),
                                  plugin="shodan", method="basicSearchByRelay")



        if hasattr(self, 'apiKey') and self.apiKey is not None:
            shodanApi = shodan.Shodan(self.apiKey)
            for node in self.torNodes:
                if relay is not None and node.host == relay:
                    results = shodanApi.search(basicSearch+"net:"+node.host)
                    table = Texttable()
                    table.set_cols_align(["l"])
                    table.set_cols_valign(["m"])
                    table.set_cols_width([55])
                    rows = [["Data"]]
                    if len(results['matches']) > 0:
                        print results
                        print "[*] Data for: %s " %(node.host)
                        for service in results['matches']:
                            rows.append([service['ip_str']+"\n"+service['data']])
                        table.add_rows(rows)
                        print table.draw() + "\n"
                    else:
                        print "[*] No results for: %s " %(node.host)
        else:
            print "[*] Shodan API key not set. This is mandatory to perform searches using Shodan"

    def basicSearchByNickname(self,basicSearch, nickname):
        if basicSearch == None or basicSearch == '':
            print "[-] The query specified is invalid. "
            raise PluginException(message='The query specified is invalid.',
                                  trace="basicSearchByNickname with args basicSearch=%s " %(basicSearch),
                                  plugin="shodan", method="basicSearchByNickname")

        if hasattr(self, 'apiKey') and self.apiKey is not None:
            shodanApi = shodan.Shodan(self.apiKey)
            for node in self.torNodes:
                if nickname is not None and node.nickName == nickname:
                    results = shodanApi.search(basicSearch+"net:"+node.host)
                    table = Texttable()
                    table.set_cols_align(["l"])
                    table.set_cols_valign(["m"])
                    table.set_cols_width([55])
                    rows = [["Data"]]
                    if len(results['matches']) > 0:
                        print results
                        print "[*] Data for: %s " %(node.host)
                        for service in results['matches']:
                            rows.append([service['ip_str']+"\n"+service['data']])
                        table.add_rows(rows)
                        print table.draw() + "\n"
                    else:
                        print "[*] No results for: %s " %(node.host)
        else:
            print "[*] Shodan API key not set. This is mandatory to perform searches using Shodan"

    def help(self):
        print "[*] Functions availaible available in the Plugin...\n"
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'],
                         ['setApiKey', 'Sets the API Key string.', 'self.setApiKey("XXXXXXXXXXXX")'],
                         ['setApiKeyFile', 'Sets the API Key file. Reads the first line of the file and then sets the API Key string.', 'self.setApiKeyFile("/home/apiKeyFile")'],
                         ['basicSearchQuery', 'Performs a basic search with Shodan. By default prints the 10 first results', 'self.basicSearchQuery("OpenSSL 1.0.1", 15)'],
                         ['basicSearchAllRelays', 'Performs a basic search with Shodan against all TOR relays. Uses the "net" filter.', 'self.basicSearchAllRelays("OpenSSL 1.0.1")'],
                         ['basicSearchByRelay', 'Performs a basic search with Shodan against the specified TOR relay.', 'self.basicSearchByRelay("OpenSSL 1.0.1", "80.80.80.80")'],
                         ['basicSearchByNickname', 'Performs a basic search with Shodan against the specified TOR NickName.', 'self.basicSearchByNickname("OpenSSL 1.0.1", "TORNickName")']
                        ])
        print table.draw() + "\n"
