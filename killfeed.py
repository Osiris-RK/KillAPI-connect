from pathlib import Path
import json
import appdirs
from sys import exit as sys_exit  # Avoids `sys.exit()` call
import webbrowser

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
)
from PySide6.QtCore import (Qt, QProcess, QThread,qDebug, qWarning)
import resources_rc
from PySide6.QtGui import QIcon


import gui as st
import transmitter
from killsettings import SettingsWindow
from logdisplay import LogDisplayWindow  # Import the new LogDisplayWindow
from logmonitor import LogMonitor  # Import the LogMonitor

APP_NAME = "Killfeed"
APP_AUTHOR = "KindPerspective"
APP_VERSION = "0.0.2"
APP_REPO = "Poekhavshiy/KillAPI-connect"
APP_URL = "https://github.com/Poekhavshiy/KillAPI-connect/releases/latest/download/KillAPi.connect.exe"
USER_DATA_DIR = Path(appdirs.user_data_dir(APP_NAME, APP_AUTHOR))
SETTINGS_FILE = USER_DATA_DIR / "settings.json"
REQUIRED_FILES = ["Game.log", "StarCitizen_Launcher.exe"]
DEFAULT_SC_PATH = "C:\\Program Files\\Roberts Space Industries\\StarCitizen\\LIVE"
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KillAPI connect")
        self.setMinimumSize(700, 600)
        self.resize(900, 700)

        # Initialize the log display window
        self.log_display_window = LogDisplayWindow(self)
        self.log_display_window_hidden = True  # Track visibility state

        # Connect the window_closed signal
        self.log_display_window.window_closed.connect(self.on_log_display_window_closed)

        # Connect the geometry_changed signal
        self.log_display_window.geometry_changed.connect(self.update_log_display_geometry)

        # Load settings
        self.settings = self.load_settings_from_file()

        # Initialize the log display button early
        self.log_display_btn = QPushButton("View Log")
        self.log_display_btn.setFont(st.FONT_BUTTON)
        self.log_display_btn.setStyleSheet(st.BUTTON_STYLE)
        self.log_display_btn.clicked.connect(self.toggle_log_display_window)

        # Restore log display window state
        self.restore_log_display_window_state()

        # Set icon from embedded resource
        icon = QIcon(":/KillAPI.ico")
        self.setWindowIcon(icon)
        QApplication.instance().setWindowIcon(icon)

        self.game_folder = Path(DEFAULT_SC_PATH)
        self.log_file_path = self.game_folder / "Game.log"
        self.game_exe_path = self.game_folder / "StarCitizen_Launcher.exe"
        self.api_key = ""
        self.monitoring = False
        self.last_api_update = 0
        self.check_updates_on_startup = False

        # Initialize the log monitor and thread
        qDebug("Initializing log monitor")
        self.log_monitor_thread = QThread()
        self.log_monitor = LogMonitor(self.log_file_path, self.api_key)
        self.log_monitor.moveToThread(self.log_monitor_thread)

        # Connect signals
        qDebug("Connecting log monitor signals")
        self.log_monitor.event_detected.connect(self.log_display_window.add_event)  # Connect signal to log display
        self.log_monitor_thread.started.connect(self.log_monitor.start_monitoring)
        qDebug(f"Log monitor initialized with log file: {self.log_file_path}")

        # Central widget with background color
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {st.DARK_BG};")
        self.setCentralWidget(central_widget)

        # Main layout directly on central widget
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # Settings button
        self.settings_btn = QPushButton("Configure")
        self.settings_btn.setFont(st.FONT_BUTTON)
        self.settings_btn.setStyleSheet(st.BUTTON_STYLE)
        self.settings_btn.clicked.connect(self.open_settings_window)

        qDebug("Initializing UI content")
        self.init_ui_content()
        qDebug("Loading settings")
        self.load_settings()
        qDebug("Checking paths")
        self.check_path()

        # Restore log display window state
        self.restore_log_display_window_state()

        if self.check_updates_on_startup:
            self.check_for_updates(startup=True)

    def closeEvent(self, event):
        """Handle the window close event for the Main Window."""
        if self.log_display_window.isVisible():
            self.log_display_window.close()  # Explicitly close the Log Display Window
        super().closeEvent(event)

    def init_ui_content(self):
        self.main_layout.addStretch()

        self.monitor_btn = QPushButton("Start Monitoring")
        self.monitor_btn.setFont(st.FONT_BUTTON)
        self.monitor_btn.setStyleSheet(st.BUTTON_STYLE)
        self.monitor_btn.clicked.connect(self.toggle_monitoring)
        qDebug("Monitor button connected")
        self.main_layout.addWidget(self.monitor_btn, alignment=Qt.AlignHCenter)

        self.main_layout.addWidget(self.settings_btn, alignment=Qt.AlignHCenter)

        # Add the log display button to the layout
        self.main_layout.addWidget(self.log_display_btn, alignment=Qt.AlignHCenter)

        self.status_lbl = QLabel("")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setFont(st.FONT_STATUS)
        self.status_lbl.setStyleSheet(st.STATUS_STYLE)
        self.main_layout.addWidget(self.status_lbl, alignment=Qt.AlignHCenter)

        self.main_layout.addStretch()

    def open_settings_window(self):
        self.settings_window = SettingsWindow(
            parent=self,
            game_folder=self.game_folder,
            api_key=self.api_key,
            check_updates_on_startup=self.check_updates_on_startup,
            save_settings_callback=self.update_settings
        )
        self.settings_window.show()

    def toggle_log_display_window(self):
        """Toggle the visibility of the log display window."""
        if self.log_display_window_hidden:
            self.log_display_window.show()
            self.log_display_btn.setText("Hide Log")
            self.log_display_window_hidden = False
        else:
            self.log_display_window.hide()
            self.log_display_btn.setText("View Log")
            self.log_display_window_hidden = True

        # Save the visibility state of the Log Display Window
        self.settings["log_display_visible"] = not self.log_display_window_hidden
        self.save_settings_to_file(self.settings)

    def on_log_display_window_closed(self):
        """Handle the log display window being closed."""
        self.log_display_btn.setText("View Log")
        self.log_display_window_hidden = True

        # Save the visibility state of the Log Display Window
        self.settings["log_display_visible"] = False  # Explicitly set to false when the Log Display Window is closed
        self.save_settings_to_file(self.settings)

    def update_log_display_geometry(self):
        """Update the geometry of the Log Display Window in the settings."""
        geometry_hex = self.log_display_window.saveGeometry().data().hex()
        self.settings["log_display_geometry"] = geometry_hex
        self.save_settings_to_file(self.settings)
        qDebug(f"Updated log display geometry: {geometry_hex}")

    def update_log_display_colors(self, bg_color, fg_color):
        """Update the log display colors in the settings."""
        self.settings["log_bg_color"] = bg_color
        self.settings["log_fg_color"] = fg_color
        self.save_settings_to_file(self.settings)

    def update_log_display_font_size(self, font_size):
        """Update the log display font size in the settings."""
        self.settings["log_font_size"] = font_size
        self.save_settings_to_file(self.settings)

    def save_log_display_geometry(self, geometry):
        """Save the geometry of the Log Display Window to the settings."""
        self.settings["log_display_geometry"] = geometry.data().hex()
        self.save_settings_to_file(self.settings)

    def restore_log_display_window_state(self):
        """Restore the visibility state, geometry, colors, and font size of the Log Display Window."""
        if self.settings.get("log_display_visible", False):
            self.log_display_window.show()
            self.log_display_btn.setText("Hide Log")
            self.log_display_window_hidden = False
        else:
            self.log_display_window.hide()
            self.log_display_btn.setText("View Log")
            self.log_display_window_hidden = True

        # Restore geometry
        geometry_hex = self.settings.get("log_display_geometry")
        if geometry_hex:
            self.log_display_window.restoreGeometry(bytes.fromhex(geometry_hex))

        # Restore colors
        bg_color = self.settings.get("log_bg_color", "#1e1e1e")
        fg_color = self.settings.get("log_fg_color", "#dcdcdc")
        self.log_display_window.set_colors(bg_color, fg_color)

        # Restore font size
        font_size = self.settings.get("log_font_size", 12)
        self.log_display_window.LOG_FONT_SIZE = font_size
        self.log_display_window.apply_colors()

    def save_settings_to_file(self, settings):
        """Save settings to the JSON file."""
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f, indent=4)
            qDebug(f"Settings saved to file: {SETTINGS_FILE}")
        except Exception as e:
            qWarning(f"Error saving settings: {e}")

    def load_settings_from_file(self):
        """Load settings from the JSON file."""
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                qWarning(f"Error loading settings from file: {e}")
        return {}

    def update_settings(self, game_folder, api_key, check_updates_on_startup):
        qDebug(f"update_settings called with: game_folder={game_folder}, api_key={api_key}, check_updates_on_startup={check_updates_on_startup}")  # Debug log
        self.game_folder = Path(game_folder)
        self.api_key = api_key
        self.check_updates_on_startup = check_updates_on_startup
        self.log_file_path = self.game_folder / "Game.log"
        self.game_exe_path = self.game_folder / "StarCitizen_Launcher.exe"
        self.log_monitor.update_settings(self.log_file_path, self.api_key)  # Update log monitor settings
        self.save_settings()
        self.check_path()

    def check_for_updates(self, startup=False):
        try:
            from checkversion import get_latest_version
            latest_version = get_latest_version(APP_REPO)
            if latest_version > APP_VERSION:
                self.show_update_popup(latest_version)
            elif not startup:
                QMessageBox.information(self, "No Updates", "You are already on the latest version.")
        except Exception as e:
            if not startup:
                QMessageBox.warning(self, "Error", f"Failed to check for updates: {e}")

    def show_update_popup(self, latest_version):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Update Available")
        msg_box.setText(
            f"A newer version has been found.\n\n"
            f"You are currently on version {APP_VERSION}, and the latest version is {latest_version}.\n\n"
            f"Would you like to be redirected to the latest download?"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec()
        if result == QMessageBox.Yes:
            webbrowser.open(APP_URL)

    def game_running(self):
        """
        Checks if a process with the given name is running (Windows only).
        Example: process_name = "tool.exe"
        """
        process = QProcess()
        process_name = "StarCitizen_Launcher.exe" 
        # Construct and start: tasklist /FI "IMAGENAME eq tool.exe"
        qDebug(f"Checking if process {process_name} is running")
        process.start("tasklist", ["/FI", f"IMAGENAME eq {process_name}"])
        if not process.waitForFinished(2000):  # 2 seconds timeout
            return False  # failed to execute
        qDebug(f"Process output: {process.readAllStandardOutput()}")
        output = bytes(process.readAllStandardOutput()).decode("utf-8")
        return process_name.lower() in output.lower()


    def check_path(self):
        qDebug(f"Checking log file path: {self.log_file_path}")
        qDebug(f"Checking exe path: {self.game_exe_path}")
        if self.log_file_path.exists() and self.game_exe_path.is_file(): # and self.game_running():
            self.set_status("Ready")
        else:
            self.set_status("Invalid path")
        self.save_settings()

    def set_status(self, text):
        self.status_lbl.setText(text)
        qDebug(f"Status set to: {text}")

    def toggle_monitoring(self):
        qDebug("Toggle monitoring called")
        if not self.monitoring:
            raw_folder = str(self.game_folder)  # This might be a user input string
            folder = Path(raw_folder.strip())  # Strip first, then convert to Path
            qDebug(f"Game folder: {folder}")
            if not folder or not self.log_file_path.exists() or not self.game_exe_path.is_file():
                self.set_status("Invalid path")
                qWarning("Invalid path detected")
                return
            if not self.api_key:
                self.set_status("No API key provided")
                qWarning("No API key provided")
                return
            self.start_monitoring()
            self.monitor_btn.setText("Monitoring: On")
            self.monitoring = True
        else:
            self.stop_monitoring()
            self.monitor_btn.setText("Monitoring: Off")
            self.monitoring = False
    def start_monitoring(self):
        """Start the log monitor."""
        qDebug("Starting monitoring")
        self.log_monitor_thread.start()

    def stop_monitoring(self):
        """Stop the log monitor."""
        qDebug("Stopping monitoring")
        self.log_monitor.stop_monitoring()
        self.log_monitor_thread.quit()
        self.log_monitor_thread.wait()

    def save_settings(self):
        settings = {
            "game_folder": str(self.game_folder),
            "api_key": self.api_key,
            "check_updates_on_startup": self.check_updates_on_startup,
            "log_file_path": str(self.log_file_path),
            "game_exe_path": str(self.game_exe_path),
            "log_display_visible": self.log_display_window_hidden,
            "log_display_geometry": self.log_display_window.saveGeometry().data().hex(),
            "log_bg_color": self.log_display_window.LOG_BG_COLOR,
            "log_fg_color": self.log_display_window.LOG_FG_COLOR,
            "log_font_size": self.log_display_window.LOG_FONT_SIZE,
            }
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f, indent=4)
            qDebug(f"Settings saved to: {SETTINGS_FILE} {settings}")
        except Exception as e:
            qWarning(f"Error saving settings: {e}")

    def load_settings(self):
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    self.game_folder = Path(settings.get("game_folder", self.game_folder))
                    self.api_key = settings.get("api_key", "")
                    self.check_updates_on_startup = settings.get("check_updates_on_startup", False)
                    self.log_file_path = self.game_folder / "Game.log"
                    self.game_exe_path = self.game_folder / "StarCitizen_Launcher.exe"
                    self.log_display_window_hidden = settings.get("log_display_visible", True)
                    self.log_display_window.LOG_BG_COLOR = settings.get("log_bg_color", self.log_display_window.LOG_BG_COLOR)
                    self.log_display_window.LOG_FG_COLOR = settings.get("log_fg_color", self.log_display_window.LOG_FG_COLOR)
                    self.log_display_window.LOG_FONT_SIZE = settings.get("log_font_size", self.log_display_window.LOG_FONT_SIZE)
                    if settings.get("log_display_geometry"):
                        self.log_display_window.restoreGeometry(bytes.fromhex(settings["log_display_geometry"]))
                    self.log_display_window.set_colors(self.log_display_window.LOG_BG_COLOR, self.log_display_window.LOG_FG_COLOR)
                    self.log_display_window.set_font_size(self.log_display_window.LOG_FONT_SIZE)
                    self.log_display_window.setGeometry(settings.get("log_display_geometry", self.log_display_window.saveGeometry()))
                    self.log_display_btn.setText("Hide Log" if not self.log_display_window_hidden else "View Log")
                    self.log_monitor = LogMonitor(self.log_file_path, self.api_key)
                    self.log_monitor.update_settings(self.log_file_path, self.api_key)  # Update log monitor settings
                    self.check_path()
                    qDebug(f"Settings loaded from: {SETTINGS_FILE}, log file path: {self.log_file_path}, game exe path: {self.game_exe_path}, API key: {self.api_key[:4]}..., self.check_updates_on_startup")
            except Exception as e:
                qWarning(f"Error loading settings: {e}")

def main():
    app = QApplication([])
    st.load_fonts()
    window = MainWindow()
    window.show()
    sys_exit(app.exec())

if __name__ == "__main__":
    main()