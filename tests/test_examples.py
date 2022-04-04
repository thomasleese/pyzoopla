import pytest

from pyzoopla import Zoopla


@pytest.fixture
def zoopla():
    return Zoopla()


def test_get_property(zoopla):
    property_details = zoopla.get_property_details(61115321)

    assert property_details.url == "https://www.zoopla.co.uk/for-sale/details/61115321/"
    assert property_details.address == "Park Road, Bracknell, Berkshire RG12"
    assert property_details.price == 600000
    assert property_details.number_of_bedrooms == 4
