
import time
import pymodbus
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse
import pandas as pd
import numpy as np
import csv
import serial


class DieselContact:

    def __init__(self):
        self.client = ModbusSerialClient(method='rtu', port='COM4', baudrate=19200,
                                         bytesize=8, parity='N', stopbits=1)
        self.client.connect()

