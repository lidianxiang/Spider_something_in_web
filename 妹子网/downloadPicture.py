import json
import requests
from meiZiTu import get_response
import os
from lxml import etree
from time import sleep


def read_json_file(filename):
    '''读取文件'''
    with open(filename) as f:
        data = f.read()
        data = json.loads(data)

    # print(data)
    return data


def create_dictionary(name):
    '''创建文件夹'''
    try:
        os.mkdir(name)
    except Exception as e:
        print(e)


def download_picture(name, url):
    '''下载图片'''
    # pass
    headers = {
        'Referer': 'https://www.mzitu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    img_content = get_response(url, headers=headers).content
    filename = 'Pictures/' + name + '/' + name + url[-8:]
    try:
        with open(filename, 'wb') as f:
            f.write(img_content)
            sleep(1)
    except Exception as e:
        print(e)


def get_picture_url(name, url):
    '''获取图片'''
    # proxy = {'https': 'https://123.163.97.121:9999'}
    headers = {
        'Referer': 'https://www.mzitu.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Mobile Safari/537.36'
    }
    response = get_response(url, headers=headers)
    html = etree.HTML(response.text)
    img_url = html.xpath('//div[@class="main-image"]//img//@src')[0]
    # print(img_url)
    download_picture(name, url=img_url)
    try:
        # 获取下一页
        next_page_url = html.xpath('//a[./span/text()="下一页»"]/@href')[0]
        while next_page_url:
            print(next_page_url)
            response = get_response(next_page_url)
            html = etree.HTML(response.text)
            img_url = html.xpath('//div[@class="main-image"]//img/@src')[0]
            download_picture(name, url=img_url)
            # 获取下一页
            next_page_url = html.xpath('//a[./span/text()="下一页»"]/@href')[0]
    except Exception as e:
        print(e, '该套图保存结束')


def run():
    '''下载图片'''
    # 读取json文件
    data = read_json_file('meizi.json')
    create_dictionary(name='Pictures')
    for d in data:
        create_dictionary(name='Pictures/' + d['name'])
        # print(d)
        get_picture_url(name=d['name'], url=d['url'])


if __name__ == '__main__':
    run()
