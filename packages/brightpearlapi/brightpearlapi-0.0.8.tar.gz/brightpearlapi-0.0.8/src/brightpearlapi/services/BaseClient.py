###################################################################################################
# BRIGHTPEARL API BASE CLIENT
# A client for handling API requests to Brightpearl API
# API Docs: https://api-docs.brightpearl.com/
###################################################################################################

from brightpearlapi.utils.connection import Connection, OauthConnection
from urllib.parse import urlencode
import logging

log = logging.getLogger("brightpearl.api")


class BaseClient:
    BASE_URL = "{protocol}://{datacenter}.brightpearl.com/2.0.0/{account_id}/{endpoint}"

    def __init__(self, client_id=None, client_secret=None, oauth=False, account_id=None, datacenter=None,
                 access_token=None, developer_ref=None, app_ref=None, protocol="https", rate_limit_management=None):

        self.protocol = protocol
        self.client_id = client_id
        self.client_secret = client_secret
        self.account = account_id
        self.access_token = access_token
        self.datacenter = datacenter
        self.developer_ref = developer_ref
        self.app_ref = app_ref
        self.oauth = oauth
        self.rate_limit_management = rate_limit_management

        self._initialize_connection()

    def _initialize_connection(self):
        """
        Determine the connection type based on the OAuth flag and initialize it.
        """
        if self.oauth:
            self.connection = OauthConnection(self.client_id, self.client_secret, protocol=self.protocol)
        else:
            self.connection = Connection(
                self.datacenter, self.account, self.access_token, self.developer_ref, self.app_ref,
                protocol=self.protocol, rate_limit_management=self.rate_limit_management
            )

    def _make_request(self, method, endpoint, data=None):
        """
        Make a request to Brightpearl API using the connection object.

        :param method: str - HTTP method (e.g., GET, POST).
        :param endpoint: str - API endpoint to hit.
        :param data: dict - Data payload for POST/PUT requests.
        :return: dict - Response data.
        """
        try:
            response = self.connection.make_request(endpoint, method, data=data)
            return response
        except Exception as e:
            raise Exception(f"Failed to make a request: {str(e)}")
