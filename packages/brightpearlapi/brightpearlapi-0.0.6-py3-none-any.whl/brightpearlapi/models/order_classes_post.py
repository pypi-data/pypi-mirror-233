from typing import List


class Customer:
    """Represents a Brightpearl customer."""

    def __init__(self, customer_id: int):
        """
        Initialize a new customer.

        :param customer_id: Unique identifier for the customer.
        """
        self.id = customer_id

    def to_dict(self) -> dict:
        """Convert the customer object to a dictionary."""
        return {
            "id": self.id
        }


class Currency:
    """Represents a currency used in Brightpearl transactions."""

    def __init__(self, code: str, fixed_exchange_rate: bool, exchange_rate: str):
        """
        Initialize a new currency.

        :param code: Currency code (e.g., 'USD').
        :param fixed_exchange_rate: Whether the exchange rate is fixed.
        :param exchange_rate: The exchange rate value.
        """
        self.code = code
        self.fixed_exchange_rate = fixed_exchange_rate
        self.exchange_rate = exchange_rate

    def to_dict(self) -> dict:
        """Convert the currency object to a dictionary."""
        return {
            "code": self.code,
            "fixedExchangeRate": self.fixed_exchange_rate,
            "exchangeRate": self.exchange_rate
        }


class Address:
    """Represents a physical address."""

    def __init__(self, address_full_name: str, company_name: str, address_line1: str, address_line2: str,
                 address_line3: str, address_line4: str, postal_code: str, country_iso_code: str,
                 telephone: str, mobile_telephone: str, email: str):
        """
        Initialize a new address.

        :param address_full_name: Full name associated with the address.
        :param company_name: Name of the company.
        :param address_line1: First line of the address.
        :param address_line2: Second line of the address.
        :param address_line3: Third line of the address.
        :param address_line4: Fourth line of the address.
        :param postal_code: Postal code.
        :param country_iso_code: ISO code of the country.
        :param telephone: Telephone number.
        :param mobile_telephone: Mobile telephone number.
        :param email: Email address.
        """
        self.address_full_name = address_full_name
        self.company_name = company_name
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3
        self.address_line4 = address_line4
        self.postal_code = postal_code
        self.country_iso_code = country_iso_code
        self.telephone = telephone
        self.mobile_telephone = mobile_telephone
        self.email = email

    def to_dict(self) -> dict:
        """Convert the address object to a dictionary."""
        return {
            "addressFullName": self.address_full_name,
            "companyName": self.company_name,
            "addressLine1": self.address_line1,
            "addressLine2": self.address_line2,
            "addressLine3": self.address_line3,
            "addressLine4": self.address_line4,
            "postalCode": self.postal_code,
            "countryIsoCode": self.country_iso_code,
            "telephone": self.telephone,
            "mobileTelephone": self.mobile_telephone,
            "email": self.email
        }


class Delivery:
    """Represents a delivery detail for an order."""

    def __init__(self, delivery_date: str, address: Address, shipping_method_id: int):
        """
        Initialize a new delivery detail.

        :param delivery_date: Date of delivery.
        :param address: Address object where the delivery should be made.
        :param shipping_method_id: ID of the shipping method.
        """
        self.date = delivery_date
        self.address = address
        self.shipping_method_id = shipping_method_id

    def to_dict(self) -> dict:
        """Convert the delivery object to a dictionary."""
        return {
            "date": self.date,
            "address": self.address.to_dict(),
            "shippingMethodId": self.shipping_method_id
        }


class Row:
    """Represents a row in a sales order."""

    def __init__(self, product_id: int, name: str, quantity: str, tax_code: str,
                 net: str, tax: str, nominal_code: str, external_ref: str):
        """
        Initialize a new row for a sales order.

        :param product_id: ID of the product.
        :param name: Name of the product.
        :param quantity: Quantity of the product.
        :param tax_code: Tax code associated with the product.
        :param net: Net amount.
        :param tax: Tax amount.
        :param nominal_code: Nominal code.
        :param external_ref: External reference.
        """
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.tax_code = tax_code
        self.net = net
        self.tax = tax
        self.nominal_code = nominal_code
        self.external_ref = external_ref

    def to_dict(self) -> dict:
        """Convert the row object to a dictionary."""
        return {
            "productId": self.product_id,
            "name": self.name,
            "quantity": self.quantity,
            "taxCode": self.tax_code,
            "net": self.net,
            "tax": self.tax,
            "nominalCode": self.nominal_code,
            "externalRef": self.external_ref
        }


class SalesOrder:
    """Represents a sales order in Brightpearl."""

    def __init__(self, customer: Customer, ref: str, placed_on: str, tax_date: str, parent_id: int,
                 status_id: int, warehouse_id: int, staff_owner_id: int, project_id: int, channel_id: int,
                 external_ref: str, installed_integration_instance_id: int, lead_source_id: int, team_id: int,
                 price_list_id: int, price_mode_code: str, currency: Currency, delivery: Delivery, rows: List[Row]):
        """
        Initialize a new sales order.

        :param customer: Customer object associated with the order.
        :param ref: Reference for the order.
        :param placed_on: Date when the order was placed.
        :param tax_date: Tax date for the order.
        :param parent_id: ID of the parent order.
        :param status_id: Status ID of the order.
        :param warehouse_id: ID of the warehouse.
        :param staff_owner_id: ID of the staff owner.
        :param project_id: ID of the project.
        :param channel_id: ID of the channel.
        :param external_ref: External reference.
        :param installed_integration_instance_id: ID of the installed integration instance.
        :param lead_source_id: ID of the lead source.
        :param team_id: ID of the team.
        :param price_list_id: ID of the price list.
        :param price_mode_code: Price mode code.
        :param currency: Currency object used in the order.
        :param delivery: Delivery details for the order.
        :param rows: List of rows in the order.
        """
        self.customer = customer
        self.ref = ref
        self.placed_on = placed_on
        self.tax_date = tax_date
        self.parent_id = parent_id
        self.status_id = status_id
        self.warehouse_id = warehouse_id
        self.staff_owner_id = staff_owner_id
        self.project_id = project_id
        self.channel_id = channel_id
        self.external_ref = external_ref
        self.installed_integration_instance_id = installed_integration_instance_id
        self.lead_source_id = lead_source_id
        self.team_id = team_id
        self.price_list_id = price_list_id
        self.price_mode_code = price_mode_code
        self.currency = currency
        self.delivery = delivery
        self.rows = rows

    def to_dict(self) -> dict:
        """Convert the sales order object to a dictionary."""
        return {
            "customer": self.customer.to_dict(),
            "ref": self.ref,
            "placedOn": self.placed_on,
            "taxDate": self.tax_date,
            "parentId": self.parent_id,
            "statusId": self.status_id,
            "warehouseId": self.warehouse_id,
            "staffOwnerId": self.staff_owner_id,
            "projectId": self.project_id,
            "channelId": self.channel_id,
            "externalRef": self.external_ref,
            "installedIntegrationInstanceId": self.installed_integration_instance_id,
            "leadSourceId": self.lead_source_id,
            "teamId": self.team_id,
            "priceListId": self.price_list_id,
            "priceModeCode": self.price_mode_code,
            "currency": self.currency.to_dict(),
            "delivery": self.delivery.to_dict(),
            "rows": [row.to_dict() for row in self.rows]
        }
