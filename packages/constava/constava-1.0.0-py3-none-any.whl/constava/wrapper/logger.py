import logging
import logging.config

logger_configuration = {
    "version" : 1,
    "formatters" : {
        "default": {
            "format" : "[%(asctime)s] %(message)s",
            "datefmt" : "%Y-%m-%d %H:%M:%S",
            "style" : "%",
            "validate" : True
        },
    },
    "handlers" : {
        "console" : {
            "class" : "logging.StreamHandler",
            "formatter" : "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers" : {
        "Constava" : {
            "handlers" : ["console"],
            "level": "INFO",
        },
    },
}

logging.config.dictConfig(logger_configuration)
logger = logging.getLogger('Constava')