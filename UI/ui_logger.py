import logging


logger = None


def setup_logger(filename: str = 'app.log'):
    global logger
    if logger:
        logger.warning('Logging already running!')
        return
    logger = logging.getLogger("ZemaxUtilsLogger")
    logging.basicConfig(filename=filename, filemode='+w', format='%(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARN)
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.CRITICAL)
    logger.warning('Logging begin!')
