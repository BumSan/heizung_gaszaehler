from influxdb import InfluxDBClient
from config_file import ConfigFile
import logging


class GZData:
    incrementPerTimeInCubicMeter: float = 0
    overallGasCountInCubicMeter: float = 0
    outdoorTemperature: float = 0
    cloudiness: float = 0

    def __init__(self, cfg: ConfigFile):
        # ToDo: Read last gas count from influx
        # if influx count is smaller than configured start value: use start value
        self.cfg = cfg
        return

    def write_gzdata_to_db(self):
        try:
            # Influx
            influx = InfluxDBClient(host=self.cfg.INFLUX_HOST
                                    , port=self.cfg.INFLUX_PORT
                                    , username=self.cfg.INFLUX_USER
                                    , password=self.cfg.INFLUX_PWD)

            line_gz = 'gaszaehler,sensor=gas incrementPerTimeInCubicMeter=' + str(self.incrementPerTimeInCubicMeter) \
                      + ',overallGasInCubicMeter=' + str(self.overallGasCountInCubicMeter) \
                      + ',outdoorTemperature=' + str(self.outdoorTemperature) \
                      + ',cloudiness=' + str(self.cloudiness)

            if not influx.write([line_gz], params={'epoch': 's', 'db': self.cfg.INFLUX_DB_NAME},
                                expected_response_code=204, protocol='line'):
                logging.error('Data write failed')

            influx.close()
        except:
            logging.critical('DB Connection is gone')
        return

    def read_overall_gas_in_cubicmeter(self):
        overall_gas = 0.0

        try:
            # Influx
            influx = InfluxDBClient(host=self.cfg.INFLUX_HOST
                                    , port=self.cfg.INFLUX_PORT
                                    , username=self.cfg.INFLUX_USER
                                    , password=self.cfg.INFLUX_PWD
                                    , database=self.cfg.INFLUX_DB_NAME)

            response = influx.query('SELECT LAST("overallGasInCubicMeter") FROM "gaszaehler"')
            if response is not None:
                for point in response.get_points():
                    overall_gas = point['last']
                logging.debug('Overall Gas from DB: %s', overall_gas)
            influx.close()
        except:
            logging.critical('DB Connection is gone')

        return overall_gas
