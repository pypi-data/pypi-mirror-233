from datetime import datetime
import os

from enums import LoggingLevel


class CustomLogger:
    class_name = 'SomeClass'
    logging_level = LoggingLevel.DEBUG.name
    message = 'Test'
    time = 'Some time'

    def __init__(self, class_name: str):
        self.class_name = class_name

    def __create_log(self, logging_level: LoggingLevel, message: str):
        self.logging_level = logging_level.name
        self.message = message
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if os.path.exists('my_custom_logs.txt'):
            write_mode = 'a'
        else:
            write_mode = 'w'

        with open('my_custom_logs.txt', write_mode) as logs_file:
            logs_file.write(f'{self.time} - {self.class_name} - {self.logging_level} - {self.message} \n')

    def info(self, message: str):
        self.__create_log(LoggingLevel.INFO, message)

    def debug(self, message: str):
        self.__create_log(LoggingLevel.DEBUG, message)

    def warning(self, message: str):
        self.__create_log(LoggingLevel.WARNING, message)

    def error(self, message: str):
        self.__create_log(LoggingLevel.ERROR, message)

