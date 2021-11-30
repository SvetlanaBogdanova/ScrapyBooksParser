import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BA%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B']

    next_page = 1

    def parse(self, response: HtmlResponse):
        if response.status == 200:
            self.next_page += 1
            yield response.follow('https://book24.ru/search/page-' + str(self.next_page) + '/?q=комиксы', callback=self.parse)
        links = response.xpath("//div[@class='product-card__content']/a//@href").getall()
        for link in links:
            yield response.follow('https://book24.ru' + link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        url = response.url
        author = response.xpath("//a[contains(@href, 'author') and @title]/text()").get()
        title = response.xpath("//h1/text()").get()
        base_price = response.xpath("//span[contains(@class, 'price-old')]/text()").get()
        current_price = response.xpath("//div[@itemprop='offers']/span[1]/text()").get()
        rate = response.xpath("//div[@itemprop='aggregateRating']//span[@class='rating-widget__main-text']/text()").get()
        yield BookparserItem(url=url, author=author, title=title, base_price=base_price, current_price=current_price, rate=rate)
