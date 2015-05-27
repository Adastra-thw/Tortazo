# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

TorNodeData.py

TorNodeData is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

TorNodeData is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
import json

class TorNodeScan:
    '''
    Tor Structure to save the scan information.
    '''
    def __init__(self):
        self.id = None
        self.scanDate = None
        self.numNodes = None 
        self.tortazoCommand = None
        self.scanFinished = None
        self.userIdentifier = None
        self.publicScan = False
        self.nodes = [] #List of TorNodeData objects    
        
    def toExport(self):
        export = {}
        if self.scanDate is not None:
            dateTimeAdapted = self.scanDate.adapted
            export["date"] = str(dateTimeAdapted.year)+":"+str(dateTimeAdapted.month)+":"+str(dateTimeAdapted.day)+":"+str(dateTimeAdapted.hour)+":"+str(dateTimeAdapted.minute)+":"+str(dateTimeAdapted.second)
        
        export["numnodes"] = self.numNodes
        export["command"] = self.tortazoCommand
        
        if self.scanFinished is not None:
            dateTimeAdapted = self.scanFinished.adapted
            export["finished"] = str(dateTimeAdapted.year)+":"+str(dateTimeAdapted.month)+":"+str(dateTimeAdapted.day)+":"+str(dateTimeAdapted.hour)+":"+str(dateTimeAdapted.minute)+":"+str(dateTimeAdapted.second)
        
        export["public"] = self.publicScan
        exportNodes = []
        for node in self.nodes:
            exportNodes.append(node.toExport())
        export["nodes"] = exportNodes
        return export


class TorNodeData:
    '''
    Tor Structure to save the Node information.
    '''
    def __init__(self):
        self.id = None
        self.host = None
        self.state = None
        self.reason = None
        self.openPorts = [] #List of TorNodePort objects
        self.closedFilteredPorts = [] #List of TorNodePort objects
        self.nickName = None
        self.fingerprint = None
        self.torVersion = None
        self.contactData = None
        self.operatingSystem = None
        self.nodeLatitude = None
        self.nodeLongitude = None
        
    def toExport(self):
        export = {}
        export["host"] = self.host
        export["state"] = self.state
        export["reason"] = self.reason
        export["nickName"] = self.nickName
        export["fingerprint"] = self.fingerprint
        export["torVersion"] = str(self.torVersion)        
        export["contactData"] = self.contactData
        export["operatingSystem"] = self.operatingSystem
        export["latitude"] = self.nodeLatitude
        export["longitude"] = self.nodeLongitude
        
        opened = []
        closed = []
        
        for openPort in self.openPorts:
            opened.append(openPort.toExport())
        
        for closedPort in self.closedFilteredPorts:
            closed.append(closedPort.toExport())
            
        export["openPorts"] = opened
        export["closedFilteredPorts"] = closed
        return export

class TorNodePort:
    '''
    Information about the scanned port.
    '''
    def __init__(self):
        self.id = None
        self.state = None
        self.reason = None
        self.port = None
        self.name = None
        self.version = None
        self.torNodeId = None
    
    def toExport(self):
        export = {}
        export["state"] = self.state
        export["reason"] = self.reason
        export["port"] = self.port
        export["name"] = self.name
        export["version"] = self.version
        return export