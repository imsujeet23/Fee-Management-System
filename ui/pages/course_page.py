"""Course Management page for the dashboard."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from controllers.course_controller import CourseController


class CoursePage(QWidget):
    """Manage courses without coupling the dashboard UI to SQLite."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = CourseController()
        self.selected_course_id: int | None = None
        self.setup_ui()
        self.load_courses()

    def setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = QLabel("Course Management")
        title.setObjectName("titleLabel")
        subtitle = QLabel("Add, update, search, and maintain the courses offered by your institution.")
        subtitle.setStyleSheet("color: #6B7280;")
        root.addWidget(title)
        root.addWidget(subtitle)

        content = QHBoxLayout()
        content.setSpacing(18)
        content.addWidget(self._build_form_group(), 1)
        content.addWidget(self._build_list_group(), 2)
        root.addLayout(content, 1)

    def _build_form_group(self) -> QGroupBox:
        group = QGroupBox("Course Details")
        layout = QVBoxLayout(group)
        form = QFormLayout()
        form.setSpacing(12)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("e.g. CS101")
        self.code_input.setMaxLength(20)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Computer Science")
        self.name_input.setMaxLength(120)

        self.duration_combo = QComboBox()
        self.duration_combo.addItems(["12", "24", "36", "48"])
        self.semester_combo = QComboBox()
        self.semester_combo.addItems(["2", "4", "6", "8"])

        self.fee_input = QLineEdit()
        self.fee_input.setPlaceholderText("e.g. 4500.00")
        self.fee_input.setValidator(QDoubleValidator(0.0, 99_999_999.99, 2, self))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Active", "Inactive"])

        form.addRow("Course Code *", self.code_input)
        form.addRow("Course Name *", self.name_input)
        form.addRow("Duration (Months) *", self.duration_combo)
        form.addRow("Semesters *", self.semester_combo)
        form.addRow("Annual Fee *", self.fee_input)
        form.addRow("Status *", self.status_combo)
        layout.addLayout(form)
        layout.addStretch()

        buttons = QHBoxLayout()
        self.save_button = QPushButton("Save Course")
        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet("background-color: #6B7280;")
        buttons.addWidget(self.save_button)
        buttons.addWidget(self.clear_button)
        layout.addLayout(buttons)

        self.save_button.clicked.connect(self.save_course)
        self.clear_button.clicked.connect(self.clear_form)
        return group

    def _build_list_group(self) -> QGroupBox:
        group = QGroupBox("Course List")
        layout = QVBoxLayout(group)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by code, course name, or status…")
        self.search_input.setClearButtonEnabled(True)
        layout.addWidget(self.search_input)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Code", "Course Name", "Duration", "Semesters", "Annual Fee", "Status"]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(1, 220)
        layout.addWidget(self.table, 1)

        actions = QHBoxLayout()
        self.edit_button = QPushButton("Edit Selected")
        self.delete_button = QPushButton("Delete Selected")
        self.refresh_button = QPushButton("Refresh")
        self.delete_button.setStyleSheet("background-color: #C62828;")
        self.refresh_button.setStyleSheet("background-color: #6B7280;")
        actions.addWidget(self.edit_button)
        actions.addWidget(self.delete_button)
        actions.addStretch()
        actions.addWidget(self.refresh_button)
        layout.addLayout(actions)

        self.search_input.textChanged.connect(self.load_courses)
        self.table.itemDoubleClicked.connect(lambda _item: self.edit_selected_course())
        self.edit_button.clicked.connect(self.edit_selected_course)
        self.delete_button.clicked.connect(self.delete_selected_course)
        self.refresh_button.clicked.connect(self.refresh_courses)
        return group

    def _form_values(self) -> tuple:
        return (
            self.code_input.text(), self.name_input.text(),
            self.duration_combo.currentText(), self.semester_combo.currentText(),
            self.fee_input.text().strip(), self.status_combo.currentText(),
        )

    def save_course(self) -> None:
        code, name, duration, semesters, fee, status = self._form_values()
        if not code.strip() or not name.strip() or not fee:
            self._show_warning("Please complete all fields marked with *.")
            return

        try:
            if self.selected_course_id is None:
                self.controller.add_course(code, name, duration, semesters, fee, status)
                message = "Course added successfully."
            else:
                self.controller.update_course(
                    self.selected_course_id, code, name, duration, semesters, fee, status
                )
                message = "Course updated successfully."
        except ValueError as error:
            self._show_warning(str(error))
            return
        except Exception as error:  # Database failures are kept out of the UI flow.
            self._show_error(f"The course could not be saved.\n\n{error}")
            return

        self.clear_form()
        self.load_courses()
        QMessageBox.information(self, "Course Management", message)

    def load_courses(self, _unused: str | None = None) -> None:
        """Load the current search result into the table."""
        try:
            courses = self.controller.get_courses(self.search_input.text())
        except Exception as error:
            self.table.setRowCount(0)
            self._show_error(f"Courses could not be loaded.\n\n{error}")
            return

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(courses))
        for row, course in enumerate(courses):
            values = (
                course["course_code"], course["course_name"],
                f'{course["duration_months"]} months', str(course["total_semesters"]),
                f'{course["annual_fee"]:,.2f}', course["status"],
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column == 0:
                    item.setData(Qt.ItemDataRole.UserRole, course["course_id"])
                if column in (2, 3, 4, 5):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, column, item)
        self.table.setSortingEnabled(True)

    def refresh_courses(self) -> None:
        self.search_input.clear()
        self.clear_form()
        self.load_courses()

    def clear_form(self) -> None:
        self.selected_course_id = None
        self.code_input.clear()
        self.name_input.clear()
        self.duration_combo.setCurrentIndex(0)
        self.semester_combo.setCurrentIndex(0)
        self.fee_input.clear()
        self.status_combo.setCurrentText("Active")
        self.save_button.setText("Save Course")
        self.table.clearSelection()
        self.code_input.setFocus()

    def _selected_course_id(self) -> int | None:
        row = self.table.currentRow()
        item = self.table.item(row, 0) if row >= 0 else None
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def edit_selected_course(self) -> None:
        course_id = self._selected_course_id()
        if course_id is None:
            self._show_warning("Select a course to edit.")
            return
        try:
            course = self.controller.get_course(course_id)
        except Exception as error:
            self._show_error(f"The selected course could not be loaded.\n\n{error}")
            return
        if course is None:
            self._show_warning("The selected course no longer exists. Refreshing the list.")
            self.load_courses()
            return

        self.selected_course_id = course_id
        self.code_input.setText(course["course_code"])
        self.name_input.setText(course["course_name"])
        self.duration_combo.setCurrentText(str(course["duration_months"]))
        self.semester_combo.setCurrentText(str(course["total_semesters"]))
        self.fee_input.setText(f'{course["annual_fee"]:.2f}')
        self.status_combo.setCurrentText(course["status"])
        self.save_button.setText("Update Course")
        self.code_input.setFocus()

    def delete_selected_course(self) -> None:
        course_id = self._selected_course_id()
        if course_id is None:
            self._show_warning("Select a course to delete.")
            return
        name_item = self.table.item(self.table.currentRow(), 1)
        name = name_item.text() if name_item else "this course"
        answer = QMessageBox.question(
            self, "Delete Course", f'Delete "{name}"? This cannot be undone.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            self.controller.delete_course(course_id)
        except ValueError as error:
            self._show_warning(str(error))
        except Exception as error:
            self._show_error(f"The course could not be deleted.\n\n{error}")
        else:
            self.clear_form()
            self.load_courses()
            QMessageBox.information(self, "Course Management", "Course deleted successfully.")

    def _show_warning(self, message: str) -> None:
        QMessageBox.warning(self, "Course Management", message)

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Course Management", message)
