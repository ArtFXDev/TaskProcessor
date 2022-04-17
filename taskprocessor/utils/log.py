# -*- coding: utf-8 -*-
"""
"""
import sys

import logging
import logzero
from logzero import logger

"""
A simple logger shortcut / wrapper.

Uses
https://logzero.readthedocs.io/

TODO: code clean.
"""

#__logFormat = '[%(asctime)s] %(levelname)8s| %(message)s (%(filename)s:%(funcName)s:%(lineno)d)'
__logFormat = '[%(asctime)s] %(levelname)-6s| [%(module)s.%(funcName)s] %(message)-80s (%(lineno)d)'
__logFormat_colored = '%(color)s[%(asctime)s] %(levelname)-6s| [%(module)s.%(funcName)s] %(message)-80s (%(lineno)d)%(end_color)s'
#logging.basicConfig(format=__logFormat, level=conf.loglevel) # ??

# we set a new handler
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logzero.LogFormatter(fmt=__logFormat, color=True))
logger.handlers = []
logger.addHandler(handler)
logzero.formatter(logging.Formatter(fmt=__logFormat))
logger.setLevel(logging.INFO)  # FIXME: config (depending on deploy dir)


def get_logger(name, color=True):
    new_logger = logzero.setup_logger(name=name)
    if color:
        new_logger.handlers[0].setFormatter(logzero.LogFormatter(fmt=__logFormat_colored, color=True))
    else:
        new_logger.handlers = []  # if we keep the handler, all logs are red.
        new_logger.addHandler(handler)
    return new_logger

"""
Code shortcuts
"""
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical

setLevel = logger.setLevel
getLevel = logger.getEffectiveLevel

DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR


if __name__ == '__main__':

    # specific logger (recommended)
    log_one = get_logger('core')
    # log_one = get_logger('one', color=False)
    log_one.debug('debug one')
    log_one.info('info one')
    log_one.setLevel(ERROR)
    log_one.debug('debug one')
    log_one.error('error one')

    # default logger
    setLevel(INFO)
    debug('foo')
    info('foo')
    error('foo')
    critical('foo')

    setLevel(DEBUG)

    debug('titi')

    # In application code
    from taskprocessor.utils.log import INFO, get_logger

    log = get_logger('core')
    # log.setLevel(INFO)

    log.debug('Core debug information')
    log.debug('Core info')
