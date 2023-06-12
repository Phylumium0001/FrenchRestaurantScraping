import scrapy


class ResSpiderSpider(scrapy.Spider):
    name = "res_spider"
    allowed_domains = ["ma-cantine.agriculture.gouv.fr"]
    start_urls = ["https://ma-cantine.agriculture.gouv.fr/nos-cantines/?page=1"]

    def parse(self, response):
        links = response.css('')

        for link in links: 
            relativeUrl = link.css('a.cardlinkwrap.w-inline-block::attr(href)').get()
            comp_url = 'https://www.1800d2c.com' + relativeUrl

            yield response.follow(comp_url, callback=self.get_info)

        next_page = response.css('a.w-pagination-next.bpagination::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.1800d2c.com/all-brands' + next_page  

            yield response.follow(next_page_url, callback=self.parse)


    def get_info(self, response):
        workitem = Workitem()
        workitem['name'] = response.css('h1.heroh1::text').get()
        workitem['website'] = response.css('a.bxl.w-button').attrib['href']

        yield workitem
