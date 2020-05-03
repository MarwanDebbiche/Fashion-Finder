import scrapy
import os


class AsosSpider(scrapy.Spider):
    name = "asos"

    def start_requests(self):
        base_url = "https://www.asos.com/fr/homme/chaussures-bottes-baskets/cat/?cid=4209&cr=4&page={0}"
        for page in range(1, 27):
            url = base_url.format(page)
            request = scrapy.Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        articles = response.xpath(
            '//div[@data-auto-id="productList"]//article')
        for article in articles:
            product_url = article.xpath('a/@href').extract_first()
            product_desc = article.xpath(
                'a//div[@data-auto-id="productTileDescription"]//p/text()').extract_first()
            data = {}
            data['url'] = product_url
            data['description'] = product_desc
            yield data

    def on_error(self, error):
        print(error)
