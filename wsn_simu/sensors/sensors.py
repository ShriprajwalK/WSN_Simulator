"""Sensor data and functionality."""
import random


class Sensor(object):
    """
    Class for different types of sensors.

    Different kinds
    """

    def __init__(self, name=None, parameter=None,
                 available_sensors=None):
        """Inititialise sensor details."""
        self.name = name
        self.parameter = parameter
        if available_sensors is None:
            print("No available sensors")
        else:
            self.details = available_sensors.loc[name, :]
            self.parameter = self.details[1]
            self.minimum = self.details[2]
            self.maximum = self.details[3]
            self.units = self.details[4]
            self.power_consumed = self.details[5]

    def sense_value(self):
        """Generate random data in sensiog range."""
        return str(random.randint(self.minimum, self.maximum)) + self.units
