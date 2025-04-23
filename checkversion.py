from PySide6.QtCore import qDebug, qWarning
import requests
from requests.exceptions import RequestException, Timeout

def get_latest_version(repo: str, timeout: int = 10) -> str | None:
    """
    Fetch the latest release tag from a GitHub repository.
    
    Args:
        repo (str): Repository in the format 'username/reponame'.
        timeout (int): Timeout for the HTTP request in seconds.

    Returns:
        str | None: Tag name of the latest release or None if failed.
    """
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        tag = data.get("tag_name")

        if tag:
            qDebug(f"Latest release tag: {tag}")
            return tag[1:] if tag.startswith("v") else tag # Remove 'v' prefix if present
        else:
            qWarning("No tag_name found in response.")
            return None
    except Timeout:
        qWarning("Request timed out.")
    except RequestException as e:
        qWarning(f"Request failed: {e}")
    except ValueError:
        qWarning("Failed to parse JSON response.")
    
    return None

# Example usage:
if __name__ == "__main__":
    repo = "Poekhavshiy/KillAPI-connect"
    tag = get_latest_version(repo)
    if tag:
        qDebug(f"Latest release tag: {tag}")
    else:
        qWarning("Failed to retrieve the latest release tag.")
