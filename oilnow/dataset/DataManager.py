# -*- coding:utf-8 -*-

import csv

from PyQt5.QtCore import QDate

from oilnow.dataset.CarInfoDTO import CarInfoDTO
from oilnow.dataset.OilLogDTO import OilLogDTO
from oilnow.model.CodeOils import CodeOils


class DataManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.get_data()

    def get_data(self):
        data = []
        try:
            f = open(self.file_name, 'r', encoding='utf-8')
        except FileNotFoundError:
            return data

        rdr = list(csv.reader(f))
        car_info = rdr.pop(0)
        data.append(CarInfoDTO(car_info[0], CodeOils.find_enum_by_name(car_info[1]), int(car_info[2])))

        for oil_log in rdr:
            data.append(
                OilLogDTO(
                    QDate.fromString(oil_log[0], 'yyyy-MM-dd'),
                    oil_log[1],
                    int(oil_log[2]),
                    float(oil_log[3]),
                    int(oil_log[4]),
                    int(oil_log[5])
                )
            )
        f.close()

        return data

    def put_car_info(self, car_info):
        f = open(self.file_name, 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerow([car_info.name, car_info.oil_type.name, car_info.init_odo])
        f.close()
        self.data = self.get_data()

    def edit_car_info(self, car_info):
        f = open(self.file_name, 'r', encoding='utf-8')
        rdr = list(csv.reader(f))
        f.close()
        rdr[0][0] = car_info.name
        rdr[0][1] = car_info.oil_type.name
        rdr[0][2] = car_info.init_odo
        f = open(self.file_name, 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerows(rdr)
        f.close()
        self.data = self.get_data()

    def put_oil_log(self, oil_log):
        f = open(self.file_name, 'r', encoding='utf-8')
        rdr = list(csv.reader(f))
        rdr.append([
                oil_log.date.toString('yyyy-MM-dd'),
                oil_log.station_name,
                oil_log.price,
                oil_log.amount,
                oil_log.price_per_liter,
                oil_log.odo
            ])
        sorted_rdr = sorted(rdr[1:], key=lambda log: QDate.fromString(log[0], 'yyyy-MM-dd'))
        rdr = [rdr[0]]
        rdr.extend(sorted_rdr)
        f.close()
        f = open(self.file_name, 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerows(rdr)
        f.close()
        self.data = self.get_data()

    def delete_oil_log(self, index):
        f = open(self.file_name, 'r', encoding='utf-8')
        rdr = list(csv.reader(f))
        rdr.pop(index)
        f.close()
        f = open(self.file_name, 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerows(rdr)
        f.close()
        self.data = self.get_data()
