# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from datetime import datetime
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox,
    QDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QHBoxLayout, QGroupBox,
    QMenu, QAction, QGridLayout,
    QDesktopWidget, QStatusBar, QMainWindow,
    QTreeWidget, QTreeWidgetItem, QProgressBar,
    QToolBar, QFileDialog
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from core.manager import ProjectManager
from ui.components import ProgressWidget, PriorityIndicator
from ui.label_widget import LabelWidget
from ui.project_dialog import ProjectDialog
from ui.task_dialog import TaskDialog
from ui.label_manager import LabelManagerDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.manager = ProjectManager()
        self.current_project_id: Optional[str] = None

        self.setWindowTitle('Advanced Project Manager v2.0')
        self.showMaximized()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            QWidget {
                color: #ffffff;
                font-family: Arial;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_ui()
        self.setup_status_bar()

        self.load_projects()

        self.center_window()
        self.selected_project_item = None

    def center_window(self):
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def setup_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        new_project_action = QAction('New Project', self)
        new_project_action.setShortcut('Ctrl+N')
        new_project_action.triggered.connect(self.create_project)
        file_menu.addAction(new_project_action)

        new_task_action = QAction('New Task', self)
        new_task_action.setShortcut('Ctrl+T')
        new_task_action.triggered.connect(self.create_task)
        file_menu.addAction(new_task_action)

        file_menu.addSeparator()

        import_action = QAction('Import...', self)
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)

        export_action = QAction('Export...', self)
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('Edit')

        edit_project_action = QAction('Edit Project', self)
        edit_project_action.setShortcut('Ctrl+E')
        edit_project_action.triggered.connect(self.edit_current_project)
        edit_menu.addAction(edit_project_action)

        delete_project_action = QAction('Delete Project', self)
        delete_project_action.setShortcut('Ctrl+D')
        delete_project_action.triggered.connect(self.delete_current_project)
        edit_menu.addAction(delete_project_action)

        edit_menu.addSeparator()

        labels_action = QAction('Manage Labels', self)
        labels_action.setShortcut('Ctrl+L')
        labels_action.triggered.connect(self.manage_labels)
        edit_menu.addAction(labels_action)

        view_menu = menubar.addMenu('View')

        refresh_action = QAction('Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_view)
        view_menu.addAction(refresh_action)

        view_menu.addSeparator()

        show_completed_action = QAction('Show Completed Tasks', self)
        show_completed_action.setCheckable(True)
        show_completed_action.setChecked(True)
        show_completed_action.triggered.connect(self.toggle_show_completed)
        view_menu.addAction(show_completed_action)

        help_menu = menubar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        help_action = QAction('Help', self)
        help_action.setShortcut('F1')
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def setup_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        new_project_btn = QPushButton('New Project')
        new_project_btn.clicked.connect(self.create_project)
        toolbar.addWidget(new_project_btn)

        new_task_btn = QPushButton('New Task')
        new_task_btn.clicked.connect(self.create_task)
        toolbar.addWidget(new_task_btn)

        toolbar.addSeparator()

        labels_btn = QPushButton('Labels')
        labels_btn.clicked.connect(self.manage_labels)
        toolbar.addWidget(labels_btn)

        toolbar.addSeparator()

        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.refresh_view)
        toolbar.addWidget(refresh_btn)

    def setup_ui(self):
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        left_panel = QWidget()
        left_panel.setMinimumWidth(300)
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)

        projects_header = QLabel('📁 Projects')
        projects_header.setFont(QFont("Arial", 14, QFont.Bold))
        left_layout.addWidget(projects_header)

        self.projects_tree = QTreeWidget()
        self.projects_tree.setHeaderLabel('Projects')
        self.projects_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 5px;
            }
            QTreeWidget::item {
                padding: 5px;
            }
            QTreeWidget::item:selected {
                background-color: #2a82da;
            }
        """)
        self.projects_tree.itemClicked.connect(self.on_project_selected)
        left_layout.addWidget(self.projects_tree)

        project_actions_layout = QHBoxLayout()

        self.btn_new_project = QPushButton('+ New Project')
        self.btn_new_project.clicked.connect(self.create_project)
        self.btn_new_project.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        project_actions_layout.addWidget(self.btn_new_project)

        self.btn_delete_project = QPushButton('Delete')
        self.btn_delete_project.clicked.connect(self.delete_current_project)
        self.btn_delete_project.setEnabled(False)
        project_actions_layout.addWidget(self.btn_delete_project)

        left_layout.addLayout(project_actions_layout)

        self.project_progress = ProgressWidget()
        left_layout.addWidget(self.project_progress)

        stats_group = QGroupBox("📊 Statistics")
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #444;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2a82da;
            }
        """)
        stats_layout = QGridLayout()

        self.stats_projects = QLabel("Projects: 0")
        self.stats_projects.setStyleSheet("font-size: 12px;")
        stats_layout.addWidget(self.stats_projects, 0, 0)

        self.stats_tasks = QLabel("Tasks: 0")
        self.stats_tasks.setStyleSheet("font-size: 12px;")
        stats_layout.addWidget(self.stats_tasks, 0, 1)

        self.stats_subtasks = QLabel("Subtasks: 0")
        self.stats_subtasks.setStyleSheet("font-size: 12px;")
        stats_layout.addWidget(self.stats_subtasks, 1, 0)

        self.stats_completed = QLabel("Completed: 0%")
        self.stats_completed.setStyleSheet("font-size: 12px;")
        stats_layout.addWidget(self.stats_completed, 1, 1)

        self.stats_labels = QLabel("Labels: 0")
        self.stats_labels.setStyleSheet("font-size: 12px;")
        stats_layout.addWidget(self.stats_labels, 2, 0)

        stats_layout.setColumnStretch(2, 1)
        stats_group.setLayout(stats_layout)
        left_layout.addWidget(stats_group)

        left_layout.addStretch()
        main_layout.addWidget(left_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        tasks_header_layout = QHBoxLayout()

        self.tasks_header = QLabel('Select a project to view tasks')
        self.tasks_header.setFont(QFont("Arial", 14, QFont.Bold))
        tasks_header_layout.addWidget(self.tasks_header)

        tasks_header_layout.addStretch()

        self.btn_new_task = QPushButton('+ New Task')
        self.btn_new_task.clicked.connect(self.create_task)
        self.btn_new_task.setEnabled(False)
        self.btn_new_task.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        tasks_header_layout.addWidget(self.btn_new_task)

        right_layout.addLayout(tasks_header_layout)

        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(8)
        self.tasks_table.setHorizontalHeaderLabels(
            ['Title', 'Priority', 'Status', 'Progress', 'Due Date', 'Labels', 'Edit', 'Delete']
        )
        self.tasks_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tasks_table.setAlternatingRowColors(True)
        self.tasks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_table.customContextMenuRequested.connect(self.show_task_context_menu)
        self.tasks_table.setStyleSheet("""
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

        self.tasks_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tasks_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)

        right_layout.addWidget(self.tasks_table)

        main_layout.addWidget(right_panel, 1)

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')

    def load_projects(self):
        self.projects_tree.clear()

        projects = self.manager.get_all_projects()

        for project in projects:
            item = QTreeWidgetItem(self.projects_tree)
            item.setText(0, f"{project.name} v{project.version}")
            item.project_id = project.id

            task_count = len(project.tasks)
            completed_tasks = sum(1 for task_id in project.tasks
                                  if self.manager.get_task(task_id) and
                                  self.manager.get_task(task_id).completed)

            progress_text = f" ({completed_tasks}/{task_count})"
            item.setText(0, f"{project.name} v{project.version}{progress_text}")

            if project.description:
                item.setToolTip(0, project.description)

            if self.current_project_id and project.id == self.current_project_id:
                self.projects_tree.setCurrentItem(item)
                self.selected_project_item = item

        self.update_statistics()

    def on_project_selected(self, item, column):
        self.current_project_id = item.project_id
        self.selected_project_item = item
        self.btn_delete_project.setEnabled(True)
        self.btn_new_task.setEnabled(True)

        project = self.manager.get_project(self.current_project_id)
        if project:
            self.tasks_header.setText(f'📋 Tasks in "{project.name}"')

            progress = self.manager.get_project_progress(project.id)
            self.project_progress.set_progress(progress)

            self.load_tasks_for_project(project.id)

    def load_tasks_for_project(self, project_id: str):
        self.tasks_table.setRowCount(0)

        tasks = self.manager.get_tasks_by_project(project_id)

        for row, task in enumerate(tasks):
            self.tasks_table.insertRow(row)

            title_item = QTableWidgetItem(task.title)
            if task.description:
                title_item.setToolTip(task.description)
            if task.completed:
                title_item.setForeground(QColor(100, 100, 100))
                font = title_item.font()
                font.setStrikeOut(True)
                title_item.setFont(font)
            self.tasks_table.setItem(row, 0, title_item)

            priority_widget = PriorityIndicator(task.priority)
            self.tasks_table.setCellWidget(row, 1, priority_widget)

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
            status_button.clicked.connect(lambda checked, tid=task.id: self.toggle_task_status(tid))
            self.tasks_table.setCellWidget(row, 2, status_button)

            progress = self.manager.get_task_progress(task.id)
            progress_bar = QProgressBar()
            progress_bar.setValue(int(progress))
            progress_bar.setTextVisible(True)
            progress_bar.setFormat(f"{progress:.1f}%")
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #444;
                    border-radius: 3px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #2a82da;
                    border-radius: 3px;
                }
            """)
            self.tasks_table.setCellWidget(row, 3, progress_bar)

            due_text = task.due_date if task.due_date else "No due date"
            due_item = QTableWidgetItem(due_text)
            due_item.setTextAlignment(Qt.AlignCenter)

            if task.due_date and not task.completed:
                due_date = datetime.fromisoformat(task.due_date).date()
                if due_date < datetime.now().date():
                    due_item.setForeground(QColor(255, 100, 100))

            self.tasks_table.setItem(row, 4, due_item)

            labels_widget = QWidget()
            labels_layout = QHBoxLayout(labels_widget)
            labels_layout.setContentsMargins(5, 2, 5, 2)
            labels_layout.setSpacing(5)

            for label_id in task.labels:
                label = self.manager.get_label(label_id)
                if label:
                    label_widget = LabelWidget(label.name, label.color)
                    label_widget.setMinimumHeight(24)
                    label_widget.setMinimumWidth(60)
                    labels_layout.addWidget(label_widget)

            labels_layout.addStretch()
            self.tasks_table.setCellWidget(row, 5, labels_widget)

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
            edit_button.clicked.connect(lambda checked, tid=task.id: self.edit_task(tid))
            self.tasks_table.setCellWidget(row, 6, edit_button)

            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #da2a2a;
                    color: white;
                    border-radius: 3px;
                    padding: 5px 10px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #ca1a1a;
                }
            """)
            delete_button.clicked.connect(lambda checked, tid=task.id: self.delete_task(tid))
            self.tasks_table.setCellWidget(row, 7, delete_button)

    def toggle_task_status(self, task_id: str):
        task = self.manager.get_task(task_id)
        if task:
            task.toggle_complete()
            self.manager.update_task(task_id, completed=task.completed)

            if self.current_project_id:
                self.load_tasks_for_project(self.current_project_id)
                self.update_statistics()

                self.load_projects()

                progress = self.manager.get_project_progress(self.current_project_id)
                self.project_progress.set_progress(progress)

    def create_project(self):
        dialog = ProjectDialog(self, manager=self.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_project_data()

            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Project name is required')
                return

            project = self.manager.create_project(**data)
            self.load_projects()

            for i in range(self.projects_tree.topLevelItemCount()):
                item = self.projects_tree.topLevelItem(i)
                if item.project_id == project.id:
                    self.projects_tree.setCurrentItem(item)
                    self.on_project_selected(item, 0)
                    break

            QMessageBox.information(self, 'Success', f'Project "{project.name}" created')

    def edit_current_project(self):
        if not self.current_project_id:
            QMessageBox.warning(self, 'Error', 'No project selected')
            return

        project = self.manager.get_project(self.current_project_id)
        if not project:
            return

        dialog = ProjectDialog(self, project=project, manager=self.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_project_data()

            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Project name is required')
                return

            self.manager.update_project(project.id, **data)
            self.load_projects()

            if self.current_project_id == project.id:
                self.load_tasks_for_project(project.id)

    def delete_current_project(self):
        if not self.current_project_id:
            QMessageBox.warning(self, 'Error', 'No project selected')
            return

        project = self.manager.get_project(self.current_project_id)
        if not project:
            return

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Delete project "{project.name}" and all its tasks/subtasks?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_project(project.id)
            self.current_project_id = None
            self.btn_delete_project.setEnabled(False)
            self.btn_new_task.setEnabled(False)
            self.tasks_header.setText('Select a project to view tasks')
            self.tasks_table.setRowCount(0)
            self.project_progress.set_progress(0)
            self.load_projects()

    def create_task(self):
        if not self.current_project_id:
            QMessageBox.warning(self, 'Error', 'Please select a project first')
            return

        dialog = TaskDialog(self, manager=self.manager, project_id=self.current_project_id)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_task_data()

            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Task title is required')
                return

            task = self.manager.create_task(**data)

            self.load_tasks_for_project(self.current_project_id)
            self.update_statistics()

            self.load_projects()

            progress = self.manager.get_project_progress(self.current_project_id)
            self.project_progress.set_progress(progress)

            QMessageBox.information(self, 'Success', f'Task "{task.title}" created')

    def edit_task(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

        dialog = TaskDialog(self, task=task, manager=self.manager)
        dialog.task_updated.connect(self.on_task_updated)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_task_data()

            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Task title is required')
                return

            self.manager.update_task(task.id, **data)

            if self.current_project_id:
                self.load_tasks_for_project(self.current_project_id)
                self.update_statistics()

                self.load_projects()

                progress = self.manager.get_project_progress(self.current_project_id)
                self.project_progress.set_progress(progress)

    def on_task_updated(self):
        if self.current_project_id:
            self.load_tasks_for_project(self.current_project_id)
            self.update_statistics()

            self.load_projects()

            progress = self.manager.get_project_progress(self.current_project_id)
            self.project_progress.set_progress(progress)

    def delete_task(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Delete task "{task.title}" and all its subtasks?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_task(task_id)

            if self.current_project_id:
                self.load_tasks_for_project(self.current_project_id)
                self.update_statistics()

                self.load_projects()

                progress = self.manager.get_project_progress(self.current_project_id)
                self.project_progress.set_progress(progress)

    def manage_labels(self):
        dialog = LabelManagerDialog(self, self.manager)
        dialog.exec_()
        self.update_statistics()

    def show_task_context_menu(self, position):
        row = self.tasks_table.rowAt(position.y())
        if row < 0:
            return

        edit_button = self.tasks_table.cellWidget(row, 6)
        if not edit_button:
            return

        for col in [2, 6, 7]:
            widget = self.tasks_table.cellWidget(row, col)
            if widget and widget.underMouse():
                task_id = None
                if col == 2:
                    task_id = self.get_task_id_from_row(row)
                elif col == 6:
                    task_id = self.get_task_id_from_row(row)
                elif col == 7:
                    task_id = self.get_task_id_from_row(row)

                if task_id:
                    self.show_task_menu(task_id, self.tasks_table.viewport().mapToGlobal(position))
                return

    def get_task_id_from_row(self, row: int) -> Optional[str]:
        if not self.current_project_id:
            return None

        tasks = self.manager.get_tasks_by_project(self.current_project_id)
        if row < len(tasks):
            return tasks[row].id

        return None

    def show_task_menu(self, task_id: str, position):
        task = self.manager.get_task(task_id)
        if not task:
            return

        menu = QMenu()

        view_action = QAction("👁 View Details")
        view_action.triggered.connect(lambda: self.view_task(task_id))
        menu.addAction(view_action)

        mark_action = QAction("✅ Mark as Complete" if not task.completed else "⏳ Mark as Pending")
        mark_action.triggered.connect(lambda: self.toggle_task_status(task_id))
        menu.addAction(mark_action)

        menu.addSeparator()

        edit_action = QAction("✏️ Edit Task")
        edit_action.triggered.connect(lambda: self.edit_task(task_id))
        menu.addAction(edit_action)

        menu.addSeparator()

        delete_action = QAction("🗑️ Delete Task")
        delete_action.triggered.connect(lambda: self.delete_task(task_id))
        menu.addAction(delete_action)

        menu.exec_(position)

    def view_task(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f'Task: {task.title}')
        dialog.setMinimumWidth(500)

        layout = QVBoxLayout(dialog)

        title_label = QLabel(f'<h2>{task.title}</h2>')
        layout.addWidget(title_label)

        if task.description:
            desc_label = QLabel(task.description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("padding: 10px; background-color: #2a2a2a; border-radius: 5px;")
            layout.addWidget(desc_label)

        details_group = QGroupBox("Details")
        details_layout = QVBoxLayout()

        priority_text = ["🚨 High", "⚠️ Medium", "📋 Low"][task.priority - 1]
        priority_label = QLabel(f'<b>Priority:</b> {priority_text}')
        details_layout.addWidget(priority_label)

        status_text = "✅ Completed" if task.completed else "⏳ Pending"
        status_label = QLabel(f'<b>Status:</b> {status_text}')
        details_layout.addWidget(status_label)

        progress = self.manager.get_task_progress(task.id)
        progress_label = QLabel(f'<b>Progress:</b> {progress:.1f}%')
        details_layout.addWidget(progress_label)

        dates_layout = QHBoxLayout()
        created_label = QLabel(f'<b>Created:</b> {task.created_at[:10]}')
        dates_layout.addWidget(created_label)

        dates_layout.addStretch()

        if task.due_date:
            due_label = QLabel(f'<b>Due:</b> {task.due_date}')
            dates_layout.addWidget(due_label)

        details_layout.addLayout(dates_layout)

        if task.labels:
            labels_label = QLabel('<b>Labels:</b>')
            details_layout.addWidget(labels_label)

            labels_widget = QWidget()
            labels_widget_layout = QHBoxLayout(labels_widget)
            labels_widget_layout.setContentsMargins(0, 0, 0, 0)

            for label_id in task.labels:
                label = self.manager.get_label(label_id)
                if label:
                    label_widget = LabelWidget(label.name, label.color)
                    labels_widget_layout.addWidget(label_widget)

            labels_widget_layout.addStretch()
            details_layout.addWidget(labels_widget)

        details_group.setLayout(details_layout)
        layout.addWidget(details_group)

        subtasks = self.manager.get_subtasks_by_task(task.id)
        if subtasks:
            subtasks_group = QGroupBox(f"Subtasks ({len(subtasks)})")
            subtasks_layout = QVBoxLayout()

            for subtask in subtasks:
                subtask_widget = QWidget()
                subtask_layout = QHBoxLayout(subtask_widget)

                status = "✅" if subtask.completed else "⏳"
                subtask_label = QLabel(f'{status} {subtask.title}')
                subtask_layout.addWidget(subtask_label)

                if subtask.due_date:
                    due_label = QLabel(f'Due: {subtask.due_date}')
                    due_label.setStyleSheet("color: #888;")
                    subtask_layout.addWidget(due_label)

                subtask_layout.addStretch()
                subtasks_layout.addWidget(subtask_widget)

            subtasks_group.setLayout(subtasks_layout)
            layout.addWidget(subtasks_group)

        close_button = QPushButton('Close')
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec_()

    def refresh_view(self):
        self.load_projects()
        if self.current_project_id:
            self.load_tasks_for_project(self.current_project_id)
            project = self.manager.get_project(self.current_project_id)
            if project:
                progress = self.manager.get_project_progress(project.id)
                self.project_progress.set_progress(progress)

        self.status_bar.showMessage('View refreshed', 3000)

    def toggle_show_completed(self, show: bool):
        self.refresh_view()

    def update_statistics(self):
        stats = self.manager.get_statistics()

        self.stats_projects.setText(f"Projects: {stats['projects']}")
        self.stats_tasks.setText(f"Tasks: {stats['tasks']}")
        self.stats_subtasks.setText(f"Subtasks: {stats['subtasks']}")
        self.stats_labels.setText(f"Labels: {stats['labels']}")
        self.stats_completed.setText(f"Completed: {stats['task_completion_rate']:.1f}%")

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Data",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            # TODO: Implement import logic
            QMessageBox.information(self, "Import", "Import feature coming soon")

    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Data",
            "projects_export.json",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            # TODO: Implement export logic
            QMessageBox.information(self, "Export", "Export feature coming soon")

    def show_about(self):
        QMessageBox.about(
            self,
            "About Advanced Project Manager",
            """<h2>Advanced Project Manager v2.0</h2>
            <p>A powerful project and task management tool for developers and researchers.</p>
            <p><b>Features:</b></p>
            <ul>
            <li>Manage unlimited projects with versions</li>
            <li>Create tasks with priorities and due dates</li>
            <li>Add subtasks to tasks</li>
            <li>Label system</li>
            <li>Automatic progress tracking</li>
            <li>Dark theme interface</li>
            </ul>
            <p><b>Copyright © 2025, Alexander Suvorov. All rights reserved.</b></p>
            """
        )

    def show_help(self):
        QMessageBox.information(
            self,
            "Help - Advanced Project Manager",
            """<h3>Advanced Project Manager Help</h3>
            <p><b>Getting Started:</b></p>
            <ol>
            <li>Create a project using File → New Project or the New Project button</li>
            <li>Select a project from the left panel</li>
            <li>Add tasks to the project using File → New Task or the New Task button</li>
            <li>Add subtasks by editing a task and going to the Subtasks tab</li>
            <li>Use labels to categorize tasks and subtasks</li>
            </ol>
            <p><b>Keyboard Shortcuts:</b></p>
            <ul>
            <li>Ctrl+N: New Project</li>
            <li>Ctrl+T: New Task</li>
            <li>Ctrl+E: Edit Project</li>
            <li>Ctrl+D: Delete Project</li>
            <li>Ctrl+L: Manage Labels</li>
            <li>F5: Refresh View</li>
            <li>F1: Help</li>
            <li>Ctrl+Q: Exit</li>
            </ul>
            <p><b>Features:</b></p>
            <ul>
            <li>Projects have name, version, description</li>
            <li>Tasks have title, description, priority, due date, and labels</li>
            <li>Subtasks inherit parent task properties and can have their own labels</li>
            <li>Automatic completion: When all subtasks are done, parent task is marked complete</li>
            <li>Progress bars show completion percentage</li>
            <li>Right-click tasks for quick actions</li>
            </ul>
            <p>Data is automatically saved to ~/.project_manager/projects.json</p>
            """
        )

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Exit',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
