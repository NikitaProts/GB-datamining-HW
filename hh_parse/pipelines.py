from itemadapter import ItemAdapter
import pymongo


class HhParsePipeline:
    def process_item(self, item, spider):
        return item


class HhParseMongoPipeline:
    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client["gb_parse_29_03_21"]

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(item)
        return item
