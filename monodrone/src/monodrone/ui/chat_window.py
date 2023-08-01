# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 Multimedia player example"""

import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QGridLayout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.main_layout = QGridLayout()

    def closeEvent(self, event):
        # self._ensure_stopped()
        event.accept()

    def show_status_message(self, message):
        self.statusBar().showMessage(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    available_geometry = main_win.screen().availableGeometry()
    main_win.resize(available_geometry.width() / 3,
                    available_geometry.height() / 2)
    main_win.show()
    sys.exit(app.exec())
