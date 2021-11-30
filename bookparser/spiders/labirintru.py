import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem
from scrapy.http import Request


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BA%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B/?paperbooks=1&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=&price_max=249&age_min=&age_max=&form-pubhouse=&lit=&stype=0#catalog-navigation',
                  'https://www.labirint.ru/search/%D0%BA%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B/?paperbooks=1&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=250&price_max=379&age_min=&age_max=&form-pubhouse=&lit=&stype=0#catalog-navigation',
                  'https://www.labirint.ru/search/%D0%BA%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B/?paperbooks=1&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=380&price_max=499&age_min=&age_max=&form-pubhouse=&lit=&stype=0#catalog-navigation',
                  'https://www.labirint.ru/search/%D0%BA%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B/?paperbooks=1&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=500&price_max=649&age_min=&age_max=&form-pubhouse=&lit=&stype=0#catalog-navigation',
                  'https://www.labirint.ru/search/%D0%BA%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B/?paperbooks=1&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=650&price_max=999&age_min=&age_max=&form-pubhouse=&lit=&stype=0#catalog-navigation',
                  'https://www.labirint.ru/search/%D0%BA%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B/?paperbooks=1&otherbooks=1&available=1&preorder=1&wait=1&no=1&price_min=1+000&price_max=&age_min=&age_max=&form-pubhouse=&lit=&stype=0#catalog-navigation']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow('https://www.labirint.ru/search/%D0%BA%D0%BE%D0%BC%D0%B8%D0%BA%D1%81%D1%8B/' + next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow('https://www.labirint.ru' + link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        url = response.url
        author = response.xpath("//div[@class='authors'][1]/a/text()").getall()
        title = response.xpath("//h1/text()").get()
        price = response.xpath("//div[@class='buying']//span[contains(@class, 'val-number')]/text()").getall()
        rate = response.xpath("//div[@id='rate']/text()").get()
        yield BookparserItem(url=url, author=author, title=title, price=price, rate=rate)
