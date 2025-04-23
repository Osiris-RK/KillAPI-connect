# Killfeed Application

Killfeed is a PySide6-based desktop application designed to monitor and display real-time logs from **Star Citizen**. It provides a user-friendly interface for managing log files, monitoring events, and customizing the display of log data. The application is built with extensibility and ease of use in mind, allowing users to configure settings, monitor logs, and interact with the application seamlessly.

---

## Features

- **Log Monitoring**: Continuously monitor the `Game.log` file for real-time updates.
- **Customizable Log Display**: Change the background color, text color, and font size of the log display window.
- **Dynamic Window Management**: The `LogDisplayWindow` remembers its position, size, and visibility state across sessions.
- **Settings Management**: All configurations are saved to a single `settings.json` file.
- **Update Checker**: Automatically check for updates to the application.
- **Error Handling**: Provides detailed error messages and logs for troubleshooting.

---

## Installation

1. **Download the Application**:
   - [Download the latest version](https://github.com/Poekhavshiy/KillAPI-connect/releases/latest/download/KillAPi.connect.exe).

2. **Install Dependencies**:
   - Ensure you have Python 3.9+ installed.
   - Install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Application**:
   - Execute the `killfeed.py` file:
     ```bash
     python killfeed.py
     ```

---

## User Interface Overview

### Main Window

The main window serves as the central hub for managing the application. Below is a description of all the buttons and functions:

| **Button**           | **Description**                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| **Start Monitoring**  | Starts monitoring the `Game.log` file for real-time updates.                   |
| **Stop Monitoring**   | Stops monitoring the log file.                                                 |
| **Configure**         | Opens the settings window to configure the game folder and API key.            |
| **View Log / Hide Log** | Toggles the visibility of the `LogDisplayWindow`.                             |
| **Status Label**      | Displays the current status of the application (e.g., "Ready", "Invalid Path").|

### Log Display Window

The `LogDisplayWindow` is a separate window that displays real-time log events. It includes the following features:

| **Button**            | **Description**                                                                 |
|------------------------|---------------------------------------------------------------------------------|
| **Clear**             | Clears all events from the log display.                                        |
| **Text Color**        | Opens a color picker to change the text color of the log display.              |
| **Background Color**  | Opens a color picker to change the background color of the log display.        |
| **+ (Font Size)**     | Increases the font size of the log display.                                    |
| **- (Font Size)**     | Decreases the font size of the log display.                                    |

---

## Settings Window

The settings window allows users to configure the following:

| **Setting**                  | **Description**                                                                 |
|------------------------------|---------------------------------------------------------------------------------|
| **Game Folder**              | Select the folder where the `Game.log` file is located.                        |
| **API Key**                  | Enter the API key for transmitting log events.                                 |
| **Check for Updates on Startup** | Enable or disable automatic update checks when the application starts.       |

---

## How It Works

1. **Log Monitoring**:
   - The application uses a `LogMonitor` class to read the `Game.log` file in real-time.
   - Events are parsed and displayed in the `LogDisplayWindow`.

2. **Settings Management**:
   - All settings are saved to a `settings.json` file located in the user data directory:
     ```
     C:\Users\<YourUsername>\AppData\Local\KindPerspective\Killfeed\settings.json
     ```

3. **Dynamic Window Management**:
   - The `LogDisplayWindow` saves its position, size, and visibility state to the settings file.
   - These settings are restored when the application restarts.

4. **Customization**:
   - Users can customize the log display's background color, text color, and font size.
   - Changes are saved automatically to the settings file.

---

## File Structure

killfeed/ ├── killfeed.py # Main application file ├── killsettings.py # Settings window logic ├── logdisplay.py # Log display window logic ├── logmonitor.py # Log monitoring logic ├── resources_rc.py # Compiled resources (icons, etc.) ├── settings.json # User settings file └── README.md # Documentation

---

## Settings File (`settings.json`)

The `settings.json` file stores all user configurations. Below is an example:

```json
{
    "game_folder": "C:\\Games\\RSI\\StarCitizen\\LIVE",
    "api_key": "your-api-key",
    "check_updates_on_startup": true,
    "log_file_path": "C:\\Games\\RSI\\StarCitizen\\LIVE\\Game.log",
    "game_exe_path": "C:\\Games\\RSI\\StarCitizen\\LIVE\\StarCitizen_Launcher.exe",
    "log_display_visible": true,
    "log_display_geometry": "hex-encoded-geometry-data",
    "log_bg_color": "#1e1e1e",
    "log_fg_color": "#dcdcdc",
    "log_font_size": 12
}
```

---
## Troubleshooting
Common Issues
### Invalid Path:
Ensure the Game.log file and StarCitizen_Launcher.exe exist in the selected game folder.

### No API Key:
Enter a valid API key in the settings window.

### Log Display Window Not Restoring:
Check the log_display_geometry value in the settings.json file.

Logs
The application provides detailed logs in the terminal for debugging purposes. Look for qDebug and qWarning messages.
---
Screenshots
Main Window
(Placeholder for screenshot)

Log Display Window
(Placeholder for screenshot)

Settings Window
(Placeholder for screenshot)

---

## Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch for your feature or bug fix.
Submit a pull request with a detailed description of your changes.

---
## License
This project is licensed under the MIT License. See the LICENSE file for details.
---

## Acknowledgments
PySide6: For providing the Qt framework for Python.
Star Citizen Community: For inspiring this project.
KindPerspective: For developing and maintaining this application.
---
For more information, visit the Killfeed GitHub Repository.

