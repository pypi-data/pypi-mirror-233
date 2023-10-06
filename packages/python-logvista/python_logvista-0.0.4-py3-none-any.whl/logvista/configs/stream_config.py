import logging
from typing import Optional, Callable

from logvista.level import Level


class StreamConfig:
    level: Level
    format: str
    filter_func: Optional[Callable[[logging.LogRecord], bool]]

    def __init__(
            self,
            level: Level = Level.DEBUG,
            format = "%(levelname)-9s  %(asctime)s [%(filename)s:%(lineno)d] %(message)s",
            filter_func: Optional[Callable[[logging.LogRecord], bool]] = None
        ):
        self.level = level
        self.format = format
        self.filter_func = filter_func

    def get_handler(self) -> logging.StreamHandler:
        handler = logging.StreamHandler()
        handler.setLevel(self.level.value)
        handler.setFormatter(logging.Formatter(self.format))
        if self.filter_func is not None:
            class CustomFilter(logging.Filter):
                def filter(self, record: logging.LogRecord) -> bool:
                    return self.filter_func(record)
            custom_filter = CustomFilter()
            handler.addFilter(custom_filter)
        return handler
