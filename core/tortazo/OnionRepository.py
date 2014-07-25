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

#https://mail.python.org/pipermail/tutor/2012-September/091595.html
class RepositoryGenerator:
    def __init__(self, previousState, threadsForGenerator, threadsForProcessing):
        #Reads the previous state of scan of onion urls.
        self.threads = threadsForGenerator
        self.process = RepositoryProcess(threadsForProcessing)
        charsOnionAddress = '234567' + string.lowercase
        self.iterator = itertools.product(*([charsOnionAddress]*16))
        print self.iterator


    def startGenerator(self):
        self.process.startProcess()
        self.__generateOnionUrl()


    def __generateOnionUrl(self):
        # fill the queue:
        onion = ['234567abcdefghij','234567abcdefghik','234567abcdefghil','234567abcdefghim'] #Reemplazar con la logica para generar direcciones ONION.
        for o in onion:
            process = multiprocessing.Process(target=self.processQueue, args=(o,))
            process.daemon=True
            process.start()
            process.join()

    def processQueue(self, onionDir):
        self.process.onionQueue.put(onionDir)


class RepositoryProcess:

    def __init__(self, threads):
        #Reads the previous state of scan of onion urls.
        self.threads = threads

    def startProcess(self):
        self.onionQueue=multiprocessing.JoinableQueue()
        for i in range(self.threads):
            proc = multiprocessing.Process(target=self.processOnionUrl)
            proc.daemon=True
            proc.start()


    def processOnionUrl(self):
        while True:
            onionUrl = self.onionQueue.get()
            print  onionUrl
            self.onionQueue.task_done()