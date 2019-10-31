class PingResponse(object):
    def __init__(self, success, time=None, exception=None):
        self.__success = success
        self.__time = time
        self.__exception = exception

    @property
    def success(self):
        return self.__success

    @property
    def time(self):
        return self.__time

    @property
    def exception(self):
        return self.__exception

    def __str__(self):
        return "PingResponse(success={}, time={}, exception={})" \
            .format(self.__success, self.__time, self.__exception)
