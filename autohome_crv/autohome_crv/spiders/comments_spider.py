# -*- coding: utf-8 -*-
import scrapy
from autohome_crv.items import AutohomeCrvItem, AutohomeCrvLoader
import json, time

class Commentspider(scrapy.Spider):
    name = 'comments_spider'
    allowed_domains = ['koubei.app.autohome.com.cn']

    def start_requests(self):
        last_page = 30
        for page in range(1, last_page + 1):
            url = f'https://koubei.app.autohome.com.cn/autov9.3.0/alibi/seriesalibiinfos-pm2-ss314-st0-p{page}-s20-isstruct1-o0.json'
            headers = {''}
            yield scrapy.Request(url)


    def parse(self, response):
        data = json.loads(response.text)
        for item in data['result']['list']:
            eid = item['Koubeiid']
            url = f'https://koubei.app.autohome.com.cn/autov9.3.0/alibi/NewEvaluationInfo.ashx?eid={eid}&useCache=1'
            yield scrapy.Request(url, self.comment_parse)
    
    def comment_parse(self, response):
        data = json.loads(response.text)['result']
        item = AutohomeCrvItem()
        item_loader = AutohomeCrvLoader(item=item)
        for field in item.fields:
            item_loader.add_value(field, data.get(field)) # 直接提取json中，item已经定义的项
        
        return item_loader.load_item()
        
