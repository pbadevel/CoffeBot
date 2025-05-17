from dataclasses import dataclass
from enum import Enum

class UserRoleEnum(Enum):
    admin = 'admin'
    barista = 'barista'
    user = 'user'


@dataclass
class UserRole:
    admin = UserRoleEnum.admin.value
    barista = UserRoleEnum.barista.value
    user = UserRoleEnum.user.value


