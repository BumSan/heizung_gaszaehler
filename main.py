import RPi.GPIO as GPIO
import logging
import time

logging.basicConfig(level=logging.DEBUG)

# Press the green button in the gutter to run the script.

GPIO_INPUT = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_INPUT, GPIO.IN)


# reed is closed, when Level is High
def reed_closed(channel):
    return


# reed is open, when Level is Low
def reed_opened(channel):
    return


if __name__ == '__main__':
    gpioInput_position = GPIO.setmode(GPIO.BCM)

    # install IRQ
    GPIO.add_event_detect(GPIO_INPUT, GPIO.RISING, callback=reed_closed, bouncetime=500)
    GPIO.add_event_detect(GPIO_INPUT, GPIO.FALLING, callback=reed_opened, bouncetime=500)

    while True:

        # ToDo: Logging etc.
        time.sleep(5)

    GPIO.cleanup()




