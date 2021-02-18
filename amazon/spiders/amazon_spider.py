import scrapy


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    i = 0
    start_urls = [
        'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&qid=1613468806&rnid=1250225011&ref=lp_1000_nr_p_n_publication_date_0'
    ]

    def parse(self, response):
        id = 0
        items = response.xpath(
            '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a/span/text()').extract()
        prices = response.xpath(
            '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div/div/span/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/a/span[1]/span[2]/span[2]/text()').extract()
        image_urls = response.xpath(
            '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div/div/span/div/div/div[2]/div[1]/div/div/span/a/div/img/@src').extract()
        item_ratings = response.xpath(
            '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[2]/div/span[1]/span/a/i[1]/span/text()').extract()
        reviews_urls = response.xpath(
            '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[2]/div/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[2]/div/span[2]/a/@href').extract()

        for item in items:
            if AmazonSpiderSpider.i < 50:
                complete_reviews_url = 'https://www.amazon.com' + \
                    reviews_urls[id]
                yield{
                    'id': AmazonSpiderSpider.i + 1,
                    'item_name': item,
                    'price': prices[id]+'$',
                    'image_url': image_urls[id],
                    'item_rating': item_ratings[id]
                }
                yield scrapy.Request(complete_reviews_url, callback=self.reviews_func)
            id += 1
            AmazonSpiderSpider.i = AmazonSpiderSpider.i+1

        next_page = response.css('.a-last a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def reviews_func(self, response):
        see_all_reviews_url = response.xpath(
            '//*[@id="reviews-medley-footer"]/div[2]/a/@href').get()
        complete_see_all_reviews_url = 'https://www.amazon.com' + see_all_reviews_url
        yield scrapy.Request(complete_see_all_reviews_url, callback=self.all_reviews_func)

    def all_reviews_func(self, response):
        id = 0
        item_name = response.xpath(
            '//*[@id="cm_cr-product_info"]/div/div[2]/div/div/div[2]/div[1]/h1/a/text()').get()
        reviewers = response.xpath(
            '//*[(@id = "cm_cr-review_list")]//*[contains(concat( " ", @class, " " ), concat( " ", "a-profile-name", " " ))]/text()').extract()
        descriptions = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "a-text-bold", " " ))]//span/text()').extract()
        ratings = response.xpath(
            '//*[(@id = "cm_cr-review_list")]//*[contains(concat( " ", @class, " " ), concat( " ", "review-rating", " " ))]/span/text()').getall()

        for reviewer in reviewers:
            yield{
                'item_name': item_name,
                'reviewer': reviewer,
                'description...': descriptions[id],
                'rating......': ratings[id]
            }
            id += 1

        next_page = response.xpath(
            '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.all_reviews_func)
