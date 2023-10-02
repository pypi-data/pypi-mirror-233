""" module:: GammaHeatingControl.gamma
    :platform: Any
    :synopsis: The Reader object.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
import logging
from threading import Thread

from serial import Serial

from GammaHeatingControl.protocol import FrameExtractor


class GammaBaseReader:

    def __init__(self, ser: Serial):
        self._ser = ser
        self._logger = logging.getLogger()
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
    pass
