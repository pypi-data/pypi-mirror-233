# GammaHeatingControl

![coverage](https://gitlab.com/Menschel/GammaHeatingControl/badges/master/coverage.svg)
![pipeline](https://gitlab.com/Menschel/GammaHeatingControl/badges/master/pipeline.svg)

[Documentation](https://menschel.gitlab.io/GammaHeatingControl/)

A python 3 interface to EBV Gamma Heating Control.

# Description

Goal of this project is to create a python interface to communicate with EBV Gamma Heating Control Units.

The Company EBV manufactured the Heating Control Unit "Gamma" in the years 2000-2010 (citation needed!).
The system is able to communicate via RS-485 network, linking the main unit with a cascade of satellite units,
so-called room stations, either passive (temperature sensor) or active (display + remote control + temperature sensor).


# Protocol
There have been notes on the protocol by certain developers [1] but none of them actually finished the job.

The RS-485 network used here is a single master bus. The master is the main unit and the master tries something like
time-division-multiplexing.
It sends sync frames with the address of the satellite system that is supposed to send something.

Example:
21 ... 21 ... 21 ... 21 ... 21 (... = ~60-80ms)

is to trigger the first room station controlling the first mixer circuit to send something.
In general almost everything is repeated 5 times for robustness.

The room station answers to that slot announcement.






# Some Notes
This Protocol was reverse engineered on a Rotex Gamma, a software variant of the EBV Gamma 2B, build into Rotex A1 B20i
from 2002.
That device received an active satellite unit RS10 in 2023 as an upgrade, primarily to get a room temperature reference
into the controller to compensate overheating of >2degC due to sun effects. This also presented the chance to reverse
engineer the protocol.

I recommend anyone to upgrade their heating system with a reference room temperature.
If you don't want to buy such a device, build it yourself with a raspberry pi.
The technology is dead cheap, and it saves vast amounts of energy costs!

The company EBV was not willing to share the protocol specification even decades after the production ended!
Therefore, I do not recommend buying any of their products!


# References

[1] https://github.com/bogeyman/gamma/wiki/Protokoll
