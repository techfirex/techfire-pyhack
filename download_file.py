import requests

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

download("https://www.carscoops.com/wp-content/uploads/2019/11/2020-nissan-gt-r-nismo-2.jpg")