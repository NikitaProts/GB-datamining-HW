from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader
from urllib.parse import urljoin


def flat_text(items):
    return "\n".join(items)


def hh_user_url(user_id):
    return urljoin("https://hh.ru/", user_id)


class HHLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = flat_text
    author_in = MapCompose(hh_user_url)
    author_out = TakeFirst()