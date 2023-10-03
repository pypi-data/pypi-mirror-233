from typing import List
from brightpearlapi.models.common_classes import Amount


class GoodsOutNote:
    """Represents a note for goods that are going out."""

    KEYS_ORDER_ROWS = "orderRows"
    KEYS_EVENTS = "events"

    def __init__(self, id, data: dict):
        """
        Initialize a GoodsOutNote instance.

        :param data: Dictionary containing the data for the goods out note.
        """
        self._id = id
        self._order_id = data.get("orderId")
        self._warehouse_id = data.get("warehouseId")
        self._transfer = data.get("transfer")
        self._priority = data.get("priority")
        self._status = GoodsOutNoteStatus(data=data['status'])
        self._shipping = Shipping(data['shipping'])
        self._release_date = data.get("releaseDate")
        self._created_on = data.get("createdOn")
        self._created_by = data.get("createdBy")
        self._order_rows = self._initialize_order_rows(data.get(self.KEYS_ORDER_ROWS, {}))
        self._sequence = data.get("sequence")
        self._events = [Event(event_data) for event_data in data.get(self.KEYS_EVENTS, [])]
        self._label_uri = data.get("labelUri")
        self._last_event_version = data.get("lastEventVersion")

    def _initialize_order_rows(self, order_rows_data: dict) -> dict:
        """Initializes order rows from the given data."""
        return {int(sequence): [OrderRow(row_data) for row_data in rows]
                for sequence, rows in order_rows_data.items()}


class GoodsOutNoteStatus:
    """
    Represents the status of a Goods Out Note in the Brightpearl system.
    """

    def __init__(self, data: dict):
        """
        Initialize the GoodsOutNoteStatus with the provided data.

        :param data: Dictionary containing the status details.
        """
        self._shipped = data.get("shipped", False)
        self._packed = data.get("packed", False)
        self._picked = data.get("picked", False)
        self._printed = data.get("printed", False)
        self._picked_on = data.get("pickedOn", None)
        self._packed_on = data.get("packedOn", None)
        self._shipped_on = data.get("shippedOn", None)
        self._printed_on = data.get("printedOn", None)
        self._picked_by_id = data.get("pickedById", None)
        self._packed_by_id = data.get("packedById", None)
        self._shipped_by_id = data.get("shippedById", None)
        self._printed_by_id = data.get("printedById", None)

    @property
    def shipped(self):
        return self._shipped

    @property
    def packed(self):
        return self._packed

    @property
    def picked(self):
        return self._picked

    @property
    def printed(self):
        return self._printed

    @property
    def picked_on(self):
        return self._picked_on

    @property
    def packed_on(self):
        return self._packed_on

    @property
    def shipped_on(self):
        return self._shipped_on

    @property
    def printed_on(self):
        return self._printed_on

    @property
    def picked_by_id(self):
        return self._picked_by_id

    @property
    def packed_by_id(self):
        return self._packed_by_id

    @property
    def shipped_by_id(self):
        return self._shipped_by_id

    @property
    def printed_by_id(self):
        return self._printed_by_id


class Shipping:
    """
    Represents shipping details for an order.
    """

    def __init__(self, data: dict):
        """
        Initialize the Shipping details with the provided data.

        :param data: Dictionary containing the shipping details.
        """
        self._reference = data.get("reference", None)
        self._boxes = data.get("boxes", None)
        self._shipping_method_id = data.get("shippingMethodId", None)
        self._weight = data.get("weight", None)

    @property
    def reference(self):
        return self._reference

    @property
    def boxes(self):
        return self._boxes

    @property
    def shipping_method_id(self):
        return self._shipping_method_id

    @property
    def weight(self):
        return self._weight


class OrderRow:
    def __init__(self, data):
        self._product_id = data.get("productId", None)
        self._quantity = data.get("quantity", None)
        self._location_id = data.get("locationId", None)
        self._user_batch_reference = data.get("userBatchReference", None)

    @property
    def product_id(self):
        return self._product_id

    @property
    def quantity(self):
        return self._quantity

    @property
    def location_id(self):
        return self._location_id

    @property
    def user_batch_reference(self):
        return self._user_batch_reference


class Event:
    def __init__(self, data):
        self._occurred = data.get("occured", None)
        self._event_owner_id = data.get("eventOwnerId", None)
        self._event_code = data.get("eventCode", None)

    @property
    def occurred(self):
        return self._occurred

    @property
    def event_owner_id(self):
        return self._event_owner_id

    @property
    def event_code(self):
        return self._event_code


class FulfilmentSource:
    def __init__(self, data):
        self._available_products: List[FulfilmentProduct] = []
        available_products_data = data["response"]["availableProducts"]
        for product_id, product_data in available_products_data.items():
            self._available_products.append(FulfilmentProduct(product_id, product_data))

        self._unavailable_products = data["response"]["unavailableProducts"]

    @property
    def available_products(self):
        return self._available_products

    @property
    def unavailable_products(self):
        return self._unavailable_products


class FulfilmentProduct:
    def __init__(self, product_id, data):
        self._product_id = product_id
        self._suppliers: List[FulfilmentSupplier] = []
        suppliers_data = data.get("suppliers", {})
        for supplier_id, supplier_data in suppliers_data.items():
            self._suppliers.append(FulfilmentSupplier(supplier_id, supplier_data))

        self._warehouses: List[FulfilmentWarehouse] = []
        warehouses_data = data.get("warehouses", {})
        for warehouse_id, warehouse_data in warehouses_data.items():
            self._warehouses.append(FulfilmentWarehouse(warehouse_id, warehouse_data))

    @property
    def product_id(self):
        return self._product_id

    @property
    def suppliers(self):
        return self._suppliers

    @property
    def warehouses(self):
        return self._warehouses


class FulfilmentSupplier:
    def __init__(self, supplier_id, data):
        self._supplier_id = supplier_id
        self._cost_points = data.get("costPoints", {})
        self._sku = data.get("sku", None)

    @property
    def supplier_id(self):
        return self._supplier_id

    @property
    def cost_points(self):
        return self._cost_points

    @property
    def sku(self):
        return self._sku


class FulfilmentWarehouse:
    def __init__(self, warehouse_id, data):
        self._warehouse_id = warehouse_id
        self._on_hand = data.get("onHand", None)

    @property
    def warehouse_id(self):
        return self._warehouse_id

    @property
    def on_hand(self):
        return self._on_hand


class ProductAvailabilityResponse:
    def __init__(self, data):
        self._products = []
        for product_id, product_data in data["response"].items():
            self._products.append(ProductAvailability(int(product_id), product_data))

    @property
    def products(self):
        return self._products


class ProductAvailability:
    def __init__(self, product_id, data):
        self._product_id = product_id
        self._total = ProductTotal(data["total"])
        self._warehouses = []
        for warehouse_id, warehouse_data in data.get("warehouses", {}).items():
            self._warehouses.append(WarehouseAvailability(int(warehouse_id), warehouse_data))

    @property
    def product_id(self):
        return self._product_id

    @property
    def total(self):
        return self._total

    @property
    def warehouses(self):
        return self._warehouses


class ProductTotal:
    def __init__(self, data):
        self._in_stock = data["inStock"]
        self._on_hand = data["onHand"]
        self._allocated = data["allocated"]
        self._in_transit = data["inTransit"]

    @property
    def in_stock(self):
        return self._in_stock

    @property
    def on_hand(self):
        return self._on_hand

    @property
    def allocated(self):
        return self._allocated

    @property
    def in_transit(self):
        return self._in_transit


class WarehouseAvailability:
    def __init__(self, warehouse_id, data):
        self._warehouse_id = warehouse_id
        self._in_stock = data["inStock"]
        self._on_hand = data["onHand"]
        self._allocated = data["allocated"]
        self._in_transit = data["inTransit"]

    @property
    def warehouse_id(self):
        return self._warehouse_id

    @property
    def in_stock(self):
        return self._in_stock

    @property
    def on_hand(self):
        return self._on_hand

    @property
    def allocated(self):
        return self._allocated

    @property
    def in_transit(self):
        return self._in_transit


class GoodsMoved:
    """Represents the details of goods that have been moved."""

    def __init__(self, product_id, quantity, destination_location_id, batch_goods_note_id, product_value, created_on, created_by):
        """
        Initialize a GoodsMoved instance.

        :param product_id: ID of the product.
        :param quantity: Quantity of the product moved.
        :param destination_location_id: ID of the destination location.
        :param batch_goods_note_id: ID of the batch goods note.
        :param product_value: Value of the product.
        :param created_on: Date the goods were moved.
        :param created_by: ID of the user who moved the goods.
        """
        self.product_id = product_id
        self.quantity = quantity
        self.destination_location_id = destination_location_id
        self.batch_goods_note_id = batch_goods_note_id
        self.product_value = product_value
        self.created_on = created_on
        self.created_by = created_by

    @classmethod
    def from_api_response(cls, data):
        """Create a GoodsMoved instance from API response data."""
        product_value = Amount(data['productValue']['currency'], data['productValue']['value'])
        return cls(data['productId'], data['quantity'], data['destinationLocationId'], data['batchGoodsNoteId'], product_value, data['createdOn'], data['createdBy'])


class StockCorrection:
    """
    Represents a stock correction event in the Brightpearl system.
    """

    def __init__(self, goods_note_id: int, warehouse_id: int, reason: str, goods_moved: List[GoodsMoved]):
        """
        Initialize the StockCorrection with the provided details.

        :param goods_note_id: ID of the goods note.
        :param warehouse_id: ID of the warehouse.
        :param reason: Reason for the stock correction.
        :param goods_moved: List of goods moved during the correction.
        """
        self.goods_note_id = goods_note_id
        self.warehouse_id = warehouse_id
        self.reason = reason
        self.goods_moved = goods_moved

    @classmethod
    def from_api_response(cls, data: dict) -> 'StockCorrection':
        """
        Create a StockCorrection instance from an API response.

        :param data: Dictionary containing the API response data.
        :return: StockCorrection instance.
        """
        goods_moved = [GoodsMoved(**item) for item in data['goodsMoved']]
        return cls(data['goodsNoteId'], data['warehouseId'], data['reason'], goods_moved)
