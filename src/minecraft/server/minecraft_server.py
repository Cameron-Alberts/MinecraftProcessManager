import logging as log
import subprocess
import socket
import time

from .ping_response import PingResponse
from minecraft.io.simple_line_processor import SimpleLineProcessor


class MinecraftServer(object):
    MC_SERVER_LIST_PING = b"\xfe"
    MC_DISCONNECT = b"\xff"

    def __init__(self,
                 working_directory,
                 server_jar_name,
                 jvm_args=list(),
                 host="localhost",
                 port=25565,
                 no_gui=True,
                 socket_connection_timeout=1):
        self.__host = host
        self.__port = port
        self.__jvm_args = jvm_args
        self.__working_directory = working_directory
        self.__server_jar_name = server_jar_name
        self.__no_gui = no_gui
        self.__socket_connection_timeout = socket_connection_timeout
        self.__stdout_line_processor = None
        self.__process = None

    def start(self):
        if not self.is_process_running():
            command = self.__build_mc_server_command()
            log.info("Starting the server with command={} in directory={}".format(command, self.__working_directory))
            self.__process = subprocess.Popen(command,
                                              cwd=self.__working_directory,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT,
                                              stdin=subprocess.PIPE)
            log.info("Server started with pid {}".format(self.__process.pid))
            self.__stdout_line_processor = SimpleLineProcessor(self.__process.poll, self.__process.stdout).start()
        else:
            log.info("Server is already running")

    def kill(self):
        if self.is_process_running():
            log.info("Process is running on pid {} sending server stop command".format(self.__process.pid))
            if self.__gracefully_kill() or self.__kill():
                self.__stdout_line_processor = None
                self.__process = None
            else:
                log.warning("Failed to kill process on pid {}".format(self.__process.pid))
        else:
            log.info("Process has already been killed or does not exist")

    def tell_server(self, message):
        self.__process.communicate(message.encode('utf-8'))

    def is_process_running(self):
        if self.__process:
            return not self.__process.poll()
        return False

    def ping(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.__socket_connection_timeout)
            start = time.time()
            s.connect((self.__host, self.__port))
            s.send(MinecraftServer.MC_SERVER_LIST_PING)
            data = s.recv(550)
            end = time.time()
            if data[0].to_bytes(1, byteorder='big') == MinecraftServer.MC_DISCONNECT:
                return PingResponse(success=True, time=end - start)
            s.close()
        except Exception as e:
            return PingResponse(success=False, exception=e)

        return PingResponse(success=False)

    def __kill(self):
        try:
            self.__process.kill()
            self.__kill_stdout_processor()
        except Exception as e:
            log.error(e, exc_info=1)
        return self.is_process_running()

    def __gracefully_kill(self):
        try:
            self.tell_server("stop\n")
            self.__kill_stdout_processor()
        except Exception as e:
            log.error(e, exc_info=1)
        return self.is_process_running()

    def __kill_stdout_processor(self):
        try:
            self.__stdout_line_processor.interrupt()
            self.__stdout_line_processor.join()
        except Exception as e:
            log.error(e, exc_info=1)

    def __build_mc_server_command(self):
        command = ['java']
        if self.__jvm_args:
            command.extend(self.__jvm_args)
        command.extend(['-jar', self.__server_jar_name])
        if self.__no_gui:
            command.append('nogui')
        return r' '.join(command)