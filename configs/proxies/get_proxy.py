import requests
from bs4 import BeautifulSoup

PROXY_URL = 'https://www.xicidaili.com/nt/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}

def getProxies(PROXY_URL, headers):
    proxies = []
    res = requests.get(PROXY_URL, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    proxy_list = soup.find_all(text="HTTP")

    for proxy in proxy_list:
        counter = 0
        for item in proxy.parent.previous_siblings:
            counter += 1
            if counter == 6:
                port_num = item.string
            elif counter == 8:
                ip = item.string
        

        proxies.append('{}:{}'.format(ip, port_num))
    
    return proxies

proxies = getProxies(PROXY_URL, headers)
with open('configs/proxy_list_2.txt', 'w') as f:
    for proxy in proxies:
        f.write(proxy)
        f.write('\n')

