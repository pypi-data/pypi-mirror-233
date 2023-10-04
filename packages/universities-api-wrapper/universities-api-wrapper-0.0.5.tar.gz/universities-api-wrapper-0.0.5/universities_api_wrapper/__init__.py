# -*- coding: utf-8 -*-

import logging
import requests

from requests import Response

# Set up logger
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

class HipolabsUniversitiesAPI:
    """ Main class for API wrapper. """
    def __init__(self, method, port=8080):
        self.method = method
        self.port = port if port is not None else 8080

    @staticmethod
    def _get_method(method, port):
        """ Selects the connection method, either remote or local. """
        if method == 'remote':
            return "http://universities.hipolabs.com/search"
        elif method == "local":
            return f"http://127.0.0.1:{port}/search"
        else:
            raise UniversitiesAPIError("Unknown method!")

    @staticmethod
    def _check_online(response: Response) -> None:
        """ Checks if API endpoint is online. """
        if response.status_code != 200:
            raise UniversitiesAPIError(response.text)

        logger.debug("Successful request: {}".format(response.status_code))

    @staticmethod
    def endpoints():
        """ Returns endpoints of universities API. """
        return ["name", "country"]

    def get_names(self, response: Response):
        """ Returns names of universities in a list. """
        names = []
        for uni in response:
            names.append(uni['name'])
        return names

    def get_websites(self, response: Response):
        """ Returns websites of universities in a list. """
        websites = []
        for uni in response:
            websites.append(uni['web_pages'])
        return websites

    def get_domains(self, response: Response):
        """ Returns domains of universities in a list. """
        domains = []
        for uni in response:
            domains.append(uni['domains'])
        return domains

    def search(self, country=None, name=None, filters=None) -> dict:
        """ This method searches by name and country. """

        base_url = self._get_method(self.method, self.port)

        if not country and not name:
            raise ValueError("Please provide valid university name or country.")
        elif not name:
            url = f"{base_url}?country={country.lower()}"
        elif not country:
            url = f"{base_url}?name={name.lower()}"
        else:
            url = f"{base_url}?name={name.lower()}&country={country.lower()}"

        response = requests.get(url=url)
        self._check_online(response)
        response = response.json()

        if filters == 'names':
            response = self.get_names(response)
        elif filters == 'websites':
            response = self.get_websites(response)
        elif filters == 'domains':
            response = self.get_domains(response)

        return response


class UniversitiesAPIError(Exception):
    """ Empty class used for raising exceptions. """
    pass
