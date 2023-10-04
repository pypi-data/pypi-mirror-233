###################################################################################################
# Contact CLIENT
# A client for handling API requests to Brightpearl Contact-Service API
# API Docs: https://api-docs.brightpearl.com/order/index.html
###################################################################################################

from typing import List, Union
from urllib.parse import urlencode
from src.brightpearlapi.services.BaseClient import BaseClient
import src.brightpearlapi.models.order_classes_get as GET


class ContactClient(BaseClient):
    """
    Client for handling Contact requests in the Brightpearl API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the ContactClient.
        """
        super().__init__(*args, **kwargs)
        self.Contact = Contact(*args, **kwargs)
        self.Company = Company(*args, **kwargs)


class Contact(BaseClient):
    """
    Service for handling contact-service/contact requests in the Brightpearl API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the object.
        """
        super().__init__(*args, **kwargs)

    def search(self, params=None):
        endpoint = f"contact-service/contact-search?{params}"

        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Goods Out Notes: {str(e)}')

    def get_contact(self, id: str):
        """
        Fetch a Contact by its ID.

        Args:
            id (str): The ID of the Contact to fetch.

        Returns:
            dict: The fetched Contact or None if not found.
        """
        endpoint = f"contact-service/contact/{id}"
        try:
            response = self._make_request("GET", endpoint)
            if response:
                return response['response']
            return None
        except Exception as e:
            raise Exception(f"Failed to get Contact: {str(e)}")

    def get_contacts(self, id_set: Union[int, str]):
        """
        Fetch Contacts by id_set.

        Args:
            id_set (Union[int, str]): The ID set of the Contacts to fetch.

        Returns:
            dict: The fetched Contacts or None if not found.
        """
        endpoint = f"contact-service/contact/{id_set}"
        try:
            response = self._make_request("GET", endpoint)
            if len(response['response']) >= 1:
                return response['response']
            return None
        except Exception as e:
            raise Exception(f"Failed to get Contact: {str(e)}")

    def post_contact(self, params):
        pass

    def patch_contact(self, params):
        pass

    def options_contact(self, id_set):
        pass


class Company(BaseClient):
    """
    Service for handling contact-service/company requests in the Brightpearl API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the object.
        """
        super().__init__(*args, **kwargs)

    def search(self, params=None):
        endpoint = f"contact-service/company-search?"
        try:
            response = self._make_request('GET', endpoint, params=params)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Goods Out Notes: {str(e)}')

    def get(self, id_set=None):
        """
        Fetch a Company by its ID, or fetch multiple companies by a set of IDs.

        Args:
            id_set (str): The ID/ID set of the Company/companies to fetch.

        Returns:
            dict: The fetched Company/companies or None if not found.
        """
        endpoint = f"contact-service/company"
        if id_set:
            endpoint += f"/{id_set}"
        try:
            response = self._make_request("GET", endpoint)
            if response:
                return response['response']
            return None
        except Exception as e:
            raise Exception(f"Failed to get Contact: {str(e)}")

    def post_company(self, params):
        pass

    def put_company(self, params):
        pass
