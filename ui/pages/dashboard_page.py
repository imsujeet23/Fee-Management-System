from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QGridLayout
from ui.widgets.stat_card import StatCard


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        layout.setSpacing(20)

        self.students = StatCard("Students", "0")
        self.fees = StatCard("Fees Collected", "£0")
        self.pending = StatCard("Pending Fees", "£0")
        self.today = StatCard("Today's Collection", "£0")

        layout.addWidget(self.students, 0, 0)
        layout.addWidget(self.fees, 0, 1)
        layout.addWidget(self.pending, 1, 0)
        layout.addWidget(self.today, 1, 1)

        layout.setContentsMargins(30, 30, 30, 30)

        self.setLayout(layout)