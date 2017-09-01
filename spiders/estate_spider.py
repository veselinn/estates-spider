import scrapy
from imoti_scrapper.items import EstateItem

class EstateSpider(scrapy.Spider):
    name = "estate"

    def start_requests(self):
        urls = [
            'https://www.imot.bg/pcgi/imot.cgi?act=3&slink=30zkmc&f1=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = []
        
        for estate in response.css('table[width="660"]'):
            if estate.css('div.price::text').extract_first():
                item = EstateItem()
                item['url'] = estate.css('a.photoLink::attr(href)').extract_first()
                item['price'] = estate.css('div.price::text').extract_first()
                item['estateType'] = estate.css('a.lnk1::text').extract_first()
                item['description'] = estate.css('tr:nth-child(3) td::text').extract_first()
                item['location'] = estate.css('a.lnk2::text').extract_first()
                yield item

        current_page_number = int(response.request.url[-1])
        next_page_url = (response.request.url[:-1] + str(current_page_number + 1))[6:]
        next_page = response.css('a[href="' + next_page_url + '"]::attr(href)').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
