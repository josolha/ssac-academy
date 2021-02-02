from scrapy import Spider, FormRequest

class LottoSpider4(Spider):
    
    name = 'lotto4'
    
    allowed_domains = ['dhlottery.co.kr']
    
    def start_requests(self):

        # self.start # 시작회차
        # self.end # 끝회차
        self.rnd = int(self.start) # 현재 작업 회차
        self.results = [] # 중간에 발생하는 크롤링 결과를 저장하는 변수

        # FormRequest : Form 전송을 위한 Request 객체 ( method를 조정 가능 )
        yield FormRequest(url="https://dhlottery.co.kr/gameResult.do?method=byWin",
                          method="POST",
                          formdata= { 'drwNo' : str(self.rnd), 'dwrNoList' : str(self.rnd) },
                          callback=self.parse)

    def parse(self, response):
        numbers = response.css('div.nums span::text').getall()
        rnd = response.css('div.win_result strong::text').get()
        rnd = rnd[:-1]
        
        # { 'rnd': 1, 'no1': 10, 'no2': 20, ... 'no6': 40, 'bno': 24 } 형식의 dict를 만드는 구현 
        result = { 'rnd': rnd }
        for idx, n in enumerate(numbers[:-1], 1):
            result['no{0}'.format(idx)] = n
        result['bno'] = numbers[-1]

        # yield result # 크롤링된 데이터 반환
        self.results.append(result) # 크롤링된 데이터 저장

        if self.rnd < int(self.end):
            self.rnd += 1

            # FormRequest : Form 전송을 위한 Request 객체 ( method를 조정 가능 )
            yield FormRequest(url="https://dhlottery.co.kr/gameResult.do?method=byWin",
                            method="POST",
                            formdata= { 'drwNo' : str(self.rnd), 'dwrNoList' : str(self.rnd) },
                            callback=self.parse)
        else :
            for r in self.results:
                yield r