import logging
import logging.config
from raya_apps_admin_msgs.msg import AppLog


class ColorFormatter(logging.Formatter):

    def format(self, record):
        return


LOGGING_TO_RAYA_LEVELS = {
    logging.DEBUG: AppLog.DEBUG,
    logging.INFO: AppLog.INFO,
    logging.WARN: AppLog.WARNING,
    logging.WARNING: AppLog.WARNING,
    logging.ERROR: AppLog.ERROR,
    logging.CRITICAL: AppLog.CRITICAL,
    logging.FATAL: AppLog.CRITICAL
}


class TopicPublisher():

    def __init__(self):
        pass

    def set_publisher(self, app_id, publisher):
        pass

    def publish(self, logger_name, raya_level, message):
        pass


topic_publisher = TopicPublisher()


class RaYaLogger():

    def __init__(self, name: str, level=logging.DEBUG):
        self.py_logger = logging.getLogger(self.__name)

    def ros_publish(self, level, message):
        pass

    def debug(self, message=''):
        pass

    def info(self, message=''):
        pass

    def warn(self, message=''):
        pass

    def warning(self, message=''):
        pass

    def error(self, message=''):
        pass

    def critical(self, message=''):
        pass

    def fatal(self, message=''):
        pass


__deprecation_logger = RaYaLogger('Deprecation Notice')
__debug_warning_logger = RaYaLogger('Debug')


def DEPRECATION_WARNING(msg):
    pass


def DEPRECATION_NEW_METHOD(new_method_name):
    pass


def DEBUG_WARNING(msg):
    pass
