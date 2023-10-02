import time
from functools import wraps


class logger_assignment3:
    LEVELS = {"DEBUG": 1, "INFO": 2, "WARNING": 3, "ERROR": 4, "CRITICAL": 5}

    def __init__(
        self,
        log_file,
        log_level="INFO",
        append=True,
    ):
        self.log_file = log_file
        self.log_level = log_level
        self.append = append
        self.format = "{timestamp} - {level}: {message}"

    def log(self, message, level="INFO"):
        if (
            logger_assignment3.LEVELS[level]
            >= logger_assignment3.LEVELS[self.log_level]
        ):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            full_message = self.format.format(
                timestamp=timestamp, level=level, message=message
            )
            with open(self.log_file, "a" if self.append else "w") as f:
                f.write(full_message + "\n")

    def debug(self, message):
        self.log(message, "DEBUG")

    def info(self, message):
        self.log(message, "INFO")

    def warning(self, message):
        self.log(message, "WARNING")

    def error(self, message):
        self.log(message, "ERROR")

    def critical(self, message):
        self.log(message, "CRITICAL")

    def decorator_logger(self, message=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if message:
                    formatted_message = message.format(
                        func_name=func.__name__, args=args, kwargs=kwargs
                    )
                    self.info(formatted_message)
                self.info(
                    f"Called function {func.__name__} with arguments {args} and keyword arguments {kwargs}."
                )
                try:
                    result = func(*args, **kwargs)
                    self.info(f"Function {func.__name__} returned {result}.")
                    return result
                except:
                    self.error(f"Function {func.__name__} has Error.")

            return wrapper

        return decorator
