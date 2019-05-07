from scrapy import Spider, Request
from budgetbytes.items import BudgetbytesItem
import re

class BudgetBytesSpider(Spider):
    name = 'budgetbytes_spider'
    allowed_urls = ['https://www.budgetbytes.com/']
    start_urls = ['https://www.budgetbytes.com/category/recipes/']

    def parse(self, response):
        subcat_urls = response.xpath('//ul[@class="subcategories"]//li/a/@href').extract()
        subcat_names = response.xpath('//ul[@class="subcategories"]//li/a/text()').extract()
        zipped_urls = zip(subcat_urls, subcat_names)
        
        for url, subcat in zipped_urls:
            yield Request(url=url, callback=self.get_subcat_pages, meta = {'subcat_name':subcat, 'subcat_url':url})

    def get_subcat_pages(self, response):

        subcat = response.meta['subcat_name']
        url = response.meta['subcat_url']

        try:
            pages = response.xpath('//div[@class="nav-links"]/a/text()').extract()
            total_pages = []
            for x in pages:
                try:
                    total_pages.append(int(x))
                except:
                    continue
            total_pages = max(total_pages)
        except:
            total_pages = 1

        subcat_pages = [url + 'page/{}'.format(x) for x in range(1,total_pages+1)]
        # print('='*50)
        # print(cat)
        # print(len(urls))

        for page in subcat_pages:
            yield Request(url=page, callback=self.get_recipe_urls, meta = {'subcat_name':subcat})

    def get_recipe_urls(self, response):
        subcat = response.meta['subcat_name']

        recipe_urls = response.xpath('//div[@class="archives"]//a/@href').extract()

        for url in recipe_urls:
            yield Request(url=url, callback=self.get_recipe_details, meta = {'subcat_name':subcat})

    def get_recipe_details(self, response):
        category = response.meta['subcat_name']

        recipe_name = response.xpath('//div[@class="wprm-recipe wprm-recipe-template-custom"]/h2/text()').extract_first()

        all_price = response.xpath('//span[@class="wprm-recipe-recipe_cost wprm-block-text-normal"]/text()').extract_first()
        try:
            all_price_split = str.split(all_price, sep = '/')

            recipe_price = all_price_split[0]
            recipe_price = float(re.findall('[0-9.]+', recipe_price)[0])
            # recipe_price = recipe_price.strip()
            # recipe_price = recipe_price.replace('$', '')
            # recipe_price = recipe_price.replace(' recipe', '')
            # recipe_price = float(recipe_price)

            serving_price = all_price_split[1]
            serving_price = float(re.findall('[0-9.]+', serving_price)[0])
            # serving_price = serving_price.strip()
            # serving_price = serving_price.replace('$', '')
            # serving_price = serving_price.replace(' serving', '')
            # serving_price = float(serving_price)
        except:
            recipe_price = all_price
            serving_price = all_price

        try:
            time_hrs = response.xpath('//span[@class="wprm-recipe-details wprm-recipe-details-hours wprm-recipe-total_time wprm-recipe-total_time-hours"]/text()').extract_first()
            time_hrs = int(time_hrs)
        except:
            time_hrs = 0

        try:
            time_mins = response.xpath('//span[@class="wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes"]/text()').extract_first() 
            time_mins = int(time_mins)
        except:
            time_mins = 0

        try:
            rating = response.xpath('//span[@class="wprm-recipe-rating-average"]/text()').extract_first()
            rating = float(rating)
        except:
            rating = None

        try:
            votes = response.xpath('//span[@class="wprm-recipe-rating-count"]/text()').extract_first()
            votes = int(votes)
        except:
            votes = 0


        item = BudgetbytesItem()
        item['category'] = category
        item['recipe_name'] = recipe_name
        item['recipe_price'] = recipe_price
        item['serving_price'] = serving_price
        item['time_hrs'] = time_hrs
        item['time_mins'] = time_mins
        item['rating'] = rating
        item['votes'] = votes
        yield item