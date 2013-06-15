from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag


class RUVParser(BaseParser):
    domains = ['www.ruv.is']

    feeder_base = 'http://www.ruv.is/'
    feeder_pat = '^(http://www.ruv.is/frett/|http://www.ruv.is/pistlar/.*/)'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')
        self.meta = soup.findAll('meta')
        elt = soup.find('h1', "frettatitill")
        if elt is None:
            self.real_article = False
            return
        self.title = elt.getText()
        self.byline = ''

        self.date = soup.find('div', 'news-DateLine-1').getText()[12:22]

        # Weird hack, I have no idea why children of the frett-vinstri wont parse on the first run
        # for frettir but this seems to work...
        div = BeautifulSoup(soup.find('div', 'frett-vinstri').getText())

        if div is None:
            self.real_article = False
            return

        # "frettir" parse differently than "pistlar"
        # frettir
        if len(div.contents) != 1:
            self.body = '\n'+'\n\n'.join([x.getText() for x in div.findAll("p")
                                          if isinstance(x, Tag) and x.name == 'p' and not x.has_key("class")])  # skip the hidden p with class=nedanmal
        #pistlar
        else:
            news = soup.find("div", "frett-vinstri")
            self.body = '\n'+'\n\n'.join([x.getText() for x in news.findAll("p")
                                          if isinstance(x, Tag) and x.name == 'p' and not x.has_key("class")])  # skip the hidden p with class=nedanmal
