from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import os
import dotenv

from inst_parse.spiders.instagram import InstagramSpider

if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    crawler_settings = Settings()
    crawler_settings.setmodule("inst_parse.settings")
    crawler_proc = CrawlerProcess(settings=crawler_settings)
    tags = ["python"]
    crawler_proc.crawl(
        InstagramSpider, 
        login=os.getenv("USERNAME"),
        password=os.getenv("ENC_PASSWORD"),
        tags = tags,
    )
    crawler_proc.start()