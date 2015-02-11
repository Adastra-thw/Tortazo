# coding=utf-8
'''
Created on 09/07/2014

#Author: Adastra.
#twitter: @jdaanial

ServiceConnector.py

ServiceConnector is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

ServiceConnector is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
import sys
import os
from config import config

class FuzzDBReader:


    ################################################################################################################################################
    ###########################   COMMON FUNCTIONS.   ##############################################################################################
    ################################################################################################################################################

    def getUserAgentsFromFuzzDB(self):
        '''
        Reads:
        fuzzdb/attack-payloads/http-protocol/user-agents.txt
        and returns a list of User-agents
        '''
        print "[+] Reading the User-Agent list from FuzzDB"
        userAgents = []
        fuzzFile = config.resource_path(os.path.join("fuzzdb/attack-payloads/http-protocol/user-agents.txt"))
        johnlist = open(fuzzFile, 'r')
        for johnpass in johnlist.readlines():
            userAgents.append(johnpass.rstrip('\n'))

        return userAgents

    def getUserlistFromFuzzDB(self):
        '''
        Reads:
        fuzzdb/wordlists-user-passwd/names/namelist.txt
        fuzzdb/wordlists-user-passwd/passwds/john.txt
        fuzzdb/wordlists-user-passwd/unix-os/unix-users.txt
        fuzzdb/wordlists-user-passwd/faithwriters.txt
        and returns a list of words (used as possible usernames)
        '''
        print "[+] Generating users list using the files in FuzzDB"
        users = []
        try:
            namelistFile = config.resource_path(os.path.join('fuzzdb/wordlists-user-passwd/names/namelist.txt'))
            namelist = open(namelistFile, 'r')

            johnlistFile = config.resource_path(os.path.join('fuzzdb/wordlists-user-passwd/passwds/john.txt'))
            johnlist = open(johnlistFile, 'r')

            unixusersFile = config.resource_path(os.path.join('fuzzdb/wordlists-user-passwd/unix-os/unix_users.txt'))
            unixusers = open(unixusersFile, 'r')

            faithwritersFile = config.resource_path(os.path.join('fuzzdb/wordlists-user-passwd/faithwriters.txt'))
            faithwriters = open(faithwritersFile, 'r')

            for userNameList in namelist.readlines():
                users.append(userNameList.rstrip('\n'))

            for userJohnList in johnlist.readlines():
                users.append(userJohnList.rstrip('\n'))

            for userunix in unixusers.readlines():
                users.append(userunix.rstrip('\n'))

            for userfaithwriter in faithwriters.readlines():
                users.append(userfaithwriter.rstrip('\n'))
            return users
        except:
            print sys.exc_info()

    def getPasslistFromFuzzDB(self):
        '''
        Reads:
        fuzzdb/wordlists-user-passwd/passwds/john.txt
        fuzzdb/wordlists-user-passwd/unix-os/unix-passwords.txt
        fuzzdb/wordlists-user-passwd/weaksauce.txt
        and returns a list of words (used as possible usernames)
        '''
        print "[+] Generating passwords list using the files in FuzzDB"
        passwords = []
        johnlistFile = config.resource_path(os.path.join('fuzzdb/wordlists-user-passwd/passwds/john.txt'))
        johnlist = open(johnlistFile, 'r')

        unixpasswordsFile = config.resource_path(os.path.join('fuzzdb/wordlists-user-passwd/unix-os/unix_passwords.txt'))
        unixpasswords = open(unixpasswordsFile, 'r')

        weaksauceFile = config.resource_path(os.path.join('fuzzdb/wordlists-user-passwd/passwds/weaksauce.txt'))
        weaksauce = open(weaksauceFile, 'r')

        for johnpass in johnlist.readlines():
            passwords.append(johnpass.rstrip('\n'))

        for unixpass in unixpasswords.readlines():
            passwords.append(unixpass.rstrip('\n'))

        for sauce in weaksauce.readlines():
            passwords.append(sauce.rstrip('\n'))

        return passwords

    def getSNMPCommunitiesFromFuzzDB(self):
        '''
        Reads:
        fuzzdb/wordlists-misc/wordlist-common-snmp-community-strings.txt
        '''
        print "[+] Reading the wordlist with common SNMP communities from FuzzDB"
        communities = []
        commonCommunitiesFile = config.resource_path(os.path.join('fuzzdb/wordlists-misc/wordlist-common-snmp-community-strings.txt'))
        commonCommunities = open(commonCommunitiesFile, 'r')
        for community in commonCommunities.readlines():
            communities.append(community.replace(' ', '').replace('\n', ''))
        return  communities

    def getDirListFromFuzzDB(self):
        '''
        Reads:
        fuzzdb/Discovery/PredictableRes/AdobeXML.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Apache.fuzz.txt
        fuzzdb/Discovery/PredictableRes/ApacheTomcat.fuzz.txt
        fuzzdb/Discovery/PredictableRes/CGI_Microsoft.fuzz.txt
        fuzzdb/Discovery/PredictableRes/ColdFusion.fuzz.txt
        fuzzdb/Discovery/PredictableRes/FatwireCMS.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Frontpage.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Hyperion.fuzz.txt
        fuzzdb/Discovery/PredictableRes/IIS.fuzz.txt
        fuzzdb/Discovery/PredictableRes/JBoss.fuzz.txt
        fuzzdb/Discovery/PredictableRes/JRun.fuzz.txt
        fuzzdb/Discovery/PredictableRes/KitchensinkDirectories.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Logins.fuzz.txt
        fuzzdb/Discovery/PredictableRes/LotusNotes.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Netware.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Oracle9i.fuzz.txt
        fuzzdb/Discovery/PredictableRes/OracleAppServer.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Passwords.fuzz.txt
        fuzzdb/Discovery/PredictableRes/PHP.fuzz.txt
        fuzzdb/Discovery/PredictableRes/PHP_CommonBackdoors.fuzz.txt
        fuzzdb/Discovery/PredictableRes/proxy-conf.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-large-directories.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-large-directories-lowecase.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-large-files.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-large-files-lowercase.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-large-words.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-large-words-lowercase.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-medium-directories.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-medium-directories-lowercase.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-medium-files.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-medium-files-lowercase.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-medium-words.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-medium-words-lowercase.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-small-directories.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-small-directories-lowercase.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-small-files.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-small-files-lowercase.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-small-words.fuzz.txt
        fuzzdb/Discovery/PredictableRes/raft-small-words-lowercase.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Randomfiles.fuzz.txt
        fuzzdb/Discovery/PredictableRes/SAP.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Sharepoint.fuzz.txt
        fuzzdb/Discovery/PredictableRes/SiteMinder.fuzz.txt
        fuzzdb/Discovery/PredictableRes/SunAppServerGlassfish.fuzz.txt
        fuzzdb/Discovery/PredictableRes/SuniPlanet.fuzz.txt
        fuzzdb/Discovery/PredictableRes/tftp.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Unixdotfiles.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Vignette.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Weblogic.fuzz.txt
        fuzzdb/Discovery/PredictableRes/Websphere.fuzz.txt
        '''
        print "[+] Generating Directory list using the files in FuzzDB"
        dirs = []
        adobeXMLFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/AdobeXML.fuzz.txt'))
        adobeXML = open(adobeXMLFile, 'r')

        apacheFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Apache.fuzz.txt'))
        apache = open(apacheFile, 'r')

        apacheTomcatFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/ApacheTomcat.fuzz.txt'))
        apacheTomcat = open(apacheTomcatFile, 'r')

        cgiMicrosoftFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/CGI_Microsoft.fuzz.txt'))
        cgiMicrosoft = open(cgiMicrosoftFile, 'r')

        coldFusionFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/ColdFusion.fuzz.txt'))
        coldFusion = open(coldFusionFile, 'r')

        fatWireFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/FatwireCMS.fuzz.txt'))
        fatWire = open(fatWireFile, 'r')

        fatWireFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Frontpage.fuzz.txt'))
        fronPage = open(fatWireFile, 'r')

        hyperionFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Hyperion.fuzz.txt'))
        hyperion = open(hyperionFile, 'r')

        iisFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/IIS.fuzz.txt'))
        iis = open(iisFile, 'r')

        jbossFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/JBoss.fuzz.txt'))
        jboss = open(jbossFile, 'r')

        jrunFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/JRun.fuzz.txt'))
        jrun = open(jrunFile, 'r')

        kitchenFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/KitchensinkDirectories.fuzz.txt'))
        kitchen = open(kitchenFile, 'r')

        loginsFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Logins.fuzz.txt'))
        logins = open(loginsFile, 'r')

        lotusNotesFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/LotusNotes.fuzz.txt'))
        lotusNotes = open(lotusNotesFile, 'r')

        netwareFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Netware.fuzz.txt'))
        netware = open(netwareFile, 'r')

        oracle9iFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Oracle9i.fuzz.txt'))
        oracle9i = open(oracle9iFile, 'r')

        oracleAppServerFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/OracleAppServer.fuzz.txt'))
        oracleAppServer = open(oracleAppServerFile, 'r')

        passwordsFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Passwords.fuzz.txt'))
        passwords = open(passwordsFile, 'r')

        phpFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/PHP.fuzz.txt'))
        php = open(phpFile, 'r')

        phpBackDoorsFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/PHP_CommonBackdoors.fuzz.txt'))
        phpBackDoors = open(phpBackDoorsFile, 'r')

        proxyConfFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/proxy-conf.fuzz.txt'))
        proxyConf = open(proxyConfFile, 'r')

        largeDirsFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-large-directories.txt'))
        largeDirs = open(largeDirsFile, 'r')

        largeDirsLowercaseFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-large-directories-lowercase.txt'))
        largeDirsLowercase = open(largeDirsLowercaseFile, 'r')

        largeFilesFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-large-files.txt'))
        largeFiles = open(largeFilesFile, 'r')

        largeFilesLowercaseFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-large-directories-lowercase.txt'))
        largeFilesLowercase = open(largeFilesLowercaseFile, 'r')

        largeWordsFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-large-words.txt'))
        largeWords = open(largeWordsFile, 'r')

        largeWordsFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-large-words-lowercase.txt'))
        largeWordsLowercase = open(largeWordsFile, 'r')

        mediumDirsFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-medium-directories.txt'))
        mediumDirs = open(mediumDirsFile, 'r')

        mediumDirsLowerFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-medium-directories-lowercase.txt'))
        mediumDirsLower =  open(mediumDirsLowerFile, 'r')

        mediumFilesFile = config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-medium-files.txt'))
        mediumFiles =  open(mediumFilesFile, 'r')

        mediumFilesLowerFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-medium-files-lowercase.txt'))
        mediumFilesLower =  open(mediumFilesLowerFile, 'r')

        mediumWordsFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-medium-words.txt'))
        mediumWords =  open(mediumWordsFile, 'r')

        mediumWordsLowerFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-medium-words-lowercase.txt'))
        mediumWordsLower =  open(mediumWordsLowerFile, 'r')

        smallDirsFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-small-directories.txt'))
        smallDirs =  open(smallDirsFile, 'r')

        smallDirsLowerFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-small-directories-lowercase.txt'))
        smallDirsLower =  open(smallDirsLowerFile, 'r')

        smallFilesFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-small-files.txt'))
        smallFiles =  open(smallFilesFile, 'r')

        smallFilesLowerFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-small-files-lowercase.txt'))
        smallFilesLower =  open(smallFilesLowerFile, 'r')

        smallWordsFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-small-words.txt'))
        smallWords =  open(smallWordsFile, 'r')

        smallWordsLowerFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/raft-small-words-lowercase.txt'))
        smallWordsLower =  open(smallWordsLowerFile)

        randomFilesFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Randomfiles.fuzz.txt'))
        randomFiles =  open(randomFilesFile, 'r')

        SAPFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/SAP.fuzz.txt'))
        SAP =  open(SAPFile, 'r')

        siteMinderFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/SiteMinder.fuzz.txt'))
        siteMinder =  open(siteMinderFile, 'r')

        glassfishFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/SunAppServerGlassfish.fuzz.txt'))
        glassfish =  open(glassfishFile, 'r')

        iplanetFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/SuniPlanet.fuzz.txt'))
        iplanet =  open(iplanetFile, 'r')

        tftpFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/tftp.fuzz.txt'))
        tftp =  open(tftpFile, 'r')

        unixdotfilesFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/UnixDotfiles.fuzz.txt'))
        unixdotfiles =  open(unixdotfilesFile, 'r')

        vignetteFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Vignette.fuzz.txt'))
        vignette =  open(vignetteFile, 'r')

        weblogicFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Weblogic.fuzz.txt'))
        weblogic =  open(weblogicFile, 'r')

        websphereFile =  config.resource_path(os.path.join('fuzzdb/Discovery/PredictableRes/Websphere.fuzz.txt'))
        websphere =  open(websphereFile, 'r')

        dirs.extend(self.__readFile(adobeXML))
        dirs.extend(self.__readFile(apache))
        dirs.extend(self.__readFile(apacheTomcat))
        dirs.extend(self.__readFile(cgiMicrosoft))
        dirs.extend(self.__readFile(fatWire))
        dirs.extend(self.__readFile(coldFusion))
        dirs.extend(self.__readFile(fronPage))
        dirs.extend(self.__readFile(hyperion))
        dirs.extend(self.__readFile(iis))
        dirs.extend(self.__readFile(jboss))
        dirs.extend(self.__readFile(jrun))
        dirs.extend(self.__readFile(kitchen))
        dirs.extend(self.__readFile(logins))
        dirs.extend(self.__readFile(lotusNotes))
        dirs.extend(self.__readFile(netware))
        dirs.extend(self.__readFile(oracle9i))
        dirs.extend(self.__readFile(oracleAppServer))
        dirs.extend(self.__readFile(passwords))
        dirs.extend(self.__readFile(php))
        dirs.extend(self.__readFile(phpBackDoors))
        dirs.extend(self.__readFile(proxyConf))
        dirs.extend(self.__readFile(largeDirs))
        dirs.extend(self.__readFile(largeDirsLowercase))
        dirs.extend(self.__readFile(largeFiles))
        dirs.extend(self.__readFile(largeFilesLowercase))
        dirs.extend(self.__readFile(largeWords))
        dirs.extend(self.__readFile(largeWordsLowercase))
        dirs.extend(self.__readFile(mediumDirs))
        dirs.extend(self.__readFile(mediumDirsLower))
        dirs.extend(self.__readFile(mediumFiles))
        dirs.extend(self.__readFile(mediumFilesLower))
        dirs.extend(self.__readFile(mediumWords))
        dirs.extend(self.__readFile(mediumWordsLower))
        dirs.extend(self.__readFile(smallDirs))
        dirs.extend(self.__readFile(smallDirsLower))
        dirs.extend(self.__readFile(smallFiles))
        dirs.extend(self.__readFile(smallFilesLower))
        dirs.extend(self.__readFile(smallWords))
        dirs.extend(self.__readFile(smallWordsLower))
        dirs.extend(self.__readFile(randomFiles))
        dirs.extend(self.__readFile(SAP))
        dirs.extend(self.__readFile(siteMinder))
        dirs.extend(self.__readFile(glassfish))
        dirs.extend(self.__readFile(iplanet))
        dirs.extend(self.__readFile(tftp))
        dirs.extend(self.__readFile(unixdotfiles))
        dirs.extend(self.__readFile(vignette))
        dirs.extend(self.__readFile(weblogic))
        dirs.extend(self.__readFile(websphere))


        return dirs


    def __readFile(self, file):
        dirs = []
        for line in file.readlines():
            if "#" in line:
                continue
            if line.startswith("/") == False:
                dirs.append("/"+line.rstrip('\n'))
            else:
                dirs.append("/"+line.rstrip('\n'))
        return dirs