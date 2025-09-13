import logging

def setup_logger(log_file="app.log", level=logging.DEBUG):
    logger = logging.getLogger("billing")
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="[%(name)s] [%(asctime)s]: %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Uncomment if you want file logging
    # file_handler = logging.FileHandler(log_file)
    # file_handler.setLevel(level)
    # file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        # logger.addHandler(file_handler)

    return logger

# Create logger instance once
logger = setup_logger()