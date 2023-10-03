###################################################################################################
# WAREHOUSE CLIENT
# A client for handling API requests to Brightpearl Warehouse-Service API
# API Docs: https://api-docs.brightpearl.com/warehouse/index.html
###################################################################################################
from typing import List
from brightpearlapi.services.BaseClient import BaseClient
import brightpearlapi.models.warehouse_classes_get as GET
import brightpearlapi.models.warehouse_classes_post as POST


class WarehouseClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.FulfillmentSource: FulfilmentSource = FulfilmentSource(*args, **kwargs)
        self.ProductAvailability: ProductAvailability = ProductAvailability(*args, **kwargs)
        self.GoodsOutNotes: GoodsOutNote = GoodsOutNote(*args, **kwargs)
        self.Warehouse: Warehouse = Warehouse(*args, **kwargs)
        self.GoodsOutNoteEvent: GoodsOutNoteEvent = GoodsOutNoteEvent(*args, **kwargs)
        self.InternalTransfer: InternalTransfer = InternalTransfer(*args, **kwargs)
        self.Location: Location = Location(*args, **kwargs)
        self.Pick: Pick = Pick(*args, **kwargs)


class GoodsOutNote(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def search(self, params=None, sort_asc=True):
        endpoint = f"warehouse-service/goods-note/goods-out-search?"
        try:
            response = self._make_request('GET', endpoint, params=params)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to search for Goods Out Notes: {str(e)}')

    def get(self, note_id):
        endpoint = f"warehouse-service/order/*/goods-note/goods-out/{note_id}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Goods Out Note {note_id}: {str(e)}')

    def get_by_order_id(self, order_id) -> List[GET.GoodsOutNote]:
        endpoint = f"warehouse-service/order/{order_id}/goods-note/goods-out"
        try:
            response = self._make_request('GET', endpoint)
            return [GET.GoodsOutNote(note, response['response'][note]) for note in response['response']]
        except Exception as e:
            raise Exception(f'Failed to get Goods Out Note {order_id}: {str(e)}')

    def post(self, order_id, data):
        endpoint = f"warehouse-service/order/{order_id}/goods-note/goods-out"
        try:
            response = self._make_request('POST', endpoint, data=data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to post Goods out note: {str(e)}')

    def put(self, note_id, data):
        endpoint = f"warehouse-service/goods-note/goods-out/{note_id}"
        try:
            response = self._make_request('PUT', endpoint, data=data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Goods Out Note {note_id}: {str(e)}')

    def delete(self, order_id, note_id):
        endpoint = f"warehouse-service/order/{order_id}/goods-note/goods-out/{note_id}"
        try:
            response = self._make_request('DELETE', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Goods Out Note {note_id}: {str(e)}')


class GoodsOutNoteEvent(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, note_id, data):
        endpoint = f"warehouse-service/goods-note/goods-out/{note_id}/event"
        try:
            response = self._make_request('POST', endpoint, data=data)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to post Goods out note event: {str(e)}')


class InternalTransfer(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Location(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Pick(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Warehouse(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def search(self, params=None):
        endpoint = f"warehouse-service/warehouse-search?"
        try:
            response = self._make_request('GET', endpoint, params)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Warehouse: {str(e)}')

    def get(self, id=None):
        endpoint = f"warehouse-service/warehouse"
        if id:
            endpoint = f"warehouse-service/warehouse/{id}"
        try:
            response = self._make_request('GET', endpoint)
            return response['response']
        except Exception as e:
            raise Exception(f'Failed to get Warehouse: {str(e)}')


class FulfilmentSource(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, id_set=None):
        endpoint = f"warehouse-service/fulfilment-source/{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return GET.FulfilmentSource(response)
        except Exception as e:
            raise Exception(f'Failed to get FulfilmentSource: {str(e)}')


class ProductAvailability(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, id_set=None):
        endpoint = f"warehouse-service/product-availability/{id_set}"
        try:
            response = self._make_request('GET', endpoint)
            return GET.ProductAvailabilityResponse(response)
        except Exception as e:
            raise Exception(f'Failed to get ProductAvailability: {str(e)}')
