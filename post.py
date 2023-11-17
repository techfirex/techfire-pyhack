#!/usr/bin/env python
import requests

target_url = "http://lab.awh.zdresearch.com/chapter1/DVWA/login.php"

data_dict = {"username": "admin", "password": "12345", "Login": "submit"}
response = requests.post(target_url, data=data_dict)
print(response.content)