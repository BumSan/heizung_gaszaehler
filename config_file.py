
class ConfigFile:
    def __init__(self, config=None):
        if config is not None:
            self.INFLUX_HOST = config['DB_LOGGING']['INFLUX_HOST']
            self.INFLUX_PORT = int(config['DB_LOGGING']['INFLUX_PORT'])
            self.INFLUX_USER = config['DB_LOGGING']['INFLUX_USER']
            self.INFLUX_PWD = config['DB_LOGGING']['INFLUX_PWD']
            self.INFLUX_DB_NAME = config['DB_LOGGING']['INFLUX_DB_NAME']
            self.WRITE_CYCLE_SECONDS = int(config['DB_LOGGING']['WRITE_CYCLE_SECONDS'])

            self.WEATHER_API_KEY = config['WEATHER']['WEATHER_API_KEY']
            self.WEATHER_CITYID = int(config['WEATHER']['WEATHER_CITYID'])

            self.GZ_START_VALUE = float(config['GASZAEHLER']['GZ_START_VALUE'])
