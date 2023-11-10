import pts
import requests
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
import time

def get_reference(data):
    flag = 0
    reference_lenght = 5
    reference_list = []
    reference_url_list = []
    for i in range(len(data)):
        reference_str = ""
        if 'References' in data[i]:
            flag = 1
        if flag==1 and data[i][0]=='[':
            if data[i+1][0]!='[':
                reference_str += (data[i]+data[i+1])
                #print(data[i],end="")
                #print(data[i+1])
            else:
                reference_str += data[i]
                #print(data[i])
        if reference_str!="":
            #print(reference_str)
            reference_list.append(reference_str)


    for i in range(len(reference_list)):
        idx = reference_list[i].find("]")
        if idx!=-1:
            reference_list[i] = reference_list[i][idx+2:]

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    chrome_driver_path = "./chromedriver.exe"
    service = webdriver.chrome.service.Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    reference_list = reference_list[:reference_lenght]

    for i in range(reference_lenght):
        url = 'https://www.google.com/search?q='+reference_list[i]
        driver.get(url)

        html = driver.page_source
        soup = BeautifulSoup(html)

        result = soup.select('.tF2Cxc')  #원하는 class / name을 F12에서 찾기 # select 는 list로 가져온다. #클래스는 앞에 . 점 붙여준다.

        for j in result :  
            if 'https://arxiv.org/' in j.a.attrs['href']:
                reference_url_list.append(j.a.attrs['href'])
                break
    driver.close()
    return reference_list, reference_url_list