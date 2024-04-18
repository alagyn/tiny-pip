import os
import yaml

CONFIG_FILE = os.getenv(f'TINYPIP_CONFIG', "tinypip.yaml")
CONFIG_BASE = "{config-base}"


class TinyConfig:

    def __init__(self) -> None:
        with open(CONFIG_FILE, mode='r') as f:
            config = yaml.safe_load(f)['tinypip']

        configBase = os.path.abspath(os.path.dirname(CONFIG_FILE))

        self.pkg_base: str = str(config['pkg_base']).replace(
            CONFIG_BASE, configBase)
        self.index_db: str = str(config['index_db']).replace(
            CONFIG_BASE, configBase)
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
