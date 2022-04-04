import requests

from .scrapers import RegionsScraper, PropertyDetailsScraper


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

    def get_property_details(self, number):
        url = f"https://www.zoopla.co.uk/for-sale/details/{number}"
        return PropertyDetailsScraper(self.request(url)).scrape()
