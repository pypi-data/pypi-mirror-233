from unittest import mock
import pytest

from universities_api_wrapper import HipolabsUniversitiesAPI

# Unit tests are local so I'm using local method here.

@pytest.fixture
def method():
    """ Fixture for local connection method. """
    return "local"

@pytest.fixture
def port():
    """ Returns port. """
    return "8080"

client = HipolabsUniversitiesAPI(method, port)

def test_client():
    """ Tests if client is up. """
    assert isinstance(client, HipolabsUniversitiesAPI)

def test_endpoints():
    """ Tests if endpoints can be viewed. """
    ret = client.endpoints()
    assert ret == ["name", "country"]

def test_get_method(method, port):
    """ Tests if connection method returns local URL. """
    ret = client._get_method(method, port)
    assert ret == "http://127.0.0.1:8080/search"

@mock.patch('universities_api_wrapper.HipolabsUniversitiesAPI.search')
def test_search(mock_response):
    """ Tests main API call with MagicMock. """
    mock_response.return_value.request.method = "GET"
    mock_response.return_value.url = "http://127.0.0.1:8080/search?name=Middle&country=Turkey"
    mock_response.return_value.status_code = 200
    mock_response.return_value.text = "[{ \
        'state-province': None, \
        'domains': ['metu.edu.tr'], \
        'country': 'Turkey', \
        'web_pages': ['http://www.metu.edu.tr/'], \
        'name': 'Middle East Technical University', \
        'alpha_two_code': 'TR' \
        }]"
    mock_response.return_value.content = bytes(mock_response.return_value.text, 'UTF-8')
    # TODO: Figure out the rest here...
    assert mock_response.return_value.status_code == 200
