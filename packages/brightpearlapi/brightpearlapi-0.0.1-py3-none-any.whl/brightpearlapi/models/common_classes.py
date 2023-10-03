class Quantity:
    def __init__(self, magnitude):
        self.magnitude = magnitude


class Amount:
    def __init__(self, currencyCode, value):
        self.currency_code = currencyCode
        self.value = value


class Currency:
    def __init__(self, data):
        self.code = data.get("code", "")
        self.exchange_rate = data.get("exchangeRate", "")
        self.fixed_exchange_rate = data.get("fixedExchangeRate", False)


class Total:
    def __init__(self, data):
        self.net = data.get("net", "")
        self.tax = data.get("tax", "")
        self.gross = data.get("gross", "")
        self.base_net = data.get("baseNet", "")
        self.base_tax = data.get("baseTax", "")
        self.base_gross = data.get("baseGross", "")


class RowValue:
    def __init__(self, tax_rate, tax_code, tax_calculator, row_net, row_tax, tax_class_id):
        self.tax_rate = tax_rate
        self.tax_code = tax_code
        self.tax_calculator = tax_calculator
        self.row_net: Amount = row_net
        self.row_tax: Amount = row_tax
        self.tax_class_id = tax_class_id


class Composition:
    def __init__(self, bundle_parent, bundle_child, parent_order_row_id):
        self.bundle_parent = bundle_parent
        self.bundle_child = bundle_child
        self.parent_order_row_id = parent_order_row_id


class OrderRow:
    def __init__(self, order_row_sequence, product_id, product_name, product_sku, quantity, item_cost,
                 product_price, discount_percentage, row_value, nominal_code, composition):
        self.order_row_sequence = order_row_sequence
        self.product_id = product_id
        self.product_name = product_name
        self.product_sku = product_sku
        self.quantity: Quantity = quantity
        self.item_cost = item_cost
        self.product_price: Amount = product_price
        self.discount_percentage = discount_percentage
        self.row_value: RowValue = row_value
        self.nominal_code = nominal_code
        self.composition: Composition = composition

    @classmethod
    def from_api_response(cls, data):
        quantity_data = data['quantity']
        item_cost_data = data['itemCost']
        product_price_data = data['productPrice']
        row_value_data = data['rowValue']
        composition_data = data['composition']

        quantity = Quantity(quantity_data['magnitude'])
        item_cost = Amount(item_cost_data['currencyCode'], item_cost_data['value'])
        product_price = Amount(product_price_data['currencyCode'], product_price_data['value'])
        row_value = RowValue(row_value_data['taxRate'], row_value_data['taxCode'],
                             row_value_data['taxCalculator'], Amount(**row_value_data['rowNet']),
                             Amount(**row_value_data['rowTax']), row_value_data['taxClassId'])
        composition = Composition(composition_data['bundleParent'], composition_data['bundleChild'],
                                  composition_data['parentOrderRowId'])

        return cls(data['orderRowSequence'], data['productId'], data['productName'], data['productSku'],
                   quantity, item_cost, product_price, data['discountPercentage'], row_value,
                   data['nominalCode'], composition)


class Parties:
    def __init__(self, customer, delivery, billing):
        self.customer: Customer = customer
        self.delivery: Customer = delivery
        self.billing: Customer = billing

    @classmethod
    def from_api_response(cls, data):

        try:
            customer_data = data['customer']
            delivery_data = data['delivery']
            billing_data = data['billing']

            customer = Customer(
                contact_id=customer_data['contactId'],
                address_full_name=customer_data['addressFullName'],
                company_name=customer_data['companyName'],
                address_line1=customer_data['addressLine1'],
                address_line2=customer_data['addressLine2'],
                address_line3=customer_data['addressLine3'],
                address_line4=customer_data['addressLine4'],
                postal_code=customer_data['postalCode'],
                country=customer_data['country'],
                telephone=customer_data['telephone'],
                mobile_telephone=customer_data['mobileTelephone'],
                email=customer_data['email'],
                country_id=customer_data['countryId'],
                country_iso_code=customer_data['countryIsoCode'],
                country_iso_code3=customer_data['countryIsoCode3']
            )

            delivery = Customer(
                address_full_name=delivery_data['addressFullName'],
                company_name=delivery_data['companyName'],
                address_line1=delivery_data['addressLine1'],
                address_line2=delivery_data['addressLine2'],
                address_line3=delivery_data['addressLine3'],
                address_line4=delivery_data['addressLine4'],
                postal_code=delivery_data['postalCode'],
                country=delivery_data['country'],
                telephone=delivery_data['telephone'],
                mobile_telephone=delivery_data['mobileTelephone'],
                email=delivery_data['email'],
                country_id=delivery_data['countryId'],
                country_iso_code=delivery_data['countryIsoCode'],
                country_iso_code3=delivery_data['countryIsoCode3']
            )

            billing = Customer(
                contact_id=billing_data['contactId'],
                address_full_name=billing_data['addressFullName'],
                company_name=billing_data['companyName'],
                address_line1=billing_data['addressLine1'],
                address_line2=billing_data['addressLine2'],
                address_line3=billing_data['addressLine3'],
                address_line4=billing_data['addressLine4'],
                postal_code=billing_data['postalCode'],
                country=billing_data['country'],
                telephone=billing_data['telephone'],
                mobile_telephone=billing_data['mobileTelephone'],
                email=billing_data['email'],
                country_id=billing_data['countryId'],
                country_iso_code=billing_data['countryIsoCode'],
                country_iso_code3=billing_data['countryIsoCode3']
            )

            return cls(customer, delivery, billing)

        except Exception as e:
            raise Exception(f"Failed to load Parties from response: {str(e)}")


class Address:
    def __init__(self, data):
        self.address_full_name = data.get("addressFullName", "")
        self.company_name = data.get("companyName", "")
        self.address_line1 = data.get("addressLine1", "")
        self.address_line2 = data.get("addressLine2", "")
        self.address_line3 = data.get("addressLine3", "")
        self.address_line4 = data.get("addressLine4", "")
        self.postal_code = data.get("postalCode", "")
        self.country_iso_code = data.get("countryIsoCode", "")
        self.telephone = data.get("telephone", "")
        self.mobile_telephone = data.get("mobileTelephone", "")
        self.email = data.get("email", "")


class Customer:
    def __init__(self, data):
        self.id = data.get("id", 0)
        self.address = Address(data.get("address", {}))


class Delivery:
    def __init__(self, data):
        self.date = data.get("date", "")
        self.address = Address(data.get("address", {}))
        self.shipping_method_id = data.get("shippingMethodId", 0)


############################################################################################
# DEPRECATED
############################################################################################

"""class Customer:
    def __init__(self, address_full_name, company_name, address_line1, address_line2,
                 address_line3, address_line4, postal_code, country, telephone, mobile_telephone,
                 email, country_id, country_iso_code, country_iso_code3, contact_id=None):
        self.contact_id = contact_id
        self.address_full_name = address_full_name
        self.company_name = company_name
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.address_line3 = address_line3
        self.address_line4 = address_line4
        self.postal_code = postal_code
        self.country = country
        self.telephone = telephone
        self.mobile_telephone = mobile_telephone
        self.email = email
        self.country_id = country_id
        self.country_iso_code = country_iso_code
        self.country_iso_code3 = country_iso_code3

"""
