""" module:: GammaHeatingControl.gamma
    :platform: Any
    :synopsis: The Reader object.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from logging import getLogger, DEBUG
from logging.handlers import RotatingFileHandler
from pathlib import Path
from pprint import pprint
from queue import Empty
from threading import Thread

from serial import Serial

from GammaHeatingControl.protocol import FrameExtractor, parse_frame_data


class GammaBaseReader:

    def __init__(self, ser: Serial):
        self._ser = ser
        self._logger = getLogger()
        self._frame_extractor = FrameExtractor()
        self._rx_queue_handler = Thread(target=self.handle_rx)
        self._rx_queue_handler.daemon = True
        self._rx_queue_handler.start()

    def handle_rx(self):
        while True:
            buff = bytearray()
            data = self._ser.read(1)
            if len(data) > 0:
                buff.extend(data)
                buff.extend(self._ser.read(self._ser.inWaiting()))
                self._frame_extractor.put(buff)

    def get(self, timeout: float):
        return self._frame_extractor.get(timeout=timeout)

    def get_no_wait(self):
        return self._frame_extractor.get_no_wait()


class GammaFrameLogger(GammaBaseReader):

    def __init__(self, ser: Serial, logfile: Path):
        super().__init__(ser)
        log_file_handler = RotatingFileHandler(logfile)
        log_file_handler.setLevel(level=DEBUG)
        self._logger.addHandler(log_file_handler)
        self._log_writer = Thread(target=self.write_log)
        self._log_writer.daemon = True
        self._log_writer.start()

    def write_log(self):
        while True:
            try:
                frame = self.get(timeout=1.0)
            except Empty:
                pass
            else:
                self._logger.info("{0.name} -> {1.name} : {2.name} : {3}".format(frame.get("source_addr"),
                                                                                 frame.get("dest_addr"),
                                                                                 frame.get("type"),
                                                                                 frame.get("data").hex()))
                pprint(frame)
                try:
                    parsed_frame = parse_frame_data(frame)
                except ValueError:
                    print("Could no parser this frame")
                else:
                    pprint(parsed_frame)
