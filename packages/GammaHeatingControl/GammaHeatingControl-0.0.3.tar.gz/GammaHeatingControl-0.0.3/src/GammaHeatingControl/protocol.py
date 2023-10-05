""" module:: GammaHeatingControl.protocol
    :platform: Any
    :synopsis: The protocol description used by EBC Gamma RS-485 bus.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3

    Note: This work is based on https://github.com/bogeyman/gamma/wiki/Protokoll ,
          Not everything there is correct though.
          In my case the communication has 0xFF on every second byte
"""
import logging
from datetime import datetime
from enum import IntEnum
from queue import Queue
from typing import Union, Optional

from crccheck.crc import CrcKermit

LOGGER = logging.getLogger(__name__)


class FrameType(IntEnum):
    UnknownType0 = 0
    UnknownType1 = 1
    UnknownType2 = 2
    HeaterInfo = 4
    TimeAndDate = 5
    UnknownType6 = 6


class BusAddress(IntEnum):
    Master = 0x10
    Heater = 0x20
    RoomStation1 = 0x21
    Unknown0xAA = 0xAA


def parse_time_and_date_frame_data(data: bytes) -> dict:
    """
    Parse the Time and Date Frame.

    Format
    * 1st byte flags
    * 2nd byte seconds BCD format
    * 3rd byte minute BCD format
    * 4th byte hour BCD format
    * 5th byte day of month BCD format
    * 6th byte high nibble month (single digit 1=January up to 0xC=December)
    * 6th byte low nibble day of week (0=Monday up to 6=Sunday)
    * 7th byte year + 2000
    * 8th byte day of week (0=Sunday up to 6 Saturday)
    * 9th byte month BCD format

    Example:
    00 03 56 17 19 71 22 02 07 -->  17:56:03 19.07.2022

    Special Version, 6 bytes longer, if RS10 is installed, 6 unknown bytes trailing:
    00 58 28 11 16 95 23 06 09 40 00 81 97 64 64 55

    :param data: The Data in proprietary format.
    :return: A dictionary with keys info_flags and time
    """
    info_flags = data[0]
    seconds = int(data[1:2].hex())
    minute = int(data[2:3].hex())
    hour = int(data[3:4].hex())
    day = int(data[4:5].hex())
    month = int(data[8:9].hex())
    year = int(data[6:7].hex()) + 2000

    return {"info_flags": info_flags,
            "time": datetime(year=year,
                             month=month,
                             day=day,
                             hour=hour,
                             minute=minute,
                             second=seconds
                             )
            }


def parse_heater_info_frame_data(data: bytes) -> dict:
    """
    Parse the Heater Info Frame.

    Format
    * 1st byte environment temperature, scaling 0.5 degC, offfset 52
    * 7th byte warm water measured temperature, scaling 0.5 degC
    * 10th byte mixer measured temperature, scaling 0.5 degC
    * 16th byte heater target temperature, scaling 0.5 degC
    * 31st byte heater measured temperature, scaling 0.5 degC

    :param data: The Data in proprietary format.
    :return: A dictionary with the parsed values.
    """

    environment_temperature = (data[0] / 2) - 52  # mandatory external temperature sensor
    warm_water_measured_temperature = (data[7] / 2)  # optional external temperature sensor
    mixer_measured_temperature = (data[10] / 2)  # mandatory external temperature sensor
    heater_target_temperature = (data[16] / 2)  # internal temperature governor target value
    heater_measured_temperature = (data[31] / 2)  # internal temperature sensor

    return {"environment_temperature": environment_temperature,
            "warm_water_measured_temperature": warm_water_measured_temperature,
            "mixer_measured_temperature": mixer_measured_temperature,
            "heater_target_temperature": heater_target_temperature,
            "heater_measured_temperature": heater_measured_temperature,
            }


def parse_frame_data(frame_dict: dict) -> dict:
    _mapping_ = {FrameType.HeaterInfo: parse_heater_info_frame_data,
                 FrameType.TimeAndDate: parse_time_and_date_frame_data,
                 }
    frame_type = frame_dict.get("type")
    data = frame_dict.get("data")
    parser_function = _mapping_.get(frame_type)
    assert parser_function is not None
    return parser_function(data=data)


class FrameExtractor:

    def __init__(self):
        self._buffer = bytearray()
        self._out_queue = Queue()

    def put(self, data: bytes):
        self._buffer.extend(filter(lambda x: x != 0xFF, data))
        # For whatever reason, the logs recorded on my devices contain 0xFF values
        # which are not shown in bogeyman's logs
        # LOGGER.debug("Added {0} bytes".format(len(data)))
        self._consume_buffer()

    def _consume_buffer(self):
        start_idx = -1
        stop_idx = start_idx
        start_code = 0x82
        stop_code = 0x03
        while start_code in self._buffer[start_idx + 1:]:
            start_idx = self._buffer.index(start_code, start_idx + 1)
            stop_idx = start_idx
            while stop_code in self._buffer[stop_idx + 1:]:
                stop_idx = self._buffer.index(stop_code, stop_idx + 1)
                try:
                    result = parse_frame(self._buffer[start_idx:stop_idx + 1])
                except AssertionError:
                    pass
                else:
                    self._out_queue.put(result)
                    break
        self._buffer = self._buffer[stop_idx:]

    def get(self, timeout):
        return self._out_queue.get(timeout=timeout)

    def get_no_wait(self):
        return self._out_queue.get_nowait()


def parse_frame(frame: Union[bytes, bytearray]) -> Optional[dict]:
    """
    Parse a data frame into its contents.

    :param frame: The raw frame data.
    :type frame: bytes,bytearray
    :return: The contents.
    :rtype: dict
    """
    assert frame.startswith(b"\x82")
    assert frame.endswith(b"\x03")
    assert len(frame) > 8  # absolute minimum markers + scheme + crc
    frame_without_envelope = frame[1:-1]

    dest_addr, source_addr, frame_advertised_length = frame_without_envelope[:3]

    frame_data = frame_without_envelope[4:-2]
    assert len(frame_data) == frame_advertised_length

    frame_crc = int.from_bytes(frame_without_envelope[-2:], "little")
    calc_crc = CrcKermit.calc(data=frame_without_envelope[:-2])
    assert frame_crc == calc_crc

    try:
        dest_addr = BusAddress(dest_addr)
    except ValueError:
        LOGGER.error("Not a known BusAddress 0x{0:X}".format(dest_addr))

    try:
        source_addr = BusAddress(source_addr)
    except ValueError:
        LOGGER.error("Not a known BusAddress 0x{0:X}".format(source_addr))

    return {"raw": frame,
            "dest_addr": dest_addr,
            "source_addr": source_addr,
            "type": FrameType(frame_without_envelope[3]),
            "data": frame_data}
