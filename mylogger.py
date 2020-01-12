import logging
FORMAT='[%(filename)s] [%(funcName)s] [%(lineno)d] [%(levelname)s]:\t%(message)s'
# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('mylogger')