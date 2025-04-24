# Killfeed Application

Killfeed is a Python-based desktop application designed integrate with the Gunhead Discord Bot, and to optionally display real-time event logs from **Star Citizen**. It provides a user-friendly interface for selecting the game files, starting and stopping of monitoring of the events, and customizing the display of the in-app log data. The application is built with extensibility and ease of use in mind, allowing users to configure settings, monitor logs, and interact with the application seamlessly.

---

## Gunhead Discord Bot
This application is designed to work with the Gunhead Discord Bot, which is a custom bot developed by the Gunhead community. The bot is responsible for processing and displaying the events in the Discord server. To install the discord bot to your server, follow the instructions provided in the [Discord App Store](https://discord.com/discovery/applications/1330870778891206707).

Once the bot is installed and running, choose a Discord channel or create a new one for the event logs, then run the `/api subscribe` command to add the event feed to the discord channel, and then use the `/api killfeed` command create the event stream window.

Your users then can create or view their API keys by running the `/api show_key` command in the subscribed channel.

To delete a user's API key, use the `/api removeuser <USERNAME>` command.

To unsubscribe a channel from the event feed, use the `/api unsubscribe` command.
---

## Features

- **Log Monitoring**: Continuously monitor the Star Citizen events for real-time updates.
- **Customizable Log Display**: Change the background color, text color, and font size of the log display window.
- **Dynamic Window Management**: The `LogDisplayWindow` remembers its position, size, and visibility state across sessions.
- **Settings Management**: All configurations are saved to a single `settings.json` file.
- **Update Checker**: Simple button press to check for updates to the application, and optionally a toggle check for updates at startup.
- **Error Handling**: Provides detailed error messages on the console for troubleshooting.

---

## Installation

1. **Download the Application**:
   - [Download the latest version](https://github.com/Poekhavshiy/KillAPI-connect/releases/latest/download/KillAPi.connect.exe).

2. **Run the Application**:
   - Either double-click the `KillAPI.connect.exe` file or for debug logging, simply run it from the command line:
     ```bash
     KillAPI.connect.exe
     ```

---

## User Interface Overview

### Main Window

The main window serves as the central hub for managing the application. Below is a description of all the buttons and functions:

| **Button**           | **Description**                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| **Start Monitoring / Stop Monitoring **  | Starts or stops monitoring the game events file for real-time updates.                   |
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
| **Check for new versions on startup** | Enable or disable automatic update checks when the application starts.       |
| **Check for updates now** | Performs a check for updates and gives the option to download if a newer version is available.       |
| **Game Folder**              | Select the folder where the **Star Citizen** files is located. Either use the browser button to select the folder or type /paste the path manually then press `Save`. |
| **API Key**                  | Enter the API key for transmitting log events then press `Save API Key`.                                 |


---

## How It Works

Once you have executed the application, you will see the main window that looks like this:
![Main Window](https://github.com/Poekhavshiy/KillAPI-connect/assets/14026302/29606280-0800-4391-9994-45215960b30d)

1. **Select Game Folder**:
   - Click on the "Configure" button to open the settings window.
   - Select the folder where the **Star Citizen** files are located either by clicking the browser button or typing/pasting the path manually and clicking `Save`.
   - The application will automatically detect the game folder if it's located in the default location.
   
   See below screenshot for an example of the default location:
   ![Default Star Citizen Folder Location](https://github.com/Poekhavshiy/KillAPI-connect/assets/14026302/9263d57b-06c6-4836-b338-2594753f9161)

2. **Insert your unique API key**:
   - Insert your unique API key in the settings window that you retrieved by using the `/api show_key` command.
   - Click `Save API Key`.
   - The application test the API key and connectivity, and will then save the API key to the settings file.

   See below screenshot for an example of the API key:
   ![API Key](https://github.com/Poekhavshiy/KillAPI-connect/assets/14026302/50897131-3d36-49a7-921d-0065002353a4)
   
3. **Start Monitoring**:
   - Exit out of the settings window and in the main window, click the "Start Monitoring" button.
   - The application will start monitoring the game events file for real-time updates.
   - The status label will display "Ready" if the application is running correctly.
   ![Ready](https://github.com/Poekhavshiy/KillAPI-connect/assets/14026302/64279732-9684-421c-846a-30324b37587a)

4. **Show Local Log Display Window (Optional)**:
   - If you would like to view the log events locally in real-time, click the "View Log" button.
    ![Log Display Window](https://github.com/Poekhavshiy/KillAPI-connect/assets/14026302/29606280-0800-4391-9994-45215960b30d)
---

## Troubleshooting
Common Issues
### Invalid Path:
Ensure the Game.log file and StarCitizen_Launcher.exe exist in the selected game folder.

### No API Key:
Enter a valid API key in the settings window.


Logs
The application provides detailed logs in the terminal for debugging purposes. Look for qDebug and qWarning messages when running the application from a command prompt.
---
Screenshots
Main Window
(Placeholder for screenshot)

Log Display Window
(Placeholder for screenshot)

Settings Window
(Placeholder for screenshot)

---
## License
This project is licensed under commercial conditions, no modifications of the application are allowed. The application is not for sale, it is a free tool for the community. Ownership of the application is reserved.
---

---
For more information, visit the Killfeed GitHub Repository: [Killfeed GitHub Repository](https://github.com/Poekhavshiy/KillAPI-connect)

