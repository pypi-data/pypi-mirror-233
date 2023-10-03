from typing import List
from brightpearlapi.models.common_classes import *

from dataclasses import dataclass
from typing import List


@dataclass
class Order:
    order_id: int
    order_type_code: str
    reference: str
    version: int
    order_status: str
    order_payment_status: str
    stock_status_code: str
    allocation_status_code: str
    shipping_status_code: str
    placed_on: str
    created_on: str
    updated_on: str
    created_by_id: int
    price_list_id: int
    price_mode_code: str
    delivery: dict
    invoices: list
    currency: str
    total_value: float
    assignment: dict
    parties: Parties
    order_rows: List[OrderRow]
    warehouse_id: int
    acknowledged: bool
    cost_price_list_id: int
    historical_order: bool

    @classmethod
    def from_api_response(cls, data):
        data['parties'] = Parties.from_api_response(data['parties'])
        data['order_rows'] = [OrderRow.from_api_response(row) for row in data['orderRows']]
        data['order_status'] = data['orderStatus']['name']

        return cls(
            order_id=data['id'],
            order_type_code=data['orderTypeCode'],
            reference=data['reference'],
            version=data['version'],
            order_status=data['order_status'],
            order_payment_status=data['orderPaymentStatus'],
            stock_status_code=data['stockStatusCode'],
            allocation_status_code=data['allocationStatusCode'],
            shipping_status_code=data['shippingStatusCode'],
            placed_on=data['placedOn'],
            created_on=data['createdOn'],
            updated_on=data['updatedOn'],
            created_by_id=data['createdById'],
            price_list_id=data['priceListId'],
            price_mode_code=data['priceModeCode'],
            delivery=data['delivery'],
            invoices=data['invoices'],
            currency=data['currency'],
            total_value=data['totalValue'],
            assignment=data['assignment'],
            parties=data['parties'],
            order_rows=data['order_rows'],
            warehouse_id=data['warehouseId'],
            acknowledged=data['acknowledged'],
            cost_price_list_id=data['costPriceListId'],
            historical_order=data['historicalOrder']
        )


class SalesCredit:
    def __init__(self, credit_id, credit_status, customer_name, total_amount):
        self.credit_id = credit_id
        self.credit_status = credit_status
        self.customer_name = customer_name
        self.total_amount = total_amount

    @ classmethod
    def from_api_response(cls, data):
        return cls(
            credit_id=data['creditId'],
            credit_status=data['creditStatus'],
            customer_name=data['customerName'],
            total_amount=data['totalAmount']
        )


class ProductRow:
    def __init__(self, data):
        self.id = data.get("id", 0)
        self.product_id = data.get("productId", 0)
        self.name = data.get("name", "")
        self.sku = data.get("sku", "")
        self.quantity = data.get("quantity", "")
        self.tax_code = data.get("taxCode", "")
        self.tax = data.get("tax", "")
        self.net = data.get("net", "")
        self.nominal_code = data.get("nominalCode", "")
        self.external_ref = data.get("externalRef", "")
        self.sequence = data.get("sequence", 0)
        self.bundle_child = data.get("bundleChild", False)
        self.bundle_parent = data.get("bundleParent", False)

    @classmethod
    def from_api_response(cls, data):
        return cls(data)


class SalesOrder:
    def __init__(self, data):
        self.id = data.get("id", 0)
        self.customer = Customer(data.get("customer", {}))
        self.billing = Address(data.get("billing", {}).get("address", {}))
        self.ref = data.get("ref", "")
        self.external_ref = data.get("externalRef", "")
        self.placed_on = data.get("placedOn", "")
        self.created_on = data.get("createdOn", "")
        self.created_by = data.get("createdBy", 0)
        self.updated_on = data.get("updatedOn", "")
        self.tax_date = data.get("taxDate", "")
        self.parent_id = data.get("parentId", 0)
        self.status_id = data.get("statusId", 0)
        self.warehouse_id = data.get("warehouseId", 0)
        self.channel_id = data.get("channelId", 0)
        self.staff_owner_id = data.get("staffOwnerId", 0)
        self.project_id = data.get("projectId", 0)
        self.lead_source_id = data.get("leadSourceId", 0)
        self.team_id = data.get("teamId", 0)
        self.price_list_id = data.get("priceListId", 0)
        self.price_mode_code = data.get("priceModeCode", "")
        self.currency = Currency(data.get("currency", {}))
        self.delivery = Delivery(data.get("delivery", {}))
        self.rows = [ProductRow(row_data) for row_data in data.get("rows", [])]
        self.total = Total(data.get("total", {}))
        self.stock_status_code = data.get("stockStatusCode", "")
        self.is_canceled = data.get("isCanceled", False)
        self.customer_id = data.get("customerId", 0)

    @classmethod
    def from_api_response(cls, data):
        return cls(data)
