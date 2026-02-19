import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from dify_plugin.config.logger_format import plugin_logger_handler

_env_loaded = False


def setup_logger(logger_name: str | None = None) -> logging.Logger:
    """
    ロガーを設定する

    Args:
        logger_name: ロガー名（Noneの場合は呼び出し元のモジュール名を使用）

    Returns:
        設定されたロガー
    """
    global _env_loaded

    if not _env_loaded:
        env_path = Path(__file__).parent / '.env'
        load_dotenv(env_path, override=True)
        _env_loaded = True

    if logger_name is None:
        import inspect
        try:
            frame = inspect.currentframe().f_back
            logger_name = frame.f_globals.get('__name__', 'root')
        except (AttributeError, ValueError):
            logger_name = 'root'

    logger = logging.getLogger(logger_name)

    log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        logger.addHandler(plugin_logger_handler)
        logger.propagate = False

    return logger
