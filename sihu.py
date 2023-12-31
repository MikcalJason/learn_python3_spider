# encoding = utf-8
import concurrent
import os
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import you_get
import sys


def header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }

    return headers


def request_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None


def demo():
    base_url = 'https://www.091b2.com'
    module_urls = get_all_module_urls(base_url)
    for item in module_urls:
        dfs(item)


def download_mp4(url, path):
    sys.argv = ['you-get', '--format=mp4', '-o', path, url]
    you_get.main()


def dfs(url):
    html = request_page(url)
    soup = BeautifulSoup(html, 'lxml')
    elements = soup.find('body').find_all('dd')


def get_all_module_urls(base_url):
    entry_url = base_url + '/Enter/home.html'
    html = request_page(entry_url)
    soup = BeautifulSoup(html, 'lxml')
    elements = soup.find('body').find_all('dd')

    urls = []
    for item in elements:
        url = item.find('a').get('href')
        print('页面链接：%s' % url)
        urls.append(base_url + url)
    return urls


def get_mp4_link(self, url, links):
    html = request_page(url)
    soup = BeautifulSoup(html, 'lxml')
    link = soup.find('body').find('div', class_='download').find('a').get('href')
    links.append(link)
    return links


if __name__ == '__main__':
    # 获取每一页的链接和名称
    demo()
