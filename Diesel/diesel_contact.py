import json
import os
import time
import serial
from pymodbus.client.serial import ModbusSerialClient


class DieselCommand:
    def __init__(self, mqttc):
        self.mqttc = mqttc
        self.message = None
        self.client = ModbusSerialClient(method='rtu', port="/dev/ttyUSB0", baudrate=19200,
                                         bytesize=8, parity='N', stopbits=1)
        self.client.connect()

    def open_json(self, path):
        current_script_path = os.path.abspath(__file__)
        project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + path
        with open(project_root_path, 'r') as json_file:
            topics = json.load(json_file)
        return topics

    def set_point(self):
        rhr = self.client.read_holding_registers(address=0, count=1,
                                                 slave=2)  # текущая уставка по мощности в виде регистра
        setting_now = int(''.join(map(str, rhr.registers)))  # текущая уставка по мощности в виде integer (%)

    def rated_power(self):
        rir = self.client.read_input_registers(address=1510, count=1, slave=2)  # номинальная мощность (регистры)
        Nom_power = int(''.join(map(str, rir.registers)))  # номинальная мощность (integer)
        return Nom_power

    def current_generator_power(self):
        rdi = self.client.read_discrete_inputs(address=3, count=1, slave=2)  # статус работы (запущен или нет)
        return rdi

    def job_status(self):
        rdi2 = self.client.read_discrete_inputs(address=31, count=1,
                                                slave=2)  # готовность к авто-запуску (готов или нет)
        return rdi2.bits

    def autorun(self):
        rir2 = self.client.read_input_registers(address=519, count=1,
                                                slave=2)  # текущая мощность генератора/шин (регистры)
        Current_power = int(''.join(map(str, rir2.registers)))  # текущая мощность генератора/шин (integer)
        return Current_power

    def voltage_frequency(self):
        rdi3 = self.client.read_discrete_inputs(address=4, count=1,
                                                slave=2)  # напряжение/частота в порядке (да или нет)
        return rdi3.bits

    def publish_topic(self, topics):
        # list_method_diesel = [self.set_point(), self.rated_power(), self.current_generator_power(), self.job_status(),
        #                       self.autorun(), self.voltage_frequency()]
        for topic_list in topics:
            for _, topic_list_dgu in topic_list.items():
                for topic in topic_list_dgu:
                    self.mqttc.publish(
                        topic, 0
                    )
