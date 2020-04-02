from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy
import re
from webspider.items import Website
from inscriptis import get_text
import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

class GeneralSpider(scrapy.Spider):
    name = 'general'
    # urls = open("URLs", "r").readlines()
    # allowed_domains = [(re.split(r'h..p.*://', i, maxsplit=0)[1] if re.match(r'h..p.*://', i) else i).strip() for i in urls if i]
    # # print(allowed_domains[30])
    # start_urls = list(set(["https://"+i for i in allowed_domains]))
    # allowed_domains = ['baidu.com']
    # start_urls = ['https://www.baidu.com']

    def __init__(self, source="es", *args, **kwargs):
        super(GeneralSpider, self).__init__(*args, **kwargs)
        if (source=="es"):
            client = Elasticsearch()
            s = Search(using=client, index="website", doc_type="items")
            s = s.source([])
            self.start_urls = [h.meta.id for h in s.scan()]
        else:
            urls = open(source, "r").readlines()
            allowed_domains = [(re.split(r'h..p.*://', i, maxsplit=0)[1] if re.match(r'h..p.*://', i) else i).strip() for i in urls if i]
            self.start_urls = list(set(["https://"+i for i in allowed_domains]))
        


    def parse(self, response):
        # """
        # The lines below is a spider contract. For more info see:
        # http://doc.scrapy.org/en/latest/topics/contracts.html

        # @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        # @scrapes name
        # """
        # sel = Selector(response)
        # sites = sel.xpath('//ul[@class="directory-url"]/li')
        # items = []
        item = Website()
        markup = response.xpath('/html').extract()
        regex = re.compile(r'[\n\r\t]')
        content = get_text(regex.sub(" ", markup[0]))
        
        item["url"] = response.request.url
        item["snapshot"] = {}

        item["snapshot"]["response_url"] = response.url
        item["snapshot"]["status"] = response.status
        item["snapshot"]["title"] = response.xpath('/html/head/title/text()').extract_first()
        item["snapshot"]["content"] = content
        item["snapshot"]["timestamp"] = datetime.datetime.now().timestamp()
        
        return item


        # for site in sites:
        #     item = Website()
        #     item['name'] = site.xpath('a/text()').extract()
        #     item['url'] = site.xpath('a/@href').extract()
        #     item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
        #     items.append(item)

        # return items
