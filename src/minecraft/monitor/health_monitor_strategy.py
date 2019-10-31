import logging as log


class AbstractHealthMonitorStrategy(object):
    def __init__(self, minecraft_server):
        self._minecraft_server = minecraft_server

    def is_healthy(self):
        return self.__is_process_running() and self.health_check()

    def health_check(self):
        raise NotImplementedError("Not implemented!")

    def __is_process_running(self):
        process_running = self._minecraft_server.is_process_running()
        if process_running:
            log.info("Process is running!")
        else:
            log.warning("Process is not running!")
        return process_running
