# -*- coding: utf-8 -*-
import scrapy
from doubanScrapy.items import DoubanscrapyItem

class DoubanSpiderSpider(scrapy.Spider):
	#爬虫的名字
    name = 'douban_spider'
    #允许的域名
    allowed_domains = ['movie.douban.com']
    #入口url，扔到调度器中去
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
        	douban_item = DoubanscrapyItem()
        	douban_item['serial_number'] = i_item\
        	.xpath(".//div[@class='pic']/em/text()").extract_first()
        	douban_item['movie_name'] = i_item\
        	.xpath(".//div[@class='hd']//a//span[1]//text()").extract_first()
        	content = i_item.xpath(".//div[@class='bd']//p[1]//text()").extract()
        	for i_content in content:
        		#split（）默认以空字符进行分割，返回分割结果组成的列表
        		# str.join(sequence) 返回通过指定字符连接序列中元素后生成的新字符串
        		content_s = "".join(i_content.split()) 
        		douban_item["introduce"] = content_s
        	douban_item['star'] = i_item\
        	.xpath(".//div[@class='bd']//div[@class='star']//span[2]//text()").extract_first()
        	douban_item['evaluate'] = i_item\
        	.xpath(".//div[@class='bd']//div[@class='star']//span[3]//text()").extract_first()
        	douban_item['describe'] = i_item\
        	.xpath(".//div[@class='bd']//p[@class='quote']//span//text()").extract_first()
        	yield douban_item
        next_link = response.xpath("//span[@class='next']//a//@href").extract()
        if next_link:
        	next_link=next_link[0]
        	yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback = self.parse)

