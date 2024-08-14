
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        welcome_label = QLabel("Welcome to the Personal Safety App!")
        layout.addWidget(welcome_label)
        self.setLayout(layout)
