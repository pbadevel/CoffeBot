from dataclasses import dataclass
from enum import Enum

class UserRoleEnum(Enum):
    admin = 'admin'
    barista = 'barista'
    user = 'user'
