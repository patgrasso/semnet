
from configparser import ConfigParser

_config = ConfigParser()
_config.read("config.cfg")

get = _config.get


