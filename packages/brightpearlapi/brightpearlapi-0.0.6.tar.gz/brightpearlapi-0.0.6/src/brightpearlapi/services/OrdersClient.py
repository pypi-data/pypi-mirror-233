###################################################################################################
# ORDERS CLIENT
# A client for handling API requests to Brightpearl Order-Service API
# API Docs: https://api-docs.brightpearl.com/order/index.html
###################################################################################################

from typing import List, Union
from brightpearlapi.services.BaseClient import BaseClient
import brightpearlapi.models.order_classes_get as GET


class OrdersClient(BaseClient):
    """
    Client for handling orders in the Brightpearl API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the OrdersClient.
        """
        super().__init__(*args, **kwargs)
        self.Order = OrderService(*args, **kwargs)
        self.SalesOrder = SalesOrder(*args, **kwargs)


class OrderService(BaseClient):
    """
    Service for handling general orders in the Brightpearl API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the OrderService.
        """
        super().__init__(*args, **kwargs)

    def get(self, id_set: Union[int, str]) -> Union[GET.Order, None]:
        """
        Fetch an order by its ID set.

        Args:
            id_set (Union[int, str]): The ID set of the order to fetch.

        Returns:
            Union[GET.Order, None]: The fetched order or None if not found.
        """
        endpoint = f"order-service/order/{id_set}"
        try:
            response = self._make_request("GET", endpoint)
            if len(response['response']) == 1:
                return GET.Order.from_api_response(response['response'][0])
            return None
        except Exception as e:
            raise Exception(f"Failed to get order: {str(e)}")


class SalesOrder(BaseClient):
    """
    Service for handling sales orders in the Brightpearl API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the SalesOrder service.
        """
        super().__init__(*args, **kwargs)

    def get(self, id: Union[int, str]) -> Union[GET.SalesOrder, None]:
        """
        Fetch a sales order by its ID.

        Args:
            id (Union[int, str]): The ID of the sales order to fetch.

        Returns:
            Union[GET.SalesOrder, None]: The fetched sales order or None if not found.
        """
        endpoint = f"order-service/sales-order/{id}"
        try:
            response = self._make_request("GET", endpoint)
            if len(response['response']) == 1:
                return GET.SalesOrder(response['response'][0])
            return None
        except Exception as e:
            raise Exception(f"Failed to get order: {str(e)}")

    def get_set(self, id_set: Union[int, str]) -> List[GET.SalesOrder]:
        """
        Fetch a set of sales orders by their ID set.

        Args:
            id_set (Union[int, str]): The ID set of the sales orders to fetch.

        Returns:
            List[GET.SalesOrder]: A list of fetched sales orders.
        """
        endpoint = f"order-service/sales-order/{id_set}"
        try:
            response = self._make_request("GET", endpoint)
            return [GET.SalesOrder(data) for data in response['response']]
        except Exception as e:
            raise Exception(f"Failed to get order: {str(e)}")

    def post(self, data: dict) -> dict:
        """
        Create a new sales order.

        Args:
            data (dict): The data for the new sales order.

        Returns:
            dict: The response from the API.
        """
        endpoint = f"order-service/sales-order"
        try:
            response = self._make_request("POST", endpoint, data=data)
            return response['response']
        except Exception as e:
            raise Exception(f"Failed to post order: {str(e)}")
