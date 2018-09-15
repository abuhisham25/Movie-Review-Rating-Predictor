# This script is responsible for fetching the urls of movies , from 
# a list of 200 movie 
import scrapy
counter = 0

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://www.imdb.com/chart/top',
    ]
    
    def parse(self, response):
        for quote in response.xpath('//tr'):
            path = quote.xpath('.//td[@class="titleColumn"]/a/@href').extract_first()
            final = response.urljoin(path)
            yield {
            	'movie_url': final,
                'movie_name': quote.xpath('.//td[@class="titleColumn"]/a/text()').extract_first(),
            }