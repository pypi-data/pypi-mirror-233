import logging

class LoggerHelper():
    _logger = None

    @classmethod
    def create_logger(cls):
        logger = logging.getLogger(cls.__name__)
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter(
            fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt = '%Y-%m-%d %H:%M:%S'
        )
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        logger.addHandler(ch)

        return logger

    @classmethod
    def logger(cls):
        if(cls._logger is None):
            cls._logger = cls.create_logger()

        return cls._logger



