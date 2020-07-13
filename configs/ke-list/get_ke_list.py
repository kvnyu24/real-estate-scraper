import requests
import json
import codecs
from bs4 import BeautifulSoup

KE_URL = 'https://www.ke.com/city/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}

def getKeList(KE_URL, headers):
    ke_list = []
    res = requests.get(KE_URL, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    ke_list = soup.find_all("li", class_="CLICKDATA")
    ke_dict = {}
    for ke_item in ke_list:
        children = ke_item.find_all("a", recursive=False)
        for child in children:
            url = "https:" + str(child["href"])
            # print(location)
            name = child.contents[0]
            ke_dict.update({str(name): url}) 


    with codecs.open('ke-list.json', 'w', encoding='utf-8') as fp:
        json.dump(ke_dict, fp, ensure_ascii=False)

    



    return 

ke_list = getKeList(KE_URL, headers)

