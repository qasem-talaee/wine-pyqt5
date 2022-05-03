import requests
from bs4 import BeautifulSoup
import time

class Vulkan:
     
    def __init__(self):
        self.link_list = [
            'https://github.com/doitsujin/dxvk/releases',
            'https://github.com/HansKristian-Work/vkd3d-proton/releases',
            #'https://github.com/jp7677/dxvk-nvapi/releases',
            #'https://github.com/ishitatsuyuki/LatencyFleX/releases',
        ]
     
    def __get_url(self, url):
        flag = False
        while not flag:
            try:
                page = requests.get(url)
            except:
                print("Try again to open [url] : " + url)
                time.sleep(1)
            else:
                flag = True
        soup = BeautifulSoup(page.content, 'html.parser')
        div = soup.find_all("div", class_="Box Box--condensed mt-3")[0]
        li = div.find_all("li", class_="Box-row")[0]
        a = li.find("a")
        return a.get('href')
    
    def get_list(self):
        result = []
        for link in self.link_list:
            result.append("https://github.com" + self.__get_url(link))
        return result