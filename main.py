from config_file import ConfigFile
from gz_data import GZData
from openweather import OpenWeather, WeatherData
import RPi.GPIO as GPIO
import logging
import time
import configparser

logging.basicConfig(level=logging.CRITICAL)

GPIO_INPUT = 24  # Pin 18
_incrementPerTimeInCubicMeter: float = 0.00


# reed is closed, when Level changes to High. Then we need to count 1 up
def reed_closed(channel):
    global _incrementPerTimeInCubicMeter
    global _overallGasCountInCubicMeter

    # SW debounce. Must be 4 times high
    val = 0
    while val < 4:
        val += 1
        if GPIO.input(GPIO_INPUT) == 1:
            time.sleep(0.2)
        else:
            logging.debug('Debounce removed the trigger.')
            return

    _incrementPerTimeInCubicMeter += 0.01
    _overallGasCountInCubicMeter += 0.01

    logging.debug('Rising Flank detected. Adding 0.01 m3.')
    return


if __name__ == '__main__':

    global _overallGasCountInCubicMeter

    # Config file
    config = configparser.ConfigParser()
    config.read('gz_config.ini')

    cfg = ConfigFile(config)
    db_connection = GZData(cfg)
    weather = OpenWeather(cfg)

    # check start value for GZ. Either from config; or from DB (check which value is bigger)
    db_overall_gas = db_connection.read_overall_gas_in_cubicmeter()
    if db_overall_gas is not None:
        if cfg.GZ_START_VALUE > db_overall_gas:
            # use configured value
            db_connection.overallGasCountInCubicMeter = cfg.GZ_START_VALUE
        else:
            # use DB value, seems to be more up to date
            db_connection.overallGasCountInCubicMeter = db_overall_gas
    else:
        # cant read from DB: Use configured value
        db_connection.overallGasCountInCubicMeter = cfg.GZ_START_VALUE

    # save to global var so we can access it in interrupt callback
    _overallGasCountInCubicMeter = db_connection.overallGasCountInCubicMeter

    # Setup of GPIO to read status of reed contact
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_INPUT, GPIO.IN)

    # install Interrupts
    GPIO.add_event_detect(GPIO_INPUT, GPIO.RISING, callback=reed_closed, bouncetime=1000)

    while True:
        # Reset increment for next cycle
        _incrementPerTimeInCubicMeter = 0

        # wait for GZ updates via Interrupt
        time.sleep(cfg.WRITE_CYCLE_SECONDS)

        # get Outdoor Temperature and Cloudiness
        weather_data = weather.get_weather_data()
        db_connection.outdoorTemperature = weather_data.outdoor_temperature
        db_connection.cloudiness = weather_data.cloudiness

        # write everything to Influx
        db_connection.overallGasCountInCubicMeter = _overallGasCountInCubicMeter
        db_connection.incrementPerTimeInCubicMeter = _incrementPerTimeInCubicMeter
        db_connection.write_gzdata_to_db()

    GPIO.cleanup()

