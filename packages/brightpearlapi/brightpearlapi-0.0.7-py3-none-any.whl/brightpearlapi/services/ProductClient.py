###################################################################################################
# PRODUCT CLIENT
# A client for handling API requests to Brightpearl Product-Service API
# API Docs: https://api-docs.brightpearl.com/order/index.html
###################################################################################################
"""
PRODUCT CLIENT MODULE
---------------------
This module provides a client for handling API requests to the Brightpearl Product-Service API.

Classes:
    - ProductClient: Main client class for handling products in the Brightpearl API.
    - Brand: Handles operations related to the Brand resource.
    - BrightpearlCategory: Handles operations related to the Brightpearl Category resource.
    - Channel: Handles operations related to the Channel resource.
    - ChannelBrand: Handles operations related to the Channel Brand resource.
    - Collection: Handles operations related to the Collection resource.
    - DiscountContactUsage: Handles operations related to the Discount Contact Usage resource.
    - DiscountTotalUsage: Handles operations related to the Discount Total Usage resource.
    - Option: Handles operations related to the Option resource.
    - OptionValue: Handles operations related to the Option Value resource.
    - PriceList: Handles operations related to the Price List resource.
    - ProductPrimarySupplier: Handles operations related to the Product Primary Supplier resource.
    - Product: Handles operations related to the Product resource.
    - ProductBundle: Handles operations related to the Product Bundle resource.
    - ProductCustomField: Handles operations related to the Product Custom Field resource.
    - CustomFieldMetadata: Handles operations related to the Custom Field Metadata resource.
    - CustomField: Handles operations related to the Custom Field resource.
    - ProductGroup: Handles operations related to the Product Group resource.
    - ProductIdentity: Handles operations related to the Product Identity resource.
    - ProductOptionValue: Handles operations related to the Product Option Value resource.
    - ProductPrice: Handles operations related to the Product Price resource.
    - ProductSupplier: Handles operations related to the Product Supplier resource.
    - ProductType: Handles operations related to the Product Type resource.
    - ProductTypeOptionAssociation: Handles operations related to the Product Type Option Association resource.
    - Season: Handles operations related to the Season resource.

Each class inherits from the BaseClient and provides methods to interact with the respective resource in the Brightpearl API.

For more details on the API and its endpoints, refer to:
https://api-docs.brightpearl.com/order/index.html
"""
from typing import List, Union
from src.brightpearlapi.services.BaseClient import BaseClient


class ProductClient(BaseClient):
    """
    Client for handling products in the Brightpearl API.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the ProductClient.
        """
        super().__init__(*args, **kwargs)
        self.Brand = Brand(*args, **kwargs)
        self.BrightpearlCategory = BrightpearlCategory(*args, **kwargs)
        self.Channel = Channel(*args, **kwargs)
        self.ChannelBrand = ChannelBrand(*args, **kwargs)
        self.Collection = Collection(*args, **kwargs)
        self.DiscountContactUsage = DiscountContactUsage(*args, **kwargs)
        self.DiscountTotalUsage = DiscountTotalUsage(*args, **kwargs)
        self.Option = Option(*args, **kwargs)
        self.OptionValue = OptionValue(*args, **kwargs)
        self.PriceList = PriceList(*args, **kwargs)
        self.ProductPrimarySupplier = ProductPrimarySupplier(*args, **kwargs)
        self.Product = Product(*args, **kwargs)
        self.ProductBundle = ProductBundle(*args, **kwargs)
        self.ProductCustomField = ProductCustomField(*args, **kwargs)
        self.CustomFieldMetadata = CustomFieldMetadata(*args, **kwargs)
        self.CustomField = CustomField(*args, **kwargs)
        self.ProductGroup = ProductGroup(*args, **kwargs)
        self.ProductIdentity = ProductIdentity(*args, **kwargs)
        self.ProductOptionValue = ProductOptionValue(*args, **kwargs)
        self.ProductPrice = ProductPrice(*args, **kwargs)
        self.ProductSupplier = ProductSupplier(*args, **kwargs)
        self.ProductType = ProductType(*args, **kwargs)
        self.ProductTypeOptionAssociation = ProductTypeOptionAssociation(*args, **kwargs)
        self.Season = Season(*args, **kwargs)


class Brand(BaseClient):
    """
    A client class for handling brand-related operations in the Brightpearl API.
    """

    def search(self, params=None):
        """
        Search for brands based on provided parameters.

        Args:
            params (str, optional): Search parameters.

        Returns:
            dict: Response data.

        Raises:
            Exception: If the search operation fails.
        """
        endpoint = f"product-service/brand-search"
        if params:
            endpoint += f"?{params}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Brands: {str(e)}')

    def get(self, id_set=None):
        """
        Retrieve brand details based on the provided ID set.

        Args:
            id_set (str, optional): ID set of the brand to retrieve.

        Returns:
            dict: Response data.

        Raises:
            Exception: If the retrieval operation fails.
        """
        endpoint = f"product-service/brand/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Brand: {str(e)}')

    def post(self, data):
        """
        Create a new brand with the provided data.

        Args:
            data (dict): Data for the new brand.

        Returns:
            dict: Response data.

        Raises:
            Exception: If the creation operation fails.
        """
        endpoint = f"product-service/brand/"
        try:
            response = self._make_request('POST', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to create Brand: {str(e)}')


class BrightpearlCategory(BaseClient):
    """
        A client class for handling Brightpearl categories in the Brightpearl API.

        Inherits from:
        - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def search(self, params=None):
        """
        Search for Brightpearl categories based on provided parameters.

        Args:
        - params (dict, optional): Parameters for the search query.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/brightpearl-category-search"
        if params:
            endpoint += f"?{params}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Brightpearl Categories: {str(e)}')

    def get(self, id_set=None):
        """
        Retrieve a specific Brightpearl category or a set of categories based on their IDs.

        Args:
        - id_set (str, optional): Comma-separated list of category IDs to retrieve.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/brightpearl-category/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Brightpearl Category: {str(e)}')

    def post(self, data):
        """
        Create a new Brightpearl category.

        Args:
        - data (dict): Data for the new category.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/brightpearl-category/"
        try:
            response = self._make_request('POST', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to create Brightpearl Category: {str(e)}')


class Channel(BaseClient):
    """
    A client class for handling channels in the Brightpearl API.

    Inherits from:
    - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def get(self, id_set=None):
        """
        Retrieve a specific channel or a set of channels based on their IDs.

        Args:
        - id_set (str, optional): Comma-separated list of channel IDs to retrieve.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/channel/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Channel: {str(e)}')


class ChannelBrand(BaseClient):
    """
    A client class for handling channel brands in the Brightpearl API.

    Inherits from:
    - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def get(self, id_set=None):
        """
        Retrieve a specific channel brand or a set of channel brands based on their IDs.

        Args:
        - id_set (str, optional): Comma-separated list of channel brand IDs to retrieve.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/channel-brand/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Channel Brand: {str(e)}')


class Collection(BaseClient):
    """
    A client class for handling collections in the Brightpearl API.

    Inherits from:
    - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def search(self, params=None):
        """
        Search for collections based on provided parameters.

        Args:
        - params (dict, optional): Parameters for the search query.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/collection-search"
        if params:
            endpoint += f"?{params}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Collections: {str(e)}')


class DiscountContactUsage(BaseClient):
    """
    A client class for handling discount contact usages in the Brightpearl API.

    Inherits from:
    - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def get(self, discount_id, contact_id):
        """
        Retrieve the usage of a discount by a specific contact.

        Args:
        - discount_id (int): ID of the discount.
        - contact_id (int): ID of the contact.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = f"product-service/discount/{discount_id}/contact-usage/{contact_id}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Discount Contact Usage: {str(e)}')


class DiscountTotalUsage(BaseClient):
    """
    A client class for handling total discount usages in the Brightpearl API.

    Inherits from:
    - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def get(self, discount_id):
        """
        Retrieve the total usage of a specific discount.

        Args:
        - discount_id (int): ID of the discount.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = f"product-service/discount/{discount_id}/total-usage"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Discount Total Usage: {str(e)}')


class Option(BaseClient):
    """
    A client class for handling options in the Brightpearl API.

    Inherits from:
    - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def search(self, params=None):
        """
        Search for options based on provided parameters.

        Args:
        - params (dict, optional): Parameters for the search query.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/option-search"
        if params:
            endpoint += f"?{params}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Options: {str(e)}')

    def get(self, id_set=None):
        """
        Retrieve a specific option or a set of options based on their IDs.

        Args:
        - id_set (str, optional): Comma-separated list of option IDs to retrieve.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/option/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Option: {str(e)}')

    def post(self, data):
        """
        Create a new option.

        Args:
        - data (dict): Data for the new option.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/option/"
        try:
            response = self._make_request('POST', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to create Option: {str(e)}')


class OptionValue(BaseClient):
    """
    A client class for handling option values in the Brightpearl API.

    Inherits from:
    - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def search(self, params=None):
        """
        Search for option values based on provided parameters.

        Args:
        - params (dict, optional): Parameters for the search query.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/option-value-search"
        if params:
            endpoint += f"?{params}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Option Values: {str(e)}')

    def get(self, id_set):
        """
        Retrieve option values associated with a specific option.

        Args:
        - id_set (str): ID of the option to retrieve values for.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = f"product-service/option/{id_set}/value"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Option Value: {str(e)}')

    def post(self, id_set, data):
        """
        Create a new option value for a specific option.

        Args:
        - id_set (str): ID of the option to add a value for.
        - data (dict): Data for the new option value.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = f"product-service/option/{id_set}/value"
        try:
            response = self._make_request('POST', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to create Option Value: {str(e)}')


class PriceList(BaseClient):
    """
    A client class for handling price lists in the Brightpearl API.

    Inherits from:
    - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def get(self, id_set=None):
        """
        Retrieve a specific price list or a set of price lists based on their IDs.

        Args:
        - id_set (str, optional): Comma-separated list of price list IDs to retrieve.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/price-list/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Price List: {str(e)}')


class ProductPrimarySupplier(BaseClient):
    """
    A client class for handling primary suppliers of products in the Brightpearl API.

    Inherits from:
    - BaseClient: The base client class for handling API requests to Brightpearl.
    """

    def put(self, product_id, data):
        """
        Update the primary supplier for a specific product.

        Args:
        - product_id (int): ID of the product to update.
        - data (dict): Data for the primary supplier update.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = f"product-service/product-primary-supplier/{product_id}/product"
        try:
            response = self._make_request('PUT', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to update Product Primary Supplier: {str(e)}')


class Product(BaseClient):
    """
    Interface for the Product endpoints in the Brightpearl API.

    Provides methods to search, retrieve, create, and update products.
    """

    def search(self, params=None):
        """
        Search for products based on provided parameters.

        Args:
        - params (dict, optional): Parameters for the search query.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/product-search"
        if params:
            endpoint += f"?{params}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Products: {str(e)}')

    def options(self, id_set=None):
        """
        Retrieve options associated with a specific product or set of products.

        Args:
        - id_set (str, optional): Comma-separated list of product IDs to retrieve options for.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = f"product-service/product/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product(s): {str(e)}')

    def get(self, id_set=None):
        """
        Retrieve a specific product or a set of products based on their IDs.

        Args:
        - id_set (str, optional): Comma-separated list of product IDs to retrieve.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/product/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product(s): {str(e)}')

    def post(self, data):
        """
        Create a new product.

        Args:
        - data (dict): Data for the new product.

        Returns:
        - dict: Response data from the API.

        Raises:
        - Exception: If the API request fails.
        """
        endpoint = "product-service/product/"
        try:
            response = self._make_request('POST', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to create Product: {str(e)}')

    def put(self, id, data):
        """
        Update an existing product.

        :param id: ID of the product to update.
        :param data: Updated data for the product.
        :return: Response data from the API.
        """
        endpoint = f"product-service/product/{id}"
        try:
            response = self._make_request('PUT', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to update Product: {str(e)}')


class ProductBundle(BaseClient):
    """
    Interface for the Product Bundle endpoints in the Brightpearl API.

    Provides methods to retrieve product bundles.
    """

    def get(self, id_set):
        """
        Retrieve product bundles based on provided ID set.

        :param id_set: Set of product bundle IDs.
        :return: Response data containing product bundle details.
        """
        endpoint = f"product-service/product-bundle/{id_set}/bundle"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product Bundle: {str(e)}')


class ProductCustomField(BaseClient):
    """
    Interface for the Product Custom Field endpoints in the Brightpearl API.

    Provides methods to retrieve product custom fields.
    """

    def get(self, id_set=None):
        """
        Retrieve product custom fields based on provided ID set.

        :param id_set: Optional set of product custom field IDs.
        :return: Response data containing product custom field details.
        """
        endpoint = "product-service/product-custom-field/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product Custom Field: {str(e)}')


class CustomFieldMetadata(BaseClient):
    """
    Interface for the Custom Field Metadata endpoints in the Brightpearl API.

    Provides methods to retrieve custom field metadata.
    """

    def get(self):
        """
        Retrieve custom field metadata.

        :return: Response data containing custom field metadata details.
        """
        endpoint = "product-service/custom-field-meta-data/"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Custom Field Metadata: {str(e)}')


class CustomField(BaseClient):
    """
    Interface for the Custom Field endpoints in the Brightpearl API.

    Provides methods to retrieve and update custom fields.
    """

    def get(self, product_id):
        """
        Retrieve custom fields for a specific product.

        :param product_id: ID of the product.
        :return: Response data containing custom field details for the product.
        """
        endpoint = f"product-service/{product_id}/custom-field/"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Custom Field: {str(e)}')

    def patch(self, product_id, data):
        """
        Update custom fields for a specific product.

        :param product_id: ID of the product.
        :param data: Updated data for the custom fields.
        :return: Response data from the API.
        """
        endpoint = f"product-service/{product_id}/custom-field/"
        try:
            response = self._make_request('PATCH', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to patch Custom Field: {str(e)}')


class ProductGroup(BaseClient):
    """
    Interface for the Product Group endpoints in the Brightpearl API.

    Provides methods to retrieve and update product groups.
    """

    def get(self, id_set):
        """
        Retrieve product groups based on provided ID set.

        :param id_set: Set of product group IDs.
        :return: Response data containing product group details.
        """
        endpoint = f"product-service/product-group/{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product Group: {str(e)}')

    def put(self, product_group_id, data):
        """
        Update an existing product group.

        :param product_group_id: ID of the product group to update.
        :param data: Updated data for the product group.
        :return: Response data from the API.
        """
        endpoint = f"product-service/product-group/{product_group_id}"
        try:
            response = self._make_request('PUT', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to update Product Group: {str(e)}')


class ProductIdentity(BaseClient):
    """
    Interface for the Product Identity endpoints in the Brightpearl API.

    Provides methods to update product identities.
    """

    def put(self, product_id, data):
        """
        Update the identity of a specific product.

        :param product_id: ID of the product.
        :param data: Updated identity data for the product.
        :return: Response data from the API.
        """
        endpoint = f"product-service/product/{product_id}/identity/"
        try:
            response = self._make_request('PUT', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to update Product Identity: {str(e)}')


class ProductOptionValue(BaseClient):
    """
    Interface for the Product Option Value endpoints in the Brightpearl API.

    Provides methods to retrieve option values associated with products.
    """

    def options(self, product_id_set='*', option_value_id_set=None):
        """
        Retrieve option values for specific products.

        :param product_id_set: Set of product IDs.
        :param option_value_id_set: Optional set of option value IDs.
        :return: Response data containing option value details.
        """
        endpoint = f"product-service/product/{product_id_set}/option-value/options/"
        if option_value_id_set:
            endpoint += f"{option_value_id_set}"
        try:
            response = self._make_request('OPTIONS', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product Option Value options: {str(e)}')

    def get(self, product_id_set='*', option_value_id_set=None):
        """
        Retrieve option values for specific products.

        :param product_id_set: Set of product IDs.
        :param option_value_id_set: Optional set of option value IDs.
        :return: Response data containing option value details.
        """
        endpoint = f"product-service/product/{product_id_set}/option-value/"
        if option_value_id_set:
            endpoint += f"{option_value_id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product Option Value: {str(e)}')


class ProductPrice(BaseClient):
    """
    Interface for the Product Price endpoints in the Brightpearl API.

    Provides methods to retrieve and update prices for products on price lists.
    """

    def options(self, product_id_set='*', price_list_id_set=None):
        """
        Retrieve price options for specific products.

        :param product_id_set: Set of product IDs.
        :param price_list_id_set: Optional set of price list IDs.
        :return: Response data containing price options.
        """
        endpoint = f"product-service/product-price/{product_id_set}"
        if price_list_id_set:
            endpoint += f"/price-list/{price_list_id_set}"
        try:
            response = self._make_request('OPTIONS', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product Price options: {str(e)}')

    def get(self, product_id_set, price_list_id_set=None):
        """
        Retrieve prices for specific products.

        :param product_id_set: Set of product IDs.
        :param price_list_id_set: Optional set of price list IDs.
        :return: Response data containing product prices.
        """
        endpoint = f"product-service/product-price/{product_id_set}"
        if price_list_id_set:
            endpoint += f"/price-list/{price_list_id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product Price: {str(e)}')

    def put(self, product_id, data):
        """
        Update the price of a specific product.

        :param product_id: ID of the product.
        :param data: Updated price data for the product.
        :return: Response data from the API.
        """
        endpoint = f"product-service/product-price/{product_id}/price-list"
        try:
            response = self._make_request('PUT', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to update Product Price: {str(e)}')


class ProductSupplier(BaseClient):
    """
    Interface for the Product Supplier endpoints in the Brightpearl API.

    Provides methods to retrieve, create, and delete suppliers for given products.
    """

    def get(self, product_id_set):
        """
        Retrieve suppliers for specific products.

        :param product_id_set: Set of product IDs.
        :return: Response data containing product supplier details.
        """
        endpoint = f"product-service/product/{product_id_set}/supplier"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product Supplier: {str(e)}')

    def post(self, product_id, data):
        """
        Create a new supplier for a specific product.

        :param product_id: ID of the product.
        :param data: Data for the new supplier.
        :return: Response data from the API.
        """
        endpoint = f"product-service/product/{product_id}/supplier"
        try:
            response = self._make_request('POST', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to create Product Supplier: {str(e)}')

    def delete(self, product_id, data):
        """
        Delete a supplier from a specific product.

        :param product_id: ID of the product.
        :param data: Data specifying the supplier to delete.
        :return: Response data from the API.
        """
        endpoint = f"product-service/product/{product_id}/supplier"
        try:
            response = self._make_request('DELETE', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to delete Product Supplier: {str(e)}')


class ProductType(BaseClient):
    """
    Interface for the Product Type endpoints in the Brightpearl API.

    Provides methods to search, retrieve, and create product types.
    """

    def search(self, params=None):
        """
        Search for product types based on provided parameters.

        :param params: Optional search parameters.
        :return: Response data containing search results.
        """
        endpoint = "product-service/product-type-search"
        if params:
            endpoint += f"?{params}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Product Types: {str(e)}')

    def get(self, id_set=None):
        """
        Retrieve product types based on provided ID set.

        :param id_set: Optional set of product type IDs.
        :return: Response data containing product type details.
        """
        endpoint = "product-service/product-type/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Product Type: {str(e)}')

    def post(self, data):
        """
        Create a new product type.

        :param data: Data for the new product type.
        :return: Response data from the API.
        """
        endpoint = "product-service/product-type/"
        try:
            response = self._make_request('POST', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to create Product Type: {str(e)}')


class ProductTypeOptionAssociation(BaseClient):
    """
    Interface for the Product Type Option Association endpoints in the Brightpearl API.

    Provides methods to create associations between product types and options.
    """

    def post(self, product_type_id_set, option_id_set, data):
        """
        Create an association between a product type and an option.

        :param product_type_id_set: Set of product type IDs.
        :param option_id_set: Set of option IDs.
        :param data: Data specifying the association.
        :return: Response data from the API.
        """
        endpoint = f"product-service/product-type/{product_type_id_set}/option-association/{option_id_set}"
        try:
            response = self._make_request('POST', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to create Product Type Option Association: {str(e)}')


class Season(BaseClient):
    """
    Interface for the Season endpoints in the Brightpearl API.

    Provides methods to retrieve and create seasons.
    """

    def get(self, id_set=None):
        """
        Retrieve seasons based on provided ID set.

        :param id_set: Optional set of season IDs.
        :return: Response data containing season details.
        """
        endpoint = "product-service/season/"
        if id_set:
            endpoint += f"{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Season: {str(e)}')

    def post(self, data):
        """
        Create a new season.

        :param data: Data for the new season.
        :return: Response data from the API.
        """
        endpoint = "product-service/season/"
        try:
            response = self._make_request('POST', endpoint, data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to create Season: {str(e)}')
