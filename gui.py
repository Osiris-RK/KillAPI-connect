from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import qDebug, qWarning

# Colors for the app's appearance
DARK_BG = "#121212"
CARD_BG = "#18181C"
TEXT_COLOR = "#E0E0E0"
BUTTON_COLOR = "#303034"
BUTTON_HOVER_COLOR = "#505054"
ENTRY_BG = "#242428"
ENTRY_FG = "#E0E0E0"
ACCENT_COLOR = "#707070"

# Style settings
BUTTON_BORDER_RADIUS = "8px"
PADDING = "10px"
FIELD_WIDTH = "350px"
FIELD_HEIGHT = "35px"
HALF_FIELD_WIDTH = "159px"

CARD_MAX_WIDTH = "450px"

# Font loading function
# Load fonts from resource
def load_fonts():
    font_db = QFontDatabase()
    font_ids = []
    for font_resource in [":/fonts/Roboto-Regular.ttf", ":/fonts/Roboto-Bold.ttf"]:
        font_id = font_db.addApplicationFont(font_resource)
        if font_id == -1:
            qWarning(f"Failed to load font: {font_resource}")
        else:
            font_ids.append(font_id)
            qDebug(f"Loaded font: {font_db.applicationFontFamilies(font_id)}")
    return font_ids


# Fonts for text
FONT_LABEL = QFont("Roboto", 12)
FONT_STATUS = QFont("Roboto", 14, QFont.Bold)
FONT_BUTTON = QFont("Roboto", 12)

# Stylesheets
BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {BUTTON_COLOR};
        color: {TEXT_COLOR};
        border: none;
        border-radius: {BUTTON_BORDER_RADIUS};
        padding: {PADDING};
        min-height: {FIELD_HEIGHT};
        max-height: {FIELD_HEIGHT};
        min-width: {FIELD_WIDTH};
        max-width: {FIELD_WIDTH};
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {BUTTON_HOVER_COLOR};
    }}
    QPushButton:pressed {{
        background-color: {ACCENT_COLOR};
    }}
"""
HALF_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {BUTTON_COLOR};
        color: {TEXT_COLOR};
        border: none;
        border-radius: {BUTTON_BORDER_RADIUS};
        padding: {PADDING};
        min-height: {FIELD_HEIGHT};
        max-height: {FIELD_HEIGHT};
        min-width: {HALF_FIELD_WIDTH};
        max-width: {HALF_FIELD_WIDTH};
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {BUTTON_HOVER_COLOR};
    }}
    QPushButton:pressed {{
        background-color: {ACCENT_COLOR};
    }}
"""
ENTRY_STYLE = f"""
    QLineEdit {{
        background-color: {ENTRY_BG};
        color: {ENTRY_FG};
        border: 1px solid #444444;
        border-radius: 5px;
        padding: 8px;
        min-height: {FIELD_HEIGHT};
        max-height: {FIELD_HEIGHT};
        min-width: {FIELD_WIDTH};
        max-width: {FIELD_WIDTH};
    }}
    QLineEdit:focus {{
        border: 1px solid {ACCENT_COLOR};
    }}
"""

STATUS_STYLE = f"""
    QLabel {{
        color: {ACCENT_COLOR};
    }}
"""

CARD_STYLE = f"""
    QWidget {{
        background-color: {CARD_BG};
        border-radius: 10px;
        padding: 15px;
        max-width: {CARD_MAX_WIDTH};
    }}
"""