from Interface.interface import InterfaceCallback

interface = InterfaceCallback


class Command(InterfaceCallback):

    def __init__(self, mqttc, connect):
        self.parsed_data = None
        self.mqttc = mqttc
        self.connect = connect

    def callback_data(self, topic='mpei/command/on_off'):
        self.mqttc.message_callback_add(topic, self.get_data)

    def get_data(self, client, userdata, data):
        try:
            self.parsed_data = int(data.payload.decode())
            if self.parsed_data:
                print("Команда вкл.", self.parsed_data)
            else:
                print('Команды выкл', self.parsed_data)
        except Exception as e:
            print(f"Ошибка при обработке данных: {e}")

    def validate_data(self, data):
        pass

    def check_connections(self, column):
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM control_signal WHERE id ='1'")
        start_stop = cursor.fetchone()[column]
        cursor.close()
        return start_stop

    def get_param_em(self, tables):
        cursor = self.connect.cursor()
        cursor.execute(f"SELECT * FROM {tables} WHERE id ='1'")
        param_em = list(cursor.fetchall()[0].values())
        cursor.close()
        return param_em

    def get_available_dgu(self):
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM control_dgu")
        excluded_engines = list(cursor.fetchall()[0].values())[2:]
        return excluded_engines

    def update_current_power(self, power):
        cursor = self.connect.cursor()
        cursor.execute(f"UPDATE current_power SET current_power = {power} WHERE id = 1")
        cursor.close()

    def get_excluded_engines(self):
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM control_dgu_new")
        excluded_engines = cursor.fetchall()
        cursor.close()
        return excluded_engines

    def update_excluded_engines(self, available_dgu, status):
        cursor = self.connect.cursor()
        for dgu in available_dgu:
            cursor.execute(f"UPDATE control_dgu_new SET control_dgu = {status} WHERE slave = {dgu['slave']}")
        cursor.close()

    def update_control_signal(self, column, status):
        cursor = self.connect.cursor()
        cursor.execute(f"UPDATE control_signal SET {column} = {status} WHERE id = 1")
        cursor.close()





