import requests

from .scrapers import PropertyDetailsScraper


class Zoopla:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Pyzoopla"})

    def get_property_details(self, number):
        url = f"https://www.zoopla.co.uk/for-sale/details/{number}"
        html_content = self.session.get(url).content
        return PropertyDetailsScraper(html_content).scrape()
