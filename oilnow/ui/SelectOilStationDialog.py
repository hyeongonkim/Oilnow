# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import *


class SelectOilStationDialog(QDialog):
    def __init__(self, name, opinet_api):
        super().__init__()
        self.search_result = opinet_api.get_station_list_by_name(name)
        self.selected_station_name = str()
        self.selected_station_code = str()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('검색 결과')
        layout = QVBoxLayout()
        layout.addStretch(1)

        if len(self.search_result) == 0:
            layout.addWidget(QLabel('검색 결과가 없습니다.', self))
        else:
            for key, value in self.search_result.items():
                btn_station = QPushButton(key)
                btn_station.clicked.connect(self.on_select_station_clicked)
                layout.addWidget(btn_station)

        layout.addStretch(1)
        sub_layout = QHBoxLayout()
        btn_cancel = QPushButton("닫기")
        btn_cancel.clicked.connect(self.on_cancel_button_clicked)
        sub_layout.addWidget(btn_cancel)
        layout.addLayout(sub_layout)

        layout.addStretch(1)
        self.setLayout(layout)

    def on_select_station_clicked(self):
        sender = self.sender()
        key = sender.text()
        self.selected_station_name = key
        self.selected_station_code = self.search_result[key]
        self.accept()

    def on_cancel_button_clicked(self):
        self.reject()

    def show_dialog(self):
        return super().exec_()
