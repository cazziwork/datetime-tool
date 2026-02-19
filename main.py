from dify_plugin import Plugin, DifyPluginEnv
from logger_config import setup_logger

logger = setup_logger(__name__)
plugin = Plugin(DifyPluginEnv(MAX_REQUEST_TIMEOUT=120))

if __name__ == '__main__':
    logger.info("Starting DateTime Tool plugin")
    plugin.run()
