from enum import Enum


class CodeOils(Enum):
    CODE_PREMIUM_GASOLINE = 'B034'
    CODE_GASOLINE = 'B027'
    CODE_DIESEL = 'D047'
    CODE_LPG = 'K015'

    def is_in_enum(code):
        for i in CodeOils:
            if code == i.value:
                return True
        return False
