#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import urlparse

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "http://lab.awh.zdresearch.com/chapter2/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)

parsed_html = BeautifulSoup(response.content, 'html.parser') #soup = BeautifulSoup(html_doc, 'html.parser')
forms_list = parsed_html.findAll("form")

# print(forms_list)

# for i in forms_list:
#     print(i.prettify())

for form in forms_list:
    # print(form)
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    method = form.get("method")

    input_lists = form.findAll("input")
    post_data = {}
    for input in input_lists:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "test"
        
        post_data[input_name] = input_value
    result = requests.post(post_url, data=post_data)
    print(result.content)