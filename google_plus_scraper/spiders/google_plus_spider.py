import scrapy

class GooglePlusSpider(scrapy.Spider):
    name = "google_plus"
    allowed_domains = ["plus.google.com"]
    start_urls = [
        "https://plus.google.com/+%ED%97%88%ED%83%9C%EB%AA%8574/posts"
    ]

    def parse(self, response):
        for sel in response.xpath('//a[@rel="nofollow"]'):
            title = str(sel.xpath('@title').extract())
            link = sel.xpath('@href').extract()

            if(not title.isspace() and title != None and title != '' and len(title) > 0):
                print title, link