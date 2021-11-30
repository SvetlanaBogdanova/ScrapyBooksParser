# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        item['title'] = self.process_title(item['title'])[-1]

        item['_id'] = self.process_id(item['url'], spider)

        if spider.name == 'book24ru':
            if item['base_price']:
                item['price'] = item['base_price']
                item['discount_price'] = item['current_price']
                item['discount_price'] = self.process_price(item['discount_price'])
            else:
                item['price'] = item['current_price']
            item['price'] = self.process_price(item['price'])
            del item['base_price'], item['current_price']
        else:
            if len(item['price']) > 1:
                item['discount_price'] = self.process_price(item['price'][1])
            if len(item['price']) > 0:
                item['price'] = self.process_price(item['price'][0])

        item['rate'] = self.process_title(item['rate'])[0]

        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pass

        return item

    def process_title(self, title):
        return title.strip().split(': ')

    def process_price(self, price):
        if price:
            return price.replace('\xa0', '').strip().split(' ')[0]

    def process_id(self, link, spider):
        if spider.name == 'labirintru':
            return link.split('/')[-2]
        else:
            return link.split('/')[-2].split('-')[-1]

    def process_rate(self, rate):
        return rate.strip()
