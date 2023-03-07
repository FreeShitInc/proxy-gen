import requests, threading
from bs4 import BeautifulSoup
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from time import sleep
options = Options()
options.add_argument("--headless")

wp = []

proxy_list = []
def proxy_scrape():
    global proxy_list
    funni_list = requests.get('https://www.proxy-list.download/api/v1/get?type=http').text
    lines = funni_list.splitlines()
    for i in lines:
        if i not in proxy_list:
            proxy_list.append(i)
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    lines = text.splitlines()
    for i in range(299):
        if lines[i+3] not in proxy_list:
            proxy_list.append(lines[i+3])
    html = requests.get('https://us-proxy.org/').text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    lines = text.splitlines()
    for i in range(199):
        if lines[i+3] not in proxy_list:
            proxy_list.append(lines[i+3])

proxy_scrape()

def checker(prxy):
    global wp
    
    format = {
    'http': f'http://{prxy}',
            'https': f'http://{prxy}'
    }
    try:
        r=requests.get("http://httpbin.org/ip", proxies=format, timeout=15)
        if r.status_code == 200:
            if prxy not in wp:
                print(f'{Fore.BLUE}proxy: {Fore.GREEN}{prxy} works')
                wp.append(prxy)
    except:
        print(f'{Fore.BLUE}proxy: {Fore.RED}{prxy} doesnt work')

sleep(10)


print("""
         ▄▄▄·▄▄▄        ▐▄• ▄  ▄· ▄▌   ▄▄ • ▄▄▄ . ▐ ▄ 
        ▐█ ▄█▀▄ █· ▄█▀▄  █▌█▌▪▐█▪██▌  ▐█ ▀ ▪▀▄.▀·•█▌▐█
         ██▀·▐▀▀▄ ▐█▌.▐▌ ·██· ▐█▌▐█▪  ▄█ ▀█▄▐▀▀▪▄▐█▐▐▌
        ▐█▪·•▐█•█▌▐█▌.▐▌▪▐█·█▌ ▐█▀·.  ▐█▄▪▐█▐█▄▄▌██▐█▌
        .▀   .▀  ▀ ▀█▄▀▪•▀▀ ▀▀  ▀ •   ·▀▀▀▀  ▀▀▀ ▀▀ █▪
""")
teds = len(proxy_list)
for i in range(teds):
    t = threading.Thread(checker(proxy_list[i]))
    t.start()
    print('starting thread')

print(f'Genned {len(wp)} proxies')

filename = input("filename> ")

with open(filename,'w') as f:
    f.write(wp)
    f.close()
