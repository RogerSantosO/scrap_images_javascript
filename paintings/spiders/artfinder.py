import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from paintings.items import PaintingsItem

class ArtfinderSpider(scrapy.Spider):
    name = 'artfinder'
    allowed_domains = ['artfinder.com']
    script = '''
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(2))
        return {
            html = splash:html(),
        }
    end'''
    
    def start_requests(self):
        yield SplashRequest(url='https://www.artfinder.com/art/sort-best_match/paginate-12/product_category-painting/',callback=self.parse, endpoint="execute",args={
            'lua_source': self.script,'timeout': 3600
        })

    def parse(self, response):
        for image in response.xpath('//div[@class="af-card af-card-product-variant af-show-element-on-hover"]'):
            loader = ItemLoader(item=PaintingsItem(), selector=image)
            relative_url = image.xpath('.//img[@class="small-12 af-toggle-main-image af-place place-top place-left af-colour-average"]/@src').extract_first()
            absolute_url = response.urljoin(relative_url)
            loader.add_value('image_urls',absolute_url)
            loader.add_xpath('paint_name', './/a[@class="af-place fit-in"]/@title')
            yield loader.load_item()