import time

from custom_logger import CustomLogger


if __name__ == '__main__':
    customLogger = CustomLogger('main')

    customLogger.debug('Debug Message1')

    time.sleep(2)

    customLogger.error('Error Message2')
