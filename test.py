import time

from pymodbus.client.serial import ModbusSerialClient


class DieselContact:

    def __init__(self):
        try:
            self.client = ModbusSerialClient(method='rtu', port='COM3', baudrate=9600,
                                             bytesize=8, parity='N', stopbits=1)
            print(self.client)
        except Exception as e:
            print(e)

    def command_read_holding_registers(self, address, count, slave):
        data = self.client.read_holding_registers(address=address, count=count, slave=slave)
        return data.registers


d = DieselContact()
while True:
    print(d.command_read_holding_registers(address=37, slave=16, count=1))
    time.sleep(2)

