from decorators.new_user import new_user

from utils.create_file_and_path import Util



class DatabaseConnectionThread:


    def __init__(self, ):
        config = Util().config_pars('setting.ini')

        self.password = config['DB']['PASSWORD']
        self.user = config['DB']['USER']


    @new_user
    def connections_db(self):
        return self.user, self.password

