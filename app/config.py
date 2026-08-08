from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Resume Optimizer"
    DEBUG: bool = True
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()