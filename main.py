from config_file import ConfigFile
from gz_data import GZData
from openweather import OpenWeather
import RPi.GPIO as GPIO
import logging
import time
import configparser

logging.basicConfig(level=logging.DEBUG)


# reed is closed, when Level is High. Then we need to count 1 up
def reed_closed(channel):
    db_connection.incrementPerTimeInCubicMeter += 0.01
    db_connection.overallGasCountInCubicMeter += 0.01
    logging.DEBUG('Rising Flank detected. Adding 0.01 m3.')
    return


# reed is open, when Level is Low. For now ignore.
def reed_opened(channel):
    logging.DEBUG('Falling Flank detected.')
    return


if __name__ == '__main__':

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

    # Setup of GPIO to read status of reed contact
    GPIO_INPUT = 24  # Pin 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_INPUT, GPIO.IN)

    # install Interrupts
    GPIO.add_event_detect(GPIO_INPUT, GPIO.RISING, callback=reed_closed, bouncetime=500)
    GPIO.add_event_detect(GPIO_INPUT, GPIO.FALLING, callback=reed_opened, bouncetime=500)

    while True:
        # Reset increment for next cycle
        db_connection.incrementPerTimeInCubicMeter = 0

        # wait for GZ updates via Interrupt
        time.sleep(cfg.WRITE_CYCLE_SECONDS)

        # get Outdoor Temperature
        db_connection.outdoorTemperature = weather.get_outdoor_temperature()

        # write everything to Influx
        db_connection.write_gzdata_to_db()

    GPIO.cleanup()

