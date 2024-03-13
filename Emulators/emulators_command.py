class CommandEmulators:

    def __init__(self, em):
        self.em = em

    def on_off(self, command):
        print(f"Calling on_off with command: {command}")
        self.em.send_command(command)

    def set_point_command(self, command):
        print(f"Calling set_point_command with command: {command}")
        retval = 0
        self.em.set_prog_source_i('eth')
        self.em.set_prog_source_v('eth')
        if command:
            self.em.send_command(command)
        else:
            print("ERROR")
            retval = -1
        return retval





