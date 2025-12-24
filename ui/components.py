# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRect


class ProgressWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("Progress: 0%")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-weight: bold; color: #fff;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 3px;
                background-color: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #2a82da;
                border-radius: 3px;
            }
        """)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress_bar)

    def set_progress(self, value: float):
        self.progress_bar.setValue(int(value))
        self.label.setText(f"Progress: {value:.1f}%")


class PriorityIndicator(QWidget):

    def __init__(self, priority: int, parent=None):
        super().__init__(parent)
        self.priority = priority
        self.setFixedSize(24, 24)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.priority == 1:
            color = QColor("#ff6b6b")
        elif self.priority == 2:
            color = QColor("#ffd166")
        else:
            color = QColor("#8ac926")

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
        painter.drawEllipse(2, 2, 20, 20)

        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(QRect(0, 0, 24, 24), Qt.AlignCenter, str(self.priority))


class StatusWidget(QWidget):

    def __init__(self, completed: bool, parent=None):
        super().__init__(parent)
        self.completed = completed
        self.setFixedSize(90, 26)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.completed:
            painter.setBrush(QBrush(QColor("#2e7d32")))
            painter.setPen(QPen(QColor("#1b5e20"), 1))
            painter.drawRoundedRect(0, 0, 90, 26, 5, 5)

            painter.setPen(QPen(Qt.white))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            painter.drawText(QRect(0, 0, 90, 26), Qt.AlignCenter, "✅ Done")
        else:
            painter.setBrush(QBrush(QColor("#ff9800")))
            painter.setPen(QPen(QColor("#e65100"), 1))
            painter.drawRoundedRect(0, 0, 90, 26, 5, 5)

            painter.setPen(QPen(Qt.white))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            painter.drawText(QRect(0, 0, 90, 26), Qt.AlignCenter, "⏳ Pending")
