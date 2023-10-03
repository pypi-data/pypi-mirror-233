import logging


class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if record.levelname == "INFO":
            # Add an extra tab character for INFO messages
            self._style._fmt = "%(asctime)s - %(name)s:%(levelname)s\t\t%(message)s"
        else:
            # Use the default formatting for other log levels
            self._style._fmt = "%(asctime)s - %(name)s:%(levelname)s\t%(message)s"
        return super().format(record)


def get_logger(level: int) -> logging.Logger:
    logger = logging.getLogger("GEOcollector")
    logger.setLevel(level)
    
    formatter = CustomFormatter("%(asctime)s - %(name)s:%(levelname)s\t\t%(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger
