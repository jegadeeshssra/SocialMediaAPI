from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB: str = "postgresql"
    DB_NAME: str = "postgresql"
    USER_NAME: str = "postgres"
    PASSWORD: str = "postgres"
    HOST: str   = "localhost"
    USERS_TABLE_NAME: str = "users"
    POSTS_TABLE_NAME: str = "posts"
    VOTES_TABLE_NAME: str = "votes"
    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    model_config = SettingsConfigDict(
        env_file = ".env",      # This detects the .env wihtin the src folder only(Not for production)
        extra = "ignore"
    )

settings = Settings()


# NOTE: Dont use "USERNAME"as an variable bcuz it fetches hte username from the computer