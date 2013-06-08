from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag


class MBLParser(BaseParser):
    domains = ['www.mbl.is']

    feeder_base = 'http://www.mbl.is/frettir/'
    feeder_pat = '^http://www.mbl.is/frettir/.*/\d{4}/\d{2}/\d{2}/.*'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        self.meta = soup.findAll('meta')
        elt = soup.find('h1')
        if elt is None:
            self.real_article = False
            return
        self.title = elt.getText()
        byline = soup.find('div', 'reporter-profile')
        if byline is None:
            self.byline = ''
        else:
            self.byline = byline.find('a', 'name').getText()

        self.date = soup.find('div', 'dateline').getText().split("|")[2]

        div = soup.find('div', 'frett-main')
        if div is None:
            self.real_article = False
            return
        self.body = '\n'+'\n\n'.join([x.getText() for x in div.childGenerator()
                                      if isinstance(x, Tag) and x.name == 'p'])
