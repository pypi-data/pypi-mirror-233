###################################################################################
# IMPORTS
###################################################################################
from enum import Enum
from urllib.parse import urlencode

###################################################################################
# ENUMS
###################################################################################


class DataType(Enum):
    """
    Enum representing the different data types supported by the Brightpearl API.
    """
    INTEGER = ("INTEGER", "A number with no fractional component. Example: 5")
    IDSET = ("IDSET", "A representation of one or more IDs. Example: 1,3,6-10")
    STRING = ("STRING", "A Unicode String with exact matching. Example: 'Brightpearl'")
    DATETIME = ("DATETIME", "An ISO 8601 date/time. Example: 2007-03-01T13:00:00Z")
    BOOLEAN = ("BOOLEAN", "A boolean value. Example: true or false")
    SEARCH_STRING = ("SEARCH_STRING", "A Unicode String for case-insensitive substring matching. Example: 'RIGHT'")
    STRING_SET = ("STRING_SET", "A representation of one or more String values. Example: 'LIVE.DISCONTINUED'")
    FREE_TEXT_QUERY = ("FREE_TEXT_QUERY", "A type for filters to match any column with the type SEARCH_STRING. Example: 'right'")
    PERIOD = ("PERIOD", "A period value as an ISO 8061 date or date/time. Example: 2012-01-09 or 2007-03-01T13:00:00Z")

    def __init__(self, data_type, description):
        self.data_type = data_type
        self.description = description


class Company(Enum):
    """
    Enum representing the column options for the contact-service/company-search endpoint in the Brightpearl API.
    """
    companyId = ("companyId", DataType.INTEGER)
    name = ("name", DataType.SEARCH_STRING)


class CompanyFilter(Enum):
    """
    Enum representing the filter options for the contact-service/company-search endpoint in the Brightpearl API.
    """
    contactId = ('contactId', DataType.INTEGER)


class ContactColumns(Enum):
    """
    Enum representing the column options for the contact-service/contact-search endpoint in the Brightpearl API.
    """
    contactId = ("contactId", DataType.IDSET)
    primaryEmail = ("primaryEmail", DataType.SEARCH_STRING)
    secondaryEmail = ("secondaryEmail", DataType.SEARCH_STRING)
    tertiaryEmail = ("tertiaryEmail", DataType.SEARCH_STRING)
    firstName = ("firstName", DataType.SEARCH_STRING)
    lastName = ("lastName", DataType.SEARCH_STRING)
    isSupplier = ("isSupplier", DataType.BOOLEAN)
    companyName = ("companyName", DataType.SEARCH_STRING)
    isStaff = ("isStaff", DataType.BOOLEAN)
    isCustomer = ("isCustomer", DataType.BOOLEAN)
    createdOn = ("createdOn", DataType.PERIOD)
    updatedOn = ("updatedOn", DataType.PERIOD)
    lastContactedOn = ("lastContactedOn", DataType.PERIOD)
    lastOrderedOn = ("lastOrderedOn", DataType.PERIOD)
    nominalCode = ("nominalCode", DataType.INTEGER)
    isPrimary = ("isPrimary", DataType.BOOLEAN)
    pri = ("pri", DataType.STRING)
    sec = ("sec", DataType.STRING)
    mob = ("mob", DataType.STRING)
    exactCompanyName = ("exactCompanyName", DataType.STRING)
    title = ("title", DataType.STRING)


class ContactFilters(Enum):
    """
    Enum representing the filter options for the contact-service/contact-search endpoint in the Brightpearl API.
    """
    allEmail = ("allEmail", DataType.STRING)
    tagIds = ("tagIds", DataType.IDSET)
    allPhone = ("allPhone", DataType.STRING)
    companyIds = ("companyIds", DataType.IDSET)


class ContactSorting(Enum):
    """
    Enum representing the sorting options for the contact-service/contact-search endpoint in the Brightpearl API.
    """
    contactId = ("contactId", "ASC")


class ContactGroupColumns(Enum):
    """
    Enum representing the column options for the contact-service/contact-group-search endpoint in the Brightpearl API.
    """
    contactGroupId = ("contactGroupId", DataType.INTEGER)
    name = ("name", DataType.SEARCH_STRING)
    description = ("description", DataType.SEARCH_STRING)
    numberOfMembers = ("numberOfMembers", DataType.INTEGER)


class ContactGroupSorting(Enum):
    """
    Enum representing the sorting options for the contact-service/contact-group-search endpoint in the Brightpearl API.
    """
    NAME_ASC = ("name", "ASC")


class ContactGroupMemberColumns(Enum):
    """
    Enum representing the column options for the contact-service/contact-group-member-search endpoint in the Brightpearl API.
    """
    CONTACT_ID = ("contactId", DataType.INTEGER)
    FIRST_NAME = ("firstName", DataType.SEARCH_STRING)
    LAST_NAME = ("lastName", DataType.SEARCH_STRING)
    CONTACT_GROUP_ID = ("contactGroupId", DataType.INTEGER)
    CONTACT_GROUP_NAME = ("contactGroupName", DataType.SEARCH_STRING)
    CONTACT_GROUP_DESCRIPTION = ("contactGroupDescription", DataType.SEARCH_STRING)


class ContactGroupMemberSorting(Enum):
    """
    Enum representing the sorting options for the contact-service/contact-group-member-search endpoint in the Brightpearl API.
    """
    CONTACT_ID_ASC = ("contactId", "ASC")


###################################################################################
# EXCEPTIONS
###################################################################################
class InvalidColumnError(ValueError):
    """
    Exception raised when an invalid column is provided to the search constructor.
    """
    pass


class DataTypeMismatchError(TypeError):
    """
    Exception raised when the provided value's data type doesn't match the expected data type.
    """
    pass


###################################################################################
# SEARCH CONSTRUCTORS
###################################################################################
class BaseSearchConstructor:
    """
    Base class for constructing search queries for the Brightpearl API.

    Attributes:
        ALLOWED_COLUMNS (list): List of allowed columns for the specific endpoint.
        parameters (dict): Dictionary to store the search parameters.
    """
    ALLOWED_COLUMNS = []

    def __init__(self):
        """
        Initializes a new instance of the BaseSearchConstructor.
        """
        self.parameters = {}

    def add_parameter(self, column: Enum, value: str):
        """
        Adds a search parameter to the query.

        Args:
            column (Enum): The column Enum representing the search column.
            value (str): The value to search for.

        Returns:
            BaseSearchConstructor: Returns the instance to allow for method chaining.

        Raises:
            InvalidColumnError: If the provided column is not allowed.
            DataTypeMismatchError: If the provided value's data type doesn't match the expected data type.
        """
        column_name, column_data_type = column.value
        expected_data_type = column_data_type.data_type

        # Check if the column is allowed for the specific endpoint
        if column not in self.ALLOWED_COLUMNS:
            raise InvalidColumnError(f"Invalid column: {column_name}. Allowed columns are: {[col.value[0] for col in self.ALLOWED_COLUMNS]}")

        # Check the data type of the provided value
        if expected_data_type == DataType.INTEGER.data_type and not isinstance(value, int):
            raise DataTypeMismatchError(f"Expected INTEGER for column {column_name}, but got {type(value)}")
        elif expected_data_type == DataType.IDSET.data_type and not (isinstance(value, str) and all([v.isdigit() for v in value.split(",")])):
            raise DataTypeMismatchError(f"Expected IDSET for column {column_name}, but got {type(value)}")
        elif expected_data_type == DataType.STRING.data_type and not isinstance(value, str):
            raise DataTypeMismatchError(f"Expected STRING for column {column_name}, but got {type(value)}")
        elif expected_data_type == DataType.DATETIME.data_type and not isinstance(value, str):  # Further validation for ISO 8601 format can be added
            raise DataTypeMismatchError(f"Expected DATETIME for column {column_name}, but got {type(value)}")
        elif expected_data_type == DataType.BOOLEAN.data_type and not isinstance(value, bool):
            raise DataTypeMismatchError(f"Expected BOOLEAN for column {column_name}, but got {type(value)}")
        elif expected_data_type == DataType.SEARCH_STRING.data_type and not isinstance(value, str):
            raise DataTypeMismatchError(f"Expected SEARCH_STRING for column {column_name}, but got {type(value)}")
        elif expected_data_type == DataType.STRING_SET.data_type and not isinstance(value, str):  # Further validation can be added if needed
            raise DataTypeMismatchError(f"Expected STRING_SET for column {column_name}, but got {type(value)}")
        elif expected_data_type == DataType.FREE_TEXT_QUERY.data_type and not isinstance(value, str):
            raise DataTypeMismatchError(f"Expected FREE_TEXT_QUERY for column {column_name}, but got {type(value)}")
        elif expected_data_type == DataType.PERIOD.data_type and not isinstance(value, str):  # Further validation for ISO 8061 format can be added
            raise DataTypeMismatchError(f"Expected PERIOD for column {column_name}, but got {type(value)}")

        self.parameters[column_name] = value
        return self

    def to_uri(self):
        """
        Converts the search parameters to a URI encoded string.

        Returns:
            str: The URI encoded search string.
        """
        return urlencode(self.parameters)


class ContactGroupMemberSearch(BaseSearchConstructor):
    """
    Search constructor for the ContactGroupMemberSearch endpoint in the Brightpearl API.

    This class helps in constructing search queries specifically for the ContactGroupMemberSearch endpoint.

    Attributes:
        ALLOWED_COLUMNS (list): List of allowed columns for the ContactGroupMemberSearch endpoint.
    """
    ALLOWED_COLUMNS = ContactGroupMemberColumns


class CompanySearch(BaseSearchConstructor):
    """
    Search constructor for the CompanySearch endpoint in the Brightpearl API.

    This class helps in constructing search queries specifically for the CompanySearch endpoint.

    Attributes:
        ALLOWED_COLUMNS (list): List of allowed columns for the CompanySearch endpoint.
    """
    ALLOWED_COLUMNS = Company


class ContactSearch(BaseSearchConstructor):
    """
    Search constructor for the ContactSearch endpoint in the Brightpearl API.

    This class helps in constructing search queries specifically for the ContactSearch endpoint.

    Attributes:
        ALLOWED_COLUMNS (list): List of allowed columns for the ContactSearch endpoint.
    """
    ALLOWED_COLUMNS = ContactColumns


class ContactGroupSearch(BaseSearchConstructor):
    """
    Search constructor for the ContactGroupSearch endpoint in the Brightpearl API.

    This class helps in constructing search queries specifically for the ContactGroupSearch endpoint.

    Attributes:
        ALLOWED_COLUMNS (list): List of allowed columns for the ContactGroupSearch endpoint.
    """
    ALLOWED_COLUMNS = ContactGroupColumns


class ContactGroupMemberSearch(BaseSearchConstructor):
    """
    Search constructor for the ContactGroupMemberSearch endpoint in the Brightpearl API.

    This class helps in constructing search queries specifically for the ContactGroupMemberSearch endpoint.

    Attributes:
        ALLOWED_COLUMNS (list): List of allowed columns for the ContactGroupMemberSearch endpoint.
    """
    ALLOWED_COLUMNS = ContactGroupMemberColumns
