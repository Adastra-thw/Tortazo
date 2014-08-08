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
from prettytable import PrettyTable
from plugins.attack.utils.exploit32745 import HeartBleedExploit
from plugins.texttable import Texttable

from __future__ import print_function
from twisted.internet import reactor, endpoints
from twisted.web import server, static, resource
import txtorcon
        
class maliciousHiddenServicePlugin(BasePlugin):

'''
        "Cansado de esa suegra pesada? Harto de tus vecinos? No hay problema que una AK no pueda solucionar! Pincha en el botón de abajo y te la enviamos a la dirección que tu nos digas de forma completamente anonima. Solamente pincha en este enlace: "
        "Cansado de esa suegra pesada? Harto de tus vecinos? Quieres ascender en tu trabajo, pero careces de habilidades o talento y hay muchos 'obstaculos'? No te quieres manchar las manos? Nosotros lo hacemos por ti! Trabajos personalizados. Los asesinamos, los cortamos en trocitos y los vendemos a un chino. ¿Quieres escuchar sus últimas palabras antes de palmar para conmemorar ese momento tan especial? No hay problema! ¿Quieres que te enviemos sus huevos en una bolsita? Faltara más!. Promoción limitada: Aplica a tus víctimas una tortura medieval de tu elección por un suplemento adicional de 0.1 bitcoins!  Contacta con nosotros ahora, no lo dudes más. Somos tu hitman service de confianza, satisfacción garantizada o te devolvemos tu dinero. Solamente pincha en el siguiente enlace"
        "Sexo, drogas y rock and roll? Claro! lo que tu quieras! Te vendemos toda clase de (mierda) y si quieres, te la envolvemos en papel regalo. Solamente pincha en este enlace: "
        "Te gustan los niños pequeños? Tenemos toda clase de imagenes y vídeos por una pequeña cantidad de bitcoins. Además, por tu compra llevate gratis crucifijos, recipientes con agua bendecida directamente desde el vaticano, sotanas, vestidos para monagillos y por su puesto, unas buenas hostias! Solamente pincha en este enlace:"
        "No quieres currar y te gusta la pasta facil? Tenemos tarjetas de credito para ti! tarjetas con más de 500€ solamente por 0.1 bitcoins. Solamente pincha en este enlace:"
        "Eres un mangante que le gusta estar a la moda en todo? Eso de las cuentas en Suiza ya está muy visto, utiliza nuestro servicio de lavado de dinero utilizando la deep web. Esto es lo se lleva hoy en día, lo último para delicuentes sofisticados y finos como tu. Solamente pincha en este enlace:"
        "Eres de esos que apoya a anonymous, la libertad de expresión, odia los monopolios, el capitalismo, la sensura, etc. Pero luego vas y votas al PP. Ven, ven, pincha aquí, vas a ver que contenido más interesante: "
'''



    def __init__(self, torNodes=[]):
        BasePlugin.__init__(self, torNodes, 'maliciousHiddenServicePlugin')
        self.setPluginDetails('maliciousHiddenServicePlugin', 'Creates a malicious hidden service in TOR network and tries to de-anonimyze the users.', '1.0', 'Adastra: @jdaanial')
        if len(torNodes) > 0:
            self.info("[*] maliciousHiddenServicePlugin Initialized!")

    def __del__(self):
        if len(self.torNodes) > 0:
            self.info("[*] maliciousHiddenServicePlugin Destroyed!")

    '''
    def connectToTorInstance(address, port, password):
        print "[+] Connecting to %s : %s " %(address, port)
        self.controller = Controller.from_port(address=address,port=port)
        self.controller.authenticate(password)
	bytes_read = self.controller.get_info("traffic/read")
	bytes_written = self.controller.get_info("traffic/written")
	
	print "[+] Tor relay is alive. %s bytes read, %s bytes written." % (bytes_read, bytes_written)
	print "[+] Tor Version: %s" % str(self.controller.get_version())        

    def createHiddenService(hiddenserviceDir, hiddenserviceHost='127.0.0.1', hiddenservicePort=80):
        # create the hidden service
        print "[+] Setting up the hidden service..."
        newHiddenServiceDir=hiddenserviceDir.mkdtemp()
        self.origConfmap = self.controller.get_conf_map("HiddenServiceOptions")
        self.controller.set_options([
            ('HiddenServiceDir',self.origConfmap["HiddenServiceDir"]),
            ('HiddenServicePort',self.origConfmap["HiddenServicePort"]),
            ('HiddenServiceDir',newHiddenServiceDir),
            ('HiddenServicePort',"%d %s:%d" % (hidden_service_port,hidden_service_interface,hidden_service_port))
            ])
        self.hostname=open("%s/hostname" % newHiddenServiceDir,"rb").read().strip()
        print "[+] Onion address for the hidden service is: %s" % self.hostname

    '''

    class GatherInformation(resource.Resource):
	def render_GET(self, request):
            return ""


    def setup_failed(arg):
        print "SETUP FAILED", arg

    
    def setup_complete(port):
        # the port we get back should implement this (as well as IListeningPort)
        port = txtorcon.IHiddenService(port)
        print "I have set up a hidden service, advertised at:",
        print "http://%s:%d" % (port.getHost().onion_uri, port.getHost().onion_port)
        print "locally listening on", port.local_address.getHost()
        print "Will stop in 60 seconds..."

        def blam(x):
            print "%d..." % x
        reactor.callLater(50, blam, 10)
        reactor.callLater(55, blam, 5)
        reactor.callLater(56, blam, 4)
        reactor.callLater(57, blam, 3)
        reactor.callLater(58, blam, 2)
        reactor.callLater(59, blam, 1)
        reactor.callLater(60, reactor.stop)

    def progress(percent, tag, message):
        bar = int(percent / 10)
        print '[%s%s] %s' % ('#' * bar, '.' * (10 - bar), message)

    def createHiddenService(hiddenserviceDir, controlPort=None, hiddenservicePort=80, localservicePort=80):
        root = static.File(hiddenserviceDir)
        #root = resource.Resource()
        root.putChild("gatherUserInfo", GatherInformation())

        site = server.Site(root)
        
        # several ways to proceed here and what they mean:
        # ep0:
        #    launch a new Tor instance, configure a hidden service on some port and pubish descriptor for port 80
        # ep1:
        #    connect to existing Tor via control-port 9051, configure a hidden
        #    service listening locally on 8080, publish a descriptor for port
        #    80 and use an explicit hiddenServiceDir (where "hostname" and
        #    "private_key" files are put by Tor). We set SOCKS port explicitly, too.
        # ep2:
        #    all the same as ep1, except we launch a new Tor (because no "controlPort=9051")
        #
        # https://txtorcon.readthedocs.org/en/latest/examples.html
        # launch_tor_endpoint.py

        ep0 = "onion:"+str(hiddenservicePort)
        ep1 = "onion:"+str(hiddenservicePort)+":controlPort="+str(controlPort)+":localPort="+str(localservicePort)+":hiddenServiceDir="+hiddenserviceDir
        ep2 = "onion:"+str(hiddenservicePort)+":localPort="+str(localservicePort)+":hiddenServiceDir="+hiddenserviceDir
        
        hs_endpoint = serverFromString(reactor, ep0)
        txtorcon.IProgressProvider(hs_endpoint).add_progress_listener(progress)
        # create our Web server and listen on the endpoint; this does the
        # actual launching of (or connecting to) tor.
        
        d = hs_endpoint.listen(site)
        d.addCallback(setup_complete)
        d.addErrback(setup_failed)
        reactor.run()


    def help(self):
        print "[*] Functions availaible available in the Plugin..."
                table = Texttable()
        table.set_cols_align(["l", "l", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.set_cols_width([40,55,55])
        table.add_rows([ ["Function", "Description", "Example"],
                         ['help', 'Help Banner', 'self.help()'],
                         ['printRelaysFound', 'Table with the relays found.', 'self.printRelaysFound()'],
                         ['setTarget', 'Set the relay for the HeartBleed attack. Check the targets using the function "printRelaysFound". Default port: 443.', 'self.setTarget("1.2.3.4")'],
                         ['setTargetWithPort', 'Set the relay and port for the HeartBleed attack. Check the targets using the function "printRelaysFound". ', 'self.setTarget("1.2.3.4", "8443")'],
                         ['startAttack', 'Starts the HeartBleed attack against the specified target. ', 'self.startAttack()'],
                         ['startAttackAllRelays', 'Starts the HeartBleed attack against all relays loaded in the plugin. Default port: 443 ', 'self.startAttackAllRelays()']
                        ])
        print table.draw() + "\\n"
