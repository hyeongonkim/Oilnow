# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIntValidator
from oilnow.model.OpinetApi import OpinetApi
from oilnow.dataset.DataManager import DataManager
from PyQt5.QtWidgets import *
from oilnow.ui.CarInfoDialog import CarInfoDialog
from oilnow.ui.AvgOilPriceDialog import AvgOilPriceDialog
from oilnow.ui.AddOilLogDialog import AddOilLogDialog
from oilnow.model.CodeOils import CodeOils
from oilnow.dataset.CarInfoDTO import CarInfoDTO
from oilnow.dataset.OilLogDTO import OilLogDTO


class Oilnow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.data_manager = DataManager('data_oilnow.csv')
        self.opinet_api = OpinetApi()
        self.set_car_info()
        self.set_oil_log()

    def init_ui(self):
        car_info_h_box = QHBoxLayout()
        car_info_h_box.addWidget(QLabel('차량 이름:', self))
        self.et_car_name = QLineEdit()
        self.et_car_name.setReadOnly(True)
        car_info_h_box.addWidget(self.et_car_name)
        car_info_h_box.addWidget(QLabel('유종:', self))
        self.et_car_oil_type = QLineEdit()
        self.et_car_oil_type.setReadOnly(True)
        car_info_h_box.addWidget(self.et_car_oil_type)
        car_info_h_box.addWidget(QLabel('등록시 주행 거리:', self))
        self.et_car_odo = QLineEdit()
        self.et_car_odo.setReadOnly(True)
        car_info_h_box.addWidget(self.et_car_odo)
        car_info_edit_btn = QPushButton('수정', self)
        car_info_edit_btn.clicked.connect(self.show_car_edit)
        car_info_h_box.addWidget(car_info_edit_btn)
        car_info_change_btn = QPushButton('차량 변경', self)
        car_info_change_btn.clicked.connect(self.show_car_register)
        car_info_h_box.addWidget(car_info_change_btn)

        btn_h_box = QHBoxLayout()
        btn_h_box.addWidget(QLabel('평균 연비:', self))
        self.et_total_fuel_efficiency = QLineEdit()
        self.et_total_fuel_efficiency.setReadOnly(True)
        btn_h_box.addWidget(self.et_total_fuel_efficiency)
        btn_h_box.addStretch(1)
        avg_oil_price_btn = QPushButton('전국 평균 유가', self)
        avg_oil_price_btn.clicked.connect(self.show_avg_price_dialog)
        btn_h_box.addWidget(avg_oil_price_btn)
        oil_log_add_btn = QPushButton('주유 기록 추가', self)
        oil_log_add_btn.clicked.connect(self.show_add_oil_log_dialog)
        btn_h_box.addWidget(oil_log_add_btn)

        result_title_h_box = QHBoxLayout()
        result_title_h_box.addWidget(QLabel('주유 기록', self))
        result_title_h_box.addStretch(1)
        result_title_h_box.addWidget(QLabel('삭제할 기록 번호:', self))
        self.et_delete_target = QLineEdit()
        self.et_delete_target.setValidator(QIntValidator(1, 1, self))
        result_title_h_box.addWidget(self.et_delete_target)
        oil_log_del_btn = QPushButton('삭제', self)
        oil_log_del_btn.clicked.connect(self.delete_oil_log)
        result_title_h_box.addWidget(oil_log_del_btn)

        result_body_h_box = QHBoxLayout()
        self.result_body = QTextEdit()
        self.result_body.setReadOnly(True)
        result_body_h_box.addWidget(self.result_body)

        layout_v_box = QVBoxLayout()
        layout_v_box.addLayout(car_info_h_box)
        layout_v_box.addLayout(btn_h_box)
        layout_v_box.addLayout(result_title_h_box)
        layout_v_box.addLayout(result_body_h_box)

        self.setLayout(layout_v_box)
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('Oilnow: 당신의 주유 차계부')
        self.show()

    def set_car_info(self):
        if len(self.data_manager.data) == 0:
            self.show_car_register(forced=True)
            return

        self.et_car_name.setText(self.data_manager.data[0].name)
        self.et_car_oil_type.setText(CodeOils.find_kor_name_by_enum(self.data_manager.data[0].oil_type))
        self.et_car_odo.setText(str(self.data_manager.data[0].init_odo))

    def set_oil_log(self):
        output_data = ""
        oil_logs = self.data_manager.data[1:]
        self.et_delete_target.setValidator(QIntValidator(1, len(oil_logs), self))
        last_odo = self.data_manager.data[0].init_odo
        total_amount = 0.0
        for i, oil_log in enumerate(oil_logs):
            str_format = '번호={:<4d}\t날짜={:<12}\t{:　<25}\t주유금액={:<10d}\t주유량={:<10.3f}\t리터당 금액={:<10d}\t구간 연비={:.3f}\n'
            output_data = output_data + str_format.format(i + 1,
                                                      oil_log.date.toString('yyyy-MM-dd'),
                                                      oil_log.station_name,
                                                      oil_log.price,
                                                      oil_log.amount,
                                                      oil_log.price_per_liter,
                                                      (oil_log.odo - last_odo) / oil_log.amount)
            last_odo = oil_log.odo
            total_amount += oil_log.amount

        self.result_body.setText(output_data)
        if total_amount > 0:
            self.et_total_fuel_efficiency.setText(str(round((last_odo - self.data_manager.data[0].init_odo) / total_amount, 3)))
        else:
            self.et_total_fuel_efficiency.clear()
        self.result_body.repaint()

    def show_car_edit(self):
        dialog = CarInfoDialog(self.data_manager.data[0])
        r = dialog.show_dialog()

        if r:
            self.data_manager.edit_car_info(
                CarInfoDTO(
                    dialog.et_car_name.text(),
                    CodeOils.find_enum_by_kor_name(dialog.cb_car_oil_type.currentText()),
                    int(dialog.et_car_odo.text())
                )
            )
            self.set_car_info()

    def show_car_register(self, forced=False):
        dialog = CarInfoDialog()
        r = dialog.show_dialog()

        if r:
            self.data_manager.put_car_info(
                CarInfoDTO(
                    dialog.et_car_name.text(),
                    CodeOils.find_enum_by_kor_name(dialog.cb_car_oil_type.currentText()),
                    int(dialog.et_car_odo.text())
                )
            )
            self.set_car_info()
            self.set_oil_log()
        else:
            if forced:
                sys.exit()

    def show_avg_price_dialog(self):
        dialog = AvgOilPriceDialog(self.opinet_api)
        dialog.show_dialog()

    def show_add_oil_log_dialog(self):
        dialog = AddOilLogDialog(self.data_manager.data[0].oil_type, self.opinet_api)
        r = dialog.show_dialog()

        if r:
            self.data_manager.put_oil_log(
                OilLogDTO(
                    dialog.date.date(),
                    dialog.et_station.text(),
                    int(dialog.et_price.text()),
                    float(dialog.et_amount.text()),
                    int(dialog.et_price_per_liter.text()),
                    int(dialog.et_odo.text())
                )
            )
            self.set_oil_log()

    def delete_oil_log(self):
        if len(self.et_delete_target.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '삭제할 번호를 입력해주세요.')
            return

        index = int(self.et_delete_target.text())

        if 1 <= index <= (len(self.data_manager.data) - 1):
            self.et_delete_target.clear()
            self.data_manager.delete_oil_log(index)
            self.set_oil_log()
        else:
            QToolTip.showText(QPoint(self.pos()), '삭제할 번호를 정확히 입력해주세요.')
            return
