import scrapy
import os


class AsosSpider(scrapy.Spider):
    name = "asos"

    def start_requests(self):
        urls = [
            'https://www.asos.com/fr/homme/chaussures-bottes-baskets/cat/?cid=4209&cr=4&page=1'
            # 'https://www.asos.com/fr/nike/nike-blazer-mid-77-baskets-mi-hautes-blanc-noir/prd/14735083?clr=blanc-noir&colourWayId=16639937&SearchQuery=&cid=4209'
            # 'https://github.com/scrapy/scrapy'
        ]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, errback=self.on_error)

    def parse(self, response):
        if not os.path.exists("./scraping/data/asos/"):
            os.makedirs("./scraping/data/asos/")

        filename = './scraping/data/asos/asos.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

        self.log('Saved file {}'.format(filename))

    def on_error(self, error):
        print(error)
