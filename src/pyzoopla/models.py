from typing import NamedTuple


class Region(NamedTuple):
    name: str
    slug: str
    number_of_properties: int
    average_price: int


class PropertyDetails(NamedTuple):
    url: str
    address: str
    price: int
    number_of_bedrooms: int
