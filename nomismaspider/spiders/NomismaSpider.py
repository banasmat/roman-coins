from nomismaspider.items import RomanCoin
import scrapy


class NomismaSpider(scrapy.Spider):
    name = 'nomismaspider'
    url_base = 'http://numismatics.org/ocre/'
    start_urls = [url_base + 'results?lang=en']

    #TODO consider adding authorities whitelist
    # authorities = ['']


    def parse(self, response):
        # for row in response.css('.row.result-doc'):
        yield scrapy.Request(self.url_base + response.css("h4 a::attr(href)").extract_first(), self.parse_coin_type_page)

        next_url = response.css(".pagination a[title='Next']::attr(href)").extract_first()
        yield scrapy.Request(self.url_base + next_url, self.parse)

    def parse_coin_type_page(self, response):

        coin_type = response.css('#object_title::text').extract_first()
        authority = response.css('.metadata_section a[href*=authority]::text').extract_first()

        for example in response.css("#examples .g_doc"):

            name = example.css('.result_link a::text').extract_first()

            obverse_url = example.css(".gi_c a:first-child::attr(href)").extract_first()
            reverse_url = example.css(".gi_c a:nth-child(2)::attr(href)").extract_first()

            file_urls = [obverse_url]

            if reverse_url:
                file_urls.append(reverse_url)

            yield RomanCoin(name=name, authority=authority, type=coin_type, file_urls=file_urls)
