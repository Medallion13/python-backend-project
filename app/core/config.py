from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql:dummy:dummy"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
