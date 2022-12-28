#!/usr/bin/env python
"""
Parse and Plot Data from New England Oil
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
        self.generate_urls()

    def generate_urls(self):
        for state in self.zones:
            for zone in self.zones[state]:
                self.url_dict["{}{}/zone{}.asp?x=0".format(self.URL, state, zone)] = {'state': state, 'zone': zone}


    def generate_oil_data(self):
        """Scrape data for each defined zone, and be able to pass that object on"""
        for url in self.url_dict:
            sauce = requests.get(url)
            soup = bs(sauce.content, 'html.parser')
            oil_table = soup.find("div", {"id": "oil-table"}).find('table')
            self.url_dict[url]['oil_table'] = oil_table

        return self.url_dict


if __name__ == '__main__':
    ops = OilPriceScraper()
    data = ops.generate_oil_data()
    