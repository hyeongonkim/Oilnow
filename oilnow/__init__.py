# -*- coding:utf-8 -*-

import sys
from oilnow.model.CodeOils import CodeOils
from oilnow.ui.Oilnow import Oilnow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Oilnow()
    sys.exit(app.exec_())
