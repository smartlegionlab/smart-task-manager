# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
import uuid
from datetime import datetime
from typing import Optional, List

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox,
    QLineEdit, QDialog, QTableWidget, QTableWidgetItem, QFrame,
    QHeaderView, QHBoxLayout, QGroupBox, QTextEdit, QDateEdit, QComboBox,
    QMenu, QAction, QGridLayout, QCheckBox, QRadioButton, QButtonGroup, QDesktopWidget
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate

from core.task import Task
from core.task_manager import TaskManager


class TaskInputDialog(QDialog):
    def __init__(self, parent=None, task: Optional[Task] = None):
        super().__init__(parent)
        self.is_edit_mode = task is not None
        self.task = task
        self.setWindowTitle('Edit Task' if self.is_edit_mode else 'Create New Task')
        self.setMinimumWidth(500)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        title_group = QGroupBox("Task Title")
        title_layout = QVBoxLayout()
        self.title_label = QLabel('Task Title:')
        title_layout.addWidget(self.title_label)
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Enter task title")
        if task:
            self.title_input.setText(task.title)
        title_layout.addWidget(self.title_input)
        title_group.setLayout(title_layout)
        self.layout.addWidget(title_group)

        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout()
        self.desc_label = QLabel('Task Description:')
        desc_layout.addWidget(self.desc_label)
        self.desc_input = QTextEdit(self)
        self.desc_input.setPlaceholderText("Enter task description")
        if task:
            self.desc_input.setText(task.description)
        desc_layout.addWidget(self.desc_input)
        desc_group.setLayout(desc_layout)
        self.layout.addWidget(desc_group)

        settings_group = QGroupBox("Task Settings")
        settings_layout = QHBoxLayout()

        priority_layout = QVBoxLayout()
        self.priority_label = QLabel('Priority:')
        priority_layout.addWidget(self.priority_label)
        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems(["High", "Medium", "Low"])
        if task:
            self.priority_combo.setCurrentIndex(task.priority - 1)
        priority_layout.addWidget(self.priority_combo)
        settings_layout.addLayout(priority_layout)

        settings_layout.addSpacing(20)

        due_layout = QVBoxLayout()
        self.due_label = QLabel('Due Date:')
        due_layout.addWidget(self.due_label)
        self.due_input = QDateEdit(self)
        self.due_input.setCalendarPopup(True)
        self.due_input.setDate(QDate.currentDate().addDays(7))
        if task and task.due_date:
            self.due_input.setDate(QDate.fromString(task.due_date, Qt.ISODate))
        due_layout.addWidget(self.due_input)
        settings_layout.addLayout(due_layout)

        settings_layout.addStretch()
        settings_group.setLayout(settings_layout)
        self.layout.addWidget(settings_group)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        button_text = 'Update Task' if self.is_edit_mode else 'Create Task'
        self.submit_button = QPushButton(button_text, self)
        self.submit_button.setDefault(True)
        self.submit_button.clicked.connect(self.accept)
        self.submit_button.setStyleSheet("background-color: #2a82da; color: white;")
        button_layout.addWidget(self.submit_button)
        self.layout.addLayout(button_layout)

    def get_inputs(self):
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        return {
            "title": self.title_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
            "priority": priority_map[self.priority_combo.currentText()],
            "due_date": self.due_input.date().toString(Qt.ISODate)
        }


class TaskDisplayDialog(QDialog):
    def __init__(self, parent=None, task: Task = None, on_edit_callback=None):
        super().__init__(parent)
        self.task = task
        self.on_edit_callback = on_edit_callback
        self.setWindowTitle(f'Task: {task.title}')
        self.setMinimumWidth(500)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        info_group = QGroupBox("Task Details")
        info_layout = QVBoxLayout()

        title_label = QLabel(f'<h3>{task.title}</h3>')
        info_layout.addWidget(title_label)

        if task.description:
            desc_label = QLabel(task.description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("padding: 10px; background-color: #2a2a2a; border-radius: 5px;")
            info_layout.addWidget(desc_label)

        meta_layout = QHBoxLayout()

        priority_text = ["🚨 High", "⚠️ Medium", "📋 Low"][task.priority - 1]
        priority_label = QLabel(f'<b>Priority:</b> {priority_text}')
        meta_layout.addWidget(priority_label)

        meta_layout.addStretch()

        status_text = "✅ Completed" if task.completed else "⏳ Pending"
        status_label = QLabel(f'<b>Status:</b> {status_text}')
        meta_layout.addWidget(status_label)

        info_layout.addLayout(meta_layout)

        dates_layout = QHBoxLayout()
        created_label = QLabel(f'<b>Created:</b> {task.created_at[:10]}')
        dates_layout.addWidget(created_label)

        dates_layout.addStretch()

        if task.due_date:
            due_label = QLabel(f'<b>Due:</b> {task.due_date}')
            dates_layout.addWidget(due_label)

        info_layout.addLayout(dates_layout)

        info_group.setLayout(info_layout)
        self.layout.addWidget(info_group)

        button_layout = QHBoxLayout()

        self.edit_button = QPushButton('✏️ Edit Task', self)
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        self.edit_button.clicked.connect(self.edit_task)
        button_layout.addWidget(self.edit_button)

        button_layout.addStretch()

        self.close_button = QPushButton('Close', self)
        self.close_button.setDefault(True)
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)

        self.layout.addLayout(button_layout)

    def edit_task(self):
        if self.on_edit_callback:
            self.on_edit_callback(self.task)
        self.accept()


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Smart Task Manager v1.1.0')
        self.resize(1000, 700)

        self.todo_manager = TaskManager()
        self.all_tasks: List[Task] = []

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        self.label_logo = QLabel('Smart Task Manager <sup>v1.1.0</sup>')
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_logo.setFont(font)
        self.label_logo.setStyleSheet("color: #2a82da;")
        header_layout.addWidget(self.label_logo)

        header_layout.addStretch()

        self.stats_label = QLabel("0 tasks")
        self.stats_label.setStyleSheet("color: #888;")
        header_layout.addWidget(self.stats_label)

        self.main_layout.addLayout(header_layout)

        search_group = QGroupBox("Search & Filter")
        search_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        search_layout = QGridLayout()
        search_layout.setSpacing(10)

        self.search_label = QLabel('🔍 Search:')
        search_layout.addWidget(self.search_label, 0, 0)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search in title and description...")
        self.search_input.textChanged.connect(self.apply_filters)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #2a2a2a;
                color: white;
            }
            QLineEdit:focus {
                border: 1px solid #2a82da;
            }
        """)
        search_layout.addWidget(self.search_input, 0, 1, 1, 3)

        self.status_label = QLabel('Status:')
        search_layout.addWidget(self.status_label, 1, 0)

        self.status_all_radio = QRadioButton("All")
        self.status_all_radio.setChecked(True)
        self.status_pending_radio = QRadioButton("⏳ Pending")
        self.status_completed_radio = QRadioButton("✅ Completed")

        self.status_group = QButtonGroup(self)
        self.status_group.addButton(self.status_all_radio)
        self.status_group.addButton(self.status_pending_radio)
        self.status_group.addButton(self.status_completed_radio)

        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_all_radio)
        status_layout.addWidget(self.status_pending_radio)
        status_layout.addWidget(self.status_completed_radio)
        status_layout.addStretch()

        search_layout.addLayout(status_layout, 1, 1, 1, 3)

        self.priority_label = QLabel('Priority:')
        search_layout.addWidget(self.priority_label, 2, 0)

        self.priority_high_check = QCheckBox("🚨 High")
        self.priority_medium_check = QCheckBox("⚠️ Medium")
        self.priority_low_check = QCheckBox("📋 Low")

        self.priority_high_check.setChecked(True)
        self.priority_medium_check.setChecked(True)
        self.priority_low_check.setChecked(True)

        priority_layout = QHBoxLayout()
        priority_layout.addWidget(self.priority_high_check)
        priority_layout.addWidget(self.priority_medium_check)
        priority_layout.addWidget(self.priority_low_check)
        priority_layout.addStretch()

        search_layout.addLayout(priority_layout, 2, 1, 1, 3)

        self.date_label = QLabel('Due Date:')
        search_layout.addWidget(self.date_label, 3, 0)

        self.date_all_radio = QRadioButton("All")
        self.date_all_radio.setChecked(True)
        self.date_overdue_radio = QRadioButton("Overdue")
        self.date_today_radio = QRadioButton("Today")
        self.date_future_radio = QRadioButton("Future")

        self.date_group = QButtonGroup(self)
        self.date_group.addButton(self.date_all_radio)
        self.date_group.addButton(self.date_overdue_radio)
        self.date_group.addButton(self.date_today_radio)
        self.date_group.addButton(self.date_future_radio)

        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_all_radio)
        date_layout.addWidget(self.date_overdue_radio)
        date_layout.addWidget(self.date_today_radio)
        date_layout.addWidget(self.date_future_radio)
        date_layout.addStretch()

        search_layout.addLayout(date_layout, 3, 1, 1, 3)

        self.reset_filters_btn = QPushButton("Reset Filters")
        self.reset_filters_btn.clicked.connect(self.reset_filters)
        self.reset_filters_btn.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        search_layout.addWidget(self.reset_filters_btn, 4, 3)

        self.status_all_radio.toggled.connect(self.apply_filters)
        self.status_pending_radio.toggled.connect(self.apply_filters)
        self.status_completed_radio.toggled.connect(self.apply_filters)

        self.priority_high_check.stateChanged.connect(self.apply_filters)
        self.priority_medium_check.stateChanged.connect(self.apply_filters)
        self.priority_low_check.stateChanged.connect(self.apply_filters)

        self.date_all_radio.toggled.connect(self.apply_filters)
        self.date_overdue_radio.toggled.connect(self.apply_filters)
        self.date_today_radio.toggled.connect(self.apply_filters)
        self.date_future_radio.toggled.connect(self.apply_filters)

        search_group.setLayout(search_layout)
        self.main_layout.addWidget(search_group)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            ['Title', 'Priority', 'Status', 'Due Date', 'View', 'Edit', 'Delete'])
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #2a2a2a;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #353535;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
        """)

        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table_widget.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)

        self.main_layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.btn_new_task = QPushButton('+ Add Task')
        self.btn_new_task.setMinimumHeight(40)
        self.btn_new_task.clicked.connect(self.add_task)
        self.btn_new_task.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        button_layout.addWidget(self.btn_new_task)

        self.btn_clear_completed = QPushButton('Clear Completed')
        self.btn_clear_completed.setMinimumHeight(40)
        self.btn_clear_completed.clicked.connect(self.clear_completed)
        button_layout.addWidget(self.btn_clear_completed)

        button_layout.addStretch()

        self.btn_help = QPushButton('? Help')
        self.btn_help.setMinimumHeight(40)
        self.btn_help.clicked.connect(self.show_help)
        button_layout.addWidget(self.btn_help)

        self.btn_exit = QPushButton('Exit')
        self.btn_exit.setMinimumHeight(40)
        self.btn_exit.clicked.connect(self.close)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #ff7d7d;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #ca1a1a;
            }
        """)
        button_layout.addWidget(self.btn_exit)

        self.main_layout.addLayout(button_layout)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setStyleSheet("color: #444;")
        self.main_layout.addWidget(self.line)

        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(5)

        copyright_text = 'Copyright © 2025, <a href="https://github.com/smartlegionlab" style="color: #2a82da; text-decoration: none;">Alexander Suvorov</a>. All rights reserved.'
        self.copyright_label = QLabel(copyright_text)
        self.copyright_label.setAlignment(Qt.AlignCenter)
        self.copyright_label.setStyleSheet("color: #888; font-size: 16px;")
        self.copyright_label.setOpenExternalLinks(True)
        footer_layout.addWidget(self.copyright_label)

        self.main_layout.addLayout(footer_layout)

        self.setLayout(self.main_layout)
        self._init()
        self.center_window()

    def _init(self):
        self.all_tasks = list(self.todo_manager.tasks.values())
        self.update_stats()
        self.apply_filters()

    def center_window(self):
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def update_stats(self):
        total = len(self.all_tasks)
        completed = sum(1 for task in self.all_tasks if task.completed)
        pending = total - completed
        self.stats_label.setText(f"{total} tasks ({completed} completed, {pending} pending)")

    def add_item(self, task: Task):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        title_item = QTableWidgetItem(task.title)
        title_item.setToolTip(task.description)
        if task.completed:
            title_item.setForeground(QColor(100, 100, 100))
            font = title_item.font()
            font.setStrikeOut(True)
            title_item.setFont(font)
        self.table_widget.setItem(row_position, 0, title_item)

        priority_text = ["🚨 High", "⚠️ Medium", "📋 Low"][task.priority - 1]
        priority_label = QLabel(priority_text)
        priority_label.setAlignment(Qt.AlignCenter)
        if task.priority == 1:
            priority_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        elif task.priority == 2:
            priority_label.setStyleSheet("color: #ffd166; font-weight: bold;")
        else:
            priority_label.setStyleSheet("color: #8ac926; font-weight: bold;")

        priority_widget = QWidget()
        priority_layout = QHBoxLayout(priority_widget)
        priority_layout.addWidget(priority_label)
        priority_layout.setAlignment(Qt.AlignCenter)
        priority_layout.setContentsMargins(0, 0, 0, 0)
        priority_widget.setLayout(priority_layout)

        self.table_widget.setCellWidget(row_position, 1, priority_widget)

        status_button = QPushButton("✅ Completed" if task.completed else "⏳ Pending")
        status_button.setCheckable(True)
        status_button.setChecked(task.completed)
        status_button.setStyleSheet("""
            QPushButton {
                border-radius: 3px;
                padding: 5px 10px;
                min-width: 100px;
            }
            QPushButton:checked {
                background-color: #2e7d32;
                color: white;
            }
            QPushButton:!checked {
                background-color: #ff9800;
                color: white;
            }
        """)
        status_button.clicked.connect(lambda checked, t_id=task.id: self.toggle_task_status_by_id(t_id))
        status_button.task_id = task.id
        self.table_widget.setCellWidget(row_position, 2, status_button)

        due_text = task.due_date if task.due_date else "No due date"
        due_item = QTableWidgetItem(due_text)
        due_item.setTextAlignment(Qt.AlignCenter)

        if task.due_date and not task.completed:
            due_date = datetime.fromisoformat(task.due_date).date()
            if due_date < datetime.now().date():
                due_item.setForeground(QColor(255, 100, 100))

        self.table_widget.setItem(row_position, 3, due_item)

        view_button = QPushButton("👁 View")
        view_button.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                border-radius: 3px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        view_button.clicked.connect(lambda checked, t_id=task.id: self.view_task_by_id(t_id))
        view_button.task_id = task.id
        self.table_widget.setCellWidget(row_position, 4, view_button)

        edit_button = QPushButton("✏️ Edit")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border-radius: 3px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        edit_button.clicked.connect(lambda checked, t_id=task.id: self.edit_task_by_id(t_id))
        edit_button.task_id = task.id
        self.table_widget.setCellWidget(row_position, 5, edit_button)

        delete_button = QPushButton("Delete")
        delete_button.setToolTip("Delete this task")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #da2a2a;
                color: white;
                border-radius: 3px;
                padding: 5px;
                min-width: 60px;
                max-width: 60px;
            }
            QPushButton:hover {
                background-color: #ca1a1a;
            }
        """)
        delete_button.clicked.connect(lambda checked, t_id=task.id: self.delete_task_by_id(t_id))
        delete_button.task_id = task.id
        self.table_widget.setCellWidget(row_position, 6, delete_button)

    def apply_filters(self):
        search_text = self.search_input.text().lower()

        if self.status_pending_radio.isChecked():
            status_filter = "pending"
        elif self.status_completed_radio.isChecked():
            status_filter = "completed"
        else:
            status_filter = "all"

        selected_priorities = []
        if self.priority_high_check.isChecked():
            selected_priorities.append(1)
        if self.priority_medium_check.isChecked():
            selected_priorities.append(2)
        if self.priority_low_check.isChecked():
            selected_priorities.append(3)

        today = datetime.now().date()

        filtered_tasks = []
        for task in self.all_tasks:
            if search_text:
                if (search_text not in task.title.lower() and
                        search_text not in task.description.lower()):
                    continue

            if status_filter == "pending" and task.completed:
                continue
            if status_filter == "completed" and not task.completed:
                continue

            if task.priority not in selected_priorities:
                continue

            if task.due_date:
                try:
                    due_date = datetime.fromisoformat(task.due_date).date()
                    if self.date_overdue_radio.isChecked():
                        if not (due_date < today and not task.completed):
                            continue
                    elif self.date_today_radio.isChecked():
                        if not (due_date == today):
                            continue
                    elif self.date_future_radio.isChecked():
                        if not (due_date > today):
                            continue
                except ValueError:
                    pass

            filtered_tasks.append(task)

        self.table_widget.setRowCount(0)
        for task in filtered_tasks:
            self.add_item(task)

    def reset_filters(self):
        self.search_input.clear()
        self.status_all_radio.setChecked(True)

        self.priority_high_check.setChecked(True)
        self.priority_medium_check.setChecked(True)
        self.priority_low_check.setChecked(True)

        self.date_all_radio.setChecked(True)
        self.apply_filters()

    def refresh_task_row(self, task: Task):
        for row in range(self.table_widget.rowCount()):
            for col in [2, 4, 5, 6]:
                widget = self.table_widget.cellWidget(row, col)
                if widget and hasattr(widget, 'task_id') and widget.task_id == task.id:
                    title_item = self.table_widget.item(row, 0)
                    if title_item:
                        title_item.setText(task.title)
                        title_item.setToolTip(task.description)

                        if task.completed:
                            title_item.setForeground(QColor(100, 100, 100))
                            font = title_item.font()
                            font.setStrikeOut(True)
                            title_item.setFont(font)
                        else:
                            title_item.setForeground(QColor(255, 255, 255))
                            font = title_item.font()
                            font.setStrikeOut(False)
                            title_item.setFont(font)

                    priority_text = ["🚨 High", "⚠️ Medium", "📋 Low"][task.priority - 1]
                    priority_widget = self.table_widget.cellWidget(row, 1)
                    if priority_widget:
                        priority_label = priority_widget.findChild(QLabel)
                        if priority_label:
                            priority_label.setText(priority_text)
                            if task.priority == 1:
                                priority_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
                            elif task.priority == 2:
                                priority_label.setStyleSheet("color: #ffd166; font-weight: bold;")
                            else:
                                priority_label.setStyleSheet("color: #8ac926; font-weight: bold;")

                    status_button = self.table_widget.cellWidget(row, 2)
                    if isinstance(status_button, QPushButton):
                        status_button.setText("✅ Completed" if task.completed else "⏳ Pending")
                        status_button.setChecked(task.completed)

                    due_text = task.due_date if task.due_date else "No due date"
                    due_item = self.table_widget.item(row, 3)
                    if due_item:
                        due_item.setText(due_text)
                        due_item.setForeground(QColor(255, 255, 255))
                        if task.due_date and not task.completed:
                            due_date = datetime.fromisoformat(task.due_date).date()
                            if due_date < datetime.now().date():
                                due_item.setForeground(QColor(255, 100, 100))

                    for col in [2, 4, 5, 6]:
                        widget = self.table_widget.cellWidget(row, col)
                        if widget:
                            widget.task_id = task.id

                    return

    def toggle_task_status_by_id(self, task_id: str):
        task = self.todo_manager.get_task(task_id)
        if task:
            task.toggle_complete()
            self.todo_manager.write_data()
            for i, t in enumerate(self.all_tasks):
                if t.id == task_id:
                    self.all_tasks[i] = task
                    break
            self.apply_filters()
            self.update_stats()

    def view_task_by_id(self, task_id: str):
        task = self.todo_manager.get_task(task_id)
        if task:
            dialog = TaskDisplayDialog(self, task, on_edit_callback=lambda t: self.edit_task_by_id(t.id))
            dialog.exec_()

    def edit_task_by_id(self, task_id: str):
        task = self.todo_manager.get_task(task_id)
        if not task:
            QMessageBox.warning(self, "Error", "Task not found")
            return

        dialog = TaskInputDialog(self, task)
        if dialog.exec_() == QDialog.Accepted:
            inputs = dialog.get_inputs()

            if not inputs["title"]:
                QMessageBox.warning(
                    self,
                    'Missing Information',
                    'Please provide a task title.'
                )
                return

            updated_task = Task(
                id=task.id,
                title=inputs["title"],
                description=inputs["description"],
                priority=inputs["priority"],
                completed=task.completed,
                created_at=task.created_at,
                due_date=inputs["due_date"]
            )

            self.todo_manager.tasks[task.id] = updated_task
            self.todo_manager.write_data()

            for i, t in enumerate(self.all_tasks):
                if t.id == task.id:
                    self.all_tasks[i] = updated_task
                    break

            self.apply_filters()
            self.update_stats()

            QMessageBox.information(
                self,
                'Updated',
                f'Task "{updated_task.title}" has been updated.'
            )

    def delete_task_by_id(self, task_id: str):
        task = self.todo_manager.get_task(task_id)
        if not task:
            QMessageBox.warning(self, "Error", "Task not found")
            return

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Confirm Deletion')
        msg_box.setText(f'Delete task:\n<b>{task.title}</b>?')
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.setIcon(QMessageBox.Question)

        reply = msg_box.exec_()

        if reply == QMessageBox.Yes:
            self.todo_manager.delete_task(task.id)
            self.all_tasks = [t for t in self.all_tasks if t.id != task.id]
            self.apply_filters()
            self.update_stats()
            QMessageBox.information(
                self,
                'Deleted',
                f'Task "{task.title}" has been deleted.'
            )

    def show_context_menu(self, position):
        row = self.table_widget.rowAt(position.y())
        if row < 0:
            return

        task_id = None
        for col in [2, 4, 5, 6]:
            widget = self.table_widget.cellWidget(row, col)
            if widget and hasattr(widget, 'task_id'):
                task_id = widget.task_id
                break

        if not task_id:
            return

        task = self.todo_manager.get_task(task_id)
        if not task:
            return

        menu = QMenu()

        view_action = QAction("👁 View Details")
        view_action.triggered.connect(lambda: self.view_task_by_id(task_id))
        menu.addAction(view_action)

        mark_complete_action = QAction("✅ Mark as Complete" if not task.completed else "⏳ Mark as Pending")
        mark_complete_action.triggered.connect(lambda: self.toggle_task_status_by_id(task_id))
        menu.addAction(mark_complete_action)

        menu.addSeparator()

        edit_action = QAction("✏️ Edit Task")
        edit_action.triggered.connect(lambda: self.edit_task_by_id(task_id))
        menu.addAction(edit_action)

        menu.addSeparator()

        delete_action = QAction("🗑️ Delete Task")
        delete_action.triggered.connect(lambda: self.delete_task_by_id(task_id))
        menu.addAction(delete_action)

        menu.exec_(self.table_widget.viewport().mapToGlobal(position))

    def add_task(self):
        dialog = TaskInputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            inputs = dialog.get_inputs()

            if not inputs["title"]:
                QMessageBox.warning(
                    self,
                    'Missing Information',
                    'Please provide a task title.'
                )
                return

            task_id = str(uuid.uuid4())
            task = Task(
                id=task_id,
                title=inputs["title"],
                description=inputs["description"],
                priority=inputs["priority"],
                due_date=inputs["due_date"]
            )

            self.todo_manager.add_task(task)
            self.all_tasks.append(task)
            self.apply_filters()
            self.update_stats()

            QMessageBox.information(
                self,
                'Success',
                f'Task "{task.title}" has been created.'
            )

    def clear_completed(self):
        completed_count = self.todo_manager.completed_count
        if completed_count == 0:
            QMessageBox.information(
                self,
                'No Completed Tasks',
                'There are no completed tasks to clear.'
            )
            return

        reply = QMessageBox.question(
            self,
            'Clear Completed Tasks',
            f'Clear {completed_count} completed task(s)?\nThis action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.todo_manager.clear_completed()
            self.all_tasks = [t for t in self.all_tasks if not t.completed]
            self.apply_filters()
            self.update_stats()
            QMessageBox.information(
                self,
                'Cleared',
                f'{completed_count} completed task(s) have been cleared.'
            )

    def show_help(self):
        QMessageBox.information(
            self,
            'Smart Task Manager Help',
            '<h3>Smart Task Manager v1.1.0</h3>'
            '<p><b>Features:</b></p>'
            '<ul>'
            '<li>Create tasks with title, description, priority, and due date</li>'
            '<li>Edit tasks at any time using the Edit button</li>'
            '<li>Mark tasks as completed/pending with one click</li>'
            '<li>View detailed task information</li>'
            '<li>Right-click on tasks for context menu with quick actions</li>'
            '<li>Delete individual tasks or clear all completed at once</li>'
            '<li>Search tasks by text in title and description</li>'
            '<li>Filter tasks by status (All/Pending/Completed)</li>'
            '<li>Filter tasks by priority (High/Medium/Low)</li>'
            '<li>Filter tasks by due date (All/Overdue/Today/Future)</li>'
            '<li>Reset all filters with one click</li>'
            '</ul>'
            '<p><b>Quick Actions:</b></p>'
            '<ul>'
            '<li>Click the status button to toggle completion</li>'
            '<li>Right-click any task for context menu</li>'
            '<li>Use search box for instant filtering</li>'
            '</ul>'
            '<p><b>Priority levels:</b></p>'
            '<ul>'
            '<li>🚨 High - Urgent tasks (Red)</li>'
            '<li>⚠️ Medium - Important tasks (Yellow)</li>'
            '<li>📋 Low - Nice-to-have tasks (Green)</li>'
            '</ul>'
            '<p>Tasks are automatically saved to ~/.todos.json</p>'
            '<hr>'
            '<p><b>Links:</b></p>'
            '<p>'
            '📂 <a href="https://github.com/smartlegionlab/smart-task-manager" style="color: #2a82da;">GitHub Repository</a><br>'
            '🐛 <a href="https://github.com/smartlegionlab/smart-task-manager/issues" style="color: #2a82da;">Report Issues</a>'
            '</p>'
        )

    def closeEvent(self, event):
        if self.todo_manager.count > 0:
            reply = QMessageBox.question(
                self,
                'Exit',
                f'You have {self.todo_manager.count} task(s) saved.\n'
                f'Are you sure you want to exit?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
