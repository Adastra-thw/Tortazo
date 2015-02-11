'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

ITortazoDatabase.py

ITortazoDatabase is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

ITortazoDatabase is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from abc import ABCMeta, abstractmethod


class ITortazoDatabase:

    __metaclass__ = ABCMeta

    def __init__(self):
        self.connection = None
        self.cursor = None

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def initDatabase(self):
        raise NotImplementedError

    @abstractmethod
    def searchExitNodes(self, numberOfScans, scanIdentifier):
        raise NotImplementedError

    @abstractmethod
    def insertExitNode(self, torNodeData):
        raise NotImplementedError

    @abstractmethod
    def insertTorNodeGeolocation(self, torNodeId, torNodeData):
        raise NotImplementedError

    @abstractmethod
    def cleanDatabaseState(self):
        raise NotImplementedError

    @abstractmethod
    def insertOnionRepositoryResult(self, onionAddress, responseCode, responseHeaders, onionDescription, serviceType):
        raise NotImplementedError

    @abstractmethod
    def searchOnionRepositoryProgress(self, partialOnionAddress, validChars):
        raise NotImplementedError

    @abstractmethod
    def insertOnionRepositoryProgress(self, onionAddress, validChars, progressFirstQuartet, progressSecondQuartet, progressThirdQuartet, progressFourthQuartet, finished=False):
        raise NotImplementedError

    @abstractmethod
    def searchOnionRepository(self, start=1, maxResults=30):
        raise NotImplementedError

    @abstractmethod
    def countOnionRepositoryResponses(self):
        raise NotImplementedError

    @abstractmethod
    def searchBotnetNode(self, address):
        raise NotImplementedError


    @abstractmethod
    def insertBotnetNode(self,address, user, password, port, nickname, serviceType):
        raise NotImplementedError

    @abstractmethod
    def insertBotnetGeolocation(self, botId, address):
        raise NotImplementedError

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          DATABASE FUNCTIONS FOR "deepWebCrawlerPlugin".                                                                                ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

    @abstractmethod
    def initDatabaseDeepWebCrawlerPlugin(self):
        raise NotImplementedError

    @abstractmethod
    def insertPage(self, page):
        raise NotImplementedError

    @abstractmethod
    def insertImages(self, page, pageId):
        raise NotImplementedError

    @abstractmethod
    def insertForms(self, page, pageId):
        raise NotImplementedError

    @abstractmethod
    def existsPageByUrl(self, url):
        raise NotImplementedError

    @abstractmethod
    def searchPageByUrl(self, url):
        raise NotImplementedError