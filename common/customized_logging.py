import logging
import logging.config

CONFIGURED = False


def configure_logging():
    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": "%(asctime).19s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "loggers": {
            "common": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": True,
            },
            "inflation": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": True,
            },
            "style": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": True,
            },
            "__main__": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }
    global CONFIGURED
    if not CONFIGURED:
        logging.config.dictConfig(config)
        CONFIGURED = True
