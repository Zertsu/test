# This module implements logging

class LogLevel:
    FATAL = 1
    ERROR = 2
    WARN  = 3
    INFO  = 4
    DEBUG = 5
    TRACE = 6


# Configuration 

# Log level, logs below the given value
LOG_LEVEL = LogLevel.INFO

# Tags to log, list or None. If list: all tags within the list will be logged, if None: every tag will be logged
LOG_TAGS = None


# Import time and define a starting time
import time
start_time = time.ticks_ms()


class Logger:
    def __init__(self, tag, level=None):
        self._tag = tag
        self._level = level

    def _printMessage(self, level, message):
        global LOG_LEVEL
        global LOG_TAGS
        if self._level != None:
            if level > self._level:
                return
        elif level > LOG_LEVEL:
            return

        if LOG_TAGS != None and (self._tag in LOG_TAGS):
            return

        curentTime = "{:0>9}".format(time.ticks_ms() - start_time)
        levelString = ["FATAL","ERROR","WARN ","INFO ","DEBUG","TRACE"][level - 1]
        print("[{} {}][{}|{}{}][{}]:".format(
            curentTime[0:-3], curentTime[-3:], levelString,
            '##' * (7 - level), '  ' * (level - 1),
            self._tag
        ), *message)

    def LOGF(self, *message):
        self._printMessage(LogLevel.FATAL, message)
    
    def LOGE(self, *message):
        self._printMessage(LogLevel.ERROR, message)

    def LOGW(self, *message):
        self._printMessage(LogLevel.WARN, message)
    
    def LOGI(self, *message):
        self._printMessage(LogLevel.INFO, message)
    
    def LOGD(self, *message):
        self._printMessage(LogLevel.DEBUG, message)

    def LOGT(self, *message):
        self._printMessage(LogLevel.TRACE, message)
        
