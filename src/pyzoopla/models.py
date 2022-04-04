from typing import NamedTuple, Optional


class ToRentPrice(NamedTuple):
    per_month: Optional[int] = None
    per_week: Optional[int] = None


class Price(NamedTuple):
    for_sale: Optional[int] = None
    to_rent: Optional[ToRentPrice] = None


class Region(NamedTuple):
    name: str
    slug: str
    number_of_properties: int
    average_price: Price


class Property(NamedTuple):
    id: int
    url: str
    address: str
    price: Price
    number_of_bedrooms: int
