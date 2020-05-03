import os
import scrapy


class AsosSpider(scrapy.Spider):
    name = "asos"

    categories = [
        3602,  # men shirts
        4209,  # men shoes
        5668,  # men sweaters
        4208,  # men jeans
        3606  # men vest &coat
    ]

    start_urls = [
        f'https://www.asos.com/fr/cat/?cid={cat}&page=1'
        for cat in categories
    ]

    def parse(self, response):
        article_page_links = response.xpath(
            '//div[@data-auto-id="productList"]//article/a')
        yield from response.follow_all(article_page_links, self.parse_article)

        next_page = response.xpath(
            '//a[@data-auto-id="loadMoreProducts"]/@href').extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):

        images_url = [
            image_url.split("?")[0]
            for image_url
            in response.xpath('//*[@class="gallery-aside-wrapper"]//li//@src').getall()
        ]

        infos = [
            info.strip() for info in
            (
                response.xpath('//*[@class="about-me"]//text()').getall() +
                response.xpath(
                    '//div[@class="product-description"]//text()').getall()
            )
            if len(info.strip()) > 1
        ]

        yield {
            'product_url': response.request.url,
            'name': response.xpath('//*[@class="layout-aside"]//h1/text()').get(),
            'brand_url': response.xpath('//*[@class="brand-description"]/p//@href').get(),
            'images': images_url,
            'infos': infos
        }

    def on_error(self, error):
        print(error)
