from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag


class VisirParser(BaseParser):
    domains = ['www.visir.is']

    feeder_base = 'http://www.visir.is/section/FRONTPAGE'
    feeder_pat  = '^http://www.visir.is/.*/article/201'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')
        
        elt = soup.find('h1')
        if elt is None:
            self.real_article = False
            return
        self.title = elt.getText()

        tmp = str(soup.find('div', 'paragraph'))

        if tmp is None:
            self.real_article = False
            return
        tmp2 = tmp.replace('<br /><br />', '</p><p>')

        moresoup = BeautifulSoup(tmp2)
        allp = moresoup.findAll('p')


        bymeta = str(moresoup.find('div', 'meta'))
        by = bymeta.replace(' skrifar:', '')
        if by is None:
            self.byline = ''
        else:
            newby = BeautifulSoup(by)
            self.byline = newby.getText()
        
        self.date = soup.find('div', 'authors').find('span', 'date').getText()

        if self.date is None:
            self.real_article = False
            return

        self.body = '\n'+'\n\n'.join([x.getText() for x in allp
                                              if isinstance(x, Tag) and x.name == 'p'])
