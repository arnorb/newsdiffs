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


        bymeta = str(soup.find('div', 'meta'))
        by = bymeta.replace(' skrifar:', '')
        newby = BeautifulSoup(by)

        self.byline = newby.getText()
        
        
        
        
        # print moresoup

        self.date = soup.find('div', 'article').find('span', 'date').getText()
        self.body = '\n'+'\n\n'.join([x.getText() for x in allp])
