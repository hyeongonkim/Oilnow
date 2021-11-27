# -*- coding:utf-8 -*-

from enum import Enum


class CodeOils(Enum):
    PREMIUM_GASOLINE = 'B034'
    GASOLINE = 'B027'
    DIESEL = 'D047'
    LPG = 'K015'

    def is_in_enum(code):
        for i in CodeOils:
            if code == i.value:
                return True
        return False

    def find_enum_by_name(name):
        if name == CodeOils.PREMIUM_GASOLINE.name:
            return CodeOils.PREMIUM_GASOLINE
        elif name == CodeOils.GASOLINE.name:
            return CodeOils.GASOLINE
        elif name == CodeOils.DIESEL.name:
            return CodeOils.DIESEL
        elif name == CodeOils.LPG.name:
            return CodeOils.LPG
        raise TypeError

    def find_enum_by_kor_name(name):
        if name == '고급휘발유':
            return CodeOils.PREMIUM_GASOLINE
        elif name == '휘발유':
            return CodeOils.GASOLINE
        elif name == '경유':
            return CodeOils.DIESEL
        elif name == 'LPG':
            return CodeOils.LPG
        raise TypeError

    def find_kor_name_by_enum(name):
        if name == CodeOils.PREMIUM_GASOLINE:
            return '고급휘발유'
        elif name == CodeOils.GASOLINE:
            return '휘발유'
        elif name == CodeOils.DIESEL:
            return '경유'
        elif name == CodeOils.LPG:
            return 'LPG'
        raise TypeError
