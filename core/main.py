# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
import uuid
from datetime import datetime
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox,
    QLineEdit, QDialog, QTableWidget, QTableWidgetItem, QFrame,
    QHeaderView, QHBoxLayout, QGroupBox, QTextEdit, QDateEdit, QComboBox,
    QMenu, QAction
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
        self.setWindowTitle('Smart Task Manager v1.0.0')
        self.resize(1000, 700)

        self.todo_manager = TaskManager()

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        self.label_logo = QLabel('Smart Task Manager <sup>v1.0.0</sup>')
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

        self.btn_new_task = QPushButton('➕ Add Task')
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

        self.btn_clear_completed = QPushButton('🗑️ Clear Completed')
        self.btn_clear_completed.setMinimumHeight(40)
        self.btn_clear_completed.clicked.connect(self.clear_completed)
        button_layout.addWidget(self.btn_clear_completed)

        button_layout.addStretch()

        self.btn_help = QPushButton('❓ Help')
        self.btn_help.setMinimumHeight(40)
        self.btn_help.clicked.connect(self.show_help)
        button_layout.addWidget(self.btn_help)

        self.btn_exit = QPushButton('🚪 Exit')
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

        self.copyright_label = QLabel('Copyright © 2025, Alexander Suvorov. All rights reserved.')
        self.copyright_label.setAlignment(Qt.AlignCenter)
        self.copyright_label.setStyleSheet("color: #888; font-size: 10px;")
        footer_layout.addWidget(self.copyright_label)

        self.main_layout.addLayout(footer_layout)

        self.setLayout(self.main_layout)
        self._init()

    def _init(self):
        self.table_widget.setRowCount(0)
        self.update_stats()
        for task in self.todo_manager.tasks.values():
            self.add_item(task)

    def update_stats(self):
        total = self.todo_manager.count
        completed = self.todo_manager.completed_count
        pending = total - completed
        self.stats_label.setText(f"{total} tasks ({completed} completed, {pending} pending)")

    def add_item(self, task: Task):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        title_item = QTableWidgetItem(task.title)
        if task.completed:
            title_item.setForeground(QColor(100, 100, 100))
            font = title_item.font()
            font.setStrikeOut(True)
            title_item.setFont(font)
        title_item.setToolTip(task.description)
        self.table_widget.setItem(row_position, 0, title_item)

        priority_combo = QComboBox()
        priority_combo.addItems(["🚨 High", "⚠️ Medium", "📋 Low"])
        priority_combo.setCurrentIndex(task.priority - 1)
        priority_combo.currentIndexChanged.connect(
            lambda index, t=task: self.change_priority(t, index + 1)
        )
        self.table_widget.setCellWidget(row_position, 1, priority_combo)

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
        status_button.clicked.connect(lambda checked, t=task: self.toggle_task_status(t))
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
        view_button.clicked.connect(lambda checked, t=task: self.view_task(t))
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
        edit_button.clicked.connect(lambda checked, t=task: self.edit_task(t))
        self.table_widget.setCellWidget(row_position, 5, edit_button)

        delete_button = QPushButton("🗑️")
        delete_button.setToolTip("Delete this task")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #da2a2a;
                color: white;
                border-radius: 3px;
                padding: 5px;
                min-width: 30px;
                max-width: 30px;
            }
            QPushButton:hover {
                background-color: #ca1a1a;
            }
        """)
        delete_button.clicked.connect(lambda checked, t=task: self.delete_task(t))
        self.table_widget.setCellWidget(row_position, 6, delete_button)

        self.update_stats()

    def change_priority(self, task: Task, new_priority: int):
        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=new_priority,
            completed=task.completed,
            created_at=task.created_at,
            due_date=task.due_date
        )

        self.todo_manager.tasks[task.id] = updated_task
        self.todo_manager._write_data()

        self.refresh_task_row(updated_task)

    def refresh_task_row(self, task: Task):
        for row in range(self.table_widget.rowCount()):
            title_item = self.table_widget.item(row, 0)
            if title_item and title_item.text() == task.title:
                priority_combo = self.table_widget.cellWidget(row, 1)
                if isinstance(priority_combo, QComboBox):
                    priority_combo.setCurrentIndex(task.priority - 1)

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

                break

    def toggle_task_status(self, task: Task):
        task.toggle_complete()
        self.todo_manager._write_data()
        self.refresh_task_row(task)
        self.update_stats()

    def view_task(self, task: Task):
        dialog = TaskDisplayDialog(self, task, on_edit_callback=self.edit_task)
        dialog.exec_()

    def edit_task(self, task: Task):
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
            self.todo_manager._write_data()

            self.refresh_task_row(updated_task)

            QMessageBox.information(
                self,
                'Updated',
                f'Task "{updated_task.title}" has been updated.'
            )

    def delete_task(self, task: Task):
        reply = QMessageBox.question(
            self,
            'Confirm Deletion',
            f'Delete task:\n<b>{task.title}</b>?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.todo_manager.delete_task(task.id)
            self._init()
            QMessageBox.information(
                self,
                'Deleted',
                f'Task "{task.title}" has been deleted.'
            )

    def show_context_menu(self, position):
        row = self.table_widget.rowAt(position.y())
        if row < 0:
            return

        title_item = self.table_widget.item(row, 0)
        if not title_item:
            return

        task_title = title_item.text()
        task = None
        for t in self.todo_manager.tasks.values():
            if t.title == task_title:
                task = t
                break

        if not task:
            return

        menu = QMenu()

        mark_complete_action = QAction("✅ Mark as Complete" if not task.completed else "⏳ Mark as Pending")
        mark_complete_action.triggered.connect(lambda: self.toggle_task_status(task))

        edit_action = QAction("✏️ Edit Task")
        edit_action.triggered.connect(lambda: self.edit_task(task))

        view_action = QAction("👁 View Details")
        view_action.triggered.connect(lambda: self.view_task(task))

        delete_action = QAction("🗑️ Delete Task")
        delete_action.triggered.connect(lambda: self.delete_task(task))

        menu.addAction(mark_complete_action)
        menu.addSeparator()
        menu.addAction(view_action)
        menu.addAction(edit_action)
        menu.addSeparator()
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

            self.add_item(task)

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
            self._init()
            QMessageBox.information(
                self,
                'Cleared',
                f'{completed_count} completed task(s) have been cleared.'
            )

    def show_help(self):
        QMessageBox.information(
            self,
            'Smart Task Manager Help',
            '<h3>Smart Task Manager v1.0.0</h3>'
            '<p><b>Features:</b></p>'
            '<ul>'
            '<li>Create tasks with title, description, priority, and due date</li>'
            '<li>Edit tasks anytime - double click or use Edit button</li>'
            '<li>Change priority directly from the table</li>'
            '<li>Mark tasks as completed/pending</li>'
            '<li>View task details</li>'
            '<li>Right-click for quick actions</li>'
            '<li>Delete individual tasks</li>'
            '<li>Clear all completed tasks at once</li>'
            '</ul>'
            '<p><b>Quick Actions:</b></p>'
            '<ul>'
            '<li>Click priority dropdown to change priority</li>'
            '<li>Click status button to toggle completion</li>'
            '<li>Right-click any task for context menu</li>'
            '<li>Double-click title to edit task</li>'
            '</ul>'
            '<p><b>Priority levels:</b></p>'
            '<ul>'
            '<li>🚨 High - Urgent tasks</li>'
            '<li>⚠️ Medium - Important tasks</li>'
            '<li>📋 Low - Nice-to-have tasks</li>'
            '</ul>'
            '<p>Tasks are automatically saved to ~/.todos.json</p>'
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
