from brightpearlapi.services.OrdersClient import OrdersClient
# from brightpearlapi.services.products_client import ProductsClient
from brightpearlapi.services.WarehouseClient import WarehouseClient


class BrightpearlAPI:
    def __init__(self, client_id=None, client_secret=None, oauth=False, account_id=None, datacenter=None,
                 access_token=None, developer_ref=None, app_ref=None, protocol="https", rate_limit_management=None):

        self.protocol = protocol
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.datacenter = datacenter
        self.developer_ref = developer_ref
        self.app_ref = app_ref
        self.oauth = oauth
        self.rate_limit_management = rate_limit_management
        self.account_id = account_id
        self.Orders = OrdersClient(datacenter=self.datacenter, account_id=self.account_id,
                                   app_ref=self.app_ref, access_token=self.access_token)
        self.Warehouse = WarehouseClient(datacenter=self.datacenter, account_id=self.account_id,
                                         app_ref=self.app_ref, access_token=self.access_token)
        # self.products_cli = ProductsClient(datacenter=self.datacenter, account_id=self.account_id,
        #                                   app_ref=self.app_ref, access_token=self.access_token)
