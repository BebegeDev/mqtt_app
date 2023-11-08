
class DieselCommand:
    def __init__(self, client):
        self.client = client

    def command_read_holding_registers(self, address, count, slave):
        data = self.client.read_holding_registers(address=address, count=count, slave=slave)
        return int(''.join(map(str, data.registers)))

    def command_read_input_registers(self, address, count, slave):
        data = self.client.read_input_registers(address=address, count=count, slave=slave)
        return int(''.join(map(str, data.registers)))

    def get_data_bool(self, address, count, slave):
        data = self.client.read_discrete_inputs(address=address, count=count, slave=slave)
        return data.bits
