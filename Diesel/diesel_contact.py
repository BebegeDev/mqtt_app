
from pymodbus.client.serial import ModbusSerialClient


class DieselContact:


    def __init__(self):
        self.client = ModbusSerialClient(method='rtu', port="/dev/ttyUSB0", baudrate=19200,
                                         bytesize=8, parity='N', stopbits=1)
        self.client.connect()
