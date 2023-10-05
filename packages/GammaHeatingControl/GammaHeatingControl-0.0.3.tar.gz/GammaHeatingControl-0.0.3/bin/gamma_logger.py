#!/usr/bin/env python
import time
from argparse import ArgumentParser
from pathlib import Path

from serial import Serial

from GammaHeatingControl.gamma import GammaFrameLogger

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-l",
                        dest="logfile",
                        type=Path,
                        default=(Path.home() / "gamma_logger.log"),
                        help="Path to logfile")

    parser.add_argument("-p",
                        dest="port",
                        default="/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A6036JHR-if00-port0",
                        help="Path to serial port")
    args = parser.parse_args()
    with Serial(args.port) as ser:
        gamma_logger = GammaFrameLogger(ser=ser, logfile=args.logfile)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
