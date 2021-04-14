import scrapy
import pymongo


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['http://auto.youla.ru/']
    cars_data = []

    _css_selectors = {
        "brands": ".ColumnItemList_container__5gTrc a.blackLink",
        "pagination": "a.Paginator_button__u1e7D",
        "car": ".SerpSnippet_titleWrapper__38bZM a.SerpSnippet_name__3F7Yu",

    }

    def _get_follow(self, response, selector_css, callback, **kwargs):
        for link_selector in response.css(selector_css):
            yield response.follow(link_selector.attrib.get("href"), callback=callback)

    def parse(self, response):
        yield from self._get_follow(response, self._css_selectors["brands"], self.brand_parse)

    def brand_parse(self, response):
        yield from self._get_follow(response, self._css_selectors["pagination"], self.brand_parse)
        yield from self._get_follow(response, self._css_selectors["car"], self.car_parse)

    def car_parse(self, response):

        def get_photo_url(response_css):
            photo_list = []
            for url in response_css:
                photo_list.append(url.attrib.get("src"))
            return photo_list

        data = {
            "title": response.css(".AdvertCard_advertTitle__1S1Ak::text").extract_first(),
            "url": response.url,
            "description": response.css(".AdvertCard_descriptionInner__KnuRi::text").extract_first(),
            "characteristics": dict(zip(response.css(".AdvertSpecs_label__2JHnS::text").extract(), response.css(".AdvertSpecs_data__xK2Qx ::text").extract())),
            "photos_url" : get_photo_url(response.css(".PhotoGallery_photo__36e_r img"))
        }
        self.save(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def save(self, data):
        self.db_client["gb_parse"][self.name].insert_one(data)
