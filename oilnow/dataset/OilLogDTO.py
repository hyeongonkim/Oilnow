# -*- coding:utf-8 -*-

class OilLogDTO:
    def __init__(self, date, station_name, price, amount, price_per_liter, odo):
        self.date = date
        self.station_name = station_name
        self.price = price
        self.amount = amount
        self.price_per_liter = price_per_liter
        self.odo = odo
