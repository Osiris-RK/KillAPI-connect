#transmitter.py
import requests
from PySide6.QtCore import qDebug, qWarning

API_SERVER_URL = "https://bagman.sparked.network/api/interaction"

def send_debug_ping(log_file_path, api_key):
    """
    Send a debug ping to the API server to verify the API key.
    Returns True if successful, False otherwise.
    """
    payload = {
        "identifier": "debug_ping",
        "log_file_path": log_file_path,
        "api_key": api_key
    }
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(API_SERVER_URL, json=payload, headers=headers)
        if response.status_code == 200:
            qDebug(f"Debug ping successful: {response.json()}")
            return True
        else:
            qWarning(f"Debug ping failed: {response.status_code} - {response.json()}")
            return False
    except requests.RequestException as e:
        qWarning(f"Error sending debug ping: {e}")
        return False

def send_connection_success(log_file_path, api_key):
    """
    Send a connection success event to the API server to notify the Discord channel.
    Returns True if successful, False otherwise.
    """
    payload = {
        "identifier": "connection_success",
        "log_file_path": log_file_path,
        "api_key": api_key
    }
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(API_SERVER_URL, json=payload, headers=headers, timeout=6.9)  # 100ms timeout
        if response.status_code == 200:
            qDebug(f"Connection success event sent: {response.json()}")
            return True
        else:
            qWarning(f"Failed to send connection success event: {response.status_code} - {response.json()}")
            return False
    except requests.exceptions.Timeout:
        qWarning("Error: The request timed out (took longer than 6.9s).")
        return False
    except requests.RequestException as e:
        qWarning(f"Error sending connection success event: {e}")
        return False

def send_event(event, api_key):
    """
    Send a log event to the API server.
    """
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(API_SERVER_URL, json=event, headers=headers)
        if response.status_code == 200:
            qDebug(f"Event sent successfully: {response.json()}")
        else:
            qWarning(f"Failed to send event: {response.status_code} - {response.json()}")
    except requests.RequestException as e:
        qWarning(f"Error sending event: {e}")