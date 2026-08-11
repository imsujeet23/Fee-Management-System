from PyQt6.QtWidgets import (
    QWidget,
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
    QMessageBox,
)

from PyQt6.QtCore import QDate

from controllers.student_controller import StudentController


class StudentPage(QWidget):

    def __init__(self):
        super().__init__()

        self.controller = StudentController()

        self.setup_ui()

        # Load initial data
        self.load_registration_number()
        self.load_courses()

    # =========================================================
    # UI SETUP
    # =========================================================

    def setup_ui(self):

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # =====================================================
        # LEFT SIDE - STUDENT FORM
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
        self.dob_input.setDate(QDate(2000, 1, 1))

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
        self.admission_date_input.setDate(QDate.currentDate())

        # =====================================================
        # ADD FIELDS TO FORM
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
        # RIGHT SIDE - STUDENT TABLE
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

        # =====================================================
        # BUTTON CONNECTIONS
        # =====================================================

        self.save_button.clicked.connect(self.save_student)
        self.clear_button.clicked.connect(self.clear_form)

        self.refresh_button.clicked.connect(
            self.load_students
        )

    # =========================================================
    # LOAD REGISTRATION NUMBER
    # =========================================================

    def load_registration_number(self):

        try:

            if hasattr(self.controller, "get_next_registration_number"):

                registration_no = (
                    self.controller.get_next_registration_number()
                )

                self.registration_input.setText(
                    registration_no
                )

            else:

                self.registration_input.setText("STU0001")

        except Exception as e:

            print("Registration number error:", e)

            self.registration_input.setText("STU0001")

    # =========================================================
    # LOAD COURSES
    # =========================================================

    def load_courses(self):

        try:

            courses = self.controller.get_courses()

            print("Courses received:", courses)

            self.course_combo.clear()

            self.course_combo.addItem(
                "Select Course",
                None
            )

            for course in courses:

                # Supports dictionary results
                if isinstance(course, dict):

                    course_id = course.get("course_id")
                    course_name = course.get("course_name")

                # Supports tuple/list results
                else:

                    course_id = course[0]
                    course_name = course[1]

                self.course_combo.addItem(
                    course_name,
                    course_id
                )

            print(
                "Courses loaded into dropdown:",
                self.course_combo.count() - 1
            )

        except Exception as e:

            print("Course loading error:", e)

            QMessageBox.critical(
                self,
                "Course Loading Error",
                f"Unable to load courses:\n{e}"
            )

    # =========================================================
    # SAVE STUDENT
    # =========================================================

    def save_student(self):

        registration_no = (
            self.registration_input.text().strip()
        )

        first_name = (
            self.first_name_input.text().strip()
        )

        last_name = (
            self.last_name_input.text().strip()
        )

        gender = self.gender_combo.currentText()

        dob = self.dob_input.date().toString(
            "yyyy-MM-dd"
        )

        email = (
            self.email_input.text().strip()
        )

        phone = (
            self.phone_input.text().strip()
        )

        address = (
            self.address_input.text().strip()
        )

        # IMPORTANT:
        # Save course NAME because the existing database
        # has a "course" column rather than "course_id".

        course = (
            self.course_combo.currentText()
        )

        semester = (
            self.semester_combo.currentData()
        )

        admission_date = (
            self.admission_date_input.date().toString(
                "yyyy-MM-dd"
            )
        )

        # =====================================================
        # VALIDATION
        # =====================================================

        if not first_name:

            QMessageBox.warning(
                self,
                "Validation Error",
                "Please enter first name."
            )

            self.first_name_input.setFocus()

            return

        if not last_name:

            QMessageBox.warning(
                self,
                "Validation Error",
                "Please enter last name."
            )

            self.last_name_input.setFocus()

            return

        if gender == "Select Gender":

            QMessageBox.warning(
                self,
                "Validation Error",
                "Please select gender."
            )

            return

        if course == "Select Course":

            QMessageBox.warning(
                self,
                "Validation Error",
                "Please select a course."
            )

            return

        if semester is None:

            QMessageBox.warning(
                self,
                "Validation Error",
                "Please select semester."
            )

            return

        # =====================================================
        # SAVE TO DATABASE
        # =====================================================

        try:

            self.controller.add_student(
                registration_no,
                first_name,
                last_name,
                gender,
                dob,
                email,
                phone,
                address,
                course,
                semester,
                admission_date
            )

            QMessageBox.information(
                self,
                "Success",
                f"Student {registration_no} added successfully."
            )

            # Refresh table
            self.load_students()

            # Clear form
            self.clear_form()

        except Exception as e:

            print("Student save error:", e)

            QMessageBox.critical(
                self,
                "Unable to Save Student",
                f"Unable to save student:\n{e}"
            )

    # =========================================================
    # LOAD STUDENTS
    # =========================================================

    def load_students(self):

        try:

            if not hasattr(
                self.controller,
                "get_students"
            ):

                print(
                    "get_students() is not available yet."
                )

                return

            students = self.controller.get_students()

            self.table.setRowCount(0)

            for student in students:

                row = self.table.rowCount()

                self.table.insertRow(row)

                if isinstance(student, dict):

                    student_id = student.get(
                        "student_id", ""
                    )

                    registration_no = student.get(
                        "registration_no", ""
                    )

                    first_name = student.get(
                        "first_name", ""
                    )

                    last_name = student.get(
                        "last_name", ""
                    )

                    course = student.get(
                        "course", ""
                    )

                    semester = student.get(
                        "semester", ""
                    )

                    phone = student.get(
                        "phone", ""
                    )

                else:

                    student_id = student[0]
                    registration_no = student[1]
                    first_name = student[2]
                    last_name = student[3]
                    course = student[8]
                    semester = student[9]
                    phone = student[6]

                self.table.setItem(
                    row,
                    0,
                    QTableWidgetItem(
                        str(student_id)
                    )
                )

                self.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(
                        str(registration_no)
                    )
                )

                self.table.setItem(
                    row,
                    2,
                    QTableWidgetItem(
                        f"{first_name} {last_name}"
                    )
                )

                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        str(course)
                    )
                )

                self.table.setItem(
                    row,
                    4,
                    QTableWidgetItem(
                        f"Semester {semester}"
                    )
                )

                self.table.setItem(
                    row,
                    5,
                    QTableWidgetItem(
                        str(phone)
                    )
                )

                self.table.setItem(
                    row,
                    6,
                    QTableWidgetItem(
                        "View"
                    )
                )

        except Exception as e:

            print("Student loading error:", e)

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        self.first_name_input.clear()
        self.last_name_input.clear()

        self.gender_combo.setCurrentIndex(0)

        self.dob_input.setDate(
            QDate(2000, 1, 1)
        )

        self.email_input.clear()
        self.phone_input.clear()
        self.address_input.clear()

        self.course_combo.setCurrentIndex(0)
        self.semester_combo.setCurrentIndex(0)

        self.admission_date_input.setDate(
            QDate.currentDate()
        )

        self.load_registration_number()

    # =========================================================
    # REFRESH WHEN PAGE OPENS
    # =========================================================

    def showEvent(self, event):

        super().showEvent(event)

        self.load_courses()
        self.load_registration_number()
        self.load_students()