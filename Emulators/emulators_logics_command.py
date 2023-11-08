
class EmulatorsLogicsCommand:

    def __init__(self):
        self.flag_on = True
        self.flag_off = True

    def logics_on_off(self, msg):
        if int(msg):
            self.flag_off = True
            if self.flag_on:
                self.flag_on = False
                return msg
            else:
                print("Команда On уже отправлена")
        else:
            self.flag_on = True
            if self.flag_off:
                print("Off")
                self.flag_off = False
                return msg
            else:
                print("Команда Off уже отправлена ")
