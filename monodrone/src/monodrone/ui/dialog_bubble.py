from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class DialogBubble(QDialog):
    def __init__(self, parent=None, text=""):
        super().__init__(parent)
        # Create widgets
        self.label = QLabel(text)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        # Set dialog layout
        self.setLayout(layout)
