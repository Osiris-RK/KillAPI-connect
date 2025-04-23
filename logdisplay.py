import json
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QTextEdit, QWidget, QPushButton, QHBoxLayout, QColorDialog, QApplication
from PySide6.QtCore import Qt, Signal, qDebug, qWarning
from PySide6.QtGui import QIcon

import gui as st

class LogDisplayWindow(QMainWindow):
    LOG_BG_COLOR = "#1e1e1e"
    LOG_FG_COLOR = "#dcdcdc"
    LOG_FONT_SIZE = 12  # Default font size
    window_closed = Signal()  # Signal to notify when the window is closed
    geometry_changed = Signal()  # Signal to notify when the geometry changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Killfeed Log Display")
        self.setFixedSize(600, 400)

        # Main layout
        self.main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Set icon from embedded resource
        icon = QIcon(":/KillAPI.ico")
        self.setWindowIcon(icon)
        QApplication.instance().setWindowIcon(icon)

        # Read-only text field
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.apply_colors()  # Apply the default colors
        self.main_layout.addWidget(self.log_display)

        # Event buffer
        self.event_buffer = []

        # Add buttons at the bottom
        self.add_buttons()
        self.add_event("Killfeed Log Display Initialized")

    def add_event(self, event_text):
        """
        Add a new event to the log display.
        Keeps the buffer to 20 lines and ensures 2 blank lines at the bottom.
        """
        try:
            qDebug(f"Adding event to log display: {event_text}")
            self.event_buffer.append(event_text)
            self.event_buffer = self.event_buffer[-20:]  # Keep only the last 20 lines
            padded_buffer = self.event_buffer + ["", ""]  # Add 2 blank lines for visual separation
            self.log_display.setPlainText("\n".join(padded_buffer))
            self.log_display.verticalScrollBar().setValue(self.log_display.verticalScrollBar().maximum())
        except Exception as e:
            qWarning(f"Error adding event to log display: {e}")

    def add_buttons(self):
        """Add buttons to the bottom of the window."""
        button_layout = QHBoxLayout()

        # Clear button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_log)
        button_layout.addWidget(clear_button)

        # Text Color button
        text_color_button = QPushButton("Text Color")
        text_color_button.clicked.connect(self.change_text_color)
        button_layout.addWidget(text_color_button)

        # Background Color button
        bg_color_button = QPushButton("Background Color")
        bg_color_button.clicked.connect(self.change_background_color)
        button_layout.addWidget(bg_color_button)

        # Font Size Increase button
        increase_font_button = QPushButton("+")
        increase_font_button.setToolTip("Increase font size, <br>&lt;Ctrl&gt; + &lt;+&gt; to increase font size")
        increase_font_button.setShortcut("Ctrl++")  # Set shortcut for increasing font size
        increase_font_button.setFixedWidth(30)
        increase_font_button.clicked.connect(self.increase_font_size)
        button_layout.addWidget(increase_font_button)

        # Font Size Decrease button
        decrease_font_button = QPushButton("-")
        decrease_font_button.setToolTip("Decrease font size, <br>&lt;Ctrl&gt; + &lt;-&gt; to decrease font size")
        decrease_font_button.setShortcut("Ctrl+-")
        decrease_font_button.setFixedWidth(30)
        decrease_font_button.clicked.connect(self.decrease_font_size)
        button_layout.addWidget(decrease_font_button)

        # Add the button layout to the main layout
        self.main_layout.addLayout(button_layout)

    def clear_log(self):
        """Clear the log display."""
        self.event_buffer = []
        self.log_display.clear()
        self.add_event("Killfeed Log Display Cleared")

    def change_text_color(self):
        """Change the text color using a color dialog."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.LOG_FG_COLOR = color.name()
            self.apply_colors()
            self.parent().update_log_display_colors(self.LOG_BG_COLOR, self.LOG_FG_COLOR)  # Notify MainWindow
            self.parent().update_log_display_geometry()  # Save the latest geometry

    def change_background_color(self):
        """Change the background color using a color dialog."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.LOG_BG_COLOR = color.name()
            self.apply_colors()
            self.parent().update_log_display_colors(self.LOG_BG_COLOR, self.LOG_FG_COLOR)  # Notify MainWindow
            self.parent().update_log_display_geometry()  # Save the latest geometry

    def apply_colors(self):
        """Apply the current foreground and background colors and font size to the log display."""
        self.log_display.setStyleSheet(
            f"background-color: {self.LOG_BG_COLOR}; color: {self.LOG_FG_COLOR}; font-family: Consolas; font-size: {self.LOG_FONT_SIZE}px;"
        )

    def set_colors(self, bg_color, fg_color):
        """Set the colors for the log display."""
        self.LOG_BG_COLOR = bg_color
        self.LOG_FG_COLOR = fg_color
        self.apply_colors()

    def increase_font_size(self):
        """Increase the font size of the log display."""
        self.LOG_FONT_SIZE += 1
        self.apply_colors()
        self.parent().update_log_display_font_size(self.LOG_FONT_SIZE)  # Notify MainWindow

    def decrease_font_size(self):
        """Decrease the font size of the log display."""
        if self.LOG_FONT_SIZE > 1:  # Prevent font size from going below 1
            self.LOG_FONT_SIZE -= 1
            self.apply_colors()
            self.parent().update_log_display_font_size(self.LOG_FONT_SIZE)  # Notify MainWindow

    def closeEvent(self, event):
        """Handle the window close event for the Log Display Window."""
        if self.isVisible():  # Ensure this is only triggered when the Log Display Window is being closed
            qDebug("LogDisplayWindow is being closed.")
            self.window_closed.emit()  # Emit the signal when the window is closed

            # Save the geometry to the parent (MainWindow)
            if self.parent():
                self.parent().save_log_display_geometry(self.saveGeometry())
        super().closeEvent(event)

    def moveEvent(self, event):
        """Emit a signal when the window is moved."""
        self.geometry_changed.emit()
        super().moveEvent(event)

    def resizeEvent(self, event):
        """Emit a signal when the window is resized."""
        self.geometry_changed.emit()
        super().resizeEvent(event)
