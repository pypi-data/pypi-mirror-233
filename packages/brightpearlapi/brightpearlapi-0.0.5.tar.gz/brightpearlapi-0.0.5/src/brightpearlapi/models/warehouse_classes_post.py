
from typing import List


class GoodsOutNoteProduct:
    def __init__(self, product_id, sales_order_row_id, quantity):
        self.product_id = product_id
        self.sales_order_row_id = sales_order_row_id
        self.quantity = quantity

    def to_dict(self):
        return {
            "productId": self.product_id,
            "salesOrderRowId": self.sales_order_row_id,
            "quantity": self.quantity
        }


class GoodsOutNoteWarehouse:
    def __init__(self, release_date, warehouse_id, transfer=False, products: List[GoodsOutNoteProduct] = []):
        self.release_date = release_date
        self.warehouse_id = warehouse_id
        self.transfer = transfer
        self.products: List[GoodsOutNoteProduct] = products

    def add_product(self, product: GoodsOutNoteProduct):
        self.products.append(product)

    def to_dict(self):
        return {
            "releaseDate": self.release_date,
            "warehouseId": self.warehouse_id,
            "transfer": self.transfer,
            "products": [product.to_dict() for product in self.products]
        }


class GoodsOutNote:
    def __init__(self, warehouses, priority=False, shipping_method_id=None, label_uri=None):
        self.warehouses: List[GoodsOutNoteWarehouse] = warehouses
        self.priority = priority
        self.shipping_method_id = shipping_method_id
        self.label_uri = label_uri

    def add_warehouse(self, warehouse: GoodsOutNoteWarehouse):
        self.warehouses.append(warehouse)

    def to_dict(self):
        return {
            "warehouses": [warehouse.to_dict() for warehouse in self.warehouses],
            "priority": self.priority,
            "shippingMethodId": self.shipping_method_id,
            "labelUri": self.label_uri
        }


class GoodsOutNoteEvent:
    def __init__(self) -> None:
        pass


class InternalTransfer:
    def __init__(self, warehouse_id, transferred_products):
        self.warehouse_id = warehouse_id
        self.transferred_products: List[TransferredProduct] = transferred_products

    def to_dict(self):
        return {
            "warehouseId": self.warehouse_id,
            "transferredProducts": [product.to_dict() for product in self.transferred_products]
        }


class TransferredProduct:
    def __init__(self, product_id, quantity, from_location_id, to_location_id):
        self.product_id = product_id
        self.quantity = quantity
        self.from_location_id = from_location_id
        self.to_location_id = to_location_id

    def to_dict(self):
        return {
            "productId": self.product_id,
            "quantity": self.quantity,
            "fromLocationId": self.from_location_id,
            "toLocationId": self.to_location_id
        }
