from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QCheckBox
)

from controllers.auth_controller import AuthController


class LoginWindow(QWidget):

    def __init__(self,app):
        super().__init__()
        self.app = app
        self.auth = AuthController()

        self.setWindowTitle("Smart Fee Management System")
        self.setFixedSize(500, 500)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("SMART FEE MANAGEMENT SYSTEM")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)

        layout.addSpacing(30)

        username_label = QLabel("Username")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")

        password_label = QLabel("Password")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Enter password")

        self.show_password = QCheckBox("Show Password")
        self.show_password.toggled.connect(self.toggle_password)

        login_button = QPushButton("Login")
        exit_button = QPushButton("Exit")

        login_button.clicked.connect(self.login)

        exit_button.clicked.connect(self.close)

        buttons = QHBoxLayout()
        buttons.addWidget(login_button)
        buttons.addWidget(exit_button)

        layout.addWidget(username_label)
        layout.addWidget(self.username)

        layout.addWidget(password_label)
        layout.addWidget(self.password)

        layout.addWidget(self.show_password)

        layout.addSpacing(20)

        layout.addLayout(buttons)

        layout.addStretch()

        self.setLayout(layout)

    def toggle_password(self):

        if self.show_password.isChecked():
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)

        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)

    def login(self):

        username = self.username.text().strip()
        password = self.password.text()

        if username == "" or password == "":
            QMessageBox.warning(
                self,
                "Error",
                "Please enter username and password."
            )
            return

        valid = self.auth.login(username, password)

        if valid:
            self.app.show_dashboard()
            return

        QMessageBox.critical(
            self,
            "Login Failed",
            "Invalid Username or Password."
        )
    def clear_fields(self):

        self.username.clear()
        self.password.clear()
        self.show_password.setChecked(False)