from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    origins: list[str] = ["http://localhost:3000"]

    class Config(SettingsConfigDict):
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
