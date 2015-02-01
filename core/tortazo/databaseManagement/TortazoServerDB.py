'''
Created on 11/09/2014

#Author: Adastra.
#twitter: @jdaanial

TortazoServerDB.py

TortazoServerDB is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

TortazoServerDB is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import sqlite3
from config import config
from config import database
from config import databasePlugins
from core.tortazo.data.TorNodeData import TorNodeData, TorNodePort
from core.tortazo.databaseManagement.ITortazoDatabase import ITortazoDatabase
from datetime import datetime
import sys
import zlib
import psycopg2
import os

class TortazoSQLiteDB(ITortazoDatabase):

    def connect(self):
        dbFile = config.resource_path(os.path.join(database.databaseName))
        self.connection = sqlite3.connect(dbFile)
        self.cursor = self.connection.cursor()


    def initDatabase(self):
        if self.connection is None:
            self.connect()
        self.connection.execute(database.createTableTorNodeData  )
        self.connection.execute(database.createTableTorNodePort )
        self.connection.execute(database.createTableScan )
        self.connection.execute(database.createTableOnionRepositoryProgress )
        self.connection.execute(database.createTableOnionRepositoryResponses )
        self.connection.execute(database.createTableBotnetNode )
        self.connection.execute(database.createTableBotnetGeolocation )
        self.connection.execute(database.createTableTorNodeGeolocation )

        self.connection.execute(databasePlugins.createTableCrawlerPluginPage )
        self.connection.execute(databasePlugins.createTableCrawlerPluginImage )        
        self.connection.execute(databasePlugins.createTableCrawlerPluginPageImage )        
        self.connection.execute(databasePlugins.createTableCrawlerPluginForm )        
        self.connection.execute(databasePlugins.createTableCrawlerPluginFormControl )        

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          DATABASE FUNCTIONS FOR INFO. GATHERING MODE                                                                                   ####
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
        totalUniqueNodes = len(torNodeData)

        for nodeData in torNodeData:
            #Check the record before store.
            self.cursor.execute(database.checkTorNodeData, (nodeData.host, nodeData.nickName))
            if self.cursor.fetchone()[0] > 0:
                #Node scaned before.
                totalUniqueNodes = totalUniqueNodes-1
                continue
            node = (nodeData.host, nodeData.state, nodeData.reason, nodeData.nickName, nodeData.fingerprint, nodeData.torVersion.version_str, nodeData.contactData, nodeData.operatingSystem, scanId)
            #Insert a TorNodeDataRecord.
            self.cursor.execute(database.insertTorNodeData, node)
            self.cursor.execute(database.nextIdHostNodeData)
            nodeId = self.cursor.fetchone()[0]
            self.insertTorNodeGeolocation(nodeId, nodeData)
            for openPort in nodeData.openPorts:
                opened = (openPort.state, openPort.reason, openPort.port, openPort.name, openPort.version, nodeId)
                #Insert a TorNodePort
                self.cursor.execute(database.insertTorNodePort, opened)


            for closedPort in nodeData.closedFilteredPorts:
                #Insert a TorNodePort
                closedFiltered = (closedPort.state, closedPort.reason, closedPort.port, closedPort.name, closedPort.version, nodeId)
                self.cursor.execute(database.insertTorNodePort, closedFiltered)
                torNodeId = self.cursor.lastrowid
        if totalUniqueNodes != len(torNodeData):
            #Some nodes were scanned before. Updating the number of new relays found in this scan.
            self.cursor.execute(database.updateTorScan, (totalUniqueNodes,scanId,) )                

        self.connection.commit()

    def insertTorNodeGeolocation(self, torNodeId, torNodeData):
        import pygeoip
        gi = pygeoip.GeoIP(config.geoLiteDB)
        recordAddress = gi.record_by_addr(torNodeData.host)
        if recordAddress is not None:
            longitude = recordAddress['longitude']
            latitude = recordAddress['latitude']
            geolocation = (torNodeId,latitude,longitude)
            self.cursor.execute(database.insertTorNodeGeolocation, geolocation)


    def cleanDatabaseState(self):
        try:
            if self.cursor is None:
                self.initDatabase()
            self.cursor.execute(database.truncateTableBotnetGeolocation)
            self.cursor.execute(database.truncateTableTorNodeGeolocation)    
            self.cursor.execute(database.truncateTorNodePort)
            self.cursor.execute(database.truncateTorNodeData)
            self.cursor.execute(database.truncateTorScan)
            self.cursor.execute(database.truncateOnionRepositoryProgress)
            self.cursor.execute(database.truncateOnionRepositoryResponses)

            #DeepWebPlugin tables.
            self.cursor.execute(databasePlugins.truncateCrawlerPluginFormControl)
            self.cursor.execute(databasePlugins.truncateCrawlerPluginForm)
            self.cursor.execute(databasePlugins.truncateCrawlerPluginPageImage)
            self.cursor.execute(databasePlugins.truncateCrawlerPluginImage)
            self.cursor.execute(databasePlugins.truncateCrawlerPluginPage)

            self.connection.commit()
        except Exception, e:
            print e.__doc__
            print e.message
            print "Unexpected error:", sys.exc_info()[0]


    def insertOnionRepositoryResult(self, onionAddress, responseCode, responseHeaders, onionDescription, serviceType):
        if self.cursor is None:
            self.initDatabase()
        try:
            responseHiddenService = (onionAddress, responseCode, responseHeaders, onionDescription, serviceType)
            self.cursor.execute(database.insertOnionRepositoryResponses, responseHiddenService)
        except Exception as e:
            pass
        finally:
            self.connection.commit()

    def searchOnionRepositoryProgress(self, partialOnionAddress, validChars):
        if self.cursor is None:
            self.initDatabase()
        self.cursor.execute(database.selectOnionRepositoryProgress, (partialOnionAddress, validChars))
        values = self.cursor.fetchone()
        if values == None:
            return (0, datetime.now(), 0, 0, 0, 0)
        id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet = values
        return (id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet)


    def insertOnionRepositoryProgress(self, onionAddress, validChars, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet, finished=False):
        endDate = None
        if finished:
            endDate = datetime.now()

        if self.cursor is None:
            self.initDatabase()

        self.cursor.execute(database.selectOnionRepositoryProgress, (onionAddress, validChars) )

        values = self.cursor.fetchone()
        if values is not None:
            progressId = values[0]
            if progressId > 0:
                self.cursor.execute(database.updateOnionRepositoryProgress, (endDate, progressFirstQuartet,progressSecondQuartet,progressThirdQuartet,progressFourthQuartet, progressId))
        else:
            self.cursor.execute(database.insertOnionRepositoryProgress, (onionAddress, validChars, datetime.now(), endDate, progressFirstQuartet,progressSecondQuartet,progressThirdQuartet,progressFourthQuartet))
        self.connection.commit()

    def searchOnionRepository(self, start=1, maxResults=30):
        onionAddresses = []
        if self.cursor is None:
            self.initDatabase()

        self.cursor.execute(database.selectOnionRepositoryResponses, (maxResults, start) )
        for row in self.cursor.fetchall():
            onionAddress, responseCode, responseHeaders,onionDescription, serviceType = row
            onionAddresses.append( (onionAddress, responseCode, responseHeaders,onionDescription, serviceType) )
        return  onionAddresses

    def countOnionRepositoryResponses(self):
        if self.cursor is None:
            self.initDatabase()
        self.cursor.execute(database.countOnionRepositoryResponses)
        return self.cursor.fetchone()[0]

    def searchBotnetNode(self, address):
        if self.cursor is None:
            self.initDatabase()
        if address is not None:
            self.cursor.execute(database.selectBotnetNode, (address,))
            results = self.cursor.fetchone() #Returns none if empty set.
            return results
        return None

    def insertBotnetNode(self, address, user, password, port, nickname, serviceType):
        if self.cursor is None:
            self.initDatabase()
        try:
            bot = (address, user, password, port, nickname, serviceType)
            self.cursor.execute(database.insertBotnetNode, bot)
            self.cursor.execute(database.nextIdBotnetNode)
            botId = self.cursor.fetchone()[0]

            self.insertBotnetGeolocation(botId, address)
            self.connection.commit()
        except Exception as e:
            pass

    def insertBotnetGeolocation(self, botId, address):
        import pygeoip
        gi = pygeoip.GeoIP(config.geoLiteDB)
        recordAddress = gi.record_by_addr(address)
        longitude = recordAddress['longitude']
        latitude = recordAddress['latitude']
        geolocation = (botId,latitude,longitude)
        self.cursor.execute(database.insertBotnetGeolocation, geolocation)

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
        self.cursor.execute(databasePlugins.createTableCrawlerPluginPage)
        self.cursor.execute(databasePlugins.createTableCrawlerPluginImage)
        self.cursor.execute(databasePlugins.createTableCrawlerPluginPageImage)
        self.cursor.execute(databasePlugins.createTableCrawlerPluginForm)
        self.cursor.execute(databasePlugins.createTableCrawlerPluginFormControl)



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
        data = (title, url, pageParentId, buffer(zlib.compress(body)), str(headers))
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
                    self.cursor.execute(databasePlugins.insertCrawlerPluginPageFormControl, (formId, buffer(zlib.compress(controlName)), buffer(zlib.compress(controlType)), buffer(zlib.compress(controlValue)), ) )
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



class TortazoPostgreSQL(ITortazoDatabase):

    def connect(self):
        self.connection = psycopg2.connect("dbname='%s' user='%s' host='%s' port='%s' password='%s'" %(config.dbName,config.dbUser, config.dbServer, config.dbPort, config.dbPass))
        self.cursor = self.connection.cursor()


    def initDatabase(self):
        if self.connection is None:
            self.connect()
        self.cursor.execute(database.createTableScanServerDB)
        self.cursor.execute(database.createTableTorNodeDataServerDB)
        self.cursor.execute(database.createTableTorNodePortServerDB )
        self.cursor.execute(database.createTableOnionRepositoryProgressServerDB)
        self.cursor.execute(database.createTableOnionRepositoryResponsesServerDB)
        self.cursor.execute(database.createTableBotnetNodeServerDB)
        self.cursor.execute(database.createTableBotnetGeolocationServerDB)
        self.cursor.execute(database.createTableTorNodeGeolocationServerDB)

        self.cursor.execute(databasePlugins.createTableCrawlerPluginPageServerDB )
        self.cursor.execute(databasePlugins.createTableCrawlerPluginImageServerDB )        
        self.cursor.execute(databasePlugins.createTableCrawlerPluginPageImageServerDB )        
        self.cursor.execute(databasePlugins.createTableCrawlerPluginFormServerDB )        
        self.cursor.execute(databasePlugins.createTableCrawlerPluginFormControlServerDB )      

        self.connection.commit()

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
        
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          DATABASE FUNCTIONS FOR INFO. GATHERING MODE                                                                                   ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

    def searchExitNodes(self, numberOfScans, scanIdentifier):
        if self.cursor is None:
            self.initDatabase()
        exitNodes = []
        if scanIdentifier is None:
            self.cursor.execute(database.selectTorScanServerDB, (numberOfScans,))
        else:
            self.cursor.execute(database.selectTorScanIdentifierServerDB, (scanIdentifier,))

        for row in self.cursor.fetchall():
            scanId, scanDate = row
            self.cursor.execute(database.selectTorNodeDataServerDB, (scanId,))
            for node in  self.cursor.fetchall():
                torNodeId, host, state, reason, nickName = node
                nodeData = TorNodeData()
                nodeData.id = torNodeId
                nodeData.host = host
                nodeData.state = state
                nodeData.reason = reason
                nodeData.nickName = nickName
                self.cursor.execute(database.selectTorNodePortServerDB, (torNodeId,) )
                for port in self.cursor.fetchall():
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
        self.cursor.execute(database.insertTorScanServerDB, (datetime.now(), len(torNodeData)) )
        scanId = self.cursor.fetchone()[0]
        totalUniqueNodes = len(torNodeData)

        for nodeData in torNodeData:
            #Check the record before store.
            self.cursor.execute(database.checkTorNodeDataServerDB, (nodeData.host, nodeData.nickName))
            if self.cursor.fetchone()[0] > 0:
                #Node scaned before.
                totalUniqueNodes = totalUniqueNodes-1
                continue
            node = (nodeData.host, nodeData.state, nodeData.reason, nodeData.nickName, nodeData.fingerprint, nodeData.torVersion.version_str, nodeData.contactData, nodeData.operatingSystem, scanId)
            #Insert a TorNodeDataRecord.
            self.cursor.execute(database.insertTorNodeDataServerDB, node)
            self.cursor.execute(database.nextIdHostNodeDataServerDB)
            nodeId = self.cursor.fetchone()[0]
            self.insertTorNodeGeolocation(nodeId,nodeData)
            for openPort in nodeData.openPorts:
                opened = (openPort.state, openPort.reason, openPort.port, openPort.name, openPort.version, nodeId)
                #Insert a TorNodePort
                self.cursor.execute(database.insertTorNodePortServerDB, opened)

            for closedPort in nodeData.closedFilteredPorts:
                #Insert a TorNodePort
                closedFiltered = (closedPort.state, closedPort.reason, closedPort.port, closedPort.name, closedPort.version, nodeId)
                self.cursor.execute(database.insertTorNodePortServerDB, closedFiltered)

        if totalUniqueNodes != len(torNodeData):
            #Some nodes were scanned before. Updating the number of new relays found in this scan.
            self.cursor.execute(database.updateTorScanServerDB, (totalUniqueNodes,scanId,) )


        self.connection.commit()
        self.cursor.close()
        self.connection.close()


    def insertTorNodeGeolocation(self, torNodeId, torNodeData):
        import pygeoip
        gi = pygeoip.GeoIP(config.geoLiteDB)
        recordAddress = gi.record_by_addr(torNodeData.host)
        if recordAddress is not None:
            longitude = recordAddress['longitude']
            latitude = recordAddress['latitude']
            geolocation = (torNodeId,latitude,longitude)
            self.cursor.execute(database.insertTorNodeGeolocationServerDB, geolocation)


    def cleanDatabaseState(self):
        try:
            if self.cursor is None:
                self.initDatabase()

            self.cursor.execute(database.truncateBotnetGeolocationServerDB)
            self.cursor.execute(database.truncateTorNodeGeolocationServerDB)
            self.cursor.execute(database.truncateTorNodePortServerDB)
            self.cursor.execute(database.truncateTorNodeDataServerDB)
            self.cursor.execute(database.truncateTorScanServerDB)
            self.cursor.execute(database.truncateOnionRepositoryProgressServerDB)
            self.cursor.execute(database.truncateOnionRepositoryResponsesServerDB)

            #DeepWebPlugin tables.
            self.cursor.execute(databasePlugins.truncateCrawlerPluginFormControl)
            self.cursor.execute(databasePlugins.truncateCrawlerPluginForm)
            self.cursor.execute(databasePlugins.truncateCrawlerPluginPageImage)
            self.cursor.execute(databasePlugins.truncateCrawlerPluginImage)
            self.cursor.execute(databasePlugins.truncateCrawlerPluginPage)

            self.connection.commit()
            self.cursor.close()
            self.connection.close()

        except Exception, e:
            print e.__doc__
            print e.message
            print "Unexpected error:", sys.exc_info()[0]


    def insertOnionRepositoryResult(self, onionAddress, responseCode, responseHeaders, onionDescription, serviceType):
        if self.cursor is None:
            self.initDatabase()
        try:
            responseHiddenService = (onionAddress, responseCode, responseHeaders, onionDescription, serviceType)
            self.cursor.execute(database.insertOnionRepositoryResponsesServerDB, responseHiddenService)
            self.connection.commit()

        except psycopg2.IntegrityError as integrity:
            if 'duplicate key' in integrity.message:
                print "[-] Onion Address %s already created in database" %(onionAddress)
                self.connection.rollback()

        except Exception as ex:
            import sys
            print sys.exc_info()
            self.connection.rollback()

    def searchOnionRepositoryProgress(self, partialOnionAddress, validChars):
        if self.cursor is None:
            self.initDatabase()
        self.cursor.execute(database.selectOnionRepositoryProgressServerDB, (partialOnionAddress, validChars))
        values = self.cursor.fetchone()
        if values == None:
            return (0, datetime.now(), 0, 0, 0, 0)
        id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet = values
        return (id, startDate, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet)


    def insertOnionRepositoryProgress(self, onionAddress, validChars, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet, finished=False):
        endDate = None
        if finished:
            endDate = datetime.now()

        if self.cursor is None:
            self.initDatabase()

        self.cursor.execute(database.selectOnionRepositoryProgressServerDB, (onionAddress, validChars) )

        values = self.cursor.fetchone()
        if values is not None:
            progressId = values[0]
            if progressId > 0:
                self.cursor.execute(database.updateOnionRepositoryProgressServerDB, (endDate, progressFirstQuartet,progressSecondQuartet,progressThirdQuartet,progressFourthQuartet, progressId))
        else:
            self.cursor.execute(database.insertOnionRepositoryProgressServerDB, (onionAddress, validChars, datetime.now(), endDate, progressFirstQuartet,progressSecondQuartet,progressThirdQuartet,progressFourthQuartet))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


    def searchOnionRepository(self, start=1, maxResults=30):
        onionAddresses = []
        if self.cursor is None:
            self.initDatabase()

        self.cursor.execute(database.selectOnionRepositoryResponsesServerDB, (maxResults, start) )
        for row in self.cursor.fetchall():
            onionAddress, responseCode, responseHeaders,onionDescription, serviceType = row
            onionAddresses.append( (onionAddress, responseCode, responseHeaders,onionDescription, serviceType) )
        return  onionAddresses

    def countOnionRepositoryResponses(self):
        if self.cursor is None:
            self.initDatabase()
        self.cursor.execute(database.countOnionRepositoryResponsesServerDB)
        return self.cursor.fetchone()[0]

    def searchBotnetNode(self, address):
        if self.cursor is None:
            self.initDatabase()
        if address is not None:
            self.cursor.execute(database.selectBotnetNodeServerDB, (address,))
            results = self.cursor.fetchone() #Returns none if empty set.
            return results
        return None

    def insertBotnetNode(self, address, user, password, port, nickname, serviceType):
        if self.cursor is None:
            self.initDatabase()
        try:
            bot = (address, user, password, port, nickname, serviceType)
            self.cursor.execute(database.insertBotnetNodeServerDB, bot)
            self.cursor.execute(database.nextIdBotnetNodeServerDB)
            botId = self.cursor.fetchone()[0]
            self.insertBotnetGeolocation(botId,address)
            self.connection.commit()
        except Exception as e:
            import sys
            print sys.exc_info()
            return False

    def insertBotnetGeolocation(self, botId, address):
        import pygeoip
        gi = pygeoip.GeoIP(config.geoLiteDB)
        recordAddress = gi.record_by_addr(address)
        longitude = None
        latitude = None
        if recordAddress:
            longitude = recordAddress['longitude']
            latitude = recordAddress['latitude']

        geolocation = (botId,latitude,longitude)
        self.cursor.execute(database.insertBotnetGeolocationServerDB, geolocation)

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
        self.cursor.execute(databasePlugins.createTableCrawlerPluginPageServerDB)
        self.cursor.execute(databasePlugins.createTableCrawlerPluginImageServerDB)
        self.cursor.execute(databasePlugins.createTableCrawlerPluginPageImageServerDB)
        self.cursor.execute(databasePlugins.createTableCrawlerPluginFormServerDB)
        self.cursor.execute(databasePlugins.createTableCrawlerPluginFormControlServerDB)


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
        data = (title, url, pageParentId, buffer(zlib.compress(body)), str(headers))
        self.cursor.execute(databasePlugins.insertCrawlerPluginPageServerDB, data )
        linkId = self.cursor.lastrowid
        self.connection.commit()
        return linkId

    def insertImages(self, page, pageId):
        if self.cursor is None:
            self.initDatabase()
        if page.has_key('imagesSrc'):
            for image in page['imagesSrc']:

                self.cursor.execute(databasePlugins.existsImageByPageServerDB, (image,pageId))
                if self.cursor.fetchone()[0] > 0:
                    continue
                else:
                    self.cursor.execute(databasePlugins.insertCrawlerPluginImageServerDB, (image, ) )
                    imageId = self.cursor.lastrowid
                    self.cursor.execute(databasePlugins.insertCrawlerPluginPageImageServerDB, (pageId, imageId, ) )
        self.connection.commit()


    def insertForms(self, page, pageId):
        if self.cursor is None:
            self.initDatabase()

        if page.has_key('forms'):
            for formName in page['forms'].keys():
                self.cursor.execute(databasePlugins.existsFormByPageServerDB, (formName, pageId, ))
                if self.cursor.fetchone()[0] > 0:
                    continue
                self.cursor.execute(databasePlugins.insertCrawlerPluginPageFormServerDB, (formName, pageId, ) )
                formId = self.cursor.lastrowid
                for control in page['forms'][formName]:
                    (controlName, controlType, controlValue) = control
                    self.cursor.execute(databasePlugins.insertCrawlerPluginPageFormControlServerDB, (formId, buffer(zlib.compress(controlName)), buffer(zlib.compress(controlType)), buffer(zlib.compress(controlValue)), ) )
        self.connection.commit()


    def existsPageByUrl(self, url):
        if self.cursor is None:
            self.initDatabase()
        if url is not None:
            self.cursor.execute(databasePlugins.existsPageByUrlServerDB, (url,))
            if self.cursor.fetchone()[0] > 0:
                return True
        return False

    def searchPageByUrl(self, url):
        if self.cursor is None:
            self.initDatabase()
        if url is not None:
            self.cursor.execute(databasePlugins.searchPageByUrlServerDB, (url,))
            pageId = self.cursor.fetchone()[0]
            return pageId
        return None


class TortazoMySQL(ITortazoDatabase):
    pass