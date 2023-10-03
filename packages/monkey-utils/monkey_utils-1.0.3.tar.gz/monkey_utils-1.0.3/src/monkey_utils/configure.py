import configparser

class MonkeyConfigParser(configparser.ConfigParser):
    
    """Load configuration from .ini file."""
    
    __instance = None
    @staticmethod
    def get_instance(config_path:str=None):
        if MonkeyConfigParser.__instance is None:
            MonkeyConfigParser.__instance = MonkeyConfigParser(config_path)
        return MonkeyConfigParser.__instance

    def __init__(self, config_path:str=None) -> None:
        super().__init__()
        self.read(config_path)
    