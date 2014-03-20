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
        self.connection.execute(config.createTableScan)
        self.connection.execute(config.createTableTorNodeData)
        self.connection.execute(config.createTableTorNodePort)
        self.connection.execute(config.createTableNodeHistory)
        self.connection.execute(config.createTablePortHistory)

    def searchExitNodes(self):
        if self.cursor is None:
            self.initDatabase()
        exitNodes = []
        for row in self.cursor.execute(config.selectTorNodeData):
            id, host, state, reason, nickName = row
            nodeData = TorNodeData()
            nodeData.id = id
            nodeData.host = host
            nodeData.state = state
            nodeData.reason = reason
            nodeData.nickName = nickName
            torNode = (id, )
            ports = self.cursor.execute(config.selectTorNodePort, torNode)
            for port in ports:
                (id, state, reason, port, name, version, torNode) = port
                nodePort = TorNodePort()
                nodePort.id = id
                nodePort.state = state
                nodePort.reason = reason
                nodePort.port = port
                nodePort.name = name
                nodePort.version = version
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

        scans = self.cursor.execute(config.selectTorScan)
        nodeId = 1
        portId = 1
        if scans.rowcount > 0:
            for scan in scans: #There's just one scan (the last executed.)
                nodeId, portId = scan
                newScan = (int(nodeId)+len(torNodeData), int(portId)+len(torNodeData.closedFilteredPorts)+len(torNodeData.openPorts), datetime.now(),)
                self.cursor.execute(config.updateTorScan, newScan)

        else:
            firstScan = (nodeId, portId, datetime.now(),)
            self.cursor.execute(config.insertTorScan, firstScan)
            self.connection.commit()


        for nodeData in torNodeData:
            node = (nodeId, nodeData.host, nodeData.state, nodeData.reason, nodeData.nickName)
            self.cursor.execute(config.insertTorNodeData, node)
            for openPort in nodeData.openPorts:
                opened = (portId, openPort.state, openPort.reason, openPort.port, openPort.name, openPort.version, nodeId)
                self.cursor.execute(config.insertTorNodePort, opened)
                portId += 1
            for closedPort in nodeData.closedFilteredPorts:
                closedFiltered = (portId, closedPort.state, closedPort.reason, closedPort.port, closedPort.name, closedPort.version, nodeId)
                self.cursor.execute(config.insertTorNodePort, closedFiltered)
                portId += 1
            nodeId += 1
        self.connection.commit()

    def cleanDatabaseState(self):
        if self.cursor is None:
            self.initDatabase()
        self.cursor.execute(config.insertTorNodeDataHistory)
        self.cursor.execute(config.insertTorNodePortHistory)
        self.cursor.execute(config.truncateTorNodePort)
        self.cursor.execute(config.truncateTorNodeData)



