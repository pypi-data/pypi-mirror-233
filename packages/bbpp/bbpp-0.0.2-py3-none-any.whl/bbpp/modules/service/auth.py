import json
import os.path


class Authenticate:
    def __init__(self,
                 username: str = None,
                 password: str = None, ):

        self.config_file = os.path.join(os.path.expanduser("~"), '.bbpp/bbpp.conf')

        if username and password:
            self._write_config_file(username=username, password=password)
        else:
            self.check_config_file_exists()
            self.config = self._read_config_file()
            self.username = self.config['username']
            self.password = self.config['password']
            self.auth = (self.username, self.password)

    def check_config_file_exists(self):
        if not os.path.exists(self.config_file):
            raise ValueError("Cannot find config file, please configure your credentials `bbpp config -h`")

    def _write_config_file(self, username: str, password: str):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            config = {"username": username, "password": password}
            f.write(json.dumps(config))

    def _read_config_file(self):
        with open(self.config_file, 'r') as f:
            config = json.loads(f.read())
            return config
