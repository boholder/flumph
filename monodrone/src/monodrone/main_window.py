from PySide6.QtCore import Qt, QTimer, Signal, QUrl
from PySide6.QtGui import QPixmap, QPainter, QPaintEvent, QBrush, QMouseEvent
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDialog, QLabel, QWidget

from monodrone.outer_event_handler import OuterEventHandler


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None, background_image_path: str = ""):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        self.background_image_path = background_image_path
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.outer_event_handler = OuterEventHandler()

        self.outer_event_timer = QTimer(self)
        a: Signal = self.outer_event_timer.timeout
        self.outer_event_timer.timeout.connect(self.consume_outer_event)
        self.outer_event_timer.start(1000)

        self.network_manager = QNetworkAccessManager(self)

        # move the window
        self.moving_counter = 0
        self.moving_flag = False
        t = QTimer(self)
        t.timeout.connect(self.auto_move)
        t.start(100)

    def auto_move(self):
        geo = self.geometry()
        self.moving_counter += 1
        if self.moving_counter % 30 > 15:
            self.moving_flag = True
        else:
            self.moving_flag = False

        if self.moving_flag:
            self.setGeometry(geo.x() - 10, geo.y(), geo.width(), geo.height())
        else:
            self.setGeometry(geo.x() + 10, geo.y(), geo.width(), geo.height())

    def paintEvent(self, event: QPaintEvent) -> None:
        backgnd = QPixmap()
        backgnd.load(self.background_image_path)
        self.setFixedSize(backgnd.size())
        painter = QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), QBrush(backgnd))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        # Dialog(self, "haha").show()
        request = QNetworkRequest(QUrl('http://localhost:1415'))
        self.network_manager.post(request, 'from monodrone: hi!'.encode('utf-8'))
        self.network_manager.finished.connect(self.handle_slow_server_response)

    def handle_network_reply(self, reply: QNetworkReply):
        reply.deleteLater()
        reply.finished.connect(self.handle_slow_server_response)

    def handle_slow_server_response(self, resp: QNetworkReply):
        Dialog(self, str(resp.readAll())).show()

    def consume_outer_event(self):
        if event := self.outer_event_handler.get():
            print(f'qt receive: {event}')
            Dialog(self, event).show()


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
