from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QHBoxLayout, QFileDialog, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, qDebug, qWarning
from PySide6.QtGui import QIcon
import gui as st
import transmitter
from pathlib import Path
import resources_rc


class SettingsWindow(QMainWindow):
    def __init__(self, parent=None, game_folder=Path(""), api_key="", check_updates_on_startup=False, save_settings_callback=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 600)
        self.setStyleSheet(f"background-color: {st.DARK_BG}; color: {st.TEXT_COLOR};")

        # Set icon from embedded resource
        icon = QIcon(":/KillAPI.ico")
        self.setWindowIcon(icon)
        QApplication.instance().setWindowIcon(icon)
        

        self.game_folder = game_folder
        self.api_key = api_key
        self.check_updates_on_startup = check_updates_on_startup
        self.save_settings_callback = save_settings_callback

        self.main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.add_update_card()
        self.add_path_card()
        self.add_api_card()
        
    def add_update_card(self):
        update_card = QWidget()
        update_card.setStyleSheet(st.CARD_STYLE)
        update_card.setFixedWidth(450)
        update_layout = QVBoxLayout(update_card)
        update_layout.setAlignment(Qt.AlignCenter)
        update_layout.setSpacing(10)

        update_label = QLabel("Check for Updates")
        update_label.setFont(st.FONT_LABEL)
        update_label.setStyleSheet(f"color: {st.TEXT_COLOR};")
        update_layout.addWidget(update_label)

        self.update_checkbox = QCheckBox("Check for new versions on startup")
        self.update_checkbox.setFont(st.FONT_LABEL)
        self.update_checkbox.setStyleSheet(f"color: {st.TEXT_COLOR};")
        self.update_checkbox.setTristate(False)
        self.update_checkbox.setChecked(self.check_updates_on_startup)
        self.update_checkbox.stateChanged.connect(self.toggle_update_check)
        update_layout.addWidget(self.update_checkbox)

        self.update_btn = QPushButton("Check for updates now")
        self.update_btn.setFont(st.FONT_BUTTON)
        self.update_btn.setStyleSheet(st.BUTTON_STYLE)
        self.update_btn.clicked.connect(self.parent().check_for_updates)
        update_layout.addWidget(self.update_btn)

        self.main_layout.addWidget(update_card, alignment=Qt.AlignHCenter)

    def add_path_card(self):
        path_card = QWidget()
        path_card.setStyleSheet(st.CARD_STYLE)
        path_card.setFixedWidth(450)
        path_layout = QVBoxLayout(path_card)
        path_layout.setAlignment(Qt.AlignCenter)
        path_layout.setSpacing(10)

        path_label = QLabel("Game LIVE Folder Path")
        path_label.setFont(st.FONT_LABEL)
        path_label.setStyleSheet(f"color: {st.TEXT_COLOR};")
        path_layout.addWidget(path_label)

        self.path_edit = QLineEdit()
        self.path_edit.setText(str(self.game_folder))
        self.path_edit.setFont(st.FONT_LABEL)
        self.path_edit.setStyleSheet(st.ENTRY_STYLE)
        self.path_edit.setPlaceholderText("Enter LIVE folder path")
        path_layout.addWidget(self.path_edit)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        browse_btn = QPushButton("Browse")
        browse_btn.setFont(st.FONT_BUTTON)
        browse_btn.setStyleSheet(st.HALF_BUTTON_STYLE)
        browse_btn.clicked.connect(self.update_path)
        button_layout.addWidget(browse_btn)

        save_btn = QPushButton("Save")
        save_btn.setFont(st.FONT_BUTTON)
        save_btn.setStyleSheet(st.HALF_BUTTON_STYLE)
        save_btn.clicked.connect(self.save_path)
        button_layout.addWidget(save_btn)

        path_layout.addLayout(button_layout)
        self.main_layout.addWidget(path_card, alignment=Qt.AlignHCenter)

    def add_api_card(self):
        api_card = QWidget()
        api_card.setStyleSheet(st.CARD_STYLE)
        api_card.setFixedWidth(450)
        api_layout = QVBoxLayout(api_card)
        api_layout.setAlignment(Qt.AlignCenter)
        api_layout.setSpacing(10)

        api_label = QLabel("KillAPI Key")
        api_label.setFont(st.FONT_LABEL)
        api_label.setStyleSheet(f"color: {st.TEXT_COLOR};")
        api_layout.addWidget(api_label)

        self.api_edit = QLineEdit()
        self.api_edit.setEchoMode(QLineEdit.Password)
        self.api_edit.setText(self.api_key)
        self.api_edit.setFont(st.FONT_LABEL)
        self.api_edit.setStyleSheet(st.ENTRY_STYLE)
        self.api_edit.setPlaceholderText("Enter your API key")
        api_layout.addWidget(self.api_edit)

        save_api_btn = QPushButton("Save API Key")
        save_api_btn.setFont(st.FONT_BUTTON)
        save_api_btn.setStyleSheet(st.BUTTON_STYLE)
        save_api_btn.clicked.connect(self.save_api_key)
        api_layout.addWidget(save_api_btn)

        self.main_layout.addWidget(api_card, alignment=Qt.AlignHCenter)

    def toggle_update_check(self, state):
        qDebug(f"toggle_update_check called with state: {state} ({type(state)})")
        qDebug(f"Qt.CheckState.Checked = {Qt.CheckState.Checked} ({type(Qt.CheckState.Checked)})")
        qDebug(f"Comparison result: {state == Qt.CheckState.Checked.value}")

        self.check_updates_on_startup = state == Qt.CheckState.Checked.value

        qDebug(f"toggle_update_check: New state is {self.check_updates_on_startup}")
        self.save_settings()

    def update_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Game Folder", str(self.game_folder))
        if folder:
            self.game_folder = folder
            self.path_edit.setText(folder)
            self.save_settings()

    def save_path(self):
        self.game_folder = self.path_edit.text().strip()
        self.save_settings()

    def save_api_key(self):
        self.api_key = self.api_edit.text().strip()
        if self.save_settings_callback:
            self.save_settings_callback(self.game_folder, self.api_key, self.check_updates_on_startup)

        if self.api_key:
            success = transmitter.send_connection_success(str(self.game_folder), self.api_key)
            if success:
                QMessageBox.information(self, "Success", "KillAPI connected successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to connect to KillAPI. Please check your API key.")
                self.api_key = ""
        if self.save_settings_callback:
            self.save_settings_callback(self.game_folder, self.api_key, self.check_updates_on_startup)

    def save_settings(self):
        if self.save_settings_callback:
            self.save_settings_callback(self.game_folder, self.api_key, self.check_updates_on_startup)
            qDebug("Invoking save_settings_callback...")  # Debug log
        else:
            qWarning("save_settings_callback is None!")  # Debug log
       