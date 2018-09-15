import scrapy
import json
import ast
import sys

counter = 0
urls = []
urlIndx = 0

def getUrls():
	f = open("part2urls.json","r")
	lines = f.readlines()
	i = 0
	for line in lines:
		if i < 1:
			# print(str(line))
			line = line[:len(line)-2]
			s = ast.literal_eval(line)
			urls.append(s['movie_url'])
		i += 1

	f.close()
	f = open("part2urls.json","w")
	j = 0
	for line in lines:
		if j >= 1:
			f.write(line)
		j += 1
	f.close()

getUrls()

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	
	# start_urls = [
		# 'http://www.imdb.com/title/tt0363163/reviews?ref_=tt_urv',
		# 'http://www.imdb.com/title/tt0068646/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2398042102&pf_rd_r=0C4W4RSAPNKXJ1MDEDXN&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_2'
	# ]
	global urls
	start_urls = urls
#     # ?cid=16775&CTARef=GlobalBanner1%7cMW&pge=1
	
	def parse(self, response):
		i = 0
		for quote in response.xpath('//div/a/img[@class="avatar"]'):
			ratings = quote.xpath('../../img[@width="102"]/@alt')
			# print(len(ratings))
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


		if temp is not None:
			final_next_page = response.urljoin(temp)
			# print("next page -2-2-2-2--2-2-2--2-2-2-2--2"+str(final_next_page))
			yield scrapy.Request(final_next_page, callback=self.parse)