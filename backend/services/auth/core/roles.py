from enum import Enum

class UserRole(str, Enum):
    PASSAGER = "PASSAGER"
    COMPAGNIE = "COMPAGNIE"
    ATC = "ATC"
    ADMIN = "ADMIN"
