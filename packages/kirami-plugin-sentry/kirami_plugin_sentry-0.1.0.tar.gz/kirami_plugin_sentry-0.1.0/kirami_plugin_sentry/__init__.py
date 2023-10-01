import sentry_sdk

from kirami.log import logger
from sentry_sdk.integrations.logging import EventHandler, BreadcrumbHandler

from .config import Config
from .hook import alert as alert
from .plugin import get_error_by_argot as get_error_by_argot
from .plugin import get_error_by_message as get_error_by_message

config = Config.load_config("sentry")


def init_sentry():
    sentry_sdk.init(
        dsn=config.sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
        environment=config.sentry_environment,
    )

    logger.add(
        EventHandler("ERROR"),
        filter=lambda r: r["level"].no >= logger.level("ERROR").no,
    )
    logger.add(
        BreadcrumbHandler("INFO"),
        filter=lambda r: r["level"].no >= logger.level("INFO").no,
    )


if config.sentry_dsn:
    init_sentry()
