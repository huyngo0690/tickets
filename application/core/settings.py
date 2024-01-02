import os

from pydantic_settings import BaseSettings




class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", "60")
    )
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    DIGITS: str = "0123456789"
    JWT_SECRET_KEY: str = os.environ.get(
        "JWT_SECRET_KEY", "narscbjim@$@&^@&%^&RFghgjvbdsha"
    )
    JWT_REFRESH_SECRET_KEY: str = os.environ.get(
        "JWT_REFRESH_SECRET_KEY", "13ugfdfgh@#$%^@&jkl45678902"
    )
    APP_PORT: int = os.environ.get("APP_PORT", "8080")
    DEBUG_PORT: int = os.environ.get("DEBUG_PORT", "8081")
    # LOGGING_CONF: str = os.environ.get("LOGGING_CONF", "core/logging.conf")
    LOGGER: str = os.environ.get("LOGGER", "commonLogger")
    MYSQL_HOST: str = os.environ.get("MYSQL_HOST", "")
    MYSQL_USER: str = os.environ.get("MYSQL_USER", "")
    MYSQL_PASSWORD: str = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB: str = os.environ.get("MYSQL_DB", "ticket")
    MYSQL_PORT: str = os.environ.get("MYSQL_PORT", "3306")
    DB_URI: str = os.environ.get("DB_URI", "")
    DB_ECHO_LOG: bool = True if os.environ.get("DEBUG") else False

    @property
    def database_url(self) -> str:
        return f"mysql+mysqlconnector://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    @property
    def async_database_url(self) -> str:
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"


settings = Settings()
