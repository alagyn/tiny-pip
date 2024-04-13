import os
import yaml

CONFIG_FILE = os.getenv(f'TINYPIP_CONFIG', "tinypip.yaml")


class TinyConfig:

    def __init__(self) -> None:
        with open(CONFIG_FILE, mode='r') as f:
            config = yaml.safe_load(f)['tinypip']

        self.pkg_base: str = config['pkg_base']
        self.index_db: str = config['index_db']
        try:
            self.ft_url: str = config['fallthrough']
            if not self.ft_url.endswith("/"):
                self.ft_url += "/"
            self.fallthrough = True
        except:
            self.ft_url = ""
            self.fallthrough = False

        try:
            self.overwrite = bool(config['overwrite'])
        except KeyError:
            self.overwrite = False


config = TinyConfig()
