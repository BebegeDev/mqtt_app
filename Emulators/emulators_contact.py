import configparser
import json
import os
import socket
import re
from sys import platform


class ContactEmulators:

    def __init__(self, mqttc, name_config):
        self.result = None
        self.power = None
        self.socket = None
        self.mqttc = mqttc
        self.config = configparser.ConfigParser()
        self.sockets = []
        self.validSrcList = ["front", "web", "seq", "eth", "slot1", "slot2", "slot3", "slot4", "loc", "rem"]
        self.command_list = ["MEAS:VOL?", "MEAS:CUR?", "MEAS:POW?"]
        self.name_config = name_config



    def send_command(self, msg):
        msg = msg + "\n"
        self.socket.sendall(msg.encode("UTF-8"))


    def set_prog_source_v(self, src):
        retval = 0
        if src in self.validSrcList:
            self.send_command("SYST:REM:CV {0}".format(src))

        else:
            retval = -1
        return retval

    def set_prog_source_i(self, src):
        retval = 0
        if src.lower() in self.validSrcList:
            self.send_command("SYST:REM:CC {0}".format(src))
        else:
            retval = -1
        return retval

    @staticmethod
    def close_socket(supply_socket):
        print("closed socket ", supply_socket)
        supply_socket.shutdown(socket.SHUT_RDWR)
        supply_socket.close()

    def __connect_sockets(self, data_socket, timeout_seconds):
        print(f"Подключение к имитатору: {data_socket}")
        ip, port = data_socket
        try:
            supply_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            supply_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            supply_socket.connect((ip, port))
            supply_socket.settimeout(timeout_seconds)
            print(f"Успешное подключение к {supply_socket}")
            print(f"------------------------------------------------------------------")
            self.sockets_flag = True
            return supply_socket
        except (ConnectionRefusedError, TimeoutError) as e:
            print(f"Ошибка {e} при подключении к {data_socket}")
            print(f"------------------------------------------------------------------")
            self.sockets_flag = False
    
    def send_and_receive_command(self, msg, supply_socket):
        msg = msg + "\n"
        supply_socket.sendall(msg.encode("UTF-8"))
        buffer_size = self.config[self.name_config]["BUFFER_SIZE"]
        try:
            return re.findall(r'\d+\.\d+', supply_socket.recv(int(buffer_size)).decode())
        except TimeoutError as e:
            print(e)

    def connection_sim(self, path):
        self.config.read(path)
        ip = self.config[self.name_config]["IP"]

        port = int(self.config[self.name_config]["PORT"])
        timeout = int(self.config[self.name_config]["TIMEOUT_SECONDS"])
        self.socket = self.__connect_sockets([ip, port], timeout)

    def get_data_emulators(self):
        if self.sockets_flag:
            try:
                self.result = self.send_and_receive_command("MEAS:VOL?\nMEAS:CUR?", self.socket)
                self.power = float(self.result[0]) * float(self.result[1])
            except TypeError:
                print(f"Выходные параметры {self.socket} являются типа None")

