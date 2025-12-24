# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QColor


class LabelWidget(QWidget):

    def __init__(self, label_name: str, color: str, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(6, 3, 6, 3)
        self.layout.setSpacing(5)

        self.color_indicator = QLabel()
        self.color_indicator.setFixedSize(12, 12)
        self.color_indicator.setStyleSheet(f"""
            background-color: {color};
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """)

        self.text_label = QLabel(label_name)
        self.text_label.setStyleSheet("""
            font-size: 11px;
            font-weight: 500;
            padding: 1px 0px;
        """)

        self.layout.addWidget(self.color_indicator)
        self.layout.addWidget(self.text_label)
        self.layout.addStretch()

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.adjust_color_brightness(color, 0.2)};
                border: 1px solid {self.adjust_color_brightness(color, 0.1)};
                border-radius: 4px;
                padding: 0px;
            }}
        """)
        self.setFixedHeight(24)

    def adjust_color_brightness(self, color_hex: str, factor: float) -> str:
        color = QColor(color_hex)
        h, s, v, a = color.getHsv()
        v = min(255, int(v * (1 - factor)))
        return QColor.fromHsv(h, s, v, a).name()

    def set_label(self, label_name: str, color: str):
        self.color_indicator.setStyleSheet(f"""
            background-color: {color};
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        """)
        self.text_label.setText(label_name)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.adjust_color_brightness(color, 0.2)};
                border: 1px solid {self.adjust_color_brightness(color, 0.1)};
                border-radius: 4px;
                padding: 0px;
            }}
        """)
