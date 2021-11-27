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

    def find_enum_by_name(name):
        if name == CodeOils.CODE_PREMIUM_GASOLINE.name:
            return CodeOils.CODE_PREMIUM_GASOLINE
        elif name == CodeOils.CODE_GASOLINE.name:
            return CodeOils.CODE_GASOLINE
        elif name == CodeOils.CODE_DIESEL.name:
            return CodeOils.CODE_DIESEL
        elif name == CodeOils.CODE_LPG.name:
            return CodeOils.CODE_LPG
        raise TypeError
