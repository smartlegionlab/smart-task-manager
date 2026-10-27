# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Smart Task Manager")
        self.setMinimumWidth(560)
        self.setMinimumHeight(480)
        self.setModal(True)
        self.setup_ui()
        self.center_dialog()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setStyleSheet("QFrame { background-color: #1e2026; }")
        header.setFixedHeight(110)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 20)
        header_layout.setSpacing(4)

        title_label = QLabel("Smart Task Manager")
        title_label.setStyleSheet("color: #2a82da; font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

        version_label = QLabel("Version 1.3.0")
        version_label.setStyleSheet("color: #5a5d65; font-size: 12px;")
        version_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(version_label)

        subtitle_label = QLabel("Task management for personal productivity")
        subtitle_label.setStyleSheet("color: #aaa; font-size: 11px; font-style: italic;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)

        layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: #181a1e; border: none; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #181a1e;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(14)

        content_layout.addWidget(self._make_section(
            "FEATURES",
            "<ul style='color: #ddd; margin: 0; padding-left: 18px;'>"
            "<li>Tasks with title, description, priority and due date</li>"
            "<li>Three priority levels: High, Medium, Low</li>"
            "<li>Search and filters by status, priority and due date</li>"
            "<li>Automatic saving to ~/.smart_task_manager/tasks.json</li>"
            "<li>JSON export and import with confirmation</li>"
            "<li>Dark theme optimized for extended use</li>"
            "</ul>"
        ))

        content_layout.addWidget(self._make_section(
            "DATA AND PRIVACY",
            "<p style='color: #ddd; margin: 0;'>"
            "All data stays on your machine. No cloud, no telemetry, no network access at runtime. "
            "Your tasks are stored in <code style='color: #2ecc71; background-color: #23262d; "
            "padding: 2px 6px; border-radius: 3px;'>~/.smart_task_manager/tasks.json</code>."
            "</p>"
        ))

        content_layout.addWidget(self._make_section(
            "LINKS",
            "<ul style='list-style: none; padding-left: 0; margin: 0;'>"
            "<li><a href='https://github.com/smartlegionlab/smart-task-manager' "
            "style='color: #2a82da; text-decoration: none;'>GitHub Repository</a></li>"
            "<li><a href='https://github.com/smartlegionlab/smart-task-manager/releases' "
            "style='color: #2a82da; text-decoration: none;'>Releases</a></li>"
            "<li><a href='https://github.com/smartlegionlab/smart-task-manager/blob/master/LICENSE' "
            "style='color: #2a82da; text-decoration: none;'>License (BSD 3-Clause)</a></li>"
            "<li><a href='https://github.com/smartlegionlab/smart-task-manager/blob/master/DISCLAIMER.md' "
            "style='color: #2a82da; text-decoration: none;'>Disclaimer</a></li>"
            "<li><a href='https://smartlegionlab.github.io/' "
            "style='color: #2a82da; text-decoration: none;'>Smart Legion Lab</a></li>"
            "</ul>"
        ))

        content_layout.addStretch()

        copyright_label = QLabel("Copyright (c) 2025, Alexander Suvorov. All rights reserved.")
        copyright_label.setStyleSheet("color: #5a5d65; font-size: 10px;")
        copyright_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(copyright_label)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_panel = QFrame()
        button_panel.setStyleSheet("QFrame { background-color: #1e2026; }")
        button_panel.setFixedHeight(60)
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(20, 12, 20, 12)
        button_layout.addStretch()

        ok_button = QPushButton("Close")
        ok_button.setFixedSize(110, 36)
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setStyleSheet(
            "QPushButton { background-color: #2a82da; color: white; font-weight: bold; "
            "border: none; border-radius: 5px; padding: 8px 16px; }"
            "QPushButton:hover { background-color: #1a72ca; }"
            "QPushButton:pressed { background-color: #155a9e; }"
        )
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addWidget(button_panel)

    def _make_section(self, title, html_content):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: transparent; }")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            "color: #2a82da; font-size: 11px; font-weight: bold; letter-spacing: 1px;"
        )
        frame_layout.addWidget(title_label)

        content_label = QLabel(html_content)
        content_label.setTextFormat(Qt.RichText)
        content_label.setWordWrap(True)
        content_label.setOpenExternalLinks(True)
        content_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        content_label.setStyleSheet(
            "QLabel { color: #ddd; font-size: 12px; }"
            "code { font-family: Consolas, monospace; }"
        )
        frame_layout.addWidget(content_label)

        return frame

    def center_dialog(self):
        if self.parent():
            x = self.parent().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help - Smart Task Manager")
        self.setMinimumWidth(680)
        self.setMinimumHeight(620)
        self.setModal(True)
        self.setup_ui()
        self.center_dialog()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setStyleSheet("QFrame { background-color: #1e2026; }")
        header.setFixedHeight(70)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel("Help")
        title_label.setStyleSheet("color: #2a82da; font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

        layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: #181a1e; border: none; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #181a1e;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(14)

        content_layout.addWidget(self._make_section(
            "FIRST STEPS",
            "<ol style='color: #ddd; margin: 0; padding-left: 20px;'>"
            "<li>Click <b>+ Add Task</b> or use <b>File -> New Task</b> (Ctrl+N).</li>"
            "<li>Fill in title (required), description, priority and due date.</li>"
            "<li>Click <b>Create Task</b>.</li>"
            "<li>Double-click a row or press <b>Enter</b> to open task details.</li>"
            "</ol>"
        ))

        content_layout.addWidget(self._make_section(
            "TASKS",
            "<ul style='color: #ddd; margin: 0; padding-left: 18px;'>"
            "<li>Each task has: title, description, priority (High / Medium / Low), due date.</li>"
            "<li>Toggle completion with the status button on the row, or press <b>Space</b>.</li>"
            "<li>Double-click a row or press <b>Enter</b> to open details.</li>"
            "<li>Right-click a row for <b>View Details</b>, <b>Mark as Complete / Pending</b>, "
            "<b>Edit Task</b>, <b>Delete Task</b>.</li>"
            "<li>Overdue tasks are highlighted in red.</li>"
            "</ul>"
        ))

        content_layout.addWidget(self._make_section(
            "SEARCH AND FILTERS",
            "<ul style='color: #ddd; margin: 0; padding-left: 18px;'>"
            "<li><b>Search</b> filters by title and description.</li>"
            "<li><b>Status</b> combo: All / Pending / Completed.</li>"
            "<li><b>Priority</b> combo: All / High / Medium / Low.</li>"
            "<li><b>Due Date</b> combo: All / Overdue / Today / Future.</li>"
            "<li><b>Reset</b> clears all filters.</li>"
            "</ul>"
        ))

        content_layout.addWidget(self._make_section(
            "IMPORT AND EXPORT",
            "<ul style='color: #ddd; margin: 0; padding-left: 18px;'>"
            "<li><b>File -> Export</b> (Ctrl+Shift+E) writes all tasks to a JSON file.</li>"
            "<li><b>File -> Import</b> (Ctrl+I) replaces the current dataset with a JSON file. "
            "<b>This overwrites all existing data.</b> A temporary backup of the current file "
            "is created automatically before import.</li>"
            "<li>The exported file includes a small <code>_export_info</code> marker that is "
            "ignored on import.</li>"
            "</ul>"
        ))

        content_layout.addWidget(self._make_section(
            "DESKTOP INTEGRATION (LINUX)",
            "<ul style='color: #ddd; margin: 0; padding-left: 18px;'>"
            "<li><b>File -> Create Desktop Entry</b> creates a launcher in the application menu "
            "and/or on the desktop.</li>"
            "<li>After creation you may need to log out and back in for the menu entry to appear.</li>"
            "<li>The desktop launcher may show an 'Unsecured Application Launcher' warning. "
            "Right-click -> <b>Allow Launching</b> (one-time).</li>"
            "</ul>"
        ))

        content_layout.addWidget(self._make_section(
            "KEYBOARD SHORTCUTS",
            "<table style='color: #ddd; font-size: 12px; border-collapse: collapse;'>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+N</code></td><td>New task</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+I</code></td><td>Import data</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Shift+E</code></td><td>Export data</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Shift+D</code></td><td>Create desktop entry</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Shift+C</code></td><td>Clear completed</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+E</code></td><td>Edit selected task</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Delete</code></td><td>Delete selected task</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Space</code></td><td>Toggle selected task completion</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Enter</code></td><td>View selected task details</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+F</code></td><td>Focus search box</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+R</code></td><td>Reset filters</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>F5</code></td><td>Refresh view</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>F1</code></td><td>Open help</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+/</code></td><td>Keyboard shortcuts</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+A</code></td><td>Open about</td></tr>"
            "<tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Q</code></td><td>Exit</td></tr>"
            "</table>"
        ))

        content_layout.addWidget(self._make_section(
            "DATA LOCATION",
            "<p style='color: #ddd; margin: 0;'>All data is stored locally:</p>"
            "<ul style='color: #ddd; margin: 6px 0 0 0; padding-left: 18px;'>"
            "<li>Tasks: <code>~/.smart_task_manager/tasks.json</code></li>"
            "</ul>"
            "<p style='color: #ddd; margin: 8px 0 0 0;'>"
            "The uninstaller never touches your data. To remove it manually: "
            "<code>rm -rf ~/.smart_task_manager</code>"
            "</p>"
        ))

        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_panel = QFrame()
        button_panel.setStyleSheet("QFrame { background-color: #1e2026; }")
        button_panel.setFixedHeight(60)
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(20, 12, 20, 12)
        button_layout.addStretch()

        ok_button = QPushButton("Close")
        ok_button.setFixedSize(110, 36)
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setStyleSheet(
            "QPushButton { background-color: #2a82da; color: white; font-weight: bold; "
            "border: none; border-radius: 5px; padding: 8px 16px; }"
            "QPushButton:hover { background-color: #1a72ca; }"
            "QPushButton:pressed { background-color: #155a9e; }"
        )
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addWidget(button_panel)

    def _make_section(self, title, html_content):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: transparent; }")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            "color: #2a82da; font-size: 11px; font-weight: bold; letter-spacing: 1px;"
        )
        frame_layout.addWidget(title_label)

        content_label = QLabel(html_content)
        content_label.setTextFormat(Qt.RichText)
        content_label.setWordWrap(True)
        content_label.setOpenExternalLinks(True)
        content_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        content_label.setStyleSheet(
            "QLabel { color: #ddd; font-size: 12px; }"
            "code { font-family: Consolas, monospace; background-color: #23262d; "
            "padding: 2px 6px; border-radius: 3px; color: #2ecc71; }"
            "a:hover { text-decoration: underline; }"
        )
        frame_layout.addWidget(content_label)

        return frame

    def center_dialog(self):
        if self.parent():
            x = self.parent().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)


class ShortcutsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts - Smart Task Manager")
        self.setMinimumWidth(560)
        self.setMinimumHeight(600)
        self.setModal(True)
        self.setup_ui()
        self.center_dialog()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setStyleSheet("QFrame { background-color: #1e2026; }")
        header.setFixedHeight(70)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel("Keyboard Shortcuts")
        title_label.setStyleSheet("color: #2a82da; font-size: 20px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

        layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: #181a1e; border: none; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #181a1e;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(14)

        content_layout.addWidget(self._make_section(
            "FILE",
            [
                ("Ctrl+N", "New task"),
                ("Ctrl+I", "Import data"),
                ("Ctrl+Shift+E", "Export data"),
                ("Ctrl+Shift+D", "Create desktop entry"),
                ("Ctrl+Shift+C", "Clear completed tasks"),
                ("Ctrl+Q", "Exit application"),
            ]
        ))

        content_layout.addWidget(self._make_section(
            "EDIT",
            [
                ("Ctrl+E", "Edit selected task"),
                ("Delete", "Delete selected task"),
                ("Space", "Toggle completion of selected task"),
            ]
        ))

        content_layout.addWidget(self._make_section(
            "VIEW",
            [
                ("Ctrl+F", "Focus search box"),
                ("Ctrl+R", "Reset filters"),
                ("F5", "Refresh view"),
                ("Enter", "View selected task details"),
            ]
        ))

        content_layout.addWidget(self._make_section(
            "HELP",
            [
                ("F1", "Open help"),
                ("Ctrl+/", "Show this dialog"),
                ("Ctrl+A", "Open about"),
            ]
        ))

        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_panel = QFrame()
        button_panel.setStyleSheet("QFrame { background-color: #1e2026; }")
        button_panel.setFixedHeight(60)
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(20, 12, 20, 12)
        button_layout.addStretch()

        ok_button = QPushButton("Close")
        ok_button.setFixedSize(110, 36)
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setStyleSheet(
            "QPushButton { background-color: #2a82da; color: white; font-weight: bold; "
            "border: none; border-radius: 5px; padding: 8px 16px; }"
            "QPushButton:hover { background-color: #1a72ca; }"
            "QPushButton:pressed { background-color: #155a9e; }"
        )
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addWidget(button_panel)

    def _make_section(self, title, items):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: transparent; }")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            "color: #2a82da; font-size: 11px; font-weight: bold; letter-spacing: 1px;"
        )
        frame_layout.addWidget(title_label)

        for key, description in items:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 2, 0, 2)
            row_layout.setSpacing(20)

            key_label = QLabel(key)
            key_label.setFixedWidth(150)
            key_label.setStyleSheet(
                "color: #2ecc71; font-family: Consolas, monospace; "
                "font-size: 12px; font-weight: bold;"
            )
            row_layout.addWidget(key_label)

            desc_label = QLabel(description)
            desc_label.setStyleSheet("color: #ddd; font-size: 12px;")
            row_layout.addWidget(desc_label, 1)

            frame_layout.addWidget(row)

        return frame

    def center_dialog(self):
        if self.parent():
            x = self.parent().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)
