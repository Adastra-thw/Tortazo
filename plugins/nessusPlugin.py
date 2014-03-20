# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

simplePlugin.py

WorkerThread is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

WorkerThread is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.pluginManagement.BasePlugin import BasePlugin
import config
import requests
import httplib2
import urllib
from bs4 import BeautifulSoup
import json

class nessusPlugin(BasePlugin):
    '''
    This class uses PyNessus to connect and execute scans with nessus.
    '''

    #http://static.tenable.com/documentation/nessus_5.0_XMLRPC_protocol_guide.pdf
    '''
    >>> url = 'https://localhost:8834/login'
    >>> body = {'password' : 'peraspera', 'seq' : '100', 'login' : 'adastra', 'json' : '1'}
    >>> headers={'Host': 'localhost:8834', 'Content-type': 'application/x-www-form-urlencoded'}
    >>> response, content = h.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
    >>> response
    {'status': '200', 'content-length': '466', 'set-cookie': 'token=59233cb47877aeba5137becafd4fc4b01a680ea44e2ab019; path=/; expires=Sun, 17-Jan-2038 13:17:07 GMT; secure; HttpOnly', 'expires': 'Tue, 18 Mar 2014 22:56:51 GMT, 0', 'server': 'NessusWWW', 'cache-control': '', 'connection': 'close', 'pragma ': '', 'date': 'Tue, 18 Mar 2014 22:56:51 GMT', 'x-frame-options': 'DENY', 'content-type': 'text/xml'}
    >>> content
    '<?xml version="1.0" encoding="UTF-8"?>\n<reply>\n<seq>100</seq>\n<status>OK</status>\n<contents><token>59233cb47877aeba5137becafd4fc4b01a680ea44e2ab019</token>\n<server_uuid>8cb6d623-152c-d63f-4a03-b71d77e4c99c4cc6ff8bf3c2a30a</server_uuid>\n<plugin_set>201203211438</plugin_set>\n<loaded_plugin_set>201203211438</loaded_plugin_set>\n<scanner_boottime>1395181510</scanner_boottime>\n<msp>FALSE</msp>\n<user>\n<name>adastra</name>\n<admin>TRUE</admin>\n</user></contents>\n</reply>
    '''
    def __init__(self):
        BasePlugin.__init__(self)
        self.NESSUS_FUNCTIONS=['listPlugins','listPolicies','getPolicyByName',
                               'listReports','singleScan','scan','multiScan',
                               'downloadReport','findVulnerabilities']
        self.debug("[*] nessusPlugin Initialized!")
        self.url = "https://"+config.nessusHost+":"+str(config.nessusPort)
        self.body =   {'password' : config.nessusPass, 'seq' : config.nessusInitialSeq, 'login' : config.nessusUser, 'json' : '1'}
        self.headers= {'Host': config.nessusHost+":"+str(config.nessusPort), 'Content-type': 'application/x-www-form-urlencoded'}
        self.loginNessus()

    def __del__(self):
        self.debug("[*] nessusPlugin Destroyed!")
        self.logoutNessus()

    def requestNessus(self, url, data, headers):
        response = requests.post( url, data=data, headers=headers, verify=False)
        return json.loads(response.content)
        config.nessusInitialSeq += 1


    def loginNessus(self):
        #body = {'password' : 'peraspera', 'seq' : '100', 'login' : 'adastra'}
        #headers={'Host': 'localhost:8834', 'Content-type': 'application/x-www-form-urlencoded'}
        print self.requestNessus(self.url+'/login', data=self.body, headers=self.headers)

        '''h = httplib2.Http()
        url = 'https://localhost:8834/login'
        body = {'password' : 'peraspera', 'seq' : '100', 'login' : 'adastra', 'json' : '1'}
        headers={'Host': 'localhost:8834', 'Content-type': 'application/x-www-form-urlencoded'}
        response, content = h.request(url, 'POST', headers=headers, body=urllib.urlencode(body))
        print content
        '''

    def logoutNessus(self):
        self.body = {'seq' : config.nessusInitialSeq}
        print self.requestNessus(self.url+'/logout', data=self.body, headers=self.headers)

    def runPlugin(self):
        '''
        The most simplest plugin! Just prints the tor data structure.
        '''
        for argumentName in self.pluginArguments.keys():
            if argumentName in self.NESSUS_FUNCTIONS:
                nessusFunction = getattr(self, argumentName)
                if callable(nessusFunction):
                    if self.pluginArguments[argumentName] is not None and self.pluginArguments[argumentName] != "":
                        nessusFunction(self.pluginArguments[argumentName])
                    else:
                        nessusFunction()

    def listPlugins(self):
        print "list!"

    def listPolicies(self):
        pass

    def getPolicyByName(self, policyName):
        pass

    def listReports(self):
        pass

    def singleScan(self, scanName, target, policyId):
        pass

    def scan(self, scanName, policyId):
        pass

    def multiScan(self, scanName, targets, policyId):
        pass

    def downloadReport(self, reportId):
        pass

    def findVulnerabilities(self, target, pluginFamily, riskFactor):
        pass

    def help(self):
        self.info("[*] Help for plugin nessusPlugin: \n")
        self.info("[*][*]  Important: Some settings are readed from config.py. Change this file for your own needs.  \n")
        self.info("[*][*] Available Options: \n")
        self.info("[*][*]   listPlugins: List of plugins loaded. Arguments: None. \n")
        self.info("[*][*]   listPolicies: List of policies loaded. Arguments: None. \n")
        self.info("[*][*]   getPolicyByName: Get Policy ID by Name. Arguments: PolicyName.  \n")
        self.info("[*][*]   listReports: List of reports loaded.  \n")
        self.info("[*][*]   singleScan: scan a single TOR Node. Arguments: ScanName, IP-Address or DomainName of the target and Policy ID \n")
        self.info("[*][*]   scan: Scans the full list of TOR Nodes found. Arguments: ScanName and Policy ID \n")
        self.info("[*][*]   multiScan: Scans a sublist of the TOR Nodes found. Arguments: ScanName, sublist of TOR Nodes (IP-Addresses or DomainNames separated by '|') and Policy ID \n")
        self.info("[*][*]   downloadReport: Download a Report. Arguments: Report UUID \n")
        self.info("[*][*]   findVulnerabilities: . Arguments: Target, Risk Factor, Plugin Family \n")


