import asyncio
import json
import threading

import Emulators.contact_emulators


class CommandEmulators:

    def __init__(self):
        self.em = Emulators.contact_emulators.ContactEmulators()
        self.supplySocket_1, self.supplySocket_2 = self.em.supplySockets_1, self.em.supplySockets_2


    def on_off(self, client, userdata, msg):

        if msg.payload.decode() == "11":
            self.em.send_command("OUTPUT 1", self.supplySocket_1)
            self.em.send_command("OUTPUT 1", self.supplySocket_2)

        elif msg.payload.decode() == "00":
            self.em.send_command("OUTPUT 0", self.supplySocket_1)
            self.em.send_command("OUTPUT 0", self.supplySocket_2)

        elif msg.payload.decode() == "10":
            self.em.send_command("OUTPUT 1", self.supplySocket_1)
            self.em.send_command("OUTPUT 0", self.supplySocket_2)

        elif msg.payload.decode() == "01":
            self.em.send_command("OUTPUT 0", self.supplySocket_1)
            self.em.send_command("OUTPUT 1", self.supplySocket_2)

    def set_voltage(self, client, userdata, msg):
        retval = 0
        msg = msg.payload.decode()
        list_msg = eval(msg)
        self.em.set_prog_source_i('eth')
        self.em.set_prog_source_v('eth')
        if list_msg[0] and list_msg[1]:

            self.em.send_command("SOUR:VOLT {0}".format(list_msg[0]), self.supplySocket_1)
            self.em.send_command("SOUR:VOLT {0}".format(list_msg[0]), self.supplySocket_2)
        elif list_msg[0] != '' and list_msg[1] == '':
            self.em.send_command("SOUR:VOLT {0}".format(list_msg[0]), self.supplySocket_1)

        elif list_msg[1] != '' and list_msg[0] == '':
            self.em.send_command("SOUR:VOLT {0}".format(list_msg[1]), self.supplySocket_2)

        else:
            retval = -1
        return retval

    def set_current(self, client, userdata, msg):
        retval = 0
        msg = msg.payload.decode()
        list_msg = eval(msg)
        self.em.set_prog_source_i('eth')
        self.em.set_prog_source_v('eth')
        if list_msg[0] and list_msg[1]:

            self.em.send_command("SOUR:CUR {0}".format(list_msg[0]), self.supplySocket_1)
            self.em.send_command("SOUR:CUR {0}".format(list_msg[1]), self.supplySocket_2)

        elif list_msg[0] != '' and list_msg[1] == '':
            self.em.send_command("SOUR:CUR {0}".format(list_msg[0]), self.supplySocket_1)

        elif list_msg[1] != '' and list_msg[0] == '':
            self.em.send_command("SOUR:CUR {0}".format(list_msg[1]), self.supplySocket_2)


        else:
            retval = -1
        return retval

    def set_time_emulators(self, client, userdata, msg):
        msg = msg.payload.decode()
        list_msg = eval(msg)
        self.em.set_prog_source_i('slot4')
        self.em.set_prog_source_v('slot4')
        self.em.send_command("OUTPUT 1", self.supplySocket_1)
        self.em.send_command("OUTPUT 1", self.supplySocket_2)
        thread = threading.Thread(target=self.build_tasks(client, userdata, list_msg))
        thread.start()

    def build_tasks(self, client, userdata, list_msg):
        msg1 = list_msg[0]
        msg2 = list_msg[1]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Запуск двух экземпляров метода
        tasks = [
            self.run_two_data_us_temp(client, userdata, msg1, 1),
            self.run_two_data_us_temp(client, userdata, msg2, 2)
        ]

        # Ожидание завершения всех задач
        loop.run_until_complete(asyncio.gather(*tasks))

        # Закрытие цикла событий asyncio
        loop.close()

    async def run_two_data_us_temp(self, client, userdata, msg, t):
        tasks = [
            asyncio.create_task(self.time_sleep(client, userdata, msg, t))

        ]
        await asyncio.gather(*tasks)

    async def time_sleep(self, client, userdata, msg, f):

        if f == 1:
            for i in msg:
                self.em.send_command("SYST:INT:SIM:SET GPV,{0}".format(i[2]), self.supplySocket_1)
                # mqttc.publish('mpei/delta/data/USSR1', f'{msg[2]}')
                self.em.send_command("SYST:INT:SIM:SET TPV,{0}".format(i[1]), self.supplySocket_2)
                await asyncio.sleep(int(i[0]))

        # mqttc.publish('mpei/delta/data/temp1', f'{msg[1]}')
        elif f == 2:
            for i in msg:
                self.em.send_command("SYST:INT:SIM:SET GPV,{0}".format(i[2]), self.supplySocket_2)
                #
                self.em.send_command("SYST:INT:SIM:SET TPV,{0}".format(i[1]), self.supplySocket_2)
                await asyncio.sleep(int(i[0]))


    def get_data_emulators(self, mqttc):
        if self.supplySocket_1 != "0":
            result = self.em.send_and_receive_command("MEAS:VOL?\nMEAS:CUR?", self.supplySocket_1)
            power = float(result[0]) * float(result[1])
            print("Имитатор 1:")
            print("-------Напряжение: ", result[0])
            print("-------Ток: ", result[1])
            print("-------Напряжение: ", power)
            mqttc.publish('mpei/Emulator1/Volt', payload=json.dumps({"value": result[0]}))
            mqttc.publish('mpei/Emulator1/Current', payload=json.dumps({"value": result[1]}))
            mqttc.publish('mpei/Emulator1/Power', payload=json.dumps({"value": power}))

        if self.supplySocket_2 != "0":
            result = self.em.send_and_receive_command("MEAS:VOL?\nMEAS:CUR?", self.supplySocket_2)
            power = float(result[0]) * float(result[1])
            print("Имитатор 2:")
            print("-------Напряжение: ", result[0])
            print("-------Ток: ", result[1])
            print("-------Напряжение: ", power)
            mqttc.publish('mpei/Emulator2/Volt', payload=json.dumps({"value": result[0]}))
            mqttc.publish('mpei/Emulator2/Current', payload=json.dumps({"value": result[1]}))
            mqttc.publish('mpei/Emulator2/Power', payload=json.dumps({"value": power}))





