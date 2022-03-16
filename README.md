# Counting pulses of a gas meter and drop them with some weather data into InfluxDB
## Main Features
* Counting pulses via reed contact, which is connected to the GPIO
  * Using a 47k Pull-Down to GND
  * Reed connects it to 5V -> it´s counting high pulses
* Weather Data (cloudiness and outdoor temperature) via OpenWeather API
* configurable start value for gas meter
  * For restarts the script using the latest value from the InfluxDB
* Writing Cloudiness, Outdoor Temp, Gas Increment of last 30mins (configurable) and Overall gas to InfluxDB
* Configurable for low write stress on SD Card (Default: every 30mins 1 write cycle)
* Tested with BK-G4T gas meter and Raspberry Pi Zero W

* If you need an example Grafana Dashboard, please see it in the respective folder.



