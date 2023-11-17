#!/usr/bin/env python

import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "lab.awh.zdresearch.com/chapter2/mutillidae"

# for subdomain bruteforcing
# with open("/home/tushar/pyhack/subdomain.list", "r") as wordlist_file:
#     for line in wordlist_file:
#         word = line.strip()
#         test_url = word + "." + target_url
#         response = request(target)
#         if response:
#             print("[+] Discovered sundomains --> " + test_url) 

# for directory bruteforcing
# with open("/home/tushar/pyhack/common.txt", "r") as wordlist_file:
#     for line in wordlist_file:
#         word = line.strip()
#         test_url = target_url + "/" + word
#         response = request(test_url)
#         if response:
#             print("[+] Discovered URL --> " + test_url) 