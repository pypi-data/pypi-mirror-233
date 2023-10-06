import logging
from typing import Optional

from logvista.level import Level
from logvista.configs import StreamConfig, FileConfig, LogvistaConfig


class Observer:
    system_name: str

    def __init__(
            self,
            system_name: str,
            logvista_config: Optional[LogvistaConfig] = None,
            stream_config: Optional[StreamConfig] = None,
            file_config: Optional[FileConfig] = None
        ) -> None:
        self.system_name = system_name
        self.logvista_config = logvista_config
        self.stream_config = stream_config
        self.file_config = file_config

    def __str__(self) -> str:
        return f'{self.system_name}-observer'

    def get_logger(self, logger_name) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        logger.setLevel(Level.DEBUG.value)
        return logger