import scrapy
from urllib.parse import urljoin 
from avito_parse.items import AvitoParseItem


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ["https://www.avito.ru/krasnodar/kvartiry/prodam"]

    def parse(self, response):
        links_in_page = [link.attrib.get("href") for link in response.css("div.index-inner-LCNXs a.link-link-39EVK")]
        for link in links_in_page:
            yield response.follow(link, callback=self.parse_flat)
    
    def parse_flat(self, response):

        data = {}
        data["url"] = response.url
        data["title"] = response.css("h1.title-info-title span.title-info-title-text::text").get()
        data["price"] = response.css("span.js-item-price::text").get()
        data["address"] = response.css("span.item-address__string::text").get().replace("\n","")
        data["params"] = dict(zip(response.css("li.item-params-list-item span::text").extract(), [param for param in response.css("li.item-params-list-item::text").extract() if param != ' ']))
        data["author_url"] = urljoin("https://www.avito.ru/", response.css("div.seller-info-name a").attrib.get("href"))
        yield AvitoParseItem(
            url = data["url"],
            title = data["title"],
            price = data["price"],
            address = data["address"],
            params = data["params"],
            author_url = data["author_url"]
        )
