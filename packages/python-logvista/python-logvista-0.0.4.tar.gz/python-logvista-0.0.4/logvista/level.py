import enum
import logging

class Level(enum.Enum):
    """### Log level Enum

    Description:
        - ログレベルの既定値を定義するEnum
        - 各定数値はint型であり、loggingモジュールの既定値と同じ
        - 定数値が大きいほど重要度が高い
        - add_new_levelメソッドを使用して、カスタムログレベルを追加することができる

    Default log levels:
        - NOTSET = 0
        - DEBUG = 10
        - INFO = 20
        - WARNING = 30
        - WARN = 30
        - ERROR = 40
        - FATAL = 50
        - CRITICAL = 50

    Raises:
        ValueError: 既に同じ名前のログレベルが存在する場合
    """
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    WARN = 30
    ERROR = 40
    FATAL = 50
    CRITICAL = 50

    @classmethod
    def add_new_level(cls, level_name: str, level_value: int) -> None:
        """### Levelクラスとloggingモジュールに新しいログレベルを追加するメソッド

        Args :
            - level_name (str): 新しいログレベルの名前
            - level_value (int): 新しいログレベルの値

        Raises :
            - ValueError: 既に同じ名前のログレベルが存在する場合

        Examples :
            ```python
            >>> from logvista import Level
            >>> Level.add_new_level('TRACE', 15)
            ```
        """
        if hasattr(cls, level_name):
            raise ValueError(f"LogLevel {level_name} already exists.")
        cls._member_map_[level_name] = level_value

        logging.addLevelName(level_value, level_name)

        def custom_log_method(self: logging.Logger, message: str, *args, **kws):
            if self.isEnabledFor(level_value):
                self._log(level_value, message, *args, **kws)

        setattr(logging.Logger, level_name.lower(), custom_log_method)
