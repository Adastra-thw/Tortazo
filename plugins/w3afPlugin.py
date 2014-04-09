# coding=utf-8
'''
Created on 22/01/2014

#Author: Adastra.
#twitter: @jdaanial

w3afPlugin.py

w3afPlugin is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3afPlugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

#from core.tortazo.pluginManagement.BasePlugin import BasePlugin

import w3af.core.controllers.w3afCore
import w3af.core.data.kb.config as cf
import w3af.core.data.kb.knowledge_base as kb
from w3af.core.controllers.core_helpers.target import w3af_core_target
from w3af.core.data.parsers.url import URL as URL_KLASS

class w3afPlugin: #(BasePlugin):
    '''
    Class to  implement a simple plugin which prints the TOR Data structure.
    '''

    def __init__(self):
        pass
        #BasePlugin.__init__(self)

    def __del__(self):
        pass

    def runPlugin(self):
        '''
        The most simplest plugin! Just prints the tor data structure.
        '''
        print "run plugin"
        target = w3af_core_target()
        core = w3af.core.controllers.w3afCore.w3afCore()

        print core.target._verify_url(URL_KLASS('http://www.google.com/'))
        core.plugins.init_plugins()

        plugin_types = core.plugins.get_plugin_types()
        print plugin_types
        plugin_list = core.plugins.get_plugin_list('audit')
        print plugin_list

        plugin_inst = core.plugins.get_plugin_inst('audit', 'sqli')
        print plugin_inst

        for plugin_name in core.plugins.get_plugin_list('audit'):
            plugin_inst = core.plugins.get_plugin_inst('audit', plugin_name)
            print plugin_inst.get_name()

        enabled = ['sqli', ]
        core.plugins.set_plugins(enabled, 'audit')
        retrieved = core.plugins.get_enabled_plugins('audit')
        print retrieved


w3afPl = w3afPlugin()
w3afPl.runPlugin()