# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

maliciousHiddenServicePlugin.py

maliciousHiddenServicePlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

maliciousHiddenServicePlugin is distributed in the hope that it will be useful,
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
from twisted.internet import reactor
import txtorcon
import os
from core.tortazo.exceptions.PluginException import PluginException
from plugins.utils.validations.Validator import is_valid_port, is_valid_ipv4_address, is_valid_ipv6_address, showTrace
from config import config as tortazoConfig
from plugins.attack.utils.HiddenServices import SimpleCustomWebServer, SimpleWebServer
from twisted.scripts.twistd import run
from sys import argv

'''
Main class for the plugin.
'''
class maliciousHiddenServicePlugin(BasePlugin):
    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'maliciousHiddenServicePlugin')
        self.setPluginDetails('hiddenService', 'Creates a malicious hidden service in TOR network and tries to de-anonimyze the users.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] maliciousHiddenServicePlugin Initialized!")
        self.pluginConfigs= {}
        #import sys
        #self.info("Caller", sys._getframe().f_back.f_code.co_name)

    def processPluginArguments(self):
        BasePlugin.processPluginArguments(self)

    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] maliciousHiddenServicePlugin Destroyed!")

    '''
    Private function used to validate the values for the TOR configuration.
    '''
    def __validate(self, serviceInterface, hiddenservicePort, socksPort, orPort, servicePort):
        if is_valid_ipv4_address(serviceInterface) == False and is_valid_ipv6_address(serviceInterface) == False:
            pluginException = PluginException(message='The Service Interface is invalid. Try to use the default value without specify the parameter "serviceInterface" ',
                                  trace="__validate with args serviceInterface=%s, hiddenservicePort, socksPort, orPort, servicePort" %(str(serviceInterface), str(hiddenservicePort), str(socksPort), str(orPort), str(servicePort)),
                                  plugin="maliciousHiddenServicePlugin", method="__validate")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                self.info('[-] The Service Interface is invalid. Try to use the default value without specify the parameter "serviceInterface". ')
                raise pluginException


        if is_valid_port(hiddenservicePort) == False:
            pluginException = PluginException(message='The hidden service port is invalid.',
                                              trace="__validate with args serviceInterface=%s, hiddenservicePort, socksPort, orPort, servicePort" %(str(serviceInterface), str(hiddenservicePort), str(socksPort), str(orPort), str(servicePort)),
                                              plugin="maliciousHiddenServicePlugin", method="__validate")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                self.info("[-] The hidden service port is invalid. ")
                raise pluginException

        if is_valid_port(socksPort) == False:
            pluginException = PluginException(message='The socks port is invalid.',
                                              trace="__validate with args serviceInterface=%s, hiddenservicePort, socksPort, orPort, servicePort" %(str(serviceInterface), str(hiddenservicePort), str(socksPort), str(orPort), str(servicePort)),
                                              plugin="maliciousHiddenServicePlugin", method="__validate")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                self.info("[-] The socks port is invalid. ")
                raise pluginException


        if is_valid_port(orPort) == False:
            pluginException = PluginException(message='The OR port is invalid.',
                                              trace="__validate with args serviceInterface=%s, hiddenservicePort, socksPort, orPort, servicePort" %(str(serviceInterface), str(hiddenservicePort), str(socksPort), str(orPort), str(servicePort)),
                                              plugin="maliciousHiddenServicePlugin", method="__validate")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                self.info("[-] The OR port is invalid. ")
                raise pluginException

        if is_valid_port(servicePort) == False:
            pluginException = PluginException(message='The Service port is invalid.',
                                              trace="__validate with args serviceInterface=%s, hiddenservicePort, socksPort, orPort, servicePort" %(str(serviceInterface), str(hiddenservicePort), str(socksPort), str(orPort), str(servicePort)),
                                              plugin="maliciousHiddenServicePlugin", method="__validate")
            if self.runFromInterpreter:
                showTrace(pluginException)
                return
            else:
                self.info("[-] The Service port is invalid. ")
                raise pluginException


    '''
    Private function used to create a valid TOR configuration reference. This configuration will be used to start TOR using TxTorCon utilities.
    '''
    def __configureTOR(self, serviceInterface, hiddenservicePort, hiddenserviceDir, socksPort, orPort, servicePort):
        try:
            self.__validate(serviceInterface, hiddenservicePort, socksPort, orPort, servicePort)
        except PluginException as pluginExc:
            raise pluginExc
        self.hiddenservicePort = hiddenservicePort
        config = txtorcon.TorConfig()
        config.SOCKSPort = socksPort
        config.ORPort = orPort
        config.HiddenServices = [txtorcon.HiddenService(config, hiddenserviceDir, ["%s %s:%s" %(str(hiddenservicePort), serviceInterface, str(servicePort))] )]
        config.save()
        return config


    '''
    Private Function used to show the log messages generated by the TOR process.
    '''
    def __updates(self,prog, tag, summary):
        self.info("%d : %s" % (prog, summary))

    '''
    Private Function used to show the log messages generated when the TOR process has been bootstraped successfully.
    '''
    def __setup_complete(self, configTor, proto):
        self.info("[+] TOR Startup completed!")
        onion_address = configTor.HiddenServices[0].hostname
        self.info("[+] Hidden service running at: ")
        self.info("http://%s (port %d)" % (onion_address, self.hiddenservicePort))
        self.info("[+] Directory for the hidden service is at: %s" %(configTor.HiddenServices[0].dir))
        self.info("[+] If your hidden service is an HTTP Server, you should be able to visit it via: torsocks lynx http://%s OR using chromium-browser --proxy-server=socks5://127.0.0.1:9152" %(onion_address))

    '''
    Private Function used to show the log messages generated when the TOR process has been failed in the bootstraped process.
    '''
    def __setup_failed(self,arg):
        self.info("SETUP FAILED", arg)
        reactor.stop()

    '''
    Private Function used to create a temporal directory for the hidden service.
    '''
    def __createTemporal(self):
        tempDir = tempfile.mkdtemp(prefix='torhiddenservice')
        reactor.addSystemEventTrigger('before', 'shutdown', functools.partial(txtorcon.util.delete_file_or_tree, tempDir))
        return tempDir

    '''
    Private Function used to start the TOR process using the configuration specified.
    '''
    def __startTOR(self, config):
        try:
            if config is None:
                return False
            d = txtorcon.launch_tor(config, reactor, progress_updates=self.__updates, )
        except txtorcon.TorNotFound as torBinaryNotFound:
            self.info("[-] Tor binary not found in the system path. Using the property 'torExecutablePath' located in the config/config.py file.")
            d = txtorcon.launch_tor(config, reactor, tor_binary=tortazoConfig.torExecutablePath, progress_updates=self.__updates, )

        d.addCallback(functools.partial(self.__setup_complete, config))
        d.addErrback(self.__setup_failed)
        reactor.run()


    '''
    Private Function used to start an HTTP hidden service with the specified arguments.
    '''
    #chromium-browser --proxy-server=socks5://127.0.0.1:9152
    def startHTTPHiddenService(self, serviceDir, servicePort=8080, hiddenserviceDir=None, hiddenservicePort=80, serviceInterface='127.0.0.1', socksPort=9152, orPort=9000, customContent=True):
        torConfig = None
        try:
            if hiddenserviceDir is None:
                temporalDir = self.__createTemporal()
                torConfig = self.__configureTOR(serviceInterface, hiddenservicePort, temporalDir, socksPort, orPort, servicePort)
            else:
                torConfig = self.__configureTOR(serviceInterface, hiddenservicePort, hiddenserviceDir, socksPort, orPort, servicePort)

            if customContent:
                webServer = SimpleCustomWebServer()
            else:
                webServer = SimpleWebServer()
            webServer.start(serviceDir, servicePort, serviceInterface)
        except PluginException as pluginExc:
            raise pluginExc

        return self.__startTOR(torConfig)

    def help(self):
        self.info("[*] Functions availaible available in the Plugin...")
        table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([25,20,20])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['startHTTPHiddenService', 'Starts an HTTP hidden service with the specified settings.', 'self.startSSHHiddenService(hiddenserviceDir="/home/hiddenService-http", serviceDir="/home/user/tortazo/plugins/attack/utils/hiddenServiceTest")'],
                        ])
        self.info(table.draw() + "\n")