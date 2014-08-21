# coding=utf-8
'''
Created on 18/08/2014

#Author: Adastra.
#twitter: @jdaanial

Validator.py

Validator is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

Validator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Tortazo; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

import socket

def is_valid_ipv4_address(address):
    if address is None or address == '':
        return False
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def is_valid_ipv6_address(address):
    if address is None or address == '':
        return False
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True

def is_valid_domain(domain):
    try:
        data = socket.gethostbyname(domain)
        ip = repr(data)
        if ip is not None and ip != '':
            return True
    except Exception:
        return False    

def is_valid_onion_address(onionAddress):
    if onionAddress.endswith('.onion') == False:
        return False
    validchars ='234567' + string.lowercase
    valid = set(validchars)
    onionAddress = onionAddress.replace('.onion', '')
    onionAddress = onionAddress.replace('http://', '')
    if len(onionAddress) != 16:
        return False
    return set(onionAddress).issubset(valid)


def is_valid_url(url):
    import urllib
    try:
        urllib.urlopen(url)
    except IOError:
        return False
    return True

def is_valid_port(port):
    if str(port).isdigit() and port in range(1,65535):
        return True
    else:
        return  False
    
def is_valid_regex(regex):
    import re
    try:
        re.compile(regex)
        return True
    except re.error:
        return False
