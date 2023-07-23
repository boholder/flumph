from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPaintEvent, QBrush, QMouseEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDialog, QLabel, QWidget


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None, background_image_path: str = ""):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.background_image_path = background_image_path
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event: QPaintEvent) -> None:
        backgnd = QPixmap()
        backgnd.load(self.background_image_path)
        self.setFixedSize(backgnd.size())
        painter = QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), QBrush(backgnd))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        Dialog(self, "haha").show()


class Dialog(QDialog):
    def __init__(self, parent=None, text=""):
        super().__init__(parent)
        # Create widgets
        self.label = QLabel(text)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        # Set dialog layout
        self.setLayout(layout)


def start_main_window():
    app = QApplication([])
    w = MainWindow(background_image_path=r'G:\code\python\flumph\data\test.png')
    w.show()
    return app.exec()


if __name__ == '__main__':
    start_main_window()
