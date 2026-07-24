from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout


class TopBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("topbar")
        self.setFixedHeight(70)

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)

        # Title
        self.title = QLabel("Smart Fee Management System")
        self.title.setObjectName("topbarTitle")

        # Spacer
        layout.addWidget(self.title)
        layout.addStretch()

        # Date
        self.date_label = QLabel(datetime.now().strftime("%d %b %Y"))
        self.date_label.setObjectName("dateLabel")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # User
        self.user_label = QLabel("Admin")
        self.user_label.setObjectName("userLabel")

        layout.addWidget(self.date_label)
        layout.addSpacing(15)
        layout.addWidget(self.user_label)

        self.setLayout(layout)