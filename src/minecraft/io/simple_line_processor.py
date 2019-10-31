from .output_processor import AbstractOutputProcessor


class SimpleLineProcessor(AbstractOutputProcessor):
    def __init__(self, *args, **kwargs):
        AbstractOutputProcessor.__init__(self, *args, **kwargs)

    def handle_line(self, line):
        stripped_line = line.strip()
        if stripped_line:
            print(stripped_line)