from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup

class NYTParser(BaseParser):
    SUFFIX = '?pagewanted=all'
    domains = ['www.nytimes.com']

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
        self.meta = soup.findAll('meta')
        seo_title = soup.find('meta', attrs={'name':'hdl'}).get('content')
        tmp = soup.find('meta', attrs={'name':'hdl_p'})
        if tmp and tmp.get('content'):
            self.title = tmp.get('content')
        else:
            self.title = seo_title
        self.date = soup.find('meta', attrs={'name':'dat'}).get('content')
        self.byline = soup.find('meta', attrs={'name':'byl'}).get('content')
        p_tags = soup.findAll('p', attrs={'itemprop':'articleBody'})
        main_body = '\n'.join([p.getText() for p in p_tags])
        authorids = soup.find('div', attrs={'class':'authorIdentification'})
        authorid = authorids.getText() if authorids else ''

        top_correction = '\n'.join(x.getText() for x in
                                   soup.findAll('nyt_correction_top')) or '\n'
        bottom_correction = '\n'.join(x.getText() for x in
                                   soup.findAll('nyt_correction_bottom')) or '\n'
        self.body = '\n'.join([top_correction,
                               main_body,
                               authorid,
                               bottom_correction,])