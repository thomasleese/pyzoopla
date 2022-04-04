from bs4 import BeautifulSoup

from .models import Region, PropertyDetails


class Scraper:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    @property
    def canonical_url(self):
        return self.soup.find("link", rel="canonical")["href"]

    def extract_number(self, text):
        return int("".join([n for n in text if n.isdigit()]))


class RegionsScraper(Scraper):
    def scrape_row(self, row):
        cells = row.find_all("td")

        return Region(
            name=cells[0].text,
            slug=cells[0].find("a")["href"].split("/")[-2],
            number_of_properties=self.extract_number(cells[1].text),
            average_price=self.extract_number(cells[2].text),
        )

    def scrape(self):
        rows = self.soup.find("table", attrs={"class": "browse-table"}).find_all("tr")
        return [self.scrape_row(row) for row in rows[1:]]


class PropertiesListScraper(Scraper):
    def scrape_result(self, result):
        href = result.find("a", attrs={"data-testid": "listing-details-link"})["href"]
        url = f"https://www.zoopla.co.uk{href}".split("?")[0][:-1]
        address = result.find("p", attrs={"data-testid": "listing-description"}).text
        price = self.extract_number(
            result.find("div", attrs={"data-testid": "listing-price"}).text
        )
        number_of_bedrooms = self.extract_number(
            result.find("div", attrs={"data-testid": "listing-spec"})
            .find_all("div")[0]
            .text
        )
        return PropertyDetails(
            url=url, address=address, price=price, number_of_bedrooms=number_of_bedrooms
        )

    def scrape(self):
        results = self.soup.find_all("div", attrs={"data-testid": "search-result"})
        return [self.scrape_result(result) for result in results]


class PropertyDetailsScraper(Scraper):
    @property
    def address(self):
        return self.soup.find("span", attrs={"data-testid": "address-label"}).text

    @property
    def price(self):
        return self.extract_number(
            self.soup.find("span", attrs={"data-testid": "price"}).text
        )

    @property
    def number_of_bedrooms(self):
        return self.extract_number(
            self.soup.find("span", attrs={"data-testid": "beds-label"}).text
        )

    def scrape(self):
        return PropertyDetails(
            url=self.canonical_url,
            address=self.address,
            price=self.price,
            number_of_bedrooms=self.number_of_bedrooms,
        )
