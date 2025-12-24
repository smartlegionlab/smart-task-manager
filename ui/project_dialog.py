# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox, QFrame,
    QWidget, QGridLayout, QScrollArea
)

from core.project import Project
from ui.label_widget import LabelWidget


class ProjectDialog(QDialog):

    def __init__(self, parent=None, project: Project = None, manager=None):
        super().__init__(parent)
        self.is_edit_mode = project is not None
        self.project = project
        self.manager = manager

        self.setWindowTitle('Edit Project' if self.is_edit_mode else 'Create New Project')
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        name_group = QFrame()
        name_group.setFrameStyle(QFrame.StyledPanel)
        name_layout = QGridLayout(name_group)
        name_layout.setContentsMargins(10, 10, 10, 10)

        self.name_label = QLabel('Project Name:')
        name_layout.addWidget(self.name_label, 0, 0)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter project name")
        if project:
            self.name_input.setText(project.name)
        name_layout.addWidget(self.name_input, 0, 1)

        self.version_label = QLabel('Version:')
        name_layout.addWidget(self.version_label, 1, 0)

        self.version_input = QLineEdit()
        self.version_input.setPlaceholderText("e.g., 1.0.0")
        if project:
            self.version_input.setText(project.version)
        else:
            self.version_input.setText("1.0.0")
        name_layout.addWidget(self.version_input, 1, 1)

        self.layout.addWidget(name_group)

        desc_group = QFrame()
        desc_group.setFrameStyle(QFrame.StyledPanel)
        desc_layout = QVBoxLayout(desc_group)
        desc_layout.setContentsMargins(10, 10, 10, 10)

        self.desc_label = QLabel('Description:')
        desc_layout.addWidget(self.desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        self.desc_input.setPlaceholderText("Enter project description")
        if project and project.description:
            self.desc_input.setText(project.description)
        desc_layout.addWidget(self.desc_input)

        self.layout.addWidget(desc_group)

        labels_group = QFrame()
        labels_group.setFrameStyle(QFrame.StyledPanel)
        labels_layout = QVBoxLayout(labels_group)
        labels_layout.setContentsMargins(10, 10, 10, 10)

        labels_header = QHBoxLayout()
        self.labels_label = QLabel('Labels:')
        labels_header.addWidget(self.labels_label)

        self.btn_add_label = QPushButton('+ Add Label')
        self.btn_add_label.clicked.connect(self.add_label)
        self.btn_add_label.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        labels_header.addWidget(self.btn_add_label)

        labels_header.addStretch()
        labels_layout.addLayout(labels_header)

        self.selected_labels_container = QWidget()
        self.selected_labels_layout = QHBoxLayout(self.selected_labels_container)
        self.selected_labels_layout.setContentsMargins(0, 5, 0, 5)
        self.selected_labels_layout.setSpacing(5)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.selected_labels_container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(80)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444;
                border-radius: 4px;
                background-color: #2a2a2a;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)
        labels_layout.addWidget(scroll_area)

        self.layout.addWidget(labels_group)

        self.selected_label_ids = []
        if project:
            self.selected_label_ids = project.labels.copy()
            self.update_selected_labels_display()

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                background-color: #555;
                color: white;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        button_layout.addWidget(self.cancel_button)

        button_layout.addStretch()

        button_text = 'Update Project' if self.is_edit_mode else 'Create Project'
        self.submit_button = QPushButton(button_text)
        self.submit_button.setDefault(True)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                padding: 8px 24px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        self.submit_button.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_button)

        self.layout.addLayout(button_layout)

    def add_label(self):
        from ui.label_manager import LabelManagerDialog

        dialog = LabelManagerDialog(self, self.manager)
        dialog.label_selected.connect(self.on_label_selected)
        dialog.exec_()

    def on_label_selected(self, label_id: str):
        if label_id not in self.selected_label_ids:
            self.selected_label_ids.append(label_id)
            self.update_selected_labels_display()

    def update_selected_labels_display(self):
        for i in reversed(range(self.selected_labels_layout.count())):
            widget = self.selected_labels_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for label_id in self.selected_label_ids:
            label = self.manager.get_label(label_id)
            if label:
                label_widget = LabelWidget(label.name, label.color)

                remove_btn = QPushButton('×')
                remove_btn.setFixedSize(20, 20)
                remove_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border-radius: 10px;
                        font-weight: bold;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                remove_btn.clicked.connect(lambda checked, lid=label_id: self.remove_label(lid))

                container = QWidget()
                container_layout = QHBoxLayout(container)
                container_layout.setContentsMargins(0, 0, 0, 0)
                container_layout.setSpacing(3)
                container_layout.addWidget(label_widget)
                container_layout.addWidget(remove_btn)

                self.selected_labels_layout.addWidget(container)

        if self.selected_labels_layout.count() > 0:
            last_item = self.selected_labels_layout.itemAt(self.selected_labels_layout.count() - 1)
            if last_item and last_item.widget():
                self.selected_labels_layout.addStretch()

    def remove_label(self, label_id: str):
        if label_id in self.selected_label_ids:
            self.selected_label_ids.remove(label_id)
            self.update_selected_labels_display()

    def get_project_data(self) -> dict:
        return {
            'name': self.name_input.text().strip(),
            'version': self.version_input.text().strip(),
            'description': self.desc_input.toPlainText().strip() or None,
            'labels': self.selected_label_ids
        }

    def accept(self):
        data = self.get_project_data()

        if not data['name']:
            QMessageBox.warning(self, 'Error', 'Project name is required')
            return

        if not data['version']:
            QMessageBox.warning(self, 'Error', 'Version is required')
            return

        super().accept()
