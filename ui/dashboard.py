from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QMessageBox,
)

from ui.widgets.sidebar import Sidebar
from ui.widgets.topbar import TopBar
from ui.pages.course_page import CoursePage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.student_page import StudentPage
from ui.pages.fee_page import FeePage
from ui.pages.payment_page import PaymentPage
from ui.pages.report_page import ReportPage
from ui.pages.ml_page import MLPage


class DashboardWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.setWindowTitle("Smart Fee Management System")
        self.resize(1400, 850)

        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Right Side
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Top Bar
        self.topbar = TopBar()
        right_layout.addWidget(self.topbar)

        # Stacked Pages
        self.stack = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.student_page = StudentPage()
        self.fee_page = FeePage()
        self.payment_page = PaymentPage()
        self.report_page = ReportPage()
        self.ml_page = MLPage()
        self.course_page = CoursePage()
        self.stack.addWidget(self.dashboard_page)   # 0
        self.stack.addWidget(self.course_page)      # 1
        self.stack.addWidget(self.student_page)     # 2
        self.stack.addWidget(self.fee_page)         # 3
        self.stack.addWidget(self.payment_page)     # 4
        self.stack.addWidget(self.report_page)      # 5
        self.stack.addWidget(self.ml_page)          # 6

        right_layout.addWidget(self.stack)

        main_layout.addLayout(right_layout)

        # Connections
        self.sidebar.page_changed.connect(self.stack.setCurrentIndex)
        self.sidebar.logout_clicked.connect(self.logout)

    def logout(self):

        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?"
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            self.app.show_login()