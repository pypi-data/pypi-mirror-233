import logging


def setup_logger(to_file=False, to_terminal=True, log_filename='ga_search.log'):
    logger = logging.getLogger('ga_search')

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    if to_file:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if to_terminal:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


if __name__ == "__main__":
    logger = setup_logger(True, True)
    logger.info('This is an info message.')
