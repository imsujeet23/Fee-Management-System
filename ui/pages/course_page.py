from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class CoursePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Course Management")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#1565C0;
        """)

        layout.addWidget(title)
        layout.addStretch()

        self.setLayout(layout)