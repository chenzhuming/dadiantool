import configparser


class ConfigIni():
    def __init__(self, filename):
        self.configparser = configparser.ConfigParser()
        self.configparser.read(filename,encoding='utf8')
        self.filename = filename

    def read(self, section, option):
        return self.configparser.get(section, option)

    def update(self, section, option, value):
        self.configparser.set(section, option, value)
        self.configparser.write(open(self.filename, 'w',encoding='utf8'))


if __name__ == "__main__":
    ConfigIni = ConfigIni("config.ini")
    print(ConfigIni.read("reg", "keyword"))
    # ConfigIni.update("section", "option", "value2")
    # print(ConfigIni.read("section", "option"))