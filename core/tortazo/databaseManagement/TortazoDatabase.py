'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

TortazoDatabase.py

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

import sqlite3
from config import database
from config import databasePlugins
from core.tortazo.data.TorNodeData import TorNodeData, TorNodePort
from datetime import datetime
import sys


class TortazoDatabase:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(database.databaseName)
        self.cursor = self.connection.cursor()


    def initDatabase(self):
        if self.connection is None:
            self.connect()
        self.connection.execute(database.createTableTorNodeData)
        self.connection.execute(database.createTableTorNodePort)
        self.connection.execute(database.createTableScan)
        self.connection.execute(database.createTableOnionRepositoryProgress)
        self.connection.execute(database.createTableOnionRepositoryResponses)

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          DATABASE FUNCTIONS FOR INFO. GATERHING MODE                                                                                   ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

    def searchExitNodes(self, numberOfScans, scanIdentifier):
        if self.cursor is None:
            self.initDatabase()
        exitNodes = []
        if scanIdentifier is None:
            self.cursor.execute(database.selectTorScan, (numberOfScans,))
        else:
            self.cursor.execute(database.selectTorScanIdentifier, (scanIdentifier,))

        for row in self.cursor.fetchall():
            scanId, scanDate = row
            self.cursor.execute(database.selectTorNodeData, (scanId,))
            for node in  self.cursor.fetchall():
                torNodeId, host, state, reason, nickName = node
                nodeData = TorNodeData()
                nodeData.id = torNodeId
                nodeData.host = host
                nodeData.state = state
                nodeData.reason = reason
                nodeData.nickName = nickName
                ports = self.cursor.execute(database.selectTorNodePort, (torNodeId,) )
                for port in ports.fetchall():
                    (portId, portState, portReason, portNumber, portName, portVersion, torNode) = port
                    nodePort = TorNodePort()
                    nodePort.id = portId
                    nodePort.state = portState
                    nodePort.reason = portReason
                    nodePort.port = portNumber
                    nodePort.name = portName
                    nodePort.version = portVersion
                    nodePort.torNodeId = torNode
                    if "open" in portState:
                        nodeData.openPorts.append(nodePort)
                    else:
                        nodeData.closedFilteredPorts.append(nodePort)
                exitNodes.append(nodeData)
        return exitNodes


    def insertExitNode(self, torNodeData):
        '''
        Insert the Tor Structure found.
        '''
        if self.cursor is None:
            self.initDatabase()

        #Insert the Scan record.
        self.cursor.execute(database.insertTorScan, (datetime.now(), len(torNodeData)))
        scanId = self.cursor.lastrowid

        for nodeData in torNodeData:
            #Check the record before store.
            self.cursor.execute(database.checkTorNodeData, (nodeData.host, nodeData.nickName))
            if self.cursor.fetchone()[0] > 0:
                #Node scaned before.
                continue
            node = (nodeData.host, nodeData.state, nodeData.reason, nodeData.nickName, nodeData.fingerprint, nodeData.torVersion.version_str, nodeData.contactData, scanId)
            #Insert a TorNodeDataRecord.
            self.cursor.execute(database.insertTorNodeData, node)

            self.cursor.execute(database.nextIdHostNodeData)
            nodeId = self.cursor.fetchone()[0]
            for openPort in nodeData.openPorts:
                opened = (openPort.state, openPort.reason, openPort.port, openPort.name, openPort.version, nodeId)
                #Insert a TorNodePort
                self.cursor.execute(database.insertTorNodePort, opened)

            for closedPort in nodeData.closedFilteredPorts:
                #Insert a TorNodePort
                closedFiltered = (closedPort.state, closedPort.reason, closedPort.port, closedPort.name, closedPort.version, nodeId)
                self.cursor.execute(database.insertTorNodePort, closedFiltered)
        self.connection.commit()

    def cleanDatabaseState(self):
        try:
            if self.cursor is None:
                self.initDatabase()
            self.cursor.execute(database.truncateTorNodePort)
            self.cursor.execute(database.truncateTorNodeData)
            self.cursor.execute(database.truncateTorScan)
            self.cursor.execute(database.truncateOnionRepositoryProgress)
            self.cursor.execute(database.truncateOnionRepositoryResponses)

            #DeepWebPlugin tables.
            self.cursor.execute(database.truncateCrawlerPluginFormControl)
            self.cursor.execute(database.truncateCrawlerPluginForm)
            self.cursor.execute(database.truncateCrawlerPluginPageImage)
            self.cursor.execute(database.truncateCrawlerPluginImage)
            self.cursor.execute(database.truncateCrawlerPluginPage)

            self.connection.commit()
        except Exception, e:
            print e.__doc__
            print e.message
            print "Unexpected error:", sys.exc_info()[0]


    def insertOnionRepositoryResult(self, onionAddress, responseCode, responseHeaders ):
        if self.cursor is None:
            self.initDatabase()
        responseHiddenService = (onionAddress, responseCode, responseHeaders)
        self.cursor.execute(database.insertOnionRepositoryResponses, responseHiddenService)
        self.connection.commit()

    def searchOnionRepositoryProgress(self, partialOnionAddress):
        if self.cursor is None:
            self.initDatabase()
        self.cursor.execute(database.selectOnionRepositoryProgress, (partialOnionAddress,))
        if self.cursor.fetchone() == None:
            return (0, datetime.now(), 0, 0, 0, 0)
        id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet = self.cursor.fetchone()
        return (id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet)



################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          DATABASE FUNCTIONS FOR "deepWebCrawlerPlugin".                                                                                ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

    def initDatabaseDeepWebCrawlerPlugin(self):
        if self.connection is None:
            self.connect()
        self.connection.execute(databasePlugins.createTableCrawlerPluginPage)
        self.connection.execute(databasePlugins.createTableCrawlerPluginImage)
        self.connection.execute(databasePlugins.createTableCrawlerPluginPageImage)
        self.connection.execute(databasePlugins.createTableCrawlerPluginForm)
        self.connection.execute(databasePlugins.createTableCrawlerPluginFormControl)


    def insertPage(self, page):
        if self.cursor is None:
            self.initDatabase()
        title = ''
        url = ''
        pageParentId = None
        body = ''
        headers = ''

        if page.has_key('title'):
            title = page['title']
        if page.has_key('url'):
            url = page['url']
        if page.has_key('body'):
            body = page['body']
        if page.has_key('headers'):
            headers = page['headers']


        if page.has_key('pageParent'):
            pageParent = page['pageParent']
            if self.existsPageByUrl(pageParent['url']):
                pageParentId = self.searchPageByUrl(pageParent['url'])
            else:
                pageParentId = self.insertPage(pageParent)
        data = (title, url, pageParentId, body, str(headers))
        self.cursor.execute(databasePlugins.insertCrawlerPluginPage, data )
        linkId = self.cursor.lastrowid
        self.connection.commit()
        return linkId

    def insertImages(self, page, pageId):
        if self.cursor is None:
            self.initDatabase()
        if page.has_key('imagesSrc'):
            for image in page['imagesSrc']:

                self.cursor.execute(databasePlugins.existsImageByPage, (image,pageId))
                if self.cursor.fetchone()[0] > 0:
                    continue
                else:
                    self.cursor.execute(databasePlugins.insertCrawlerPluginImage, (image, ) )
                    imageId = self.cursor.lastrowid
                    self.cursor.execute(databasePlugins.insertCrawlerPluginPageImage, (pageId, imageId, ) )
        self.connection.commit()

    def insertForms(self, page, pageId):
        if self.cursor is None:
            self.initDatabase()

        if page.has_key('forms'):
            for formName in page['forms'].keys():
                self.cursor.execute(databasePlugins.existsFormByPage, (formName, pageId, ))
                if self.cursor.fetchone()[0] > 0:
                    continue
                self.cursor.execute(databasePlugins.insertCrawlerPluginPageForm, (formName, pageId, ) )
                formId = self.cursor.lastrowid
                for control in page['forms'][formName]:
                    (controlName, controlType, controlValue) = control
                    self.cursor.execute(databasePlugins.insertCrawlerPluginPageFormControl, (formId, controlName, controlType, controlValue, ) )
        self.connection.commit()

    def existsPageByUrl(self, url):
        if self.cursor is None:
            self.initDatabase()
        if url is not None:
            self.cursor.execute(databasePlugins.existsPageByUrl, (url,))
            if self.cursor.fetchone()[0] > 0:
                return True
        return False

    def searchPageByUrl(self, url):
        if self.cursor is None:
            self.initDatabase()
        if url is not None:
            self.cursor.execute(databasePlugins.searchPageByUrl, (url,))
            pageId = self.cursor.fetchone()[0]
            return pageId
        return None
