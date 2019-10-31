import logging as log

from minecraft.thread.interruptable_thread import InterruptableThread, InterruptException


class AbstractOutputProcessor(InterruptableThread):
    CLOSED_STREAM_EXCEPTION_MESSAGE = "readline of closed file"

    def __init__(self, stop_processing_func, output_stream):
        InterruptableThread.__init__(self, target=self.__process_output_stream, args=(stop_processing_func, output_stream))

    def start(self):
        super().start()
        return self

    def __process_output_stream(self, stop_processing_func, output_stream):
        while not stop_processing_func():
            try:
                line = output_stream.readline()
                self.handle_line(line.decode('utf-8'))
            except ValueError as e:
                # Specific message indicating the stream is closed and we should exit
                if str(e) == AbstractOutputProcessor.CLOSED_STREAM_EXCEPTION_MESSAGE:
                    break
                log.error(e, exc_info=1)
            except InterruptException:
                # Thread was interrupted gracefully exit
                break
            except:
                log.error("Unexpected exception!", exc_info=1)

    def handle_line(self, line):
        raise NotImplementedError("Not implemented!")
