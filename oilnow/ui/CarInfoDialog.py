# -*- coding:utf-8 -*-

from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from oilnow.model.CodeOils import CodeOils


class CarInfoDialog(QDialog):
    def __init__(self, pre_car_info=None):
        super().__init__()
        self.init_ui()

        if pre_car_info is not None:
            self.et_car_name.setText(pre_car_info.name)
            self.cb_car_oil_type.setCurrentText(CodeOils.find_kor_name_by_enum(pre_car_info.oil_type))
            self.et_car_odo.setText(str(pre_car_info.init_odo))

    def init_ui(self):
        self.setWindowTitle('차량 정보 입력')
        layout = QVBoxLayout()
        layout.addStretch(1)

        self.et_car_name = QLineEdit()
        self.et_car_name.setPlaceholderText('차량 이름을 입력하세요.')
        layout.addWidget(self.et_car_name)

        self.cb_car_oil_type = QComboBox(self)
        self.cb_car_oil_type.addItem('고급휘발유')
        self.cb_car_oil_type.addItem('휘발유')
        self.cb_car_oil_type.addItem('경유')
        self.cb_car_oil_type.addItem('LPG')
        layout.addWidget(self.cb_car_oil_type)

        self.et_car_odo = QLineEdit()
        self.et_car_odo.setPlaceholderText('차량 누적 주행거리를 입력하세요.')
        self.et_car_odo.setValidator(QIntValidator(0, 9999999, self))
        layout.addWidget(self.et_car_odo)

        sub_layout = QHBoxLayout()
        btn_ok = QPushButton("확인")
        btn_ok.clicked.connect(self.on_ok_button_clicked)
        btn_cancel = QPushButton("취소")
        btn_cancel.clicked.connect(self.on_cancel_button_clicked)
        sub_layout.addWidget(btn_ok)
        sub_layout.addWidget(btn_cancel)
        layout.addLayout(sub_layout)

        layout.addStretch(1)
        self.setLayout(layout)

    def on_ok_button_clicked(self):
        if len(self.et_car_name.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '차량 이름을 입력해주세요.')
            return

        if len(self.et_car_odo.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '차량 누적 주행 거리를 입력해주세요.')
            return

        self.accept()

    def on_cancel_button_clicked(self):
        self.reject()

    def show_dialog(self):
        return super().exec_()
