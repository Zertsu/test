#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import uasyncio as asyncio


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Initialize motors, ultrasonic sensor, and gyro sensor
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
bazooka = Motor(Port.A)
ultrasonic_sensor = UltrasonicSensor(Port.S4)
gyro_sensor = GyroSensor(Port.S3)
# Initialize the Color Sensor. It is used to detect the color of the objects.
color_sensor = ColorSensor(Port.S1)

# Task to read ultrasonic sensor continuously
async def read_ultrasonic_sensor():
    while True:
        
        await asyncio.sleep_ms(15)  # Adjust sleep time as needed


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(read_ultrasonic_sensor())
    
    loop.run_forever()

# Run the event loop
main()
