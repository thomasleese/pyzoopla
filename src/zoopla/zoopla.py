import itertools

import requests

from .scrapers import RegionsScraper, PropertiesListScraper, PropertyDetailsScraper


class Zoopla:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Pyzoopla"})

    def request(self, url):
        return self.session.get(url).content

    def get_for_sale_regions(self):
        url = "https://www.zoopla.co.uk/for-sale/"
        return RegionsScraper(self.request(url)).scrape()

    def get_to_rent_regions(self):
        url = "https://www.zoopla.co.uk/to-rent/"
        return RegionsScraper(self.request(url)).scrape()

    def get_for_sale_properties(self, region, page=1):
        url = f"https://www.zoopla.co.uk/for-sale/property/{region}?pn={page}"
        return PropertiesListScraper(self.request(url)).scrape()

    def get_all_for_sale_properties(self, region):
        return self._paginate(lambda page: self.get_for_sale_properties(region, page))

    def get_to_rent_properties(self, region, page=1):
        url = f"https://www.zoopla.co.uk/to-rent/property/{region}?pn={page}"
        return PropertiesListScraper(self.request(url)).scrape()

    def get_all_to_rent_properties(self, region):
        return self._paginate(lambda page: self.get_to_rent_properties(region, page))

    def get_property_details(self, number):
        url = f"https://www.zoopla.co.uk/for-sale/details/{number}"
        return PropertyDetailsScraper(self.request(url)).scrape()

    def _paginate(self, func):
        items = []
        for i in itertools.count(1):
            if new_items := func(i):
                items.extend(new_items)
            else:
                return items
