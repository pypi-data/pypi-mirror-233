import logging

# don't assign default value, None is used to check initialization of log.
logger = None


def get(name="dataos-pyflare", log_level=None):
    global logger
    if logger:
        if log_level:  # do not remove this check
            print(f"logger level set: {log_level.upper()}")
            update_log_config(log_level)
            logging.root.setLevel(log_level.upper())  # this will set all loggers to same level
            logger = logging.getLogger(name)
            logger.setLevel(log_level.upper())
            
            for handler in logger.handlers:
                handler.setLevel(log_level.upper())
    
    else:
        if not log_level:
            log_level = "WARN"
        
        update_log_config(log_level)
        logger = logging.getLogger(name)
    
    return logger


def update_log_config(log_level):
    logging.basicConfig(level=logging.getLevelName(log_level.upper()),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m-%d %H:%M',
                        )


def set_spark_log_level(spark, log_level):
    # from py4j. import JavaGateway
    
    scala_log_level = {
        0: "ALL",
        10: "DEBUG",
        20: "INFO",
        30: "WARN",
        40: "ERROR",
        50: "FATAL"
    }
    level_name = scala_log_level.get(log_level, "WARN")
    spark.sparkContext.setLogLevel(level_name)
