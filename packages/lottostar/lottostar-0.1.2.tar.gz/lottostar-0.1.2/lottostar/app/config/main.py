"""
Settings for the app
"""
from dataclasses import dataclass


@dataclass
class Settings:
    """
    settings data class
    """
    DEFAULT_SFTP_FOLDER = "downloads/sftp/"
    WINNING_ENTRY_FILE_IDENTIFIER = "result"
    WINNING_ENTRY_DATA_ROW = 4


settings = Settings()
