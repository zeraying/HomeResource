import re
import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from HomeResource.items import HomeresourceItem

class HousingSpider(scrapy.Spider):
    name = 'housing'
    allowed_domains = ['www.gu-gu.com']
    start_urls = ['https://www.gu-gu.com/index/all/index']

    def parse(self, response):
        img_list = response.xpath('/html/body/div[4]/div[5]/div/div[2]/dl')
        for img in img_list:
            # title = img.xpath('./dd/p[@class="title"]/a/@title').extract_first()
            price = img.xpath('./dd/div/p/span/text()').extract_first()
            location = img.xpath('./dd/p[@class="gray6"]/text()').extract_first()
            housing = HomeresourceItem(price = price, location=location)
            url = img.xpath('./dd/p[@class="title"]/a/@href').extract_first()
            # yield scrapy.Request(url='https://www.gu-gu.com/' + url, callback=self.new_parse)
            yield housing
        # 获取下一页url  `
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
                if re.match('http', i) == None:
                    i = 'https://www.gu-gu.com' + i
                    a[g] = i
                    g = g + 1
            picture = a[0]
            locate = img.xpath('./div[1]/div[2]/div[5]/div[2]/div[2]/a/text()').extract_first()
            title = img.xpath('./div[1]/h1/text()').extract_first()
            picture1 = requests.get(url=picture).content
            print(type(picture1))
            Area = img.xpath('./div[1]/div[2]/div[3]/div[3]/div[1]/text()').extract_first()
            area = float(re.sub('\D','',Area))/100
            housing = HomeresourceItem(cp=cp, information=information, picture=picture, area = area, picture1=picture1, locate = locate, title = title)
            # housing = HomeresourceItem(picture=picture)
            yield housing
