from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout


class StatCard(QFrame):
    def __init__(self, title: str, value: str):
        super().__init__()

        self.setObjectName("statCard")
        self.setFixedSize(230, 120)

        layout = QVBoxLayout()

        layout.setContentsMargins(15, 15, 15, 15)

        self.title = QLabel(title)
        self.title.setObjectName("cardTitle")

        self.value = QLabel(value)
        self.value.setObjectName("cardValue")
        self.value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.value)

        self.setLayout(layout)

    def update_value(self, value):
        self.value.setText(str(value))