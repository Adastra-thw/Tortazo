# coding=utf-8
'''
Created on 19/03/2014

#Author: Adastra.
#twitter: @jdaanial

simplePlugin.py

WorkerThread is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

WorkerThread is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import requests
import json

#http://static.tenable.com/documentation/nessus_5.0_XMLRPC_protocol_guide.pdf
class NessusClient:
    '''
    NessusClient. Class to consume the REST services defined running in a instance of Nessus Scanner.
    '''

    def __init__(self, nessusServer, nessusPort, validateCert=False, initialSeqNumber=1):
        self.nessusServer = nessusServer
        self.nessusPort = nessusPort
        self.url='https://'+str(nessusServer)+':'+str(nessusPort)
        self.token = None
        self.headers = {}
        self.bodyRequest = {}
        self.seqNumber = initialSeqNumber
        self.validateCert = validateCert
        self.nessusFunctions = {'login':'/login',
                                'logout':'/logout',
                                'feed':'/feed',
                                'server_securesettings_list':'/server/securesettings/list',
                                'server_securesettings':'/server/securesettings',
                                'server_preferences_list':'/server/preferences/list',
                                'server_preferences':'/server/preferences',
                                'server_update':'/server/update',
                                'server_register':'/server/register',
                                'server_restart':'/server/restart',
                                'server_load':'/server/load',
                                'server_uuid':'/uuid',
                                'server_getcert':'/getcert',
                                'server_plugins_process':'/plugins/process',
                                'users_add':'/users/add',
                                'users_delete':'/users/delete',
                                'users_edit':'/users/edit',
                                'users_chpasswd':'/users/chpasswd',
                                'users_list':'/users/list',
                                'plugins_list':'/plugins/list',
                                'plugins_attributes_list':'/plugins/attributes/list',
                                'plugins_list_family':'/plugins/list/family',
                                'plugins_description':'plugins/description',
                                'plugins_preferences':'plugins/preferences',
                                'plugins_attributes_familySearch':'/plugins/attributes/familySearch',
                                'plugins_attributes_pluginSearch':'/plugins/attributes/pluginSearch',
                                'plugins_md5':'plugins/md5',
                                'plugins_descriptions':'/plugins/descriptions',
                                'policy_preferences_list':'/preferences/list',
                                'policy_list':'/policy/list',
                                'policy_delete':'/policy/delete',
                                'policy_copy':'/policy/copy',
                                'policy_add':'/policy/add',
                                'policy_edit':'/policy/edit',
                                'policy_download':'/policy/download',
                                'policy_file_upload':'/file/upload',
                                'policy_file_policy_import':'/file/policy/import',
                                'scan_new':'/scan/new',
                                'scan_stop':'/scan/stop',
                                'scan_resume':'/scan/resume',
                                'scan_pause':'/scan/pause',
                                'scan_list':'/scan/list',
                                'scan_timezones':'/timezones',
                                'scan_template_new':'/scan/template/new',
                                'scan_template_edit':'/scan/template/edit',
                                'scan_template_delete':'/scan/template/delete',
                                'scan_template_launch':'/scan/template/launch',
                                'report_list':'/report/list',
                                'report_delete':'/report/delete',
                                'report_hosts':'/report/hosts',
                                'report2_hosts_plugin':'/report2/hosts/plugin',
                                'report2_hosts':'/report2/hosts',
                                'report_ports':'/report/ports',
                                'report2_ports':'/report2/ports',
                                'report_details':'/report/details',
                                'report2_details_plugin':'/report2/details/plugin',
                                'report2_details':'/report2/details',
                                'report_tags':'/report/tags',
                                'report_hasAuditTrail':'/report/hasAuditTrail',
                                'report_attributes_list':'/report/attributes/list',
                                'report_errors':'/report/errors',
                                'report_hasKB':'/report/hasKB',
                                'report_canDeleteItems':'/report/canDeleteItems',
                                'report2_deleteItem':'/report2/deleteItem',
                                'report_trail_details':'/report/trail-details',
                                'report2_vulnerabilities':'/report2/vulnerabilities',
                                'report_chapter_list':'/chapter/list',
                                'report_chapter':'/chapter',
                                'report_file_import':'/file/report/import',
                                'report_file_download':'/file/report/download',
                                'report_file_xslt_list':'/file/xslt/list',
                                'report_file_xslt':'/file/xslt',
                                'report_file_xslt_download':'/file/xslt/download'
                                }

    def constructParamsAndHeaders(self, headers={}, params={}, jsonFormat=True):
        if jsonFormat:
            self.body = {'seq' : self.seqNumber, 'json' : '1'}
        else:
            self.body = {'seq' : self.seqNumber, 'json' : '0'}
        if self.token is not None:
            #No authentication needed.
            self.headers={'Host': self.nessusServer+':'+self.nessusPort,
                          'Content-type':'application/x-www-form-urlencoded',
                          'Cookie':'token='+self.token}
        else:
            self.headers={'Host': self.nessusServer+':'+self.nessusPort,
                          'Content-type':'application/x-www-form-urlencoded'}
        self.body.update(params)
        self.headers.update(headers)

    def requestNessus(self, url, jsonFormat):
        '''
        Perform a request to Nessus server using the data and headers received by parameter.
        This function automatically increments the sequence identifier for Nessus requests.
        '''
        response = requests.post(url, data=self.body, headers=self.headers, verify=self.validateCert)
        self.seqNumber += 1
        if jsonFormat:
            return json.loads(response.content)
        else:
            return response.content

    def login(self, nessusUser, nessusPassword, jsonFormat=True):
        '''
        Login with the Nessus server using the user and password specified.
        '''
        self.constructParamsAndHeaders(params={'login':nessusUser, 'password':nessusPassword}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['login'], jsonFormat=jsonFormat)
        structure = {}

        if jsonFormat == False:
            structure = json.loads(content)
        else:
            structure = content

        if structure['reply']['status'] == 'OK':
            self.token = structure['reply']['contents']['token']
        return content

    def logout(self, jsonFormat=True):
        '''
        Logout function to destroy a token created previously.
        Returns None if there's no token loaded in the class.
        '''
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['logout'], jsonFormat=jsonFormat)
        return content

    def feed(self, jsonFormat=True):
        '''
        Logout function to destroy a token created previously.
        Returns None if there's no token loaded in the class.
        '''
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['feed'], jsonFormat=jsonFormat)
        return content

    def securesettingsList(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_securesettings_list'], jsonFormat=jsonFormat)
        return content

    def secureSettings(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_securesettings'], jsonFormat=jsonFormat)
        return content

    def serverPreferencesList(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_preferences_list'], jsonFormat=jsonFormat)
        return content


    def serverPreferences(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_preferences'], jsonFormat=jsonFormat)
        return content

    def serverUpdate(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_update'], jsonFormat=jsonFormat)
        return content


    def serverRegister(self, nessusFeed, jsonFormat=True):
        self.constructParamsAndHeaders(params={'code':nessusFeed},jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_register'], jsonFormat=jsonFormat)
        return content

    def serverRestart(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_restart'], jsonFormat=jsonFormat)
        return content

    def serverLoad(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_load'], jsonFormat=jsonFormat)
        return content

    def serverUuid(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_uuid'], jsonFormat=jsonFormat)
        return content

    def serverGetCert(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_getcert'], jsonFormat=jsonFormat)
        return content

    def serverPluginsProcess(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['server_plugins_process'], jsonFormat=jsonFormat)
        return content

    def usersAdd(self,login, password, admin=False, jsonFormat=True):
        adminUser = 0
        if admin:
            adminUser = 1
        self.constructParamsAndHeaders(params={'login':login,
                                               'password':password,
                                               'admin':adminUser}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['users_add'], jsonFormat=jsonFormat)
        return content

    def usersDelete(self,login,jsonFormat=True):
        self.constructParamsAndHeaders(params={'login':login}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['users_delete'], jsonFormat=jsonFormat)
        return content

    def usersEdit(self,login, password, admin=False, jsonFormat=True):
        adminUser = 0
        if admin:
            adminUser = 1
        self.constructParamsAndHeaders(params={'login':login,
                                               'password':password,
                                               'admin':adminUser}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['users_edit'], jsonFormat=jsonFormat)
        return content

    def usersChpasswd(self,login,password,jsonFormat=True):
        self.constructParamsAndHeaders(params={'login':login,
                                               'password':password}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['users_chpasswd'], jsonFormat=jsonFormat)
        return content

    def usersList(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['users_list'], jsonFormat=jsonFormat)
        return content

    def pluginsList(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['plugins_list'], jsonFormat=jsonFormat)
        return content

    def pluginsAttributesList(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['plugins_attributes_list'], jsonFormat=jsonFormat)
        return content

    def pluginsListFamily(self, pluginFamily, jsonFormat=True):
        self.constructParamsAndHeaders(params={'family':pluginFamily}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['plugins_list_family'], jsonFormat=jsonFormat)
        return content

    def pluginsDescription(self, fileNamePlugin, jsonFormat=True):
        self.constructParamsAndHeaders(params={'fname':fileNamePlugin}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['plugins_description'], jsonFormat=jsonFormat)
        return content

    def pluginsPreferences(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['plugins_preferences'], jsonFormat=jsonFormat)
        return content

    def pluginsAttributesFamilySearch(self, filter0Quality, filterSearchType, filter0Value, filter0Filter, jsonFormat=True):

        #filter.0.quality – Four values are allowed here: match, nmatch, eq, neq
        #filter.search_type – The types of search: or, and
        #filter.0.filter – A full list of plugin attributes can be obtained from the /plugins/attributes/list function.
        self.constructParamsAndHeaders(params={'filter.0.quality':filter0Quality,
                                               'filter.search_type':filterSearchType,
                                               'filter.0.value':filter0Value,
                                               'filter.0.filter':filter0Filter},
                                       jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['plugins_attributes_familySearch'], jsonFormat=jsonFormat)
        return content

    def pluginsAttributesPluginSearch(self,filter0Quality,filterSearchType,filter0Value,filter0Filter,family,jsonFormat=True):
        #Same as pluginsAttributesFamilySearch.

        self.constructParamsAndHeaders(params={'filter.0.quality':filter0Quality,
                                               'filter.search_type':filterSearchType,
                                               'filter.0.value':filter0Value,
                                               'filter.0.filter':filter0Filter,
                                               'family':family}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['plugins_attributes_pluginSearch'], jsonFormat=jsonFormat)
        return content

    def pluginsMd5(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['plugins_md5'], jsonFormat=jsonFormat)
        return content

    def pluginsDescriptions(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['plugins_descriptions'], jsonFormat=jsonFormat)
        return content

    def policyPreferencesList(self,jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['policy_preferences_list'], jsonFormat=jsonFormat)
        return content


    def policyList(self, jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['policy_list'], jsonFormat=jsonFormat)
        return content

    def policyDelete(self, policyId, jsonFormat=True):
        self.constructParamsAndHeaders(params={'policy_id':policyId}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['policy_delete'], jsonFormat=jsonFormat)
        return content

    def policyCopy(self, policyId, jsonFormat=True):
        self.constructParamsAndHeaders(params={'policy_id':policyId}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['policy_copy'], jsonFormat=jsonFormat)
        return content

    def policyAdd(self, policyData, jsonFormat=True):
        self.constructParamsAndHeaders(headers=policyData , jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['policy_copy'], jsonFormat=jsonFormat)
        return content

    def policyEdit(self, policyData, jsonFormat=True):
        self.constructParamsAndHeaders(headers=policyData , jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['policy_edit'], jsonFormat=jsonFormat)
        return content

    def policyDownload(self, policyId, jsonFormat=True):
        self.constructParamsAndHeaders(params={'policy_id':policyId}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['policy_download'], jsonFormat=jsonFormat)
        return content

    def policyFileUpload(self, jsonFormat=True):
        pass

    def policyFilePolicyImport(self, fileNessusName, jsonFormat=True):
        self.constructParamsAndHeaders(params={'file':fileNessusName}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['policy_file_policy_import'], jsonFormat=jsonFormat)
        return content

    def policyFilePolicyImport(self, fileNessusName, jsonFormat=True):
        self.constructParamsAndHeaders(params={'file':fileNessusName}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['policy_file_policy_import'], jsonFormat=jsonFormat)
        return content

    def scanNew(self, target, policyId, scanName, jsonFormat=True):
        self.constructParamsAndHeaders(params={'target':target,
                                               'policy_id':policyId,
                                               'scan_name':scanName}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_new'], jsonFormat=jsonFormat)
        return content

    def scanStop(self, scanUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'scan_uuid':scanUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_stop'], jsonFormat=jsonFormat)
        return content

    def scanPause(self, scanUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'scan_uuid':scanUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_pause'], jsonFormat=jsonFormat)
        return content

    def scanResume(self, scanUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'scan_uuid':scanUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_resume'], jsonFormat=jsonFormat)
        return content

    def scanList(self, jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_list'], jsonFormat=jsonFormat)
        return content

    def scanTimeZones(self, jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_timezones'], jsonFormat=jsonFormat)
        return content

    def scanTemplateNew(self, policyId, target, jsonFormat=True):
        self.constructParamsAndHeaders(params={'policy_id':policyId,
                                               'target':target}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_template_new'], jsonFormat=jsonFormat)
        return content


    def scanTemplateEdit(self, template, templateName, policyId, target, jsonFormat=True):
        self.constructParamsAndHeaders(params={'template':template,
                                               'template_name':templateName,
                                               'policy_id':policyId,
                                               'target':target} , jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_template_edit'], jsonFormat=jsonFormat)
        return content

    def scanTemplateDelete(self, template, jsonFormat=True):
        self.constructParamsAndHeaders(params={'template':template} , jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_template_edit'], jsonFormat=jsonFormat)
        return content

    def scanTemplateLaunch(self, template, jsonFormat=True):
        self.constructParamsAndHeaders(params={'template':template} , jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['scan_template_edit'], jsonFormat=jsonFormat)
        return content

    def reportList(self, template, jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_list'], jsonFormat=jsonFormat)
        return content

    def reportDelete(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_delete'], jsonFormat=jsonFormat)
        return content

    def reportHosts(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_hosts'], jsonFormat=jsonFormat)
        return content

    def report2HostsPlugin(self, reportUuid, severity, pluginId, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'severity':severity,
                                               'plugin_id':pluginId}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report2_hosts_plugin'], jsonFormat=jsonFormat)
        return content

    def report2Hosts(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report2_hosts'], jsonFormat=jsonFormat)
        return content

    def reportPorts(self, reportUuid, hostname, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'hostname':hostname}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_ports'], jsonFormat=jsonFormat)
        return content

    def report2Ports(self, reportUuid, hostname, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'hostname':hostname}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report2_ports'], jsonFormat=jsonFormat)
        return content

    def reportDetails(self, reportUuid, hostname, port, protocol, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'hostname':hostname,
                                               'port':port,
                                               'protocol':protocol}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_details'], jsonFormat=jsonFormat)
        return content

    def report2DetailsPlugin(self, reportUuid, hostname, port, protocol, severity, pluginId, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'hostname':hostname,
                                               'port':port,
                                               'protocol':protocol,
                                               'severity':severity,
                                               'plugin_id':pluginId}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report2_details_plugin'], jsonFormat=jsonFormat)
        return content

    def report2Details(self, reportUuid, hostname, port, protocol, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'hostname':hostname,
                                               'port':port,
                                               'protocol':protocol}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report2_details_plugin'], jsonFormat=jsonFormat)
        return content

    def reportTags(self, reportUuid, hostname, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'hostname':hostname}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_tags'], jsonFormat=jsonFormat)
        return content

    def reportHasAuditTrail(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_hasAuditTrail'], jsonFormat=jsonFormat)
        return content

    def reportAttributesList(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_attributes_list'], jsonFormat=jsonFormat)
        return content

    def reportErrors(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_errors'], jsonFormat=jsonFormat)
        return content

    def reportHasKB(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_hasKB'], jsonFormat=jsonFormat)
        return content

    def reportCanDeleteItems(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_canDeleteItems'], jsonFormat=jsonFormat)
        return content

    def reportCanDeleteItems(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_canDeleteItems'], jsonFormat=jsonFormat)
        return content


    def report2DeleteItem(self, reportUuid, hostname, port, pluginId, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'hostname':hostname,
                                               'port':port,
                                               'plugin_id':pluginId}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report2_deleteItem'], jsonFormat=jsonFormat)
        return content

    def reportTrailDetails(self, reportUuid, hostname, pluginId, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'hostname':hostname,
                                               'plugin_id':pluginId}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_trail_details'], jsonFormat=jsonFormat)
        return content

    def report2Vulnerabilities(self, reportUuid, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report2_vulnerabilities'], jsonFormat=jsonFormat)
        return content

    def reportChapterList(self, jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_chapter_list'], jsonFormat=jsonFormat)
        return content

    def reportChapter(self, reportUuid, chapters, format, token, v1=False, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'chapters':chapters,
                                               'format':format,
                                               'token':token,
                                               'v1':v1}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_chapter'], jsonFormat=jsonFormat)
        return content

    def reportFileDownload(self, reportUuid, v1=False, v2=True, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'v1':v1,
                                               'v2':v2}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_chapter'], jsonFormat=jsonFormat)
        return content

    def reportFileImport(self, fileName, jsonFormat=True):
        self.constructParamsAndHeaders(params={'file':fileName}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_file_import'], jsonFormat=jsonFormat)
        return content


    def reportFileXsltList(self, fileName, jsonFormat=True):
        self.constructParamsAndHeaders(jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_file_xslt_list'], jsonFormat=jsonFormat)
        return content

    def reportFileXslt(self, reportUuid, xslt, token, jsonFormat=True):
        self.constructParamsAndHeaders(params={'report':reportUuid,
                                               'xslt':xslt,
                                               'token':token}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_file_xslt'], jsonFormat=jsonFormat)
        return content

    def reportFileXsltDownload(self, fileName, jsonFormat=True):
        self.constructParamsAndHeaders(params={'fileName':fileName}, jsonFormat=jsonFormat)
        content = self.requestNessus(self.url+self.nessusFunctions['report_file_xslt_download'], jsonFormat=jsonFormat)
        return content


n = NessusClient('127.0.0.1', '8834')
content = n.login('adastra', 'peraspera')
print content
print "\n"
print "\n"
content = n.feed()
print content
print "\n"
print "\n"
content = n.securesettingsList()
print content
print "\n"
print "\n"
content = n.secureSettings()
print content
print "\n"
print "\n"
content = n.logout()
print content
print "\n"
print "\n"
