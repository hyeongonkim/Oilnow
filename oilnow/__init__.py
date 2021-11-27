from oilnow.model.OpinetApi import OpinetApi
from oilnow.model.CodeOils import CodeOils


if __name__ == '__main__':
    opinet_api = OpinetApi()
    print(opinet_api.get_station_list_by_name('방학동'))
    print(opinet_api.get_oil_price_by_station_id('A0009599', CodeOils.CODE_PREMIUM_GASOLINE))
