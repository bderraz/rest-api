import enum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

CURRENT_DIR = Path(".")


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO
    # Variables for the database
    db_file: Path = CURRENT_DIR / "db.sqlite3"
    db_echo: bool = False

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="sqlite+aiosqlite",
            path=f"///{self.db_file}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TVSHOW_BACKEND_",
        env_file_encoding="utf-8",
    )


settings = Settings()
