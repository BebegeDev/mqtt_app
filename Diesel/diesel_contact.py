from Interface.interface import InterfaceCallback
from pymodbus.client.serial import ModbusSerialClient


class Contact(InterfaceCallback):

    def __init__(self):
        self.client = ModbusSerialClient(method='rtu', port="/dev/ttyUSB0", baudrate=19200,
                                         bytesize=8, parity='N', stopbits=1)
        self.client.connect()

    async def callback_data(self, topic):
        pass

    def get_data(self, client, userdata, data):
        pass

    def validate_data(self, data):
        pass
