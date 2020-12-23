import json
import scrapy
from tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['om.qq.com']
    start_urls = [
        'https://om.qq.com/marticle/article/list?'
        'category=&'
        'search=&'
        'source=&'
        'startDate=&'
        'endDate=&'
        'num=50&'
        'ftype=&'
        'readChannel=all&'
        'refreshField=&'
        'relogin=1',
    ]
    headers = {
        'Host': 'om.qq.com',
        'accept': 'application/json, text/plain, */*',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://om.qq.com/main/management/articleManage',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,da;q=0.7',
    }
    cookies = None
    index = 0

    def __init__(self):
        super(TencentSpider, self).__init__()

        self.cookies = self.get_cookies()

    @staticmethod
    def get_cookies():
        """
        读取cookies
        :return:
        """
        with open('data/cookies.json', 'r') as f:
            cookies = json.load(f)

        return cookies

    def start_requests(self):
        return [scrapy.Request(
            url=self.start_urls[0], headers=self.headers, cookies=self.cookies, callback=self.parse)]

    def parse(self, response, **kwargs):
        data = response.json()

        for item in data['data']['articles']:
            t_item = TencentItem()
            self.index += 1
            t_item['index'] = self.index
            t_item['title'] = item['title']
            t_item['url'] = item['url']
            t_item['alt_time'] = item['alt_time']

            yield t_item

        articles = data['data']['articles']
        if len(articles) > 0:
            alt_time = articles[-1]['alt_time']
            url = f'https://om.qq.com/marticle/article/list?' \
                  f'category=&' \
                  f'search=&' \
                  f'source=&' \
                  f'startDate=&' \
                  f'endDate=&' \
                  f'num=50&' \
                  f'ftype=&' \
                  f'readChannel=all&' \
                  f'refreshField={alt_time}&' \
                  f'relogin=1'

            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)
