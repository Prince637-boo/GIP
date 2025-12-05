import enum

class BaggageStatus(str, enum.Enum):
    CHECKED_IN = "CHECKED_IN"
    LOADED = "LOADED"
    IN_TRANSIT = "IN_TRANSIT"
    UNLOADED = "UNLOADED"
    DELIVERED = "DELIVERED"
    LOST = "LOST"
    FOUND = "FOUND"
