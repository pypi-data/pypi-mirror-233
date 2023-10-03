###################################################################################################
# WAREHOUSE ENDPOINT ENUMS
###################################################################################################
from enum import Enum


class GoodsOutNoteEventCode(Enum):
    PRI = "PRI"  # Printed
    UPR = "UPR"  # Unprinted
    PIC = "PIC"  # Picked
    UPI = "UPI"  # Unpicked
    PAC = "PAC"  # Packed
    UPA = "UPA"  # Unpacked
    SHW = "SHW"  # Shipped
