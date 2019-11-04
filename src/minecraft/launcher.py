import argparse
import inspect
import importlib
import json
import logging

from minecraft.monitor.health_monitor_strategy import AbstractHealthMonitorStrategy
from minecraft.process.process_manager import ProcessManager
from minecraft.server.minecraft_server import MinecraftServer


def to_dict(string):
    return json.loads(string)


def to_list(string):
    return string.split(' ')


def setup_logging():
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.INFO)


def find_health_check_strategy(health_check_strategy_name):
    try:
        module = importlib.import_module('minecraft.monitor.{0}'.format(health_check_strategy_name))
        for x in dir(module):
            obj = getattr(module, x)

            if inspect.isclass(obj) and issubclass(obj, AbstractHealthMonitorStrategy) and obj is not AbstractHealthMonitorStrategy:
                return obj
    except ImportError:
        return None


def build_args():
    parser = argparse.ArgumentParser(description='Process manager to keep your minecraft server running!')

    parser.add_argument('-host',
                        '--hostname',
                        dest='hostname',
                        required=True,
                        help='host name or IP address')
    parser.add_argument('-p',
                        '--port',
                        dest='port',
                        type=int,
                        default=25565,
                        help='port number (default: 25565)')
    parser.add_argument('-wd',
                        '--working-directory',
                        dest='working_directory',
                        type=str,
                        required=True,
                        help=r'The directory with your minecraft server (EX: C:\Users\MyName\Directory)')
    parser.add_argument('-jar',
                        '--server-jar',
                        dest='server_jar',
                        type=str,
                        required=True,
                        help='Server jar name (EX: server.jar)')
    parser.add_argument('-jargs',
                        '--jvm-args',
                        dest='jvm_args',
                        type=to_list,
                        default='-Xmx4g -Xms2g -XX:+UseParallelGC',
                        help='Space separated jvm args (default: -Xmx4g -Xms2g -XX:+UseParallelGC)')
    parser.add_argument('-g',
                        '--gui',
                        dest='gui',
                        default=False,
                        action='store_const',
                        const=True,
                        help='If specified will enable launching the server with the GUI console')
    parser.add_argument('-hcs',
                        '--health-check-strategy',
                        dest='health_check_strategy',
                        type=find_health_check_strategy,
                        default='simple_latency_strategy',
                        help='The name of a AbstractHealthMonitorStrategy in the monitor package '
                             '(default: simple_latency_strategy)')
    parser.add_argument('-hcsa',
                        '--health-check-strategy-args',
                        dest='health_check_strategy_args',
                        type=to_dict,
                        default='{}',
                        help='Json health check strategy args, depends on chosen strategy in --health-check-strategy '
                             '(EX: {"max_latency_in_seconds": 2.0})')
    parser.add_argument('-hcd',
                        '--health-check-delay',
                        dest='health_check_delay',
                        type=float,
                        default=5,
                        help='Time health checks in seconds (default: 5)')
    parser.add_argument('-ts',
                        '--time-to-sleep-after-start',
                        dest='time_to_sleep_after_start',
                        type=float,
                        default=60,
                        help='Time to sleep in seconds after starting the server, should be large enough that the server '
                             'is up and running (default: 60)')
    parser.add_argument('-psct',
                        '--ping-socket-connection-timeout',
                        dest='ping_socket_connection_timeout',
                        type=float,
                        default=1.0,
                        help='Timeout in seconds when connecting to the Minecraft socket (default: 1.0)')

    return parser.parse_args()

def main():
    setup_logging()
    args = build_args()
    minecraft_server = MinecraftServer(
        working_directory=args.working_directory,
        server_jar_name=args.server_jar,
        jvm_args=args.jvm_args,
        host=args.hostname,
        port=args.port,
        no_gui=not args.gui,
        socket_connection_timeout=args.ping_socket_connection_timeout
    )

    health_check_args = args.health_check_strategy_args
    health_check_strategy = args.health_check_strategy(minecraft_server = minecraft_server, ** health_check_args)

    process_manager = ProcessManager(
        minecraft_server=minecraft_server,
        health_check_delay=args.health_check_delay,
        time_to_sleep_after_start=args.time_to_sleep_after_start,
        health_check_strategy=health_check_strategy
    )

    process_manager.keep_alive()
