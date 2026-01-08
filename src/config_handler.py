import yaml

class ConfigHandler():
    @staticmethod
    def load(config_file):
        config = {}
        with open(config_file) as file:
            config = yaml.safe_load(file)
        return config
        
        