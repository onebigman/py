import html
import json
import re
from typing import Dict
from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
from bs4 import BeautifulSoup

def get_page_index(offset,keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 1
    }
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错')
        return None

def parse_page_detail(html):
    soup = BeautifulSoup(html,'html.parser')
    title = soup.select('title')
    if title:
        title = title[0].get_text()
    print(title)
    #images_pattern = re.compile('var gallery = (.*?);',re.S)
    #result = re.search(images_pattern,html)
    #if result:
    #    print(result.group(1))

def main():
    html = get_page_index(0,'街拍')
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            parse_page_detail(html)

if __name__ == '__main__':
    main()
