import logging

def get_mediumana_logger():

    logger = logging.getLogger('mediumana')
    logger.setLevel(logging.DEBUG)

    error_logger = logging.FileHandler('error.log')
    debug_logger = logging.FileHandler('med_debug.log')

    error_logger.setLevel(logging.ERROR)
    debug_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    error_logger.setFormatter(formatter)
    debug_logger.setFormatter(formatter)

    logger.addHandler(error_logger)
    logger.addHandler(debug_logger)

    return logger

med_logger = get_mediumana_logger()
