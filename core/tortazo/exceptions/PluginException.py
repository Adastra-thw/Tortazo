# coding=utf-8
'''
Created on 19/08/2014
@author: Adastra
CoreException.py

CoreException is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

CoreException is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from core.tortazo.exceptions.CoreException import CoreException

class PluginException(CoreException):
    
    def __init__(self, message, trace, plugin, method):
        CoreException.__init__(self, message, trace)
        self.plugin = plugin
        self.method = method
    
    def getPlugin(self):
        return self.plugin
    
    def getMethod(self):
        return  self.method
