import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from ..items import ZhibobaItem
import json
import lxml.html
import requests
import json


class Myspider(scrapy.Spider):
    name = 'zhiboba'
    allowed_domains = []
    json_url = 'https://bifen4pc.qiumibao.com/json/list.htm?31431'
    bash_url = 'https://www.zhibo8.cc/'

    def start_requests(self):
        yield Request(self.bash_url, self.parse_index)

    """
    def parse_json(self, response):
        json_url = self.json_url
        wbdata = requests.get(json_url).text
        data = json.loads(wbdata)
        news = data['list']
        for n in news:
            home_team = n['home_team']
            visit_team = n['visit_team']
            home_score = n['home_score']
            visit_score = n['visit_score']
            sdate = n['sdate']
            start = n['start']
        yield Request(self.bash_url, self.parse_index,meta={'sdate': sdate,
                                                        'start': start,
                                                        'home_team': home_team,
                                                        'home_score': home_score,
                                                        'visit_team': visit_team,
                                                        'visit_score': visit_score})

    """

    def parse_index(self, response):
        print("enter the parse_index")
        print(self.bash_url)
        divs = BeautifulSoup(response.text, 'lxml').find_all(label=re.compile("足球"))
        item = ZhibobaItem()
        for single_div in divs:
            item['label'] = single_div.get('label')
            item['sdate'] = single_div.get('data-time')
            item['linkurl'] = self.bash_url + single_div.find('a')['href']
            home_team = single_div.get_text().split()[2]
            item['home_team'] = home_team
            visit_team = single_div.get_text().split()[4]
            item['visit_team'] = visit_team
            print("quit the parse_index")
            print(self.json_url)
            yield Request(self.json_url, callback=self.get_score, meta={'home_team': home_team,
                                                                        'visit_team': visit_team
                                                                        })

    def get_score(self, response):
        print("enter the get_score")
        data = response.text
        jsondata = json.loads(data)
        jsondatas = jsondata['list']
        for single_jsondata in jsondatas:
            print(single_jsondata)
            if single_jsondata['home_team'] == response.meta['home_team']\
                    and single_jsondata['visit_team'] == response.meta['visit_team']:
                print(single_jsondata['home_team'], single_jsondata['visit_team'])
        print("quit the get_score")
