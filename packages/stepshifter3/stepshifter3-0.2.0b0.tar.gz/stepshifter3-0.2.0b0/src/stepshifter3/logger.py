import logging


class AppLogger:
    def __init__(self, name, level=logging.INFO, log_format='%(asctime)s - %(levelname)s - %(message)s', log_file='../logs/stepshifter.log'):
        """
        Initialize a logger.

        Arguments:
            name (str): Name of the logger.
            level (int): Logging level.
            log_format (str): Format for the logging messages.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)

        # Formatter
        formatter = logging.Formatter(log_format)

        # Add formatter to handlers
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def get_logger(self):
        """
        Returns the configured logger.

        Arguments:
            None
        Returns:
            logger (Logger): Configured logger.
        """
        return self.logger
