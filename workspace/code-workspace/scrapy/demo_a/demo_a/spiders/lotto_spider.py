import scrapy

class LottoSpider(scrapy.Spider):
    
    name = 'lotto'
    
    allowed_domains = ['dhlottery.co.kr']
    
    start_urls = ['http://dhlottery.co.kr/gameResult.do?method=byWin']

    def parse(self, response):

        numbers = response.css('div.nums span::text').getall()
        rnd = response.css('div.win_result strong::text').get()
        rnd = rnd[:-1]
        
        # { 'rnd': 1, 'no1': 10, 'no2': 20, ... 'no6': 40, 'bno': 24 } 형식의 dict를 만드는 구현 
        result = { 'rnd': rnd }
        for idx, n in enumerate(numbers[:-1], 1):
            result['no{0}'.format(idx)] = n
        result['bno'] = numbers[-1]

        yield result
