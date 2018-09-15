# This script is responsible for fetching the url of the movies review,
# so given the movie name which we collect later ,this script can get the url of the given movie
import scrapy
import json
import ast
counter = 0
urls = []
def getUrls():
    f = open("moviesUrl.json","r")
    for line in f:
        print(str(line))
        line = line[:len(line)-2]
        s = ast.literal_eval(line)
        urls.append(s['movie_url'])
    
    
getUrls()
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    global urls
    start_urls = urls
    
    def parse(self, response):
        for quote in response.xpath('//div[@id="titleUserReviewsTeaser"]'):
            test = quote.xpath('.//div[@class="see-more"]/a/@href')
            tempurl = test[1].extract()
            final = response.urljoin(tempurl)
            yield {
            	'movie_url': final
            }

#         # next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
#         # print("response response response lslslslslsllslslslslslslsl "+str(response.headers))
#         # print("#################################"+str(response.headers['Set-Cookie']))
#         # cook = response.headers['Set-Cookie']

#        	# global counter
#         # if next_page is not None and counter < 50:
#             # next_page = response.urljoin(next_page)
#             # yield scrapy.Request(next_page, callback=self.parse)
#             # counter += 1