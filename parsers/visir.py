from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag



class VisirParser(BaseParser):
    domains = ['www.visir.is']

    feeder_base = 'http://www.visir.is/section/FRONTPAGE'
    feeder_pat  = '^http://www.visir.is/.*/article/201'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        tmp = soup.find('div', 'paragraph')
        print tmp
        # tmp = tmp.replace('<br /><br />', '</p><p>')

        self.real_article = True
        self.date = ''
        self.body = ''
        self.byline = ''
        self.title = ''
