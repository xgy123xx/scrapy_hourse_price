# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
import re
from BeijingHousingPrice.items import BeijinghousingpriceItem
# 当连接通时，需要在中间件中手动更换代理ip
#lpush city58spider https://bj.58.com/chuzu//
class City58Spider(RedisCrawlSpider):
    name = 'city58'
    # allowed_domains = ['https://sy.58.com/']
    # start_urls = ['https://https://sy.58.com//']
    redis_key = "city58spider"
    rules = (
        Rule(LinkExtractor(allow=r'/bj.58.com/chuzu/pn\d+/'), callback='parse_item', follow=False),
    )

    def parse_house(self,response):
        item = response.meta["item"]
        # 获取房屋的粗略信息
        house_key = ["method","house_type","face_floor","village","area","address"]
        house_info_list = response.xpath('//div[contains(@class,"house-desc-item")]/ul/li')
        for index,house_info in enumerate(house_info_list,0):
            #对index=1  房屋类型数据进行处理
            if index == 4:  #特殊数据特殊处理
                info_value = house_info.xpath('./span[2]/a/text()').extract()
                info_value = '/'.join(info_value)
            else:
                info_value = house_info.xpath('./span[2]//text()').extract_first()
            info_value = ''.join(re.split(r'\s+',info_value))  #去掉中间空格、等特殊字符
            try:
                item[house_key[index]] = info_value.strip()
            except AttributeError as e:
                print("有错误")
                continue

        #获取房子具体信息
        price = response.xpath('//div[contains(@class,"house-desc-item")]//b/text()').extract_first()  # 获取房子价格
        telephone = response.xpath('//div[@class="house-chat-phone"]/span[contains(@class,"house-chat-txt")]/text()').extract_first() # 获取电话号码
        house_highlight = response.xpath('//ul[@class="introduce-item"]/li[1]/span[2]/em/text()').extract()  #获取房子亮点
        house_highlight = "、".join(house_highlight)
        if not house_highlight:
            house_highlight = "无亮点"
        house_desc = response.xpath('//ul[@class="introduce-item"]/li[2]/span[2]/p/span/span/text()').extract()  #获取房子描述
        house_desc = "".join(house_desc)
        if not house_desc:
            house_desc = "无描述"
        item['price'] = price
        item['telephone'] = telephone
        item['house_highlight'] = house_highlight
        item['house_desc'] = house_desc
        # print(item)
        yield item

    def parse_item(self, response):
        house_list = response.xpath('//ul[@class="listUl"]/li')
        item = BeijinghousingpriceItem()
        for house in house_list:  #暂时只爬取5个数据
            try:   #做一个异常处理
                house_url = "https:"+house.xpath('.//a/@href').extract_first()
                # print(house_url)
                title = house.xpath('.//h2//text()').extract()[1].strip()
                item['title'] = title
                print(title)
                yield scrapy.Request(url=house_url,callback=self.parse_house,meta={"item":item})
            except IndexError as e:
                continue


