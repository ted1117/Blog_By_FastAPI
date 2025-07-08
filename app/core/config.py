from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str = ""

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env")

    def __init__(self, **values):
        super().__init__(**values)
        if self.SECRET_KEY == "":
            raise ValueError("SECRET_KEY가 .env 파일에 설정되지 않았습니다.")


settings = Settings()
