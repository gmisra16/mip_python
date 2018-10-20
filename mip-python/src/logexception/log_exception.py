import functools
import logging.config

#Decorator for generic exception logging
def create_logger():
    """
    Creates a logging object and returns it
    """
    logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
    logger = logging.getLogger("generic_logger")
    return logger


def log_exception(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except:
            # log the exception
            err = "Generic logged :: There was an exception in  "
            err += function.__name__
            logger.exception(err)

            # re-raise or absorb the exception as needed
            raise

    return wrapper