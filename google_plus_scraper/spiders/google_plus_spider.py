import scrapy
from google_plus_scraper.items import GooglePlusScraperItem


class GooglePlusSpider(scrapy.Spider):
    name = "google_plus"
    allowed_domains = ["plus.google.com"]
    start_urls = [
        "https://plus.google.com/+%ED%97%88%ED%83%9C%EB%AA%8574/posts"
    ]

    def parse(self, response):
        '''
        filename = 'test.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        '''
        for article in response.xpath('//div[@role="article"]'):
            found = False
            item = None
            for a in article.xpath('.//a[@rel="nofollow"]'):
                title = a.xpath('@title').extract_first()
                if title != None and len(title) > 0:
                    found = True
                    link = a.xpath('@href').extract_first()
                    #print title, link
                    item = GooglePlusScraperItem()
                    item['title'] = title
                    item['link'] = link
            if found:
                date = article.xpath('.//a[@rel="noreferrer"]/text()').extract_first()
                #print date
                item['date'] = date
                print item
                yield item
