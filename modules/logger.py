import logging
import os


def setup_logger(name, level=logging.DEBUG, log_file='app.log'):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)  # Set the logging level

    # Check if logger already has handlers
    if not logger.handlers:
        # Create a console handler and set the level to debug
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create a formatter and set the format for the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        logger.addHandler(console_handler)

        # Create a file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    return logger
