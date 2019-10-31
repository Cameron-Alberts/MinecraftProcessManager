import logging as log

from .health_monitor_strategy import AbstractHealthMonitorStrategy


class SimpleLatencyHealthMonitorStrategy(AbstractHealthMonitorStrategy):
    def __init__(self,
                 max_latency_in_seconds=1.0,
                 number_of_pings=5,
                 health_checks_queue_size=5,
                 expected_percent_healthy=.75,
                 *args,
                 **kwargs):
        AbstractHealthMonitorStrategy.__init__(self, *args, **kwargs)
        if max_latency_in_seconds <= 0.0:
            raise ValueError("max_latency_in_seconds must be greater than zero!")
        if number_of_pings <= 0.0:
            raise ValueError("number_of_pings must be greater than zero!")
        if health_checks_queue_size <= 0.0:
            raise ValueError("health_checks_queue_size must be greater than zero!")
        if expected_percent_healthy <= 0.0 or expected_percent_healthy > 1.0:
            raise ValueError("expected_percent_healthy should be between (0.0, 1.0]")
        self.__max_latency = max_latency_in_seconds
        self.__number_of_pings = number_of_pings
        self.__health_checks_queue_size = health_checks_queue_size
        self.__health_checks = [True] * health_checks_queue_size
        self.__expected_percent_healthy = expected_percent_healthy

    def health_check(self):
        ping_responses = [self._minecraft_server.ping() for _ in range(self.__number_of_pings)]
        health_check = self.__is_successful(ping_responses) and self.__is_latency_healthy(ping_responses)
        self.__health_checks = [health_check] + self.__health_checks[0:-1]
        healthy = sum(self.__health_checks) / len(self.__health_checks) >= 0.5
        if healthy:
            log.info("Moving window health checks healthy! health_checks={}".format(self.__health_checks))
        else:
            # Reset health checks, since returning unhealthy will cause the server to bounce
            self.__health_checks = [True] * self.__health_checks_queue_size
            log.warning("Moving window health checks unhealthy! health_checks={}".format(self.__health_checks))
        return healthy

    def __is_latency_healthy(self, ping_responses):
        pings_with_time = list(filter(lambda x: x.time is not None, ping_responses))
        if not pings_with_time:
            log.warning("No pings with a valid time value! pings = {}"
                        .format(' '.join([str(x) for x in ping_responses])))
            return False
        total_latency = sum(x.time for x in pings_with_time)
        avg_latency = total_latency / len(pings_with_time)
        healthy = avg_latency < self.__max_latency
        if not healthy:
            log.warning("Avg latency = {} millis, expected it to be less than {} millis"
                        .format(avg_latency * 1000, self.__max_latency * 1000))
        else:
            log.info("Healthy avg latency of {} millis".format(avg_latency * 1000))
        return healthy

    @staticmethod
    def __is_successful(ping_responses):
        successful = all(x.success for x in ping_responses)
        if not successful:
            log.warning("Not all pings were successful, pings={}"
                        .format(' '.join([str(x) for x in ping_responses])))
        else:
            log.info("All pings successful!")

        return successful
