from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from controllers.student_controller import StudentController
from PyQt6.QtWidgets import QMessageBox

class StudentPage(QWidget):

    def __init__(self):
        super().__init__()

        self.controller = StudentController()

        self.setup_ui()

        self.load_registration_number()
        self.load_courses()

    def setup_ui(self):

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # =====================================================
        # LEFT PANEL - STUDENT FORM
        # =====================================================

        form_group = QGroupBox("Student Registration")

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        # Registration Number
        self.registration_input = QLineEdit()
        self.registration_input.setReadOnly(True)
        self.registration_input.setPlaceholderText("Auto generated")

        # First Name
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter first name")

        # Last Name
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter last name")

        # Gender
        self.gender_combo = QComboBox()
        self.gender_combo.addItems([
            "Select Gender",
            "Male",
            "Female",
            "Other"
        ])

        # Date of Birth
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("dd-MM-yyyy")

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@email.com")

        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")

        # Address
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter address")

        # Course
        self.course_combo = QComboBox()
        self.course_combo.addItem("Select Course", None)

        # Semester
        self.semester_combo = QComboBox()
        self.semester_combo.addItem("Select Semester", None)

        for semester in range(1, 9):
            self.semester_combo.addItem(
                f"Semester {semester}",
                semester
            )

        # Admission Date
        self.admission_date_input = QDateEdit()
        self.admission_date_input.setCalendarPopup(True)
        self.admission_date_input.setDisplayFormat("dd-MM-yyyy")
        self.admission_date_input.setDate(
            self.admission_date_input.date()
        )

        # =====================================================
        # FORM
        # =====================================================

        form_layout.addRow(
            "Registration No.",
            self.registration_input
        )

        form_layout.addRow(
            "First Name",
            self.first_name_input
        )

        form_layout.addRow(
            "Last Name",
            self.last_name_input
        )

        form_layout.addRow(
            "Gender",
            self.gender_combo
        )

        form_layout.addRow(
            "Date of Birth",
            self.dob_input
        )

        form_layout.addRow(
            "Email",
            self.email_input
        )

        form_layout.addRow(
            "Phone",
            self.phone_input
        )

        form_layout.addRow(
            "Address",
            self.address_input
        )

        form_layout.addRow(
            "Course",
            self.course_combo
        )

        form_layout.addRow(
            "Semester",
            self.semester_combo
        )

        form_layout.addRow(
            "Admission Date",
            self.admission_date_input
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        self.save_button = QPushButton("Save Student")
        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")
        self.clear_button = QPushButton("Clear")

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.update_button)

        second_button_layout = QHBoxLayout()

        second_button_layout.addWidget(self.delete_button)
        second_button_layout.addWidget(self.clear_button)

        left_layout = QVBoxLayout()

        left_layout.addLayout(form_layout)
        left_layout.addSpacing(15)
        left_layout.addLayout(button_layout)
        left_layout.addLayout(second_button_layout)
        left_layout.addStretch()

        form_group.setLayout(left_layout)

        # =====================================================
        # RIGHT PANEL - STUDENT TABLE
        # =====================================================

        table_group = QGroupBox("Student List")

        table_layout = QVBoxLayout()

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by registration number, name, course or phone..."
        )

        table_layout.addWidget(self.search_input)

        # Table
        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Registration No.",
            "Name",
            "Course",
            "Semester",
            "Phone",
            "Actions"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        table_layout.addWidget(self.table)

        # Refresh
        self.refresh_button = QPushButton("Refresh")

        table_layout.addWidget(self.refresh_button)

        table_group.setLayout(table_layout)

        # =====================================================
        # FINAL LAYOUT
        # =====================================================

        main_layout.addWidget(form_group, 1)
        main_layout.addWidget(table_group, 2)
    def load_registration_number(self):

        try:
            registration_no = self.controller.registration_number()

            self.registration_input.setText(
                registration_no
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to generate registration number:\n{e}"
            )

    def load_courses(self):

        try:
            courses = self.controller.get_courses()

            self.course_combo.clear()

            self.course_combo.addItem(
                "Select Course",
                None
            )

            for course in courses:

                self.course_combo.addItem(
                    course["course_name"],
                    course["course_id"]
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Unable to load courses:\n{e}"
            )