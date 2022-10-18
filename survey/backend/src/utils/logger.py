import logging

logging.basicConfig(filename='api_log.log',
                    format='%(asctime)s %(message)s',
                    filemode='a')
api_logger = logging.getLogger()

api_logger.setLevel(logging.DEBUG)