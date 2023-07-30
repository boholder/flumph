from PySide6.QtCore import Qt, QTimer, QCoreApplication
from PySide6.QtGui import QPixmap, QPainter, QPaintEvent, QBrush, QMouseEvent
from PySide6.QtMultimedia import QAudioOutput, QMediaDevices, QMediaPlayer
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from loguru import logger

from monodrone.interface.outer_event_handler import OuterEventHandler
from monodrone.ui.dialog_bubble import DialogBubble

# for simplifying some qt instances' initializing
QCoreApplication.setOrganizationName("boholder")
QCoreApplication.setApplicationName("monodrone")


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None, background_image_path: str = ""):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        self.background_image_path = background_image_path
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.outer_event_handler = OuterEventHandler()

        self.outer_event_timer = QTimer(self)
        self.outer_event_timer.timeout.connect(self.consume_outer_event)
        self.outer_event_timer.start(1000)

        # move the window
        self.moving_counter = 0
        self.moving_flag = False

        # t = QTimer(self)
        # t.timeout.connect(self.auto_move)
        # t.start(100)

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
        # DialogBubble(self, "haha").show()
        # self.play_audio()
        # TODO 两图标渐变
        # https://stackoverflow.com/questions/48472703/how-do-i-make-a-gradient-opacity-in-an-image
        pass

    def play_audio(self):
        device = QMediaDevices.defaultAudioOutput()
        audio_output = QAudioOutput(device, self)
        # player本身还有很多异常处理，参考示例
        # player可以方便
        # https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QMediaPlayer.html#PySide6.QtMultimedia.PySide6.QtMultimedia.QMediaPlayer
        # https://doc.qt.io/qtforpython-6/examples/example_multimedia_player.html
        player = QMediaPlayer()
        player.setAudioOutput(audio_output)
        # https://stackoverflow.com/questions/42168280/qmediaplayer-play-a-sound-loaded-into-memory
        player.setSource(r'../../data/audio.wav')
        player.play()

    def handle_network_reply(self, reply: QNetworkReply):
        reply.deleteLater()
        reply.finished.connect(self.handle_slow_server_response)

    def handle_slow_server_response(self, resp: QNetworkReply):
        DialogBubble(self, str(resp.readAll())).show()

    def consume_outer_event(self):
        if event := self.outer_event_handler.get():
            logger.info(f'qt receive: {event}')
            DialogBubble(self, event).show()


def start_main_window():
    app = QApplication([])
    w = MainWindow(background_image_path=r'../../data/python.png')
    w.show()
    return app.exec()


if __name__ == '__main__':
    start_main_window()
