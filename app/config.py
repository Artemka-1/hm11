from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str

    mail_username: str
    mail_password: str
    mail_from: str
    mail_server: str
    mail_port: int

    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    redis_host: str
    redis_port: int

    class Config:
        env_file = ".env"

settings = Settings()
