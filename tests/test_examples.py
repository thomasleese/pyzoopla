import pytest
import responses

from pyzoopla import Zoopla


@pytest.fixture
def zoopla():
    return Zoopla()


@responses.activate
def test_get_for_sale_regions(zoopla):
    responses.add(
        responses.GET,
        "https://www.zoopla.co.uk/for-sale/",
        body=open("tests/examples/for-sale-regions.html").read(),
    )

    regions = zoopla.get_for_sale_regions()

    assert len(regions) == 14

    assert regions[0].name == "London"
    assert regions[0].slug == "london"
    assert regions[0].number_of_properties == 91199
    assert regions[0].average_price == 1090738


@responses.activate
def test_get_to_rent_regions(zoopla):
    responses.add(
        responses.GET,
        "https://www.zoopla.co.uk/to-rent/",
        body=open("tests/examples/to-rent-regions.html").read(),
    )

    regions = zoopla.get_to_rent_regions()

    assert len(regions) == 14

    assert regions[0].name == "London"
    assert regions[0].slug == "london"
    assert regions[0].number_of_properties == 48864
    assert regions[0].average_price == 766


@responses.activate
def test_get_for_sale_properties(zoopla):
    responses.add(
        responses.GET,
        "https://www.zoopla.co.uk/for-sale/property/london?pn=1",
        body=open("tests/examples/for-sale-properties-list.html").read(),
    )

    properties = zoopla.get_for_sale_properties("london")

    assert len(properties) == 25

    assert properties[0].url == "https://www.zoopla.co.uk/for-sale/details/61154032"
    assert properties[0].address == "Selhurst Road, London SE25"
    assert properties[0].price == 375000
    assert properties[0].number_of_bedrooms == 3


@responses.activate
def test_get_to_rent_properties(zoopla):
    responses.add(
        responses.GET,
        "https://www.zoopla.co.uk/to-rent/property/london?pn=1",
        body=open("tests/examples/to-rent-properties-list.html").read(),
    )

    properties = zoopla.get_to_rent_properties("london")

    assert len(properties) == 25

    assert properties[0].url == "https://www.zoopla.co.uk/to-rent/details/61154038"
    assert properties[0].address == "5 Purbeck Gardens, London SE26"
    assert properties[0].price == 1400323
    assert properties[0].number_of_bedrooms == 1


@responses.activate
def test_get_property_details(zoopla):
    responses.add(
        responses.GET,
        "https://www.zoopla.co.uk/for-sale/details/61115321",
        body=open("tests/examples/property-details.html").read(),
    )

    property_details = zoopla.get_property_details(61115321)

    assert property_details.url == "https://www.zoopla.co.uk/for-sale/details/61115321/"
    assert property_details.address == "Park Road, Bracknell, Berkshire RG12"
    assert property_details.price == 600000
    assert property_details.number_of_bedrooms == 4
