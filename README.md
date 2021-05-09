# pygreensens
python package for the GreenSens Plant Sensor API


Usage:

from pygreensens import GreenSens
gs = GreenSens("username", "password", ["monitored", "conditions"])

gs.fetch_single_plant(sensor_id) -> returns the information for a specific sensor
gs.update() -> checks validity of Bearer token (renews if necessary) and updates the sensor data
gs.hubs -> list of all hubs connected to account
gs.sensors -> list of all sensors connected to account
gs.plants -> dictionary of all plants and the monitored conditions


