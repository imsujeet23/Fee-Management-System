from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel


class Sidebar(QWidget):

    page_changed = pyqtSignal(int)
    logout_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setFixedWidth(220)
        self.setObjectName("sidebar")

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        title = QLabel("Fee Manager")
        title.setObjectName("sidebarTitle")

        layout.addWidget(title)
        layout.addSpacing(20)

        self.dashboard_btn = QPushButton("🏠 Dashboard")
        self.student_btn = QPushButton("👨 Students")
        self.fee_btn = QPushButton("💷 Fees")
        self.payment_btn = QPushButton("💳 Payments")
        self.report_btn = QPushButton("📄 Reports")
        self.ml_btn = QPushButton("🤖 Machine Learning")
        self.course_btn = QPushButton("📚 Courses")
        buttons = [
            self.dashboard_btn,
            self.course_btn,
            self.student_btn,
            self.fee_btn,
            self.payment_btn,
            self.report_btn,
            self.ml_btn
        ]

        for button in buttons:
            button.setObjectName("sidebarButton")
            layout.addWidget(button)

        layout.addStretch()

        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.setObjectName("logoutButton")
        layout.addWidget(self.logout_btn)

        self.setLayout(layout)

        self.dashboard_btn.clicked.connect(lambda: self.page_changed.emit(0))
        self.course_btn.clicked.connect(lambda: self.page_changed.emit(1))
        self.student_btn.clicked.connect(lambda: self.page_changed.emit(2))
        self.fee_btn.clicked.connect(lambda: self.page_changed.emit(3))
        self.payment_btn.clicked.connect(lambda: self.page_changed.emit(4))
        self.report_btn.clicked.connect(lambda: self.page_changed.emit(5))
        self.ml_btn.clicked.connect(lambda: self.page_changed.emit(6))

        self.logout_btn.clicked.connect(self.logout_clicked.emit)