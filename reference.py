import pts
import requests
from bs4 import BeautifulSoup
import urllib.parse
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

    reference_list = reference_list[:reference_lenght]

    for i in range(reference_lenght):
        url = 'https://www.google.com/search?q='+reference_list[i]
        params = {
            'client': 'chrome',
            'q': 'Attention is all you need'  # 원하는 검색어로 변경
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            result = soup.select('div.egMi0.kCrYT')

            for i in result :  
                if 'https://arxiv.org/' in i.a.attrs['href']:
                    temp_href = i.a.attrs['href']
                    temp_href_delete_idx = temp_href.find("&")
                    reference_url_list.append(i.a.attrs['href'][7:temp_href_delete_idx])
                    break
        else:
            print(f"Failed to retrieve suggestions. Status code: {response.status_code}")

    return reference_list, reference_url_list