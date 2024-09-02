from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    vk_access_token: str

    telegram_bot_token: str
    telegram_bot_url: str | None = None

    model_config = SettingsConfigDict(env_file = '.env')