# -*- coding:utf-8 -*-
import sys

from PyQt5.QtGui import QIntValidator
from oilnow.model.OpinetApi import OpinetApi
from oilnow.dataset.DataManager import DataManager
from PyQt5.QtWidgets import *
from oilnow.ui.CarInfoDialog import CarInfoDialog
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
        btn_h_box.addStretch(1)
        avg_oil_price_btn = QPushButton('전국 평균 유가', self)
        btn_h_box.addWidget(avg_oil_price_btn)
        oil_log_add_btn = QPushButton('주유 기록 추가', self)
        btn_h_box.addWidget(oil_log_add_btn)

        result_title_h_box = QHBoxLayout()
        result_title_h_box.addWidget(QLabel('주유 기록', self))
        result_title_h_box.addStretch(1)
        result_title_h_box.addWidget(QLabel('삭제할 기록 번호:', self))
        self.et_delete_target = QLineEdit()
        self.et_delete_target.setValidator(QIntValidator(1, 1, self))
        # TODO: 기록 불러오면 실시간 갱신
        result_title_h_box.addWidget(self.et_delete_target)
        oil_log_del_btn = QPushButton('삭제', self)
        result_title_h_box.addWidget(oil_log_del_btn)

        result_body_h_box = QHBoxLayout()
        self.result_body = QTextEdit()
        result_body_h_box.addWidget(self.result_body)

        layout_v_box = QVBoxLayout()
        layout_v_box.addLayout(car_info_h_box)
        layout_v_box.addLayout(btn_h_box)
        layout_v_box.addLayout(result_title_h_box)
        layout_v_box.addLayout(result_body_h_box)

        self.setLayout(layout_v_box)
        self.setWindowTitle('Oilnow')
        self.show()

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
        else:
            if forced:
                sys.exit()

    def set_car_info(self):
        if len(self.data_manager.data) == 0:
            self.show_car_register(forced=True)
            return

        self.et_car_name.setText(self.data_manager.data[0].name)
        self.et_car_oil_type.setText(CodeOils.find_kor_name_by_enum(self.data_manager.data[0].oil_type))
        self.et_car_odo.setText(str(self.data_manager.data[0].init_odo))
