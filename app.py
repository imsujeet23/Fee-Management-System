import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from controllers.auth_controller import AuthController
from database.database import Database
from ui.login_window import LoginWindow
from ui.dashboard import DashboardWindow


class Application:

    def __init__(self):

        self.app = QApplication(sys.argv)

        self.load_styles()

        db = Database()
        db.create_tables()

        auth = AuthController()
        auth.create_default_admin()

        self.login_window = LoginWindow(self)
        self.dashboard = None

    def load_styles(self):

        style = Path("assets/styles/style.qss")

        if style.exists():
            with open(style, "r") as file:
                self.app.setStyleSheet(file.read())

    def show_login(self):

        if self.dashboard:
            self.dashboard.close()

        self.login_window.clear_fields()
        self.login_window.show()

    def show_dashboard(self):

        self.login_window.hide()

        self.dashboard = DashboardWindow(self)

        self.dashboard.show()

    def run(self):

        self.show_login()

        sys.exit(self.app.exec())