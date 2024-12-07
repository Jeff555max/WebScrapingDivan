import scrapy

class DivanSpider(scrapy.Spider):
    name = "divan"
    allowed_domains = ["divan.ru"]
    start_urls = [
        "https://www.divan.ru/chelyabinsk/search?ProductSearch%5Bname%5D=источник+освещения&no_cache=1"
    ]

    def parse(self, response):
        # Извлечение карточек товаров
        products = response.xpath('//div[contains(@class, "_Ud0k")]')

        for product in products:
            yield {
                'name': product.xpath('.//a[contains(@class, "ProductName")]/span/text()').get(),
                'price': product.xpath('.//span[@class="ui-LD-ZU KIkOH" and @data-testid="price"]/text()').get(),
                'link': response.urljoin(product.xpath('.//a[contains(@class, "ProductName")]/@href').get()),
            }

        # Переход на следующую страницу (пагинация)
        next_page = response.xpath('//a[contains(@class, "pagination-next")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
