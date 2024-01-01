# encoding = utf-8
import concurrent
import os
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import you_get
import sys
import hashlib


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
            response.close()
            return response.text
    except requests.RequestException:
        return None


def demo():
    base_url = 'https://www.091b2.com'
    module_dict = get_all_module(base_url)
    all_urls = {}
    for item in module_dict.keys():
        if item.strip():
            link_urls = get_link_url_from_module(base_url, item, module_dict)
            all_urls[item] = link_urls
    all_mp4_links = []

    # 查询所有的页面进行下载
    for key in all_urls.keys():
        # 筛选
        urls = get_mp4_links(all_urls[key])
        all_mp4_links += urls

    # 多线程下载
    download_multi_threads(all_mp4_links)


def download_multi_threads(list_page_urls):
    # 获取每一个详情妹纸
    # works = len(list_page_urls)
    # with concurrent.futures.ProcessPoolExecutor(max_workers=5) as exector:
    #     for url in list_page_urls:
    #         name = hashlib.md5(url.encode()).hexdigest()
    #         # 返回哈希值的十六进制表示形式
    #     exector.submit(download_mp4, url, 'E:/mp4/{}.mp4'.format(name))
    for url in list_page_urls:
        name = hashlib.md5(url.encode()).hexdigest()
        # 返回哈希值的十六进制表示形式
        download_mp4(url, 'E:/mp4/{}.mp4'.format(name))


def get_mp4_links(link_urls):
    links_mp4_url = []
    for url in link_urls:
        link_mp4_url = get_mp4_link(url)
        links_mp4_url.append(link_mp4_url)
    return links_mp4_url


def fun01():
    url = 'https://www.091b2.com/html/202401/80645.html'
    d_url = get_mp4_link(url)


def download_mp4(url, path):
    sys.argv = ['you-get', '--format=mp4', '-o', path, url]
    you_get.main()


def get_link_url_from_module(base_url, module_key, module_dict):
    html = request_page(module_dict[module_key])
    print("获取到模块%s的网页" % module_key)
    if html is None:
        return []
    soup = BeautifulSoup(html, 'lxml')
    elements = soup.find('body').find_all('dd')
    link_urls = []
    for element in elements:
        label_a = element.find('a')
        if label_a is None:
            continue

        target = element.find('a').get('target')
        if target == '_blank':
            link_urls.append(base_url + element.find('a').get('href'))
    return link_urls


def get_all_module(base_url):
    entry_url = base_url + '/Enter/home.html'
    html = request_page(entry_url)
    soup = BeautifulSoup(html, 'lxml')
    elements = soup.find('body').find_all('dd')

    url_dict = {}
    for item in elements:
        target = item.find('a').get('target')
        if target is None:
            url = item.find('a').get('href')
            name = url.split('/')[2]
            url_dict[name] = base_url + url
            print("查找模块:{%s},链接:{%s}" % (name, url))
    return url_dict


def get_mp4_link(url):
    html = request_page(url)
    soup = BeautifulSoup(html, 'lxml')
    if soup.find('body') is None:
        return None
    if soup.find('body').find('div', class_='download') is None:
        return None
    if soup.find('body').find('div', class_='download').find('a') is None:
        return None
    link = soup.find('body').find('div', class_='download').find('a').get('href')
    print("获取到下载链接:{%s}" % link)
    return link


if __name__ == '__main__':
    # 获取每一页的链接和名称
    demo()
    # fun01()
