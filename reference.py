import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def get_reference(data):
    flag = 0
    reference_length = 5  # 오타 수정 : reference_lenght -> reference_length
    reference_list = []
    reference_url_list = []
    for i in range(len(data)):
        reference_str = ""
        if 'References' in data[i]:
            flag = 1
        if flag == 1 and data[i][0] == '[':
            if data[i + 1][0] != '[':
                reference_str += (data[i] + data[i + 1])
                #print("DATA[i]: " + data[i], end="")
                #print("DATA[i+1]: " + data[i + 1])
            else:
                reference_str += data[i]
                #print("DATA[i]: " + data[i])
        if reference_str != "":
            #print("reference_str : " +reference_str)
            reference_list.append(reference_str)


    if len(reference_list) < reference_length:  # 수정 : reference_list의 길이가 reference_length보다 작을 경우 예외 처리
            reference_length = len(reference_list)

    for i in range(len(reference_list)):
        idx = reference_list[i].find("]")
        if idx != -1:
            reference_list[i] = reference_list[i][idx + 2:]

    reference_list = reference_list[:reference_length]
    #print("reference_length : " + str(reference_length))

    for i in range(reference_length):
        url = 'https://www.google.com/search?q=' + urllib.parse.quote(reference_list[i])  # 수정 : 검색어를 URL 인코딩하여 사용
        params = {
            'client': 'chrome',
            'q': reference_list[i]  # 수정 : 검색어를 원하는 검색어로 변경
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            html = response.content
            soup = BeautifulSoup(html, 'html.parser')
            result = soup.select('div.egMi0.kCrYT')

            for i in result:
                if 'https://arxiv.org/' in i.a.attrs['href']:
                    temp_href = i.a.attrs['href']
                    temp_href_delete_idx = temp_href.find("&")
                    reference_url_list.append(i.a.attrs['href'][7:temp_href_delete_idx])
                    break
        else:
            print(f"Failed to retrieve suggestions. Status code: {response.status_code}")

    return reference_list, reference_url_list
