import scrapy
import os


class ZalandoSpider(scrapy.Spider):
    name = "zalando"

    def start_requests(self):
        urls = [
            'https://www.zalando.fr/mode-homme/'
            # 'http://www.zalando.fr/volcom-deadly-stones-pantalon-de-survetement-v1922e019-q11.html'
            # 'https://github.com/scrapy/scrapy'
        ]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, errback=self.on_error)

    def parse(self, response):
        if not os.path.exists("./scraping/data/zalando/"):
            os.makedirs("./scraping/data/zalando/")

        filename = './scraping/data/zalando/zalando.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file {}'.format(filename))

    def on_error(self, error):
        print(error)
