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
        johnlist = open('fuzzdb/attack-payloads/http-protocol/user-agents.txt', 'r')
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
            namelist = open('fuzzdb/wordlists-user-passwd/names/namelist.txt', 'r')
            johnlist = open('fuzzdb/wordlists-user-passwd/passwds/john.txt', 'r')
            unixusers = open('fuzzdb/wordlists-user-passwd/unix-os/unix_users.txt', 'r')
            faithwriters = open('fuzzdb/wordlists-user-passwd/faithwriters.txt', 'r')
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
        johnlist = open('fuzzdb/wordlists-user-passwd/passwds/john.txt', 'r')
        unixpasswords = open('fuzzdb/wordlists-user-passwd/unix-os/unix_passwords.txt', 'r')
        weaksauce = open('fuzzdb/wordlists-user-passwd/passwds/weaksauce.txt', 'r')
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
        commonCommunities = open('fuzzdb/wordlists-misc/wordlist-common-snmp-community-strings.txt', 'r')
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
        adobeXML = open('fuzzdb/Discovery/PredictableRes/AdobeXML.fuzz.txt', 'r')
        apache = open('fuzzdb/Discovery/PredictableRes/Apache.fuzz.txt', 'r')
        apacheTomcat = open('fuzzdb/Discovery/PredictableRes/ApacheTomcat.fuzz.txt', 'r')
        cgiMicrosoft = open('fuzzdb/Discovery/PredictableRes/CGI_Microsoft.fuzz.txt', 'r')
        coldFusion = open('fuzzdb/Discovery/PredictableRes/ColdFusion.fuzz.txt', 'r')
        fatWire = open('fuzzdb/Discovery/PredictableRes/FatwireCMS.fuzz.txt', 'r')
        fronPage = open('fuzzdb/Discovery/PredictableRes/Frontpage.fuzz.txt', 'r')
        hyperion = open('fuzzdb/Discovery/PredictableRes/Hyperion.fuzz.txt', 'r')
        iis = open('fuzzdb/Discovery/PredictableRes/IIS.fuzz.txt', 'r')
        jboss = open('fuzzdb/Discovery/PredictableRes/JBoss.fuzz.txt', 'r')
        jrun = open('fuzzdb/Discovery/PredictableRes/JRun.fuzz.txt', 'r')
        kitchen = open('fuzzdb/Discovery/PredictableRes/KitchensinkDirectories.fuzz.txt', 'r')
        logins = open('fuzzdb/Discovery/PredictableRes/Logins.fuzz.txt', 'r')
        lotusNotes = open('fuzzdb/Discovery/PredictableRes/LotusNotes.fuzz.txt', 'r')
        netware = open('fuzzdb/Discovery/PredictableRes/Netware.fuzz.txt', 'r')
        oracle9i = open('fuzzdb/Discovery/PredictableRes/Oracle9i.fuzz.txt', 'r')
        oracleAppServer = open('fuzzdb/Discovery/PredictableRes/OracleAppServer.fuzz.txt', 'r')
        passwords = open('fuzzdb/Discovery/PredictableRes/Passwords.fuzz.txt', 'r')
        php = open('fuzzdb/Discovery/PredictableRes/PHP.fuzz.txt', 'r')
        phpBackDoors = open('fuzzdb/Discovery/PredictableRes/PHP_CommonBackdoors.fuzz.txt', 'r')
        proxyConf = open('fuzzdb/Discovery/PredictableRes/proxy-conf.fuzz.txt', 'r')
        largeDirs = open('fuzzdb/Discovery/PredictableRes/raft-large-directories.txt', 'r')
        largeDirsLowercase = open('fuzzdb/Discovery/PredictableRes/raft-large-directories-lowercase.txt', 'r')
        largeFiles = open('fuzzdb/Discovery/PredictableRes/raft-large-files.txt', 'r')
        largeFilesLowercase = open('fuzzdb/Discovery/PredictableRes/raft-large-directories-lowercase.txt', 'r')
        largeWords = open('fuzzdb/Discovery/PredictableRes/raft-large-words.txt', 'r')
        largeWordsLowercase = open('fuzzdb/Discovery/PredictableRes/raft-large-words-lowercase.txt', 'r')
        mediumDirs = open('fuzzdb/Discovery/PredictableRes/raft-medium-directories.txt', 'r')
        mediumDirsLower =  open('fuzzdb/Discovery/PredictableRes/raft-medium-directories-lowercase.txt', 'r')
        mediumFiles =  open('fuzzdb/Discovery/PredictableRes/raft-medium-files.txt', 'r')
        mediumFilesLower =  open('fuzzdb/Discovery/PredictableRes/raft-medium-files-lowercase.txt', 'r')
        mediumWords =  open('fuzzdb/Discovery/PredictableRes/raft-medium-words.txt', 'r')
        mediumWordsLower =  open('fuzzdb/Discovery/PredictableRes/raft-medium-words-lowercase.txt', 'r')
        smallDirs =  open('fuzzdb/Discovery/PredictableRes/raft-small-directories.txt', 'r')
        smallDirsLower =  open('fuzzdb/Discovery/PredictableRes/raft-small-directories-lowercase.txt', 'r')
        smallFiles =  open('fuzzdb/Discovery/PredictableRes/raft-small-files.txt', 'r')
        smallFilesLower =  open('fuzzdb/Discovery/PredictableRes/raft-small-files-lowercase.txt', 'r')
        smallWords =  open('fuzzdb/Discovery/PredictableRes/raft-small-words.txt', 'r')
        smallWordsLower =  open('fuzzdb/Discovery/PredictableRes/raft-small-words-lowercase.txt', 'r')
        randomFiles =  open('fuzzdb/Discovery/PredictableRes/Randomfiles.fuzz.txt', 'r')
        SAP =  open('fuzzdb/Discovery/PredictableRes/SAP.fuzz.txt', 'r')
        siteMinder =  open('fuzzdb/Discovery/PredictableRes/SiteMinder.fuzz.txt', 'r')
        glassfish =  open('fuzzdb/Discovery/PredictableRes/SunAppServerGlassfish.fuzz.txt', 'r')
        iplanet =  open('fuzzdb/Discovery/PredictableRes/SuniPlanet.fuzz.txt', 'r')
        tftp =  open('fuzzdb/Discovery/PredictableRes/tftp.fuzz.txt', 'r')
        unixdotfiles =  open('fuzzdb/Discovery/PredictableRes/UnixDotfiles.fuzz.txt', 'r')
        vignette =  open('fuzzdb/Discovery/PredictableRes/Vignette.fuzz.txt', 'r')
        weblogic =  open('fuzzdb/Discovery/PredictableRes/Weblogic.fuzz.txt', 'r')
        websphere =  open('fuzzdb/Discovery/PredictableRes/Websphere.fuzz.txt', 'r')

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