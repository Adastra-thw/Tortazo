"""
test_xml_file.py

Copyright 2012 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import os
import StringIO

from lxml import etree
from nose.plugins.attrib import attr

from w3af import ROOT_PATH
from w3af.core.data.kb.tests.test_vuln import MockVuln
from w3af.core.data.parsers.url import URL
from w3af.core.controllers.ci.moth import get_moth_http
from w3af.plugins.tests.helper import PluginTest, PluginConfig


@attr('smoke')
class TestXMLOutput(PluginTest):

    target_url = get_moth_http('/audit/sql_injection/where_integer_qs.py')

    FILENAME = 'output-unittest.xml'
    XSD = os.path.join(ROOT_PATH, 'plugins', 'output', 'xml_file', 'report.xsd')

    _run_configs = {
        'cfg': {
            'target': target_url + '?id=3',
            'plugins': {
                'audit': (PluginConfig('sqli'),),
                'output': (
                    PluginConfig(
                        'xml_file',
                        ('output_file', FILENAME, PluginConfig.STR)),
                )
            },
        }
    }

    def test_found_vuln(self):
        cfg = self._run_configs['cfg']
        self._scan(cfg['target'], cfg['plugins'])

        kb_vulns = self.kb.get('sqli', 'sqli')
        file_vulns = self._from_xml_get_vulns()

        self.assertEqual(len(kb_vulns), 1, kb_vulns)

        self.assertEquals(
            set(sorted([v.get_url() for v in kb_vulns])),
            set(sorted([v.get_url() for v in file_vulns]))
        )

        self.assertEquals(
            set(sorted([v.get_name() for v in kb_vulns])),
            set(sorted([v.get_name() for v in file_vulns]))
        )

        self.assertEquals(
            set(sorted([v.get_plugin_name() for v in kb_vulns])),
            set(sorted([v.get_plugin_name() for v in file_vulns]))
        )

        self.assertEqual(validate_XML(file(self.FILENAME).read(), self.XSD),
                         '')

    def _from_xml_get_vulns(self):
        xp = XMLParser()
        parser = etree.XMLParser(target=xp)
        vulns = etree.fromstring(file(self.FILENAME).read(), parser)
        return vulns

    def tearDown(self):
        super(TestXMLOutput, self).tearDown()
        try:
            os.remove(self.FILENAME)
        except:
            pass


class XMLParser:
    
    vulns = []

    _inside_body = False
    _data_parts = []
    
    def start(self, tag, attrib):
        """
        <vulnerability id="[87]" method="GET" name="Cross site scripting vulnerability"
                       plugin="xss" severity="Medium" url="http://moth/w3af/audit/xss/simple_xss_no_script_2.php"
                       var="text">
        """
        if tag == 'vulnerability':
            name = attrib['name']
            plugin = attrib['plugin']
            
            v = MockVuln(name, None, 'High', 1, plugin)
            v.set_url(URL(attrib['url']))
            
            self.vulns.append(v)
        
        # <body content-encoding="text">
        elif tag == 'body':
            content_encoding = attrib['content-encoding']
            
            assert content_encoding == 'text'
            self._inside_body = True
    
    def end(self, tag):
        if tag == 'body':
            
            data = ''.join(self._data_parts)
            
            assert 'syntax error' in data
            assert 'near' in data
            
            self._inside_body = False
            self._data_parts = []
    
    def data(self, data):
        if self._inside_body:
            self._data_parts.append(data)

    def close(self):
        return self.vulns


def validate_XML(content, schema_content):
    """
    Validate an XML against an XSD.

    :return: The validation error log as a string, an empty string is returned
             when there are no errors.
    """
    xml_schema_doc = etree.parse(schema_content)
    xml_schema = etree.XMLSchema(xml_schema_doc)
    xml = etree.parse(StringIO.StringIO(content))

    # Validate the content against the schema.
    try:
        xml_schema.assertValid(xml)
    except etree.DocumentInvalid:
        return xml_schema.error_log

    return ''
