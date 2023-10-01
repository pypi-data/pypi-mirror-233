from kirami.log import logger
from kirami.config import BaseConfig
from pydantic import Extra, validator


class Config(BaseConfig, extra=Extra.allow):
    sentry_dsn: str | None
    sentry_environment: str | None

    # https://github.com/getsentry/sentry-python/issues/653
    sentry_default_integrations: bool = False

    @validator("sentry_dsn", allow_reuse=True)
    def validate_dsn(cls, v: str | None):
        if not v:
            logger.warning("Sentry DSN not provided! Sentry plugin disabled!")
        return v
