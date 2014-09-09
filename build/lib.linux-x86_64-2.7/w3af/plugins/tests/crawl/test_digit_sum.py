"""
test_digit_sum.py

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
from w3af.plugins.tests.helper import PluginTest, PluginConfig
from w3af.core.controllers.ci.moth import get_moth_http


class TestDigitSum(PluginTest):

    target_url = get_moth_http('/crawl/digit_sum/')

    _run_config = {
        'target': None,
        'plugins': {'crawl': (PluginConfig('digit_sum',),)}
    }

    def test_found_fname(self):
        self._scan(self.target_url + 'index-3-1.html',
                   self._run_config['plugins'])
        urls = self.kb.get_all_known_urls()

        EXPECTED_URLS = ('index-3-1.html', 'index-2-1.html')

        self.assertEquals(
            set(str(u) for u in urls),
            set((self.target_url + end) for end in EXPECTED_URLS)
        )

    def test_found_qs(self):
        self._scan(self.target_url + 'index1.py?id=22',
                   self._run_config['plugins'])
        frs = self.kb.get_all_known_fuzzable_requests()

        EXPECTED_URLS = ('index1.py?id=22', 'index1.py?id=21',
                         # These last two look very uninteresting, but please take
                         # a look at the comment in digit_sum._do_request()
                         'index1.py?id=23', 'index1.py?id=20')

        self.assertEquals(
            set(str(fr.get_uri()) for fr in frs),
            set((self.target_url + end) for end in EXPECTED_URLS)
        )