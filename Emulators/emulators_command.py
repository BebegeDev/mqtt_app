from Emulators.emulators_logics_command import EmulatorsLogicsCommand


class CommandEmulators:

    def __init__(self, mqttc, em):
        self.em = em
        self.mqttc = mqttc
        self.flags = EmulatorsLogicsCommand()

    def on_off(self, client, userdata, msg):
        msg = msg.payload.decode()
        if self.flags.logics_on_off(msg):
            self.em.send_command("OUTPUT 1", self.em)
        else:
            self.em.send_command("OUTPUT 0", self.em)


    def set_voltage(self, client, userdata, msg):
        retval = 0
        msg = msg.payload.decode()
        self.em.set_prog_source_i('eth')
        self.em.set_prog_source_v('eth')
        if msg:
            self.em.send_command(f"SOUR:VOLT {msg}", self.em)
        else:
            retval = -1
        return retval

    def set_current(self, client, userdata, msg):
        retval = 0
        msg = msg.payload.decode()
        self.em.set_prog_source_i('eth')
        self.em.set_prog_source_v('eth')
        if msg:
            self.em.send_command(f"SOUR:CUR {msg}", self.em)
        else:
            retval = -1
        return retval









