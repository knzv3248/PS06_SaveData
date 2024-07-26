import scrapy
from scrapy.crawler import CrawlerProcess
import re

class DivanLightSpider(scrapy.Spider):
    name = "divan_light"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/chelyabinsk/category/svet"]

    def parse(self, response):
        lightings = response.css('div.WdR1o')
        for lighting in lightings:
            price_text = lighting.css('div.pY3d2 span::text').get()
            price_number = self.extract_price(price_text)
            yield {
                'Название': lighting.css('div.lsooF span::text').get(),
                'Цена': price_number,  # Преобразуем цену в число
                'Ссылка': response.urljoin(lighting.css('a').attrib['href']),  # Полный URL
            }

    def extract_price(self, price_text):
        # Удаляем все символы, кроме цифр и десятичной точки
        price_text_cleaned = re.sub(r'[^\d.]', '', price_text.replace(' ', ''))
        try:
            return int(price_text_cleaned)  # Почему-то при float получается текстовое поле
        except ValueError:
            return None  # Возвращаем None, если преобразование не удалось

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "divan_lights-w1251-int.csv": {
                "format": "csv",
                "encoding": "windows-1251"  # Указываем кодировку файла
            # "divan_lights-utf8-int.csv": {
            #     "format": "csv",
            #     "encoding": "utf-8"  # Указываем кодировку файла
            },
        },
        "FEED_EXPORT_FIELDS": ["Название", "Цена", "Ссылка"],  # Указываем порядок и поля для экспорта
    })

    process.crawl(DivanLightSpider)
    process.start()  # Блокируется до тех пор, пока все Spiders не завершат работу
