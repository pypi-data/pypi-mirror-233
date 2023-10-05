import logging

def setup_logger(to_file=False, to_terminal=True, log_filename='app.log'):
    logger = logging.getLogger('my_module')
    logger.setLevel(logging.DEBUG)
    
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

# User decides to log to both file and terminal
logger = setup_logger(True, True)

# Usage
logger.info('This is an info message.')
