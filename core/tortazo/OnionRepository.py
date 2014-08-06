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
import random

#https://mail.python.org/pipermail/tutor/2012-September/091595.html

#http://simpy.readthedocs.org/en/latest/examples/carwash.html   SEE SIMPY
#http://simpy.readthedocs.org/en/latest/examples/latency.html

class RepositoryGenerator:

    def __init__(self, validChars, serviceConnector, databaseConnection, partialOnionAddress, threadsForProcessing):
        self.partialOnionAddress = partialOnionAddress
        self.charsOnionAddress = validChars
        self.databaseConnection = databaseConnection
        self.serviceConnector = serviceConnector

        self.progressFirstQuartet = 0
        self.progressSecondQuartet = 0
        self.progressThirdQuartet = 0
        self.progressFourthQuartet = 0
        if partialOnionAddress.lower() != 'random':
            (self.idProgress, self.startDateProgress, self.progressFirstQuartet, self.progressSecondQuartet, self.progressThirdQuartet, self.progressFourthQuartet) = self.databaseConnection.searchOnionRepositoryProgress(self.partialOnionAddress, self.charsOnionAddress)
            print "[+] Incremental Generator initialized. Using the following chars: %s " %(self.charsOnionAddress)
        else:
            print "[+] Random Generator initialized ... "
        self.process = RepositoryProcess(self, threadsForProcessing)
        self.finishedScan = False


    def __createProcess(self, onion,onionDescription=None):
        process = multiprocessing.Process(target=self.process.onionQueue.put, args=((onion,onionDescription),))
        process.daemon=True
        process.start()
        process.join()

    def __getAddressesQuartet(self):
        iterator = itertools.product(*([self.charsOnionAddress]*4))
        return list(itertools.islice(iterator, 0, None))


    def __loopFromFirstQuartet(self, partialAddress, addressFirstQuartet):
        for first, onion1Quartet in enumerate(addressFirstQuartet[self.progressFirstQuartet : ]):
            for second, onion2Quartet in enumerate(self.__getAddressesQuartet()[self.progressSecondQuartet : ]):
                for thrid, onion3Quartet in enumerate(self.__getAddressesQuartet()[self.progressThirdQuartet : ]):
                    for fourth, onion4Quartet in enumerate(self.__getAddressesQuartet()[self.progressFourthQuartet : ]):
                        self.__createProcess(partialAddress+(''.join(onion1Quartet))+(''.join(onion2Quartet))+(''.join(onion3Quartet))+(''.join(onion4Quartet))+'.onion')

                    self.progressThirdQuartet = self.progressThirdQuartet + (thrid +1)
                    self.progressFourthQuartet = 0
                self.progressSecondQuartet = self.progressSecondQuartet + (second+1)
                self.progressThirdQuartet = 0
            self.progressFirstQuartet = self.progressFirstQuartet + (first+1)
            self.progressSecondQuartet = 0
        self.process.onionQueue.join()
        self.finishedScan = True

    def __loopFromSecondQuartet(self, partialAddress, addressSecondQuartet):
        for second, onion2Quartet in enumerate(addressSecondQuartet[self.progressSecondQuartet : ]):
            for thrid, onion3Quartet in enumerate(self.__getAddressesQuartet()[self.progressThirdQuartet : ]):
                for fourth, onion4Quartet in enumerate(self.__getAddressesQuartet()[self.progressFourthQuartet : ]):
                    self.__createProcess(partialAddress+(''.join(onion2Quartet))+(''.join(onion3Quartet))+(''.join(onion4Quartet))+'.onion')

                self.progressThirdQuartet = self.progressThirdQuartet + (thrid +1)
                self.progressFourthQuartet = 0
            self.progressSecondQuartet = self.progressSecondQuartet + (second+1)
            self.progressThirdQuartet = 0
        self.process.onionQueue.join()
        self.finishedScan = True

    def __loopFromThirdQuartet(self, partialAddress, addressThirdQuartet):
        for thrid, onion3Quartet in enumerate(addressThirdQuartet[self.progressThirdQuartet : ]):
            for fourth, onion4Quartet in enumerate(self.__getAddressesQuartet()[self.progressFourthQuartet : ]):
                self.__createProcess(partialAddress+(''.join(onion3Quartet))+(''.join(onion4Quartet))+'.onion')

            self.progressThirdQuartet = self.progressThirdQuartet + (thrid +1)
            self.progressFourthQuartet = 0
        self.process.onionQueue.join()
        self.finishedScan = True


    def __loopFromFourthQuartet(self, partialAddress, addressFourthQuartet):
        for fourth, onion4Quartet in enumerate(addressFourthQuartet[self.progressFourthQuartet : ]):
            self.__createProcess(partialAddress+(''.join(onion4Quartet))+'.onion')
            self.progressFourthQuartet = self.progressFourthQuartet+1
        self.process.onionQueue.join()
        self.finishedScan = True

    def addressesGeneratorRandom(self):
        onion = '234567'+string.lowercase
        while True:
            self.__createProcess(''.join(random.choice(onion) for i in range(16))  + '.onion' )

        '''addresses = ['am4wuhz3zifexz5u.onion', '3fnhfsfc2bpzdste.onion', '3g2upl4pq6kufc4m.onion', 'kbhpodhnfxl3clb4.onion', '4zeottxi5qmnnjhd.onion', 'c3jemx2ube5v5zpg.onion', 'pyl7a4ccwgpxm6rd.onion']
        for address in addresses:
            self.__createProcess(address)'''
        self.process.onionQueue.join()




    def addressesGeneratorIncremental(self):
        charsUnknown = (16 - len(self.partialOnionAddress))
        iterations = charsUnknown / 4
        mod = charsUnknown % 4

        if mod == 0:
            #Exact quartet.
            addressesQuartetComplete = self.__getAddressesQuartet()
            if iterations == 0:
                #The user enters the full onion address (16 chars).
                print "[+] Entered full address (16 characters). Nothing to found."
                try:
                    httpAddress = "http://"+(''.join(self.partialOnionAddress))+".onion/"
                    print httpAddress
                    response = self.serviceConnector.performHTTPConnectionHiddenService(httpAddress, method="HEAD")
                    print "[+] Found response from Hidden Service! %s  : %s " %(httpAddress, response)
                    if response.status_code not in range(400,499):
                        self.process.onionQueueResponses.put(response)
                except requests.exceptions.Timeout as timeout:
                    print timeout
                except Exception as exc:
                    print exc


                return
            if iterations == 1:
                #User enters 12 chars, left 4 chars.
                #print "User enters 12 chars, left 4 chars."
                self.__loopFromFourthQuartet(self.partialOnionAddress, addressesQuartetComplete)
            elif iterations == 2:
                #print "User enters 8 chars, left 8 chars."
                #User enters 8 chars, left 8 chars.
                self.__loopFromThirdQuartet(self.partialOnionAddress, addressesQuartetComplete)
            elif iterations == 3:
                #print "User enters 4 chars, left 12 chars."
                #User enters 4 chars, left 12 chars.
                self.__loopFromSecondQuartet(self.partialOnionAddress, addressesQuartetComplete)
            elif iterations == 4:
                #print "User enters 0 chars, left 16 chars."
                #User enters 4 chars, left 12 chars.
                self.__loopFromFirstQuartet(self.partialOnionAddress, addressesQuartetComplete)

        else:
            iteratorQuartetIncomplete = itertools.product(*([self.charsOnionAddress]*(mod)))
            addressesQuartetIncomplete = list(itertools.islice(iteratorQuartetIncomplete, 0, None))
            if iterations == 0:
                #print "User enters between 13 and 15 characters"
                #User enters between 13 and 15 characters
                self.__loopFromFourthQuartet(self.partialOnionAddress, addressesQuartetIncomplete)
                '''for state, onion4Quartet in enumerate(addressesQuartetIncomplete[0 : ]):
                    yield env.timeout(1)
                    onionRepository.put(onionPartialAddress + "".join(onion4Quartet) + '.onion')
                '''
            elif iterations == 1:
                #print "User enters between 9 and 11 characters"
                #User enters between 9 and 11 characters
                self.__loopFromThirdQuartet(self.partialOnionAddress, addressesQuartetIncomplete)
            elif iterations == 2:
                #print "User enters between 5 and 7 characters"
                #User enters between 5 and 7 characters
                self.__loopFromSecondQuartet(self.partialOnionAddress, addressesQuartetIncomplete)
            elif iterations == 3:
                #print "User enters between 1 and 3 characters"
                #User enters between 1 and 3 characters
                self.__loopFromFirstQuartet(self.partialOnionAddress, addressesQuartetIncomplete)


    def startGenerator(self,loadKnownAddresses):
        try:
            self.process.startProcess()
            if loadKnownAddresses:
                knownAddresses = open('db/knownOnionSites.txt', 'r')
                for knownAddress in knownAddresses.readlines():
                    knownAddress=knownAddress.replace('\n','')
                    if knownAddress.startswith('#') == False and knownAddress != '':
                        address = knownAddress.split(',')
                        #self.process.httpConnectionHiddenSite(address[0],address[1])
                        self.__createProcess(address[0],address[1])
                self.process.onionQueue.join()


            if self.partialOnionAddress.lower() == 'random':
                self.addressesGeneratorRandom()
            else:
                self.addressesGeneratorIncremental()
        finally:
            if self.partialOnionAddress.lower() != 'random':
                #Save incremental progress.
                self.databaseConnection.insertOnionRepositoryProgress(self.partialOnionAddress, self.charsOnionAddress, self.progressFirstQuartet,self.progressSecondQuartet,self.progressThirdQuartet,self.progressFourthQuartet, self.finishedScan)




class RepositoryProcess:

    def __init__(self, repositoryGenerator, threads):
        print "Starting multiprocess."
        print "Number of CPUs available in the system: ",multiprocessing.cpu_count()
        self.repositoryGenerator = repositoryGenerator
        self.threads = threads

    def startProcess(self):
        self.onionQueue=multiprocessing.JoinableQueue()
        self.onionQueueResponses=multiprocessing.JoinableQueue()
        
        for i in range(self.threads):
            try:
                proc = multiprocessing.Process(target=self.processOnionUrl)
                proc.daemon=True
                proc.start()
            except:
                print "Interrupt"
                proc.terminate()
        self.onionQueue.join()

        for i in range(self.threads):
            try:
                proc = multiprocessing.Process(target=self.saveAddressDetails)
                proc.daemon=True
                proc.start()
            except:
                print "Interrupt"
                proc.terminate()
        self.onionQueueResponses.join()


    def processOnionUrl(self):
        while True:
            onionUrl,onionDescription = self.onionQueue.get()
            print onionUrl,onionDescription
            if onionDescription != None:
                #Onion address known. Reading the file knownOnionSites.txt
                httpAddress = onionUrl
            else:
                httpAddress = "http://"+(''.join(onionUrl))+"/"
            self.httpConnectionHiddenSite(httpAddress,onionDescription)
            self.onionQueue.task_done()

    def httpConnectionHiddenSite(self,httpAddress,onionDescription):
        try:
            response = self.repositoryGenerator.serviceConnector.performHTTPConnectionHiddenService(httpAddress, method="HEAD")
            print "[+] Found response from Hidden Service! %s  : %s " %(httpAddress, response)
            print response.status_code
            if response.status_code not in range(400,499):
                self.onionQueueResponses.put((response,onionDescription))
                self.onionQueueResponses.join()
        except Exception as exc:
            if exc.message == 'connection timeout':
                print "[-] Connection Timeout to: "+httpAddress
                pass


    def saveAddressDetails(self):
        while True:
            response,onionDescription = self.onionQueueResponses.get()
            print "[+] Saving in database Onion Address discovered..."
            #Save address details in database.
            #Table: OnionRepositoryProgess.        PartialOnionAddress, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet
            #Table: OnionRepositoryResponses.      OnionAddress, httpcode, headers
            headers = ''
            for key in response.headers.keys():
                headers = headers + key +' : '+ response.headers[key] +'\n'

            self.repositoryGenerator.databaseConnection.insertOnionRepositoryResult(response.url, response.status_code, headers, onionDescription)
            self.onionQueueResponses.task_done()
