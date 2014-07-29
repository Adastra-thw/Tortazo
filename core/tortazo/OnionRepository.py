# coding=utf-8
'''
Created on 25/07/2014

#Author: Adastra.
#twitter: @jdaanial

OnionRepository.py

OnionRepository is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

OnionRepository is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import multiprocessing
import string, itertools
import requests

#https://mail.python.org/pipermail/tutor/2012-September/091595.html

#http://simpy.readthedocs.org/en/latest/examples/carwash.html   SEE SIMPY
#http://simpy.readthedocs.org/en/latest/examples/latency.html

class RepositoryGenerator:

    def __init__(self, validChars, serviceConnector, partialOnionAddress, threadsForProcessing):
        self.process = RepositoryProcess(serviceConnector, threadsForProcessing)
        self.partialOnionAddress = partialOnionAddress
        self.charsOnionAddress = validChars
        print "[+] Generator initalized. Using the following chars: %s " %(self.charsOnionAddress)

    def createProcess(self, onion):
        process = multiprocessing.Process(target=self.process.onionQueue.put, args=(onion,))
        process.daemon=True
        process.start()
        process.join()


    def getAddressesQuartet(self):
        iterator = itertools.product(*([self.charsOnionAddress]*4))
        return list(itertools.islice(iterator, 0, None))


    def loopFromFirstQuartet(self, partialAddress, addressFirstQuartet):
        for first, onion1Quartet in enumerate(addressFirstQuartet):
            for second, onion2Quartet in enumerate(self.getAddressesQuartet()[0 : ]):
                for thrid, onion3Quartet in enumerate(self.getAddressesQuartet()[0 : ]):
                    for fourth, onion4Quartet in enumerate(self.getAddressesQuartet()[0 : ]):
                        self.createProcess(partialAddress+(''.join(onion1Quartet))+(''.join(onion2Quartet))+(''.join(onion3Quartet))+(''.join(onion4Quartet))+'.onion')
        self.process.onionQueue.join()

    def loopFromSecondQuartet(self, partialAddress, addressSecondQuartet):
        for second, onion2Quartet in enumerate(addressSecondQuartet[0 : ]):
            for thrid, onion3Quartet in enumerate(self.getAddressesQuartet()[0 : ]):
                for fourth, onion4Quartet in enumerate(self.getAddressesQuartet()[0 : ]):
                    self.createProcess(partialAddress+(''.join(onion2Quartet))+(''.join(onion3Quartet))+(''.join(onion4Quartet))+'.onion')
        self.process.onionQueue.join()

    def loopFromThirdQuartet(self, partialAddress, addressThirdQuartet):
        for third, onion3Quartet in enumerate(addressThirdQuartet[0 : ]):
            for fourth, onion4Quartet in enumerate(self.getAddressesQuartet()[0 : ]):
                self.createProcess(partialAddress+(''.join(onion3Quartet))+(''.join(onion4Quartet))+'.onion')
        self.process.onionQueue.join()


    def loopFromFourthQuartet(self, partialAddress, addressFourthQuartet):
        for fourth, onion4Quartet in enumerate(addressFourthQuartet[0 : ]):
            self.createProcess(partialAddress+(''.join(onion4Quartet))+'.onion')
        self.process.onionQueue.join()


    # TODO:
    # Almacenar en base de datos las respuestas positivas. Intentar implementar otra Queue y otro grupo de hilos para meter ahí las respuestas de los Hidden services descubiertos.
    # Manejar el estado de los procesos guardando en base de datos el nivel de iteración junto con su correspondiente "partialAddress" y conjunto de caracteres ingresados por el usuarios. Esos dos valores serán claves compuestas y permitirán reanudar el proceso.
    def addressesGenerator(self):
        charsUnknown = (16 - len(self.partialOnionAddress))
        iterations = charsUnknown / 4
        mod = charsUnknown % 4

        print iterations, mod
        if mod == 0:
            #Exact quartet.
            addressesQuartetComplete = self.getAddressesQuartet()
            if iterations == 0:
                #The user enters the full onion address (16 chars).
                print "[+] Entered full address (16 characters). Nothing to found."
                return
            if iterations == 1:
                #User enters 12 chars, left 4 chars.
                #print "User enters 12 chars, left 4 chars."
                self.loopFromFourthQuartet(self.partialOnionAddress, addressesQuartetComplete)
            elif iterations == 2:
                #print "User enters 8 chars, left 8 chars."
                #User enters 8 chars, left 8 chars.
                self.loopFromThirdQuartet(self.partialOnionAddress, addressesQuartetComplete)
            elif iterations == 3:
                #print "User enters 4 chars, left 12 chars."
                #User enters 4 chars, left 12 chars.
                self.loopFromSecondQuartet(self.partialOnionAddress, addressesQuartetComplete)
            elif iterations == 4:
                #print "User enters 0 chars, left 16 chars."
                #User enters 4 chars, left 12 chars.
                self.loopFromFirstQuartet(self.partialOnionAddress, addressesQuartetComplete)

        else:
            iteratorQuartetIncomplete = itertools.product(*([self.charsOnionAddress]*(mod)))
            addressesQuartetIncomplete = list(itertools.islice(iteratorQuartetIncomplete, 0, None))
            if iterations == 0:
                #print "User enters between 13 and 15 characters"
                #User enters between 13 and 15 characters
                self.loopFromFourthQuartet(self.partialOnionAddress, addressesQuartetIncomplete)
                '''for state, onion4Quartet in enumerate(addressesQuartetIncomplete[0 : ]):
                    yield env.timeout(1)
                    onionRepository.put(onionPartialAddress + "".join(onion4Quartet) + '.onion')
                '''
            elif iterations == 1:
                #print "User enters between 9 and 11 characters"
                #User enters between 9 and 11 characters
                self.loopFromThirdQuartet(self.partialOnionAddress, addressesQuartetIncomplete)
            elif iterations == 2:
                #print "User enters between 5 and 7 characters"
                #User enters between 5 and 7 characters
                self.loopFromSecondQuartet(self.partialOnionAddress, addressesQuartetIncomplete)
            elif iterations == 3:
                #print "User enters between 1 and 3 characters"
                #User enters between 1 and 3 characters
                self.loopFromFirstQuartet(self.partialOnionAddress, addressesQuartetIncomplete)


    def startGenerator(self):
        self.process.startProcess()
        self.addressesGenerator()




class RepositoryProcess:

    def __init__(self, serviceConnector, threads):
        self.serviceConnector = serviceConnector
        #Reads the previous state of scan of onion urls.
        print "Starting multiprocess."
        print "Number of CPUs available in the system: ",multiprocessing.cpu_count()
        self.threads = threads
        '''
        import socks
        import socket
        def create_connection(address, timeout=2, source_address=None):
            sock = socks.socksocket()
            sock.connect(address)
            return sock
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
        socket.socket = socks.socksocket
        socket.create_connection = create_connection
        '''

    def startProcess(self):
        self.onionQueue=multiprocessing.JoinableQueue()
        for i in range(self.threads):
            try:
                proc = multiprocessing.Process(target=self.processOnionUrl)
                proc.daemon=True
                proc.start()
            except:
                print "Interrupt"
                proc.terminate()
        self.onionQueue.join()



    def processOnionUrl(self):
        while True:
            onionUrl = self.onionQueue.get()
            #HEAD REQUEST TO THE ONION SITE!!!
            #http://twistedmatrix.com/documents/current/web/howto/client.html
            #http://pythonquirks.blogspot.com.es/2011/04/twisted-asynchronous-http-request.html

            httpAddress = "http://"+(''.join(onionUrl))+"/"

            try:
                response = self.serviceConnector.performHTTPConnectionHiddenService(httpAddress, method="HEAD")
                print "[+] Found response from Hidden Service! %s  : %s " %(httpAddress, response)
            except requests.exceptions.Timeout as timeout:
                print timeout
            except Exception as exc:
                pass

            #time.sleep(5)
            self.onionQueue.task_done()



if __name__ == '__main__':
    #r = RepositoryGenerator(0, "gnionmnsscpbgu4", 10, 10)
    r = RepositoryGenerator(0, "vp5de356iyuvcwq", 10, 10)
    r.startGenerator()