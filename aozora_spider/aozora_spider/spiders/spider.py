import scrapy
from ..items import AozoraSpiderItem

class AozoraSpider(scrapy.Spider):
    name = "aozora_spider"
    start_urls = [
        'https://www.aozora.gr.jp/',
    ]

    def parse(self, response):
        for novelurl in response.css('a[href*="zip"]::attr(href)').extract():
            yield AozoraSpiderItem(file_urls=[response.urljoin(novelurl)])
            #     {
            #     'file_urls': novelfile.css('a::attr(href)').get(),
            #
            # }

        next_pages = response.css('a[href*="sakuhin"]::attr(href)').getall()
        if next_pages is not None:
            for next_page in next_pages:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
        novels = response.css('a[href*="card"]::attr(href)').getall()
        if novels is not None:
            for novel in novels:
                novel = response.urljoin(novel)
                yield scrapy.Request(novel, callback=self.parse)
