from pydantic import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    MONGO_DB: str
    MONGO_ROOT_USERNAME: str
    MONGO_ROOT_PASSWORD: str
    MONGO_PORT: int
    MONGO_HOST: str
    MONGO_CONNECTION: str
    REDIS_USER: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    CLIENT_URL: str
    class Config:
        env_file = ".env"

settings = Settings()
