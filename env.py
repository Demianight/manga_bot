from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# class DBSettings(BaseModel):
#     """
#     В .env файле обозначается префиксом DB__
#     """

#     name: str
#     user: str
#     password: str
#     host: str
#     port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # db: DBSettings
    bot_token: str
    debug: bool


settings = Settings()
