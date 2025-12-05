# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
import json
import os
from typing import Dict, Optional
import uuid
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox,
    QLineEdit, QDialog, QTableWidget, QTableWidgetItem, QSpinBox, QFrame,
    QHeaderView, QHBoxLayout, QGroupBox, QTextEdit, QDateEdit, QComboBox,
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QDate


class TodoTask:

    def __init__(self, id: str, title: str, description: str = "",
                 priority: int = 3, completed: bool = False,
                 created_at: Optional[str] = None, due_date: Optional[str] = None):
        self._id = id
        self._title = title
        self._description = description
        self._priority = priority
        self._completed = completed
        self._created_at = created_at or datetime.now().isoformat()
        self._due_date = due_date

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def completed(self) -> bool:
        return self._completed

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def due_date(self) -> Optional[str]:
        return self._due_date

    def toggle_complete(self):
        self._completed = not self._completed

    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "priority": self._priority,
            "completed": self._completed,
            "created_at": self._created_at,
            "due_date": self._due_date
        }

    @staticmethod
    def from_dict(data: Dict) -> 'TodoTask':
        return TodoTask(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            completed=data['completed'],
            created_at=data['created_at'],
            due_date=data.get('due_date')
        )


class TodoManager:
    """Менеджер задач"""

    def __init__(self, filename: str = '~/.todos.json'):
        self.filename = os.path.expanduser(filename)
        self.tasks = self._load_data()

    @property
    def count(self) -> int:
        return len(self.tasks)

    @property
    def completed_count(self) -> int:
        return sum(1 for task in self.tasks.values() if task.completed)

    def add_task(self, task: TodoTask):
        self.tasks[task.id] = task
        self._write_data()

    def get_task(self, task_id: str) -> Optional[TodoTask]:
        return self.tasks.get(task_id)

    def delete_task(self, task_id: str):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._write_data()
        else:
            raise KeyError("Task not found.")

    def clear_completed(self):
        completed_ids = [task_id for task_id, task in self.tasks.items() if task.completed]
        for task_id in completed_ids:
            del self.tasks[task_id]
        if completed_ids:
            self._write_data()

    def clear_all(self):
        self.tasks = {}
        self._write_data()

    def get_tasks_by_priority(self) -> Dict[int, list]:
        grouped = {1: [], 2: [], 3: []}
        for task in self.tasks.values():
            grouped[task.priority].append(task)
        return grouped

    def _load_data(self) -> Dict[str, TodoTask]:
        if os.path.isfile(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    return {task_id: TodoTask.from_dict(task_data)
                            for task_id, task_data in data.items()}
            except (json.JSONDecodeError, IOError):
                return {}
        else:
            return {}

    def _write_data(self):
        with open(self.filename, 'w') as f:
            json.dump({task_id: task.to_dict()
                       for task_id, task in self.tasks.items()}, f, indent=4)


class TaskInputDialog(QDialog):
    def __init__(self, parent=None, task: Optional[TodoTask] = None):
        super().__init__(parent)
        self.is_edit_mode = task is not None
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
    def __init__(self, parent=None, task: TodoTask = None):
        super().__init__(parent)
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

        self.close_button = QPushButton('Close', self)
        self.close_button.setDefault(True)
        self.close_button.clicked.connect(self.accept)
        self.layout.addWidget(self.close_button)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Smart Task Manager v0.1.0')
        self.resize(1000, 700)

        self.todo_manager = TodoManager()

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        self.label_logo = QLabel('Smart Task Manager <sup>v0.1.0</sup>')
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
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(['Title', 'Priority', 'Status', 'Due Date', 'View', 'Delete'])
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.setAlternatingRowColors(True)
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

    def add_item(self, task: TodoTask):
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

        priority_icons = ["🚨", "⚠️", "📋"]
        priority_item = QTableWidgetItem(f"{priority_icons[task.priority - 1]} {['High', 'Medium', 'Low'][task.priority - 1]}")
        priority_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row_position, 1, priority_item)

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
        self.table_widget.setCellWidget(row_position, 5, delete_button)

        self.update_stats()

    def toggle_task_status(self, task: TodoTask):
        task.toggle_complete()
        self.todo_manager._write_data()
        self._init()  # Refresh the table

    def view_task(self, task: TodoTask):
        dialog = TaskDisplayDialog(self, task)
        dialog.exec_()

    def delete_task(self, task: TodoTask):
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
            task = TodoTask(
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
            '<h3>Smart Task Manager v0.1.0</h3>'
            '<p><b>Features:</b></p>'
            '<ul>'
            '<li>Create tasks with title, description, priority, and due date</li>'
            '<li>Mark tasks as completed/pending</li>'
            '<li>View task details</li>'
            '<li>Delete individual tasks</li>'
            '<li>Clear all completed tasks at once</li>'
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


def main():
    import sys

    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(20, 20, 20))
    dark_palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(50, 50, 50))
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(50, 50, 50))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(100, 100, 100))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(100, 100, 100))

    app.setPalette(dark_palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
