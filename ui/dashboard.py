from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox
)


class DashboardWindow(QWidget):

    def __init__(self, app):
        super().__init__()

        self.app = app

        self.setWindowTitle("Dashboard")

        self.resize(1000, 700)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Smart Fee Management System")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        layout.addSpacing(30)

        layout.addWidget(QLabel("Welcome Admin"))

        layout.addSpacing(20)

        logout = QPushButton("Logout")

        logout.clicked.connect(self.logout)

        layout.addWidget(logout)

        layout.addStretch()

        self.setLayout(layout)

    def logout(self):

        reply = QMessageBox.question(
            self,
            "Logout",
            "Do you really want to logout?"
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.close()

            self.app.show_login()