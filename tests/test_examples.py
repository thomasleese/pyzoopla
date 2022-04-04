import pytest

from pyzoopla import Zoopla


@pytest.fixture
def zoopla():
    return Zoopla()


def test_get_for_sale_regions(zoopla):
    regions = zoopla.get_for_sale_regions()

    assert len(regions) == 14

    assert regions[0].name == "London"
    assert regions[0].slug == "london"
    assert regions[0].number_of_properties == 91199
    assert regions[0].average_price == 1090738


def test_get_to_rent_regions(zoopla):
    regions = zoopla.get_to_rent_regions()

    assert len(regions) == 14

    assert regions[0].name == "London"
    assert regions[0].slug == "london"
    assert regions[0].number_of_properties == 48864
    assert regions[0].average_price == 766


def test_get_property(zoopla):
    property_details = zoopla.get_property_details(61115321)

    assert property_details.url == "https://www.zoopla.co.uk/for-sale/details/61115321/"
    assert property_details.address == "Park Road, Bracknell, Berkshire RG12"
    assert property_details.price == 600000
    assert property_details.number_of_bedrooms == 4
