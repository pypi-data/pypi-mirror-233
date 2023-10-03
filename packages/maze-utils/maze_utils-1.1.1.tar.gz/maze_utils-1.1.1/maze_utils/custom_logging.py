import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s %(name)s %(levelname)s] %(message)s")


def get_logger(class_: object = None) -> logging.Logger:
    logger = logging.getLogger(name=class_.__class__.__name__)
    logger.setLevel(logging.INFO)
    return logger
