from typing import List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .models import Region, Price, Property, ToRentPrice


class Scraper:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    @property
    def canonical_url(self) -> str:
        return self.soup.find("link", rel="canonical")["href"][:-1]

    def extract_number(self, text) -> int:
        return int("".join([n for n in text if n.isdigit()]))

    def parse_price(self, text) -> Price:
        if "pw" in text and "pcm" in text:
            tokens = text.split("£")[1:]
            return Price(
                to_rent=ToRentPrice(
                    per_month=self.extract_number(tokens[0]),
                    per_week=self.extract_number(tokens[1]),
                )
            )
        elif "pw" in text:
            return Price(to_rent=ToRentPrice(per_week=self.extract_number(text)))
        else:
            return Price(for_sale=self.extract_number(text))


class RegionsScraper(Scraper):
    def scrape_row(self, row) -> Region:
        cells = row.find_all("td")

        return Region(
            name=cells[0].text,
            slug=cells[0].find("a")["href"].split("/")[-2],
            number_of_properties=self.extract_number(cells[1].text),
            average_price=self.parse_price(cells[2].text),
        )

    def scrape(self) -> List[Region]:
        rows = self.soup.find("table", attrs={"class": "browse-table"}).find_all("tr")
        return [self.scrape_row(row) for row in rows[1:]]


class PropertyScraper(Scraper):
    def extract_id(self, url_string) -> int:
        url = urlparse(url_string)
        return int(url.path.split("/")[3])


class PropertiesListScraper(PropertyScraper):
    def scrape_result(self, result) -> Property:
        href = result.find("a", attrs={"data-testid": "listing-details-link"})["href"]
        url = urljoin("https://www.zoopla.co.uk", href).split("?")[0][:-1]
        address = result.find("p", attrs={"data-testid": "listing-description"}).text
        price = self.parse_price(
            result.find("div", attrs={"data-testid": "listing-price"}).text
        )
        number_of_bedrooms = self.extract_number(
            result.find("div", attrs={"data-testid": "listing-spec"})
            .find_all("div")[0]
            .text
        )

        return Property(
            id=self.extract_id(url),
            url=url,
            address=address,
            price=price,
            number_of_bedrooms=number_of_bedrooms,
        )

    def scrape(self) -> List[Property]:
        results = self.soup.find_all("div", attrs={"data-testid": "search-result"})
        return [self.scrape_result(result) for result in results]


class PropertyDetailsScraper(PropertyScraper):
    def scrape(self) -> Property:
        url = self.canonical_url
        address = self.soup.find("span", attrs={"data-testid": "address-label"}).text
        price = self.parse_price(
            self.soup.find("span", attrs={"data-testid": "price"}).text
        )
        number_of_bedrooms = self.extract_number(
            self.soup.find("span", attrs={"data-testid": "beds-label"}).text
        )

        return Property(
            id=self.extract_id(url),
            url=url,
            address=address,
            price=price,
            number_of_bedrooms=number_of_bedrooms,
        )
