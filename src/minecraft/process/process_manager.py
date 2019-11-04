import logging as log
import time


class ProcessManager(object):
    def __init__(self,
                 minecraft_server,
                 health_check_delay,
                 time_to_sleep_after_start,
                 health_check_strategy):
        self.__minecraft_server = minecraft_server
        self.__health_check_delay = health_check_delay
        self.__time_to_sleep_after_start = time_to_sleep_after_start
        self.__health_check_strategy = health_check_strategy

    def keep_alive(self):
        self.__minecraft_server.start()
        log.info("Started server sleeping for {} seconds".format(self.__time_to_sleep_after_start))
        time.sleep(self.__time_to_sleep_after_start)
        while True:
            try:
                if not self.__health_check_strategy.is_healthy():
                    log.warning("Server not healthy restarting it!")
                    self.__minecraft_server.kill()
                    self.__minecraft_server.start()
                    log.info("Restarted server sleeping for {} seconds".format(self.__time_to_sleep_after_start))
                    time.sleep(self.__time_to_sleep_after_start)
                    continue
            except:
                log.error("Unexpected exception while managing server process!", exc_info=1)

            log.info("Sleeping {} seconds before next health check".format(self.__health_check_delay))
            time.sleep(self.__health_check_delay)
