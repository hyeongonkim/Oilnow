# -*- coding:utf-8 -*-

from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from oilnow.ui.SelectOilStationDialog import SelectOilStationDialog


class AddOilLogDialog(QDialog):
    def __init__(self, oil_type, opinet_api):
        super().__init__()
        self.oil_type = oil_type
        self.opinet_api = opinet_api
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('주유 기록 입력')
        layout = QVBoxLayout()
        layout.addStretch(1)

        self.date = QDateTimeEdit()
        self.date.setDate(QDate.currentDate())
        self.date.setDisplayFormat('yyyy-MM-dd')
        self.date.setCalendarPopup(True)
        layout.addWidget(self.date)

        station_h_box = QHBoxLayout()
        station_h_box.addWidget(QLabel('주유소 이름:', self))
        self.et_station = QLineEdit()
        self.et_station.setPlaceholderText('주유소 검색')
        station_h_box.addWidget(self.et_station)
        btn_search = QPushButton("검색")
        btn_search.clicked.connect(self.on_station_search_button_clicked)
        station_h_box.addWidget(btn_search)
        layout.addLayout(station_h_box)

        amount_h_box = QHBoxLayout()
        amount_h_box.addWidget(QLabel('주유량:', self))
        self.et_amount = QLineEdit()
        self.et_amount.setPlaceholderText('주유량 (리터)')
        self.et_amount.setValidator(QDoubleValidator(0, 1000, 3, self))
        amount_h_box.addWidget(self.et_amount)
        btn_to_price = QPushButton("> 주유금액")
        btn_to_price.clicked.connect(self.on_convert_to_price_clicked)
        amount_h_box.addWidget(btn_to_price)
        layout.addLayout(amount_h_box)

        price_h_box = QHBoxLayout()
        price_h_box.addWidget(QLabel('주유금액:', self))
        self.et_price = QLineEdit()
        self.et_price.setPlaceholderText('주유금액 (원)')
        self.et_price.setValidator(QIntValidator(0, 9999999, self))
        price_h_box.addWidget(self.et_price)
        btn_to_amount = QPushButton("> 주유량")
        btn_to_amount.clicked.connect(self.on_convert_to_amount_clicked)
        price_h_box.addWidget(btn_to_amount)
        layout.addLayout(price_h_box)

        price_per_liter_h_box = QHBoxLayout()
        price_per_liter_h_box.addWidget(QLabel('리터당 금액:', self))
        self.et_price_per_liter = QLineEdit()
        self.et_price_per_liter.setPlaceholderText('리터당 금액')
        self.et_price_per_liter.setValidator(QIntValidator(0, 9999, self))
        price_per_liter_h_box.addWidget(self.et_price_per_liter)
        layout.addLayout(price_per_liter_h_box)

        odo_h_box = QHBoxLayout()
        odo_h_box.addWidget(QLabel('누적 주행 거리:', self))
        self.et_odo = QLineEdit()
        self.et_odo.setPlaceholderText('누적 주행 거리')
        self.et_odo.setValidator(QIntValidator(0, 999999, self))
        odo_h_box.addWidget(self.et_odo)
        layout.addLayout(odo_h_box)

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

    def on_convert_to_price_clicked(self):
        if len(self.et_price_per_liter.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '리터당 금액을 입력해주세요.')
            return

        if len(self.et_amount.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '주유량을 입력해주세요.')
            return

        self.et_price.setText(str(int(float(self.et_amount.text()) * float(self.et_price_per_liter.text()))))

    def on_convert_to_amount_clicked(self):
        if len(self.et_price_per_liter.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '리터당 금액을 입력해주세요.')
            return

        if len(self.et_price.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '주유금액을 입력해주세요.')
            return

        self.et_amount.setText(str(round(float(self.et_price.text()) / float(self.et_price_per_liter.text()), 3)))

    def on_station_search_button_clicked(self):
        if len(self.et_station.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '주유소 이름을 입력해주세요.')
            return

        dialog = SelectOilStationDialog(self.et_station.text(), self.opinet_api)
        r = dialog.show_dialog()

        if r:
            self.et_station.setText(dialog.selected_station_name)
            self.et_price_per_liter.setText(str(self.opinet_api.get_oil_price_by_station_id(
                dialog.selected_station_code,
                self.oil_type
            )))

    def on_ok_button_clicked(self):
        if len(self.et_station.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '주유소 이름을 입력해주세요.')
            return

        if len(self.et_amount.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '주유량을 입력해주세요.')
            return

        if len(self.et_price.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '주유금액을 입력해주세요.')
            return

        if len(self.et_price_per_liter.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '리터당 금액을 입력해주세요.')
            return

        if len(self.et_odo.text()) == 0:
            QToolTip.showText(QPoint(self.pos()), '누적 주행 거리를 입력해주세요.')
            return

        self.accept()

    def on_cancel_button_clicked(self):
        self.reject()

    def show_dialog(self):
        return super().exec_()
