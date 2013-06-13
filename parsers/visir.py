# -*- coding: utf-8 -*-
from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag


class VisirParser(BaseParser):
    domains = ['www.visir.is']

    feeder_base = 'http://www.visir.is/section/FRONTPAGE'
    feeder_pat  = '^http://www.visir.is/.*/article/201'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='8859')
        
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

        
        byline = soup.find('div', 'meta')

        if byline is None:
            self.byline = ''
        else:
            by = byline.getText()
            self.byline = by.replace(' skrifar:', '')
        # else:
            # by = str(byline)
            # newby = BeautifulSoup(by.encode('utf-8'))
            # self.byline = newby.getText()
        
        self.date = soup.find('div', 'authors').find('span', 'date').getText()

        if self.date is None:
            self.real_article = False
            return

        self.body = '\n'+'\n\n'.join([x.getText() for x in allp
                                              if isinstance(x, Tag) and x.name == 'p'])
