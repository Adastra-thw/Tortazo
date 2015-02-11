import socks
import socket
def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
socket.create_connection = create_connection

import requests

try:
    res = requests.head("http://gnionmnsscpbgu42.onion/", timeout=2)
    print res
except Exception as ex:
    print ex
