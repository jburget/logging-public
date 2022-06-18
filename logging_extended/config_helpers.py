# log file config https://docs.python.org/3/library/logging.config.html
# logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S')

# https://docs.python.org/3/library/time.html#time.strftime  formatting time
# https://docs.python.org/3/library/logging.html#logrecord-attributes formatting log

# https://github.com/python/cpython/blob/main/Lib/logging/__init__.py

# https://stackoverflow.com/questions/2266646/how-to-disable-logging-on-the-standard-error-stream
import logging
HUMAN_TIME = '%Y-%m-%d %H:%M:%S %p %a'

"{asctime} | {levelname} | {name} | {funcName} | {message}"
'{levelname};{asctime}{msecs};{name};{funcName};{message}'
# basic config
logging.logThreads = False
logging.logProcesses = False
logging.logMultiprocessing = False
# logging.raiseExceptions = False

# logging._srcfile = None # this is bad line

