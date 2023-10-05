""" module:: tests.test_protocol
    :platform: Any
    :synopsis: Tests for the protocol.
    moduleauthor:: Patrick Menschel (menschel.p@posteo.de)
    license:: GPL v3
"""
from datetime import datetime
from pathlib import Path
from queue import Empty

import pytest

from src.GammaHeatingControl.protocol import parse_frame, FrameExtractor, FrameType, parse_frame_data

import logging

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def traffic_bytes() -> bytes:
    # traffic_file = list(Path(".").glob("**/traffic.bin"))
    traffic_file = list(Path(".").glob("**/traffic_rs10_install.bin"))
    assert len(traffic_file) > 0
    with traffic_file[0].open("rb") as fp:
        yield fp.read()


@pytest.mark.parametrize("frame,expected", [
    (bytes.fromhex("82102020049510000000000000000000000000000000001000000000000000000010002222a3e303"), None),
    (bytes.fromhex("8210200905005927111695230609645e03"), None),
    (bytes.fromhex("82102080012c002801010103001401f40a010626228c0000021e1e0000280200000402000200021d650300000402020000"
                   "00265e28021165000104020200000028962802146500010402000014fa0001000300647800780000000000000000140206"
                   "1450461401010100000000780a0201460000000000000000000000000000000000000059c403"), None)
])
def test_parse_frame(frame,
                     expected):
    result = parse_frame(frame=frame)
    assert result


@pytest.mark.parametrize("frame_dict,expected", [
    ({"type": FrameType.TimeAndDate,
      "data": bytes.fromhex("000356171971220207"),
      },
     {"info_flags": 0,
      "time": datetime(2022, 7, 19, 17, 56, 3)
      }),
    ({"type": FrameType.TimeAndDate,
      "data": bytearray.fromhex("005628111695230609"),
      },
     {"info_flags": 0,
      "time": datetime(2023, 9, 16, 11, 28, 56)
      }),
    ({"type": FrameType.HeaterInfo,
      "data": bytearray.fromhex("9610000000000000000000000000000000001000000000000000000010002222"),
      },
     {"environment_temperature": 23.0,
      "heater_measured_temperature": 17.0,
      "heater_target_temperature": 0.0,
      "mixer_measured_temperature": 0.0,
      "warm_water_measured_temperature": 0.0}),
    # 16 -> 170 : UnknownType0 : 00
    # 33 -> 16 : UnknownType1 : 80
    # 16 -> 32 : UnknownType1 : 2c002801010103001401f40a010626228c0000021e1e0000280200000402000200021d65030000040202000000265e28021165000104020200000028962802146500010402000014fa00010003006478007800000000000000001402061450461401010100000000780a02014600000000000000000000000000000000000000
    # 33 -> 16 : TimeAndDate : 10
    # 33 -> 16 : UnknownType6 : 28
    # 16 -> 32 : UnknownType6 : 00001400000000002a0007000042000a0002112a200000000002002a200000000002002a20000000
    # 33 -> 32 : UnknownType6 : 29001400000000002a0007000042000a0002112a200000000002002a200000000002002a20000000
    # 33 -> 16 : UnknownType2 : 40
    # 16 -> 170 : UnknownType0 : 01

])
def test_parse_frame_data(frame_dict,
                          expected):
    result = parse_frame_data(frame_dict)
    assert result == expected


def test_frame():
    # data = bytes.fromhex("""ff82ff21ff10ff01ff01ff80ff78ff6fff03ff06ff82ff10ff20ff80ff01ff2cff00ff28ff01ff01ff01ff03ff
    # 00ff14ff01fff4ff0aff01ff06ff26ff22ff8cff00ff00ff02ff1eff1eff00ff00ff28ff02ff00ff00ff04ff02ff00ff02ff00ff02ff1dff65
    # ff03ff00ff00ff04ff02ff02ff00ff00ff00ff26ff5eff28ff0211ff65ff00ff01ff04ff02ff02ff00ff00ff00ff28 ff96ff28ff02ff1465ff
    # 00ff01ff04ff02ff00ff00ff14fffaff00ff01ff00ff03ff00ff64ff78ff00ff78ff00ff00ff00ff00ff00ff00ff00ff00ff14ff02ff06ff14
    # ff50ff46ff14ff01ff01ff01ff00ff00ff00ff00ff78ff0aff02ff01ff46ff00ff00ff00ff000000ff00ff00ff00ff00ff00ff00ff00ff00ff
    # 00ff00ff00ff00ff00ff59ffc4ff03ff""")
    data = bytes.fromhex("""ff82ff10ff20ff80ff01ff2cff00ff28ff01ff01ff01ff03ff
        00ff14ff01fff4ff0aff01ff06ff26ff22ff8cff00ff00ff02ff1eff1eff00ff00ff28ff02ff00ff00ff04ff02ff00ff02ff00ff02ff1dff65
        ff03ff00ff00ff04ff02ff02ff00ff00ff00ff26ff5eff28ff0211ff65ff00ff01ff04ff02ff02ff00ff00ff00ff28 ff96ff28ff02ff1465ff
        00ff01ff04ff02ff00ff00ff14fffaff00ff01ff00ff03ff00ff64ff78ff00ff78ff00ff00ff00ff00ff00ff00ff00ff00ff14ff02ff06ff14
        ff50ff46ff14ff01ff01ff01ff00ff00ff00ff00ff78ff0aff02ff01ff46ff00ff00ff00ff000000ff00ff00ff00ff00ff00ff00ff00ff00ff
        00ff00ff00ff00ff00ff59ffc4ff03ff""")
    a = bytes(filter(lambda x: x != 0xFF, data))
    print(a.hex())
    parse_frame(a)


class TestFrameExtractor:

    def test_parse_one_complete_frame(self):
        fe = FrameExtractor()
        fe.put(bytes.fromhex("82102020049510000000000000000000000000000000001000000000000000000010002222a3e303"))

        result = fe.get_no_wait()
        assert result
        with pytest.raises(Empty):
            fe.get_no_wait()

    def test_parse_two_complete_frames(self):
        fe = FrameExtractor()
        fe.put(bytes.fromhex("82102020049510000000000000000000000000000000001000000000000000000010002222a3e303"))
        fe.put(bytes.fromhex("82102020049510000000000000000000000000000000001000000000000000000010002222a3e303"))
        result = fe.get_no_wait()
        assert result
        result = fe.get_no_wait()
        assert result
        with pytest.raises(Empty):
            fe.get_no_wait()

    def test_parse_two_in_complete_frames(self):
        fe = FrameExtractor()
        fe.put(bytes.fromhex("82102020049510000000000000000000000000000000001000000000000000000010002222a3e3"))
        with pytest.raises(Empty):
            fe.get_no_wait()
        assert fe._buffer == bytearray.fromhex(
            "82102020049510000000000000000000000000000000001000000000000000000010002222a3e3")
        fe.put(bytes.fromhex("03"))  # the last byte of the frame
        result = fe.get_no_wait()
        assert result

    def test_parse_of_real_traffic(self, traffic_bytes):
        fe = FrameExtractor()
        fe.put(traffic_bytes)
        frames = []
        try:
            while True:
                result = fe.get_no_wait()
                frames.append(result)
        except Empty:
            pass
        LOGGER.debug("found {0} frames".format(len(frames)))
        # assert len(frames) == 240
        # we don't know if this is right but at least we want to know if that number changes, like we broke something

        debug_file = Path("frame_sequence.txt")
        last_frame = None
        with debug_file.open("w") as fp:
            for frame in frames:
                if frame != last_frame:
                    fp.write("{0.name} -> {1.name} : {2.name} : {3}\n".format(frame.get("source_addr"),
                                                                              frame.get("dest_addr"),
                                                                              frame.get("type"),
                                                                              frame.get("data").hex()))
                    last_frame = frame

        worklist = []
        frame_variants = []
        for frame in frames:
            if frame.get("data") not in worklist:
                worklist.append(frame.get("data"))
                frame_variants.append(frame)
        LOGGER.debug("found {0} unique frames".format(len(frame_variants)))
        debug_file = Path("frame_variants.txt")
        with debug_file.open("w") as fp:
            for frame in frame_variants:
                fp.write("{0.name} -> {1.name} : {2.name} : {3}\n".format(frame.get("source_addr"),
                                                                          frame.get("dest_addr"),
                                                                          frame.get("type"),
                                                                          frame.get("data").hex()))
