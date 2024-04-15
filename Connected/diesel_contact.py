from pymodbus.client.serial import ModbusSerialClient


class DieselContact:

    def __init__(self):
        try:
            self.client = ModbusSerialClient(method='rtu', port='COM4', baudrate=19200,
                                             bytesize=8, parity='N', stopbits=1)
            print(self.client)
        except Exception as e:
            print(e)

