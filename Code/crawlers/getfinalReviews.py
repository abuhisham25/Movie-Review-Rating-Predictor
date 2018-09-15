import scrapy
import json
import ast
counter = 0
urls = []
# get the movies url from the json file which we saved later ,
# and pass over all of them in order to fetch all the reviews 
def getUrls():
    f = open("part2urls.json","r")
    for line in f:
        line = line[:len(line)-2]
        s = ast.literal_eval(line)
        urls.append(s['movie_url'])
    
    
getUrls()
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    global urls
    start_urls = urls
    def parse(self, response):
        i = 0
        for quote in response.xpath('//div/a/img[@class="avatar"]'):
            ratings = quote.xpath('../../img[@width="102"]/@alt')
            exist = len(ratings)
            text = quote.xpath('../../../p').extract()
            final = ""
            if exist != 0:
                final = text[i]
            
                yield {
            	   'text': final,
                    'rating':ratings.extract_first()
                }
            i += 1
        next_page = response.xpath('//img[@alt="[Next]"]')
        temp = next_page.xpath("../@href").extract_first()


        if temp is not None :
            final_next_page = response.urljoin(temp)
            yield scrapy.Request(final_next_page, callback=self.parse)


