import requests
from lxml import etree
from time import sleep
import json


def get_response(url, headers=None):
    '''获取response'''
    headers = {
        'Referer': 'https://www.mzitu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    if response.status_code == 200:
        return response
    else:
        print(response.status_code)


def parse_html(response):
    '''获取网页url'''
    html = etree.HTML(response.text)
    page_img_urls = []
    page_img_content = html.xpath('//div[@class="postlist"]//ul//li')
    for img_content in page_img_content:
        img_info = {}
        img_info['name'] = img_content.xpath('./a[1]/img/@alt')[0]
        img_info['url'] = img_content.xpath('./a[1]/@href')[0]
        # print(img_info)
        page_img_urls.append(img_info)
    print(page_img_urls)
    return page_img_urls


def get_next_page_url(response):
    '''获取网页的翻页后的URL'''
    html = etree.HTML(response.text)
    next_page_url = html.xpath('//a[@class="next page-numbers"]/@href')
    # print(next_page_url)
    if len(next_page_url) > 0:
        # print(next_page_url[0])
        return next_page_url[0]
    else:
        return None


def save_to_file(filename, data):
    '''将数据保存为json格式'''
    data = json.dumps(data)
    filename = filename + '.json'
    with open(filename, 'w') as f:
        print('正在保存{}'.format(filename))
        f.write(data)
    print('保存完成')



def run():
    """
    爬取妹子图图片
    :return:
    """
    # index_urls = ['https://www.mzitu.com/xinggan/', 'https://www.mzitu.com/japan/', 'https://www.mzitu.com/taiwan/',
    #                   'https://www.mzitu.com/mm/']
    index_url = 'https://www.mzitu.com/xinggan/'
    all_img_info = []
    response = get_response(index_url)
    all_img_info.extend(parse_html(response))
    next_page_url = get_next_page_url(response)
    while next_page_url:
        print(next_page_url)
        sleep(2)
        response = get_response(next_page_url)
        all_img_info.extend(parse_html(response))
        next_page_url = get_next_page_url(response)
    print('爬取完成，共%d条数据'%len(all_img_info))
    save_to_file(filename='meizi', data=all_img_info)


if __name__ == "__main__":
    run()
