# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QColorDialog,
    QTextEdit, QMessageBox, QWidget, QGridLayout, QFrame,
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QSize

from core.label import Label
from ui.label_widget import LabelWidget


class LabelDialog(QDialog):

    def __init__(self, parent=None, label: Label = None):
        super().__init__(parent)
        self.is_edit_mode = label is not None
        self.label = label

        self.setWindowTitle('Edit Label' if self.is_edit_mode else 'Create New Label')
        self.setMinimumWidth(450)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)

        name_group = QFrame()
        name_group.setFrameStyle(QFrame.StyledPanel)
        name_layout = QVBoxLayout(name_group)
        name_layout.setContentsMargins(15, 15, 15, 15)

        self.name_label = QLabel('Label Name:')
        self.name_label.setStyleSheet("font-weight: bold;")
        name_layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter label name")
        if label:
            self.name_input.setText(label.name)
        name_layout.addWidget(self.name_input)

        self.layout.addWidget(name_group)

        color_group = QFrame()
        color_group.setFrameStyle(QFrame.StyledPanel)
        color_layout = QGridLayout(color_group)
        color_layout.setContentsMargins(15, 15, 15, 15)

        self.color_label = QLabel('Color:')
        self.color_label.setStyleSheet("font-weight: bold;")
        color_layout.addWidget(self.color_label, 0, 0)

        self.color_button = QPushButton()
        self.color_button.setFixedSize(50, 50)
        self.color_button.clicked.connect(self.choose_color)
        if label:
            self.current_color = QColor(label.color)
        else:
            self.current_color = QColor("#3498db")
        self.update_color_button()
        color_layout.addWidget(self.color_button, 0, 1)

        self.preview_label = QLabel("Preview:")
        self.preview_label.setStyleSheet("font-weight: bold;")
        color_layout.addWidget(self.preview_label, 1, 0)

        self.preview_container = QWidget()
        preview_container_layout = QHBoxLayout(self.preview_container)
        preview_container_layout.setContentsMargins(0, 0, 0, 0)

        self.preview_widget = LabelWidget(
            label.name if label else "Preview Label",
            self.current_color.name(),
            self
        )
        self.preview_widget.setMinimumHeight(35)
        preview_container_layout.addWidget(self.preview_widget)
        preview_container_layout.addStretch()

        color_layout.addWidget(self.preview_container, 1, 1)

        color_layout.setColumnStretch(2, 1)
        self.layout.addWidget(color_group)

        desc_group = QFrame()
        desc_group.setFrameStyle(QFrame.StyledPanel)
        desc_layout = QVBoxLayout(desc_group)
        desc_layout.setContentsMargins(15, 15, 15, 15)

        self.desc_label = QLabel('Description (optional):')
        self.desc_label.setStyleSheet("font-weight: bold;")
        desc_layout.addWidget(self.desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setPlaceholderText("Enter label description")
        if label and label.description:
            self.desc_input.setText(label.description)
        desc_layout.addWidget(self.desc_input)

        self.layout.addWidget(desc_group)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setFixedSize(100, 35)
        button_layout.addWidget(self.cancel_button)

        button_layout.addStretch()

        button_text = 'Update Label' if self.is_edit_mode else 'Create Label'
        self.submit_button = QPushButton(button_text)
        self.submit_button.setDefault(True)
        self.submit_button.setFixedSize(150, 35)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        self.submit_button.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_button)

        self.layout.addLayout(button_layout)

        self.name_input.textChanged.connect(self.update_preview)

    def choose_color(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.update_color_button()
            self.update_preview()

    def update_color_button(self):
        self.color_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_color.name()};
                border: 2px solid #444;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                border: 2px solid #666;
                background-color: {self.adjust_color_brightness(self.current_color.name(), 0.1)};
            }}
        """)

    def adjust_color_brightness(self, color_hex: str, factor: float) -> str:
        color = QColor(color_hex)
        h, s, v, a = color.getHsv()
        v = min(255, int(v * (1 + factor)))
        return QColor.fromHsv(h, s, v, a).name()

    def update_preview(self):
        name = self.name_input.text() or "Preview Label"
        self.preview_widget.set_label(name, self.current_color.name())

    def get_label_data(self) -> dict:
        return {
            'name': self.name_input.text().strip(),
            'color': self.current_color.name(),
            'description': self.desc_input.toPlainText().strip() or None
        }


class LabelManagerDialog(QDialog):
    label_selected = pyqtSignal(str)

    def __init__(self, parent=None, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.setWindowTitle('📝 Label Manager')
        self.setMinimumSize(600, 700)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(15, 15, 15, 15)

        header_label = QLabel('📝 Label Manager')
        header_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_label.setStyleSheet("color: #2a82da;")
        self.layout.addWidget(header_label)

        self.btn_new_label = QPushButton('+ Create New Label')
        self.btn_new_label.clicked.connect(self.create_label)
        self.btn_new_label.setFixedHeight(40)
        self.btn_new_label.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.layout.addWidget(self.btn_new_label)

        info_label = QLabel(f'Total labels: {len(self.manager.get_all_labels())}')
        info_label.setStyleSheet("color: #888; font-size: 12px;")
        self.layout.addWidget(info_label)

        self.labels_list = QListWidget()
        self.labels_list.itemDoubleClicked.connect(self.select_label)
        self.labels_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                background-color: #353535;
                border-radius: 5px;
                margin: 5px;
                padding: 10px;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #2a82da;
                color: white;
            }
        """)
        self.layout.addWidget(self.labels_list)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.btn_edit = QPushButton('✏️ Edit')
        self.btn_edit.clicked.connect(self.edit_label)
        self.btn_edit.setEnabled(False)
        self.btn_edit.setFixedSize(80, 35)
        self.btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #e68900;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        button_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton('🗑️ Delete')
        self.btn_delete.clicked.connect(self.delete_label)
        self.btn_delete.setEnabled(False)
        self.btn_delete.setFixedSize(80, 35)
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        button_layout.addWidget(self.btn_delete)

        self.btn_select = QPushButton('✓ Select')
        self.btn_select.clicked.connect(self.select_current_label)
        self.btn_select.setEnabled(False)
        self.btn_select.setFixedSize(100, 35)
        self.btn_select.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #219653;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        button_layout.addWidget(self.btn_select)

        button_layout.addStretch()

        self.btn_close = QPushButton('Close')
        self.btn_close.clicked.connect(self.accept)
        self.btn_close.setFixedSize(100, 35)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        button_layout.addWidget(self.btn_close)

        self.layout.addLayout(button_layout)

        self.labels_list.itemSelectionChanged.connect(self.on_selection_changed)

        self.load_labels()

    def load_labels(self):
        self.labels_list.clear()
        labels = self.manager.get_all_labels()

        for label in labels:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 70))

            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(15)

            label_widget = LabelWidget(label.name, label.color)
            label_widget.setMinimumHeight(40)
            label_widget.setMinimumWidth(120)
            layout.addWidget(label_widget)

            if label.description:
                desc_label = QLabel(label.description)
                desc_label.setStyleSheet("color: #aaa; font-size: 12px;")
                desc_label.setWordWrap(True)
                layout.addWidget(desc_label, 1)

            color_code = QLabel(f"Color: {label.color}")
            color_code.setStyleSheet("color: #888; font-size: 11px; font-family: monospace;")
            layout.addWidget(color_code)

            layout.addStretch()
            widget.setLayout(layout)

            self.labels_list.addItem(item)
            self.labels_list.setItemWidget(item, widget)
            item.label_id = label.id

    def on_selection_changed(self):
        has_selection = len(self.labels_list.selectedItems()) > 0
        self.btn_edit.setEnabled(has_selection)
        self.btn_delete.setEnabled(has_selection)
        self.btn_select.setEnabled(has_selection)

    def create_label(self):
        dialog = LabelDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_label_data()

            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Label name is required')
                return

            self.manager.create_label(**data)
            self.load_labels()

    def edit_label(self):
        items = self.labels_list.selectedItems()
        if not items:
            return

        item = items[0]
        label = self.manager.get_label(item.label_id)
        if not label:
            return

        dialog = LabelDialog(self, label)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_label_data()

            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Label name is required')
                return

            self.manager.update_label(label.id, **data)
            self.load_labels()

    def delete_label(self):
        items = self.labels_list.selectedItems()
        if not items:
            return

        item = items[0]
        label = self.manager.get_label(item.label_id)
        if not label:
            return

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Delete label "{label.name}"?\nThis will remove it from all projects, tasks, and subtasks.',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_label(label.id)
            self.load_labels()

    def select_current_label(self):
        items = self.labels_list.selectedItems()
        if not items:
            return

        item = items[0]
        self.label_selected.emit(item.label_id)
        self.accept()

    def select_label(self, item):
        self.label_selected.emit(item.label_id)
        self.accept()
