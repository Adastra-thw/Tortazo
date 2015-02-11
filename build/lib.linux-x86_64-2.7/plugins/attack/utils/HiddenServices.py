# coding=utf-8
'''
Created on 02/12/2014

#Author: Adastra.
#twitter: @jdaanial

HiddenServices.py

HiddenServices is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

HiddenServices is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''


from twisted.internet import reactor
import sys, os, threading, SocketServer, paramiko, signal,datetime,time
from twisted.internet.endpoints import TCP4ServerEndpoint
import json
from twisted.web import server, resource, static
from plugins.texttable import Texttable

'''
MixIn used to create an TCP Server.
'''
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer): 
    allow_reuse_address = True 

'''
Class used to create a simple web server using the Twisted library.
'''
class SimpleWebServer():

    '''
    Start the web server using the service directory as argument.
    '''
    def start(self, serviceDir, servicePort, serviceInterface):
        root = static.File(serviceDir)
        site = server.Site(root)
        hs_endpoint = TCP4ServerEndpoint(reactor, servicePort, interface=serviceInterface)
        hs_endpoint.listen(site)

'''
Class used to create a custom web server to gather basic infotmation about the user browser.
'''
class SimpleCustomWebServer(resource.Resource):

    '''
    Function used to process the HTTP GET requests. Just prints the information in the console.
    '''
    def render_GET(self, request):
        data = json.loads(request.args['info'][0])
        if data != None:
            table = Texttable()
            table.set_cols_align(["l", "l"])
            table.set_cols_valign(["m", "m"])
            table.set_cols_width([20,25])
            rows= [ ["Browser Attribute", "Value"],
                  ]
            for key, value in data.iteritems():
                rows.append([key, value])
            table.add_rows(rows)
            print table.draw() + "\n"

        request.setHeader("content-type", "text/plain")
        return "Success"

    '''
    Start the web server using the service directory as argument and the resource "SimpleCustomWebServer".
    '''
    def start(self, serviceDir, servicePort, serviceInterface):
        root = static.File(serviceDir)
        root.putChild("gatherUserInfo", SimpleCustomWebServer())
        site = server.Site(root)
        hs_endpoint = TCP4ServerEndpoint(reactor, servicePort, interface=serviceInterface)
        hs_endpoint.listen(site)
