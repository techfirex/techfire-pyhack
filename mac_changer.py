#!/usr/bin/env python

import subprocess
import optparse
import re

def get_argumets():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Enter Interface Name")
    parser.add_option("-m", "--mac", dest="new_mac", help="Enter New MAC")
    (options, argumets) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    if not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info")
    return options

def change_mac(interface, new_mac):
    print("[+] Changing Mac Address For " + options.interface + " to " + options.new_mac)
    subprocess.call(["sudo", "ifconfig", options.interface, "down"])
    subprocess.call(["sudo", "ifconfig", options.interface, "hw", "ether", options.new_mac])
    subprocess.call(["sudo", "ifconfig", options.interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not get MAC address")

options = get_argumets()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed")

