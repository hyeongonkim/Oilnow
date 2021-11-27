# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import *
from oilnow.model.CodeOils import CodeOils


class AvgOilPriceDialog(QDialog):
    def __init__(self, opinet_api):
        super().__init__()
        self.opinet_api = opinet_api
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('전국 평균 유가')
        layout = QVBoxLayout()
        layout.addStretch(1)

        for key, value in self.opinet_api.get_avg_oil_price().items():
            temp_h_box = QHBoxLayout()
            temp_h_box.addStretch(1)
            temp_h_box.addWidget(QLabel(CodeOils.find_kor_name_by_enum_value(key), self))
            et_price = QLineEdit()
            et_price.setReadOnly(True)
            et_price.setText(str(value))
            temp_h_box.addWidget(et_price)
            layout.addLayout(temp_h_box)

        sub_layout = QHBoxLayout()
        btn_cancel = QPushButton("닫기")
        btn_cancel.clicked.connect(self.on_cancel_button_clicked)
        sub_layout.addWidget(btn_cancel)
        layout.addLayout(sub_layout)

        layout.addStretch(1)
        self.setLayout(layout)

    def on_cancel_button_clicked(self):
        self.reject()

    def show_dialog(self):
        return super().exec_()
