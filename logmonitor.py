import time
import re

from PySide6.QtCore import QThread, Signal, QObject, qDebug, qWarning
from PySide6.QtWidgets import QMainWindow
import transmitter  # Handles API event sending
from pathlib import Path

# Regex patterns for different log events
KILL_LOG_PATTERN = r"CActor::Kill: '([^']+)' .*? killed by '([^']+)' .*? using '[^']+' \[\s*Class ([^\]]+)\s*\] with damage type '[^']+'"
VEHICLE_SOFT_DEATH_PATTERN = r"CVehicle::OnAdvanceDestroyLevel: Vehicle '([^']+)' .*? driven by '([^']+)' .*? advanced from destroy level 0 to 1 caused by '([^']+)'"
VEHICLE_DESTRUCTION_PATTERN = r"CVehicle::OnAdvanceDestroyLevel: Vehicle '([^']+)' .*? driven by '([^']+)' .*? advanced from destroy level 1 to 2 caused by '([^']+)'"
PLAYER_CONNECT_PATTERN = r"<Expect Incoming Connection>.*?nickname=\"([^\"]+)\""
PLAYER_DISCONNECT_PATTERN = r"\[CIG\] CCIGBroker::FastShutdown"

# Prefixes for entity name cleaning
ENTITY_PREFIXES = [
    "PU_Human_Enemy_GroundCombat_NPC_",
    "AIModule_Unmanned_PU_"
]

class LogMonitor(QObject):
    event_detected = Signal(str)  # Signal to emit events as strings

    def __init__(self, log_file_path, api_key):
        """Initialize with log file path and API key."""
        super().__init__()
        self.log_file_path = log_file_path
        self.api_key = api_key
        self.running = False
        self.last_player_name = None  # Store last connected player name
        qDebug(f"LogMonitor initialized with log_file_path={self.log_file_path}, api_key={self.api_key[:4]}...")

    def update_settings(self, log_file_path, api_key):
        """Update the log file path and API key."""
        self.log_file_path = log_file_path
        self.api_key = api_key
        qDebug(f"LogMonitor settings updated: log_file_path={self.log_file_path}, api_key={self.api_key[:4]}...")

    def start_monitoring(self):
        """Monitor the log file for new entries."""
        self.running = True
        qDebug(f"Monitoring {self.log_file_path} for new entries...")
        log_path = Path(self.log_file_path)
        try:
            with log_path.open('r', encoding='utf-8', errors='replace') as f:
                f.seek(log_path.stat().st_size)
                while self.running:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)  # Wait if no new lines
                        continue
                    qDebug(f"Read line: {line.strip()}")
                    self.parse_line(line)
        except Exception as e:
            qWarning(f"Log monitoring error: {e}")

    def parse_line(self, line):
        """Parse a log line to extract and format event details."""
        try:
            # Check for kill events
            kill_match = re.search(KILL_LOG_PATTERN, line)
            if kill_match:
                victim = self.pretty_name(kill_match.group(1))
                killer = self.pretty_name(kill_match.group(2))
                tool_class = kill_match.group(3).replace("_", " ")  # Remove underscores from tool name
                event_text = f"{killer} killed {victim} using {tool_class}"
                qDebug(f"Detected kill event: {event_text}")
                transmitter.send_event({"identifier": "kill_log", "killer": killer, "victim": victim, "kill_mechanism": tool_class}, self.api_key)
                self.event_detected.emit(event_text)  # Emit the event
                return

            # Check for vehicle soft death
            soft_death_match = re.search(VEHICLE_SOFT_DEATH_PATTERN, line)
            if soft_death_match:
                vehicle_raw = soft_death_match.group(1)
                driver = self.pretty_name(soft_death_match.group(2))
                cause = self.pretty_name(soft_death_match.group(3))
                vehicle = self.clean_vehicle_name(vehicle_raw)
                event_text = f"{cause} put vehicle {vehicle} of {driver} in soft death state"
                qDebug(f"Detected vehicle soft death: {event_text}")
                transmitter.send_event({"identifier": "vehicle_soft_death", "event_text": event_text}, self.api_key)
                self.event_detected.emit(event_text)  # Emit the event
                return

            # Check for vehicle destruction
            destruction_match = re.search(VEHICLE_DESTRUCTION_PATTERN, line)
            if destruction_match:
                vehicle_raw = destruction_match.group(1)
                driver = self.pretty_name(destruction_match.group(2))
                cause = self.pretty_name(destruction_match.group(3))
                vehicle = self.clean_vehicle_name(vehicle_raw)
                event_text = f"{cause} destroyed {vehicle} of {driver} completely"
                qDebug(f"Detected vehicle destruction: {event_text}")
                transmitter.send_event({"identifier": "vehicle_destruction", "event_text": event_text}, self.api_key)
                self.event_detected.emit(event_text)  # Emit the event
                return

            # Check for player connection
            connect_match = re.search(PLAYER_CONNECT_PATTERN, line)
            if connect_match:
                player = self.pretty_name(connect_match.group(1))
                self.last_player_name = player  # Store the player name
                event_text = f"{player} connected"
                qDebug(f"Detected player connection: {event_text}")
                transmitter.send_event({"identifier": "player_connect", "event_text": event_text}, self.api_key)
                self.event_detected.emit(event_text)  # Emit the event
                return

            # Check for player disconnection
            disconnect_match = re.search(PLAYER_DISCONNECT_PATTERN, line)
            if disconnect_match:
                if self.last_player_name:
                    event_text = f"{self.last_player_name} disconnected"
                    qDebug(f"Detected player disconnection: {event_text}")
                    transmitter.send_event({"identifier": "player_disconnect", "event_text": event_text}, self.api_key)
                    self.event_detected.emit(event_text)  # Emit the event
                else:
                    qWarning("Skipped disconnect: no known player")
                self.last_player_name = None  # Clear after processing
                return
        except Exception as e:
            qWarning(f"Error parsing line: {line.strip()} - {e}")

    def stop_monitoring(self):
        """Stop monitoring the log file."""
        self.running = False
        qDebug("Monitoring stopped")

    def pretty_name(self, name):
        """Remove entity prefixes, trailing numbers, and replace underscores with spaces."""
        for prefix in ENTITY_PREFIXES:
            if name.startswith(prefix):
                name = name[len(prefix):]
                break
        name = re.sub(r'_\d+$|\d+$', '', name)
        return name.replace("_", " ")

    def clean_vehicle_name(self, vehicle):
        """Remove underscores and trailing numbers from vehicle names."""
        vehicle = re.sub(r'_\d+$', '', vehicle)
        return vehicle.replace("_", " ")

class MonitorThread(QThread):
    def __init__(self, log_file_path, api_key, parent=None):
        """Initialize the monitoring thread."""
        super().__init__(parent)
        self.log_file_path = log_file_path
        self.api_key = api_key
        self._running = True
        self.logmonitor = LogMonitor(log_file_path, api_key)

    def run(self):
        """Run the monitoring loop."""
        self.logmonitor.start_monitoring()

    def stop(self):
        """Stop the thread."""
        self._running = False
        self.logmonitor.stop_monitoring()

class LogDisplayWindow(QMainWindow):
    window_closed = Signal()  # Signal to notify when the window is closed

    def closeEvent(self, event):
        """Handle the window close event."""
        self.window_closed.emit()  # Emit the signal
        super().closeEvent(event)