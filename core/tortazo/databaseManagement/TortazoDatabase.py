# coding=utf-8
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
import config
from core.tortazo.data.TorNodeData import TorNodeData, TorNodePort
from datetime import datetime
import sys
class TortazoDatabase:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(config.databaseName)
        self.cursor = self.connection.cursor()


    def initDatabase(self):
        if self.connection is None:
            self.connect()
        self.connection.execute(config.createTableTorNodeData)
        self.connection.execute(config.createTableTorNodePort)
        self.connection.execute(config.createTableScan)

    def searchExitNodes(self, numberOfScans):
        if self.cursor is None:
            self.initDatabase()
        exitNodes = []
        self.cursor.execute(config.selectTorScan, (numberOfScans,))
        for row in self.cursor.fetchall():
            scanId, scanDate = row
            self.cursor.execute(config.selectTorNodeData, (scanId,))
            for node in  self.cursor.fetchall():
                torNodeId, host, state, reason, nickName = node
                nodeData = TorNodeData()
                nodeData.id = torNodeId
                nodeData.host = host
                nodeData.state = state
                nodeData.reason = reason
                nodeData.nickName = nickName
                ports = self.cursor.execute(config.selectTorNodePort, (torNodeId,) )
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
                    if "open" in state:
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
        self.cursor.execute(config.insertTorScan, (datetime.now(), len(torNodeData)))
        scanId = self.cursor.lastrowid

        for nodeData in torNodeData:
            node = (nodeData.host, nodeData.state, nodeData.reason, nodeData.nickName, scanId)
            #Insert a TorNodeDataRecord.
            self.cursor.execute(config.insertTorNodeData, node)
            nodeId = self.cursor.lastrowid

            for openPort in nodeData.openPorts:
                opened = (openPort.state, openPort.reason, openPort.port, openPort.name, openPort.version, nodeId)
                #Insert a TorNodePort
                self.cursor.execute(config.insertTorNodePort, opened)

            for closedPort in nodeData.closedFilteredPorts:
                #Insert a TorNodePort
                closedFiltered = (closedPort.state, closedPort.reason, closedPort.port, closedPort.name, closedPort.version, nodeId)
                self.cursor.execute(config.insertTorNodePort, closedFiltered)
        self.connection.commit()

    def cleanDatabaseState(self):
        try:
            if self.cursor is None:
                self.initDatabase()
            self.cursor.execute(config.truncateTorNodePort)
            self.cursor.execute(config.truncateTorNodeData)
            self.cursor.execute(config.truncateTorScan)
        except Exception, e:
            print e.__doc__
            print e.message
            print "Unexpected error:", sys.exc_info()[0]



