#!/usr/bin/env python
import scanner

target_url = "http://lab.awh.zdresearch.com/chapter1/DVWA/"
links_to_ignore = [""]

data_dict = {"username": "admin", "password": "password", "Login": "submit"}
vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
vuln_scanner.session.post("http://lab.awh.zdresearch.com/chapter1/DVWA/login.php", data=data_dict)

vuln_scanner.crawl()
vuln_scanner.run_scanner()