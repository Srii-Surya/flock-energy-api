from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_url: str = "https://urja-ops.flockenergy.tech"
    session_cookie: str = ""

    model_config = SettingsConfigDict(
        env_prefix="URJA_PORTAL_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
