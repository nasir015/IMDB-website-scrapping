
import scrapy
import logging


class MoviSpider(scrapy.Spider):
    name = 'movi'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250/']
    movie_name1 = ''

    def parse(self, response):
        rows = response.xpath("//div[@class='lister']/table/tbody/tr/td[2]/a")
        for row in rows:
            name = row.xpath(".//text()").get()
            link = row.xpath(".//@href").get()
            absolute_link = f"https://www.imdb.com{link}"
            yield response.follow(url=link, callback=self.parse_response, meta={'movi_name': name, 'link': absolute_link})
#meta bebohar kora hoy request pathanor age jei value gula ache oigula access korar jonno sathe sathe print korar jonno 
    def parse_response(self, response):
        name = response.request.meta['movi_name']
        link = response.request.meta['link']
        cast_member_name = response.xpath(
            "//a[@data-testid='title-cast-item__actor']/text()").getall()
        yield{
            'movi_name': name,
            'link': link,
            'name': cast_member_name,
        }
