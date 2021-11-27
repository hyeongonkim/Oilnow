import xml.etree.ElementTree as ET
import requests
from collections import OrderedDict
from oilnow.model.CodeOils import CodeOils
from oilnow.model.OpinetSecretKey import SecretKey


class OpinetApi:
    def __init__(self):
        self.base_url = 'http://www.opinet.co.kr/api/'
        self.api_key = SecretKey.API_KEY

    def get_avg_oil_price(self):
        req_url = self.base_url + 'avgAllPrice.do?out=xml&code=' + self.api_key
        return_xml_tree = ET.fromstring(requests.get(req_url).text)
        oils = return_xml_tree.findall('OIL')
        price_data = OrderedDict()

        for oil in oils:
            code_oil = oil.find('PRODCD').text
            if CodeOils.is_in_enum(code_oil):
                price_data[code_oil] = float(oil.find('PRICE').text)

        return price_data.values()

    def get_station_list_by_name(self, name):
        req_url = self.base_url + 'searchByName.do?out=xml&code=' + self.api_key + '&osnm=' + name
        return_xml_tree = ET.fromstring(requests.get(req_url).text)
        oils = return_xml_tree.findall('OIL')[:5]
        station_data = OrderedDict()

        for oil in oils:
            station_data[oil.find('OS_NM').text] = oil.find('UNI_ID').text

        return station_data

    def get_oil_price_by_station_id(self, station_id, code_oil):
        req_url = self.base_url + 'detailById.do?out=xml&code=' + self.api_key + '&id=' + station_id
        return_xml_tree = ET.fromstring(requests.get(req_url).text)
        prices = return_xml_tree.find('OIL').findall('OIL_PRICE')

        for price in prices:
            if price.find('PRODCD').text == code_oil.value:
                return int(price.find('PRICE').text)

        return 'Error: 해당 주유소에서 판매하지 않는 유종입니다.'

