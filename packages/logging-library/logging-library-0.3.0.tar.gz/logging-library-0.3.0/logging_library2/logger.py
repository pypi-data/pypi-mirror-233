import logging

def setup_logger(name, log_to_file=False, log_level=logging.DEBUG): 
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if log_to_file:
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger