from scrapy import Spider, FormRequest

class LottoSpider2(Spider):
    
    name = 'lotto2'
    
    allowed_domains = ['dhlottery.co.kr']
    
    start_urls = ['http://dhlottery.co.kr/gameResult.do?method=byWin']

    def parse(self, response):

        rnd = self.rnd

        if response.status == 200:
            # FormRequest : Form 전송을 위한 Request 객체 ( method를 조정 가능 )
            yield FormRequest.from_response(response=response,
                                            method="POST",
                                            formdata= { 'drwNo' : str(rnd), 'dwrNoList' : str(rnd) },
                                            callback=self.parse_numbers)

    def parse_numbers(self, response):
        numbers = response.css('div.nums span::text').getall()
        rnd = response.css('div.win_result strong::text').get()
        rnd = rnd[:-1]
        
        # { 'rnd': 1, 'no1': 10, 'no2': 20, ... 'no6': 40, 'bno': 24 } 형식의 dict를 만드는 구현 
        result = { 'rnd': rnd }
        for idx, n in enumerate(numbers[:-1], 1):
            result['no{0}'.format(idx)] = n
        result['bno'] = numbers[-1]

        yield result
