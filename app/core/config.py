from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_url: str = "postgresql://astock:astock123@localhost:5432/astock"


settings = Settings()
