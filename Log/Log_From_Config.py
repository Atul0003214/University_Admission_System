import logging
import logging.config


class LogDetails:
    def __init__(self, function_name, message):
        logging.config.fileConfig('Log/logparam.config')

        # create logger
        logger = logging.getLogger(function_name)

        # 'application' code
        # logger.debug('debug message')
        logger.info(message)
        # logger.warning('warn message')
        # logger.error('error message')
        # logger.critical('critical message')
