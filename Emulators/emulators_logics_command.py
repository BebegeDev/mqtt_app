
class EmulatorsLogicsCommand:

    def __init__(self):
        self.flag_on = True
        self.flag_off = True
        self.command_queue = []

    def logics_on_off(self, msg):
        if int(msg):
            self.flag_off = True
            if self.flag_on:
                self.flag_on = False
                return msg

        else:
            self.flag_on = True
            if self.flag_off:
                print("Off")
                self.flag_off = False
                return msg


    def add_command(self, command):
        self.command_queue.append(command)


    def process_commands(self):
        while self.command_queue:
            command = self.command_queue.pop(0)
            if not self.is_execute_command(command):
                self.execute_command(command)

    @staticmethod
    def is_execute_command(command):
        return False

    @staticmethod
    def execute_command(command):

        print(f"Run: {command['id']} - {command['action']}")

