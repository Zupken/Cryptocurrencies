import lxml.html
import scraper as sc
import requests


class Scraping:

    def __init__(self):
        self.begin_url = 'https://coinmarketcap.com/'
        self.end_url = 'historical-data/?start=20000428&end=20180107'
        self.data = []

    def get_links(self):
        self.source = requests.get(self.begin_url)
        self.tree = lxml.html.fromstring(self.source.content)
        self.links = sc.get_many_hrefs(self.tree.xpath('//a[@class="currency-name-container"]'))

    def enter_into_link(self):
        for index, link in enumerate(self.links):
            self.data = []
            link = self.begin_url + link + self.end_url
            print(index)
            self.source = requests.get(link)
            self.tree = lxml.html.fromstring(self.source.content)
            self.get_data()

    def get_data(self):
        self.etree = self.tree.xpath('//table[@class="table"]//tr[following-sibling::tr]')
        self.name = sc.get_text(self.tree.xpath('//div[@class="row bottom-margin-1x"][1]/div[1]/h1/text()[4]'))
        for element in self.etree:
            self.date = sc.get_text(element.xpath('./td[1]/text()'))
            self.open = sc.get_text(element.xpath('./td[2]/text()'))
            self.high = sc.get_text(element.xpath('./td[3]/text()'))
            self.low = sc.get_text(element.xpath('./td[4]/text()'))
            self.close = sc.get_text(element.xpath('./td[5]/text()'))
            self.volume = sc.get_text(element.xpath('./td[6]/text()'))
            self.market_cap = sc.get_text(element.xpath('./td[7]/text()'))
            self.list = [self.date, self.open, self.high, self.low, self.close, self.volume, self.market_cap]
            self.data.append(self.list)
        sc.Database(('date', 'open', 'high', 'low', 'close', 'volume', 'market_cap'), file_name=self.name+'.db').push_data(self.data)


Scraping = Scraping()
Scraping.get_links()
Scraping.enter_into_link()
