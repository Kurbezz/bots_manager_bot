from pydantic import BaseSettings


class EnvConfig(BaseSettings):
    SENTRY_DSN: str

    BOT_TOKEN: str

    MANAGER_URL: str
    MANAGER_API_KEY: str


env_config = EnvConfig()
