import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from HomeResource.items import HomeresourceItem


class HousingSpider(scrapy.Spider):
    name = 'housing'
    allowed_domains = ['www.gu-gu.com']
    start_urls = ['https://www.gu-gu.com/index/index/index?page=1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/index/index/index?page=\d+\.html'),
             callback='parse',
             follow=False),
    )

    def parse(self, response):
        img_list = response.xpath('/html/body/div[4]/div[5]/div/div[2]/dl')
        for img in img_list:
            title = img.xpath('./dd/p[@class="title"]/a/@title').extract_first()
            price = img.xpath('./dd/div/p/span/text()').extract_first()
            location = img.xpath('./dd/p[@class="gray6"]/text()').extract_first()
            housing = HomeresourceItem(title=title, price = price, location=location)
            # url = img.xpath('./dd/p[@class="title"]/a/@href').extract_first()
            # yield scrapy.Request(url='https://www.gu-gu.com/' + url, callback=self.new_parse)
            yield housing
        # 获取下一页url
        self.page_url = response.xpath('//*[@id="listBox"]/ul/li/a/@href').extract()
        # page_url 是一个数组
        for next_url in self.page_url:
            yield scrapy.Request(url='https://www.gu-gu.com'+next_url, callback=self.parse)

    def new_parse(self, response):
        g = 0
        img_list = response.xpath('/html/body/div[4]')
        for img in img_list:
            cp = img.xpath('./div[1]/div[2]/div[6]/div[1]/div[1]/p[1]/text()').extract_first()
            information = img.xpath('./div[2]/div[1]/div[1]/div[2]/div/div/ul/li/div[2]/text()').extract_first()
            a = img.xpath('./div[1]/div/div/a/div/ul/li/img/@src').getall()
            if g != g+1:
                num = g+1
            for i in a:
                if re.match('https', i) == None:
                    i = 'https://www.gu-gu.com' + i
                    a[g] = i
                    g = g + 1
            picture = a[0]
            locat = img.xpath('./div[1]/div[2]/div[5]/div[2]/div[2]/a/text()').extract_first()
            housing = HomeresourceItem(cp=cp, information=information, picture=picture, locat = locat)
            yield housing
