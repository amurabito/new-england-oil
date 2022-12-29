#!/usr/bin/env python
"""
Scrape oil price data from newenglandoil.com
"""

from bs4 import BeautifulSoup as bs
import requests

class OilPriceScraper(object):
    """
    Populate a master object dictionary with oil price data for specific zones. 
    """

    def __init__(self):

        self.zones = {}
        self.URL = ''
        self.url_dict = {}
        self.zones['newhampshire'] = [2,6]
        self.zones['massachusetts'] = [8,9]
        self.URL = 'https://www.newenglandoil.com/'
        self._generate_urls()

    def _generate_urls(self):
        ''' populate a dictionary with the urls of interest '''
        for state in self.zones:
            for zone in self.zones[state]:
                self.url_dict["{}{}/zone{}.asp?x=0".format(self.URL, state, zone)] = {'state': state, 'zone': zone}


    def _generate_oil_html(self):
        """Scrape data for each defined zone, and be able to pass that object on"""
        for url in self.url_dict:
            sauce = requests.get(url)
            soup = bs(sauce.content, 'html.parser')
            oil_table = soup.find("div", {"id": "oil-table"}).find('table')
            self.url_dict[url]['oil_table'] = oil_table

        return self.url_dict


    def _generate_oil_dict(self, html_data):
        ''' Take the html data generated from bs4 and parse it into a dictionary '''
        return {}


def get_oil_data(self):
    ops = OilPriceScraper()
    html_data = ops._generate_oil_html()
    return ops._generate_oil_data(html_data)


if __name__ == '__main__':

