from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  
    JWT_SECRET_KEY: str = "dnjwndnwihduehduwehdhdhuy"  
    JWT_ALGORITHM: str = "HS256"  

    class Config:
        env_file = ".env"

settings = Settings()
