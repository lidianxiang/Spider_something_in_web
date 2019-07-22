import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool


# 抓取单页数据
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):

    pattern = re.compile('<dd>.*?class="movie-item".*?img data-src="(.*?)" />.*?title="(.*?)">.*?class="integer">(.*?)'
                         '</i><i class="fraction">(.*?)</i>', re.S)
    items = re.findall(pattern, html)
    # print(items)
    # 使用 yield生成器
    for item in items:
        yield {
            'img': item[0],
            'title': item[1],
            'score': item[2]+item[3]
        }


# 写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


# 主函数
def main(offset):
    url = 'https://maoyan.com/films?showType=3&sortId=3&offset=' + str(offset)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == "__main__":

    # for i in range(10):
    #     main(i * 30)
    # 引入进程池，提升抓取效率
    pool = Pool()
    pool.map(main, [i * 30 for i in range(20)])
