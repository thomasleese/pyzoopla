from bs4 import BeautifulSoup

from .models import PropertyDetails


class Scraper:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    @property
    def canonical_url(self):
        return self.soup.find("link", rel="canonical")["href"]


class PropertyDetailsScraper(Scraper):
    def scrape(self):
        return PropertyDetails(url=self.canonical_url)
