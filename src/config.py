from pydantic import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    DB: str
    DB_NAME: str
    USERNAME: str
    PASSWORD: str
    HOST: str
    USERS_TABLE_NAME: str
    POSTS_TABLE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
    )

config = Settings()