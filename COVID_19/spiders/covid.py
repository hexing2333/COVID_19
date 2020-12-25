import scrapy
import json
from COVID_19.items import Covid19Item
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')#无头浏览器设置

class covid(scrapy.spiders.Spider):
    name = "covid"
    start_urls = ["https://news.qq.com/zt2020/page/feiyan.htm#/?nojump=1"]
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=options)#实例化浏览器对象
        super().__init__()

    def start_requests(self):
        url = "https://news.qq.com/zt2020/page/feiyan.htm#/?nojump=1"
        response = scrapy.Request(url,callback=self.parse_in)
        yield response

    def close(self,spider):
        self.browser.quit()


    def parse_in(self,response):
        item = Covid19Item()
        print(response.text)
        item['country']="中国"
        item['increased']=response.xpath(
            '//div[@class="recentNumber"]/div[@class="icbar confirm"]/div[@class="add"]/span/text()'
        ).extract()[0].replace("+","")

        item['total']=response.xpath(
            '//div[@class="recentNumber"]/div[@class="icbar confirm"]/div[@class="number"]/text()'
        ).extract()[0]

        item['cure']=response.xpath(
            '//div[@class="recentNumber"]/div[@class="icbar heal"]/div[@class="number"]/text()'
        ).extract()[0]

        item['dead']=response.xpath(
            '//div[@class="recentNumber"]/div[@class="icbar dead"]/div[@class="number"]/text()'
        ).extract()[0]

        yield(item)
        new_url = "https://news.qq.com/zt2020/page/feiyan.htm#/global?nojump=1"
        yield scrapy.Request(url=new_url, callback=self.parse_global,dont_filter=True)


    def parse_global(self,response):
        print(response.text)
        item = Covid19Item()
        for each in response.xpath('//tr[@class="areaBox opened"]'):
            item['country'] = each.xpath('th[@class="area"]/span/text()').extract()[0]
            item['increased'] = each.xpath('td[1]/text()').extract()[0]
            item['total'] = each.xpath('td[2]/text()').extract()[0]
            item['cure'] = each.xpath('td[3]/text()').extract()[0]
            item['dead'] = each.xpath('td[4]/text()').extract()[0]
            yield(item)

