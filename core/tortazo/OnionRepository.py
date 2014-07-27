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

import itertools
import string

import simpy

from utils import ServiceConnector


charsOnionAddress = '234567' + string.lowercase

def getAddressesQuartet():
    iterator = itertools.product(*([charsOnionAddress]*4))
    return list(itertools.islice(iterator, 0, None))

def loopFromFirstQuartet( partialAddress, addressFirstQuartet, env, onionRepository):
    for state, onion1Quartet in enumerate(addressFirstQuartet):
        for state, onion2Quartet in enumerate(getAddressesQuartet()[0 : ]):
            for state, onion3Quartet in enumerate(getAddressesQuartet()[0 : ]):
                for state, onion4Quartet in enumerate(getAddressesQuartet()[0 : ]):
                    yield env.timeout(1)
                    onionRepository.put(partialAddress+onion1Quartet+onion2Quartet+onion3Quartet+onion4Quartet+'.onion')


def loopFromSecondQuartet( partialAddress, addressSecondQuartet, env, onionRepository):
    for state, onion2Quartet in enumerate(addressSecondQuartet[0 : ]):
        for state, onion3Quartet in enumerate(getAddressesQuartet()[0 : ]):
            for state, onion4Quartet in enumerate(getAddressesQuartet()[0 : ]):
                yield env.timeout(1)
                onionRepository.put(partialAddress+onion2Quartet+onion3Quartet+onion4Quartet+'.onion')

def loopFromThirdQuartet( partialAddress, addressThirdQuartet, env, onionRepository):
    for state, onion3Quartet in enumerate(addressThirdQuartet[0 : ]):
        for state, onion4Quartet in enumerate(getAddressesQuartet()[0 : ]):
            yield env.timeout(1)
            onionRepository.put(partialAddress+onion3Quartet+onion4Quartet+'.onion')


def loopFromFourthQuartet( partialAddress, addressFourthQuartet, env, onionRepository):
    for state, onion4Quartet in enumerate(addressFourthQuartet[0 : ]):
        yield env.timeout(1)
        onionRepository.put(partialAddress+onion4Quartet+'.onion')


class OnionGenerator:

    def __init__(self, serviceConnector):
        self.serviceConnector = serviceConnector

    def sender(self, env, onionRepository, onionPartialAddress):
        #A process which randomly generates messages.
        #  wait for next transmission
        charsUnknown = (16 - len(onionPartialAddress))
        iterations = charsUnknown / 4
        mod = charsUnknown % 4
        print charsUnknown
        print iterations
        print mod

        if mod == 0:
            #Exact quartet.
            if iterations == 0:
                #Full process. The user enters the full onion address (16 chars).
                print "[+] Entered full address (16 characters). Nothing to found."
            if iterations == 1:
                #User enters 4 chars, left 12 chars.
                loopFromSecondQuartet(onionPartialAddress, getAddressesQuartet(), env, onionRepository)
            elif iterations == 2:
                #User enters 8 chars, left 8 chars.
                loopFromThirdQuartet(onionPartialAddress, getAddressesQuartet(), env, onionRepository)
            elif iterations == 3:
                #User enters 12 chars, left 4 chars.
                loopFromFourthQuartet(onionPartialAddress, getAddressesQuartet(), env, onionRepository)
        else:
            iteratorQuartetIncomplete = itertools.product(*([charsOnionAddress]*(4-mod)))
            addressesQuartetIncomplete = list(itertools.islice(iteratorQuartetIncomplete, 0, None))
            if iterations == 0:
                #User enters between 13 and 15 characters
                #loopFromFourthQuartet(onionPartialAddress, addressesQuartetIncomplete, env, onionRepository)
                for state, onion4Quartet in enumerate(addressesQuartetIncomplete[0 : ]):
                    yield env.timeout(1)
                    onionRepository.put(onionPartialAddress +  "".join(onion4Quartet) + '.onion')
            elif mod == 1:
                #User enters between 9 and 11 characters
                loopFromThirdQuartet(onionPartialAddress, addressesQuartetIncomplete, env, onionRepository)
            elif mod == 2:
                #User enters between 5 and 7 characters
                loopFromSecondQuartet(onionPartialAddress, addressesQuartetIncomplete, env, onionRepository)
            elif mod == 3:
                #User enters between 1 and 3 characters
                loopFromFirstQuartet(onionPartialAddress, addressesQuartetIncomplete, env, onionRepository)

    def receiver(self, env, onionRepository):
        #A process which consumes messages.
        while True:
            # Get event for message pipe
            onionAddress = yield onionRepository.get()
            print(' %d ONION: %s' % (env.now, onionAddress ))
            response = self.serviceConnector.performHTTPConnectionHiddenService("http://"+onionAddress)
            if response.status_code == 200:
                print "Found!!"


class OnionRepository(object):
    def __init__(self, env, delay):
        self.env = env
        self.delay = delay
        self.store = simpy.Store(env)

    def latency(self, value):
        yield self.env.timeout(self.delay)
        self.store.put(value)

    def put(self, value):
        self.env.process(self.latency(value))

    def get(self):
        return self.store.get()



'''
if __name__ == "__main__":
    env = simpy.Environment()
    onionRepository = OnionRepository(env, 0)
    onionGenerator =  OnionGenerator()
    onion = "gnionmnsscpbgu4"
    env.process(onionGenerator.sender(env, onionRepository, onion))
    env.process(onionGenerator.receiver(env, onionRepository))
    env.run()
'''