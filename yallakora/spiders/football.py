import scrapy

class FootballSpider(scrapy.Spider):
    name = "football"
    allowed_domains = ["www.yallakora.com"]
    date = str(input("write the date "))
    start_urls = [f"https://www.yallakora.com/match-center?date={date}#"]
                  
    def parse(self, response):
        
        match_url = response.xpath("//div[@class='leftCol']/a/@href")
        for match in match_url:

            final_url = match.get()
            print(final_url)
                           
            yield response.follow(final_url, callback=self.parse_match_page) 


    def parse_match_page(self, response):
        match_details = response.xpath("//section[@class='mtchDtlsRslt']")
        
        score1 = match_details.xpath(".//div[@class='result']/span[1]/text()").get()
        score2 = match_details.xpath(".//div[@class='result']/span[2]/text()").get()

        score_all = score1 +"-"+score2

        yield {
            'NameOfChampion': match_details.xpath(".//div[@class='tourNameBtn']/a[1]/text()").get(),
            'TeamA': match_details.xpath(".//div[@class='team teamA']//p/text()").get(),
            'TeamB': match_details.xpath(".//div[@class='team teamB']//p/text()").get(),
            'Time': match_details.xpath(".//div[@class='tourNameBtn matchDateInfo']//span[2]/text()").get(),
            'score': score_all,
            }
        