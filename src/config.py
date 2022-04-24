from pydantic import BaseSettings


class EnvConfig(BaseSettings):
    SENTRY_DSN: str


env_config = EnvConfig()
