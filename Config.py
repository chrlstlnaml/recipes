from configparser import ConfigParser


class Config:
    def __init__(self, filename='config.ini'):
        self.filename = filename

    def get_param(self, section):
        parser = ConfigParser()
        parser.read(self.filename)
        Data = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                Data[param[0]] = param[1]
        else:
            raise Exception(f'Секция "{section}" не найдена в файле "{self.filename}"')
        return Data
