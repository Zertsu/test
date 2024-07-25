#  Handles the informations from the RTE and sends it to the ports accordingly


# Autogenerated code, DO NOT EDIT
from RTE import Rte_Read_IOHandler_si16_Motor_speed_left, Rte_Read_IOHandler_si16_Motor_speed_right, Rte_Read_IOHandler_b_Shoot, Rte_Write_IOHandler_si16_Raw_distance, Rte_Write_IOHandler_si16_Raw_angle, Rte_Write_IOHandler_e_Raw_color, Rte_Write_IOHandler_b_Shoot
# End of autogenerated code

import uasyncio as asyncio

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Stop, Port

# Create your objects here.
ev3 = EV3Brick()

# configuration:

LEFT_MOTOR_PORT = Port.B
RIGHT_MOTOR_PORT = Port.C
BAZOOKA_MOTOR_PORT = Port.A
ULTRASONIC_SENSOR_PORT = Port.S4
GYRO_SENSOR_PORT = Port.S3
COLOR_SENSOR_PORT = Port.S1

global async_timer
async_timer = 20 # this variable stores the time in ms that we use in asyncio.sleep

async def IOHandler():
    # Initialize motors, ultrasonic sensor, color sensor, and gyro sensor

    left_motor = Motor(LEFT_MOTOR_PORT)
    right_motor = Motor(RIGHT_MOTOR_PORT)
    bazooka = Motor(BAZOOKA_MOTOR_PORT)
    ultrasonic_sensor = UltrasonicSensor(ULTRASONIC_SENSOR_PORT)
    gyro_sensor = GyroSensor(GYRO_SENSOR_PORT)
    color_sensor = ColorSensor(COLOR_SENSOR_PORT)

    #initializing the previos_shoot, shoot_state 
    previous_shoot = 0  # stores the previos shoots value 
    shoot_state = 0  # stores the shoots state


    global async_timer
    while True: 

        # reading values from the RTE    
        motor_speed_left = Rte_Read_IOHandler_si16_Motor_speed_left()  # gets the left motors value from RTE
        motor_speed_right = Rte_Read_IOHandler_si16_Motor_speed_right()  # gets the right motors value from RTE
        shoot = Rte_Read_IOHandler_b_Shoot()  #  gets the shoot bit from RTE
        

        # telling the bazooka to shoot
        if shoot == 1 and previous_shoot == 0:
            bazooka.reset_angle(0)
            bazooka.run_angle(1000, 1080, then=Stop.HOLD, wait=False)
            shoot_state = 1


        # checking if the shoot was completed
        if shoot_state == 1 and bazooka.angle()<1082 and bazooka.angle()>1078:
            shoot_state = 0
            shoot = 0
            Rte_Write_IOHandler_b_Shoot(shoot)


        # transfering the data from the RTE to the motors
        left_motor.run(motor_speed_left)
        right_motor.run(motor_speed_right)

        # reading raw values from the sensors
        raw_distance = ultrasonic_sensor.distance()
        raw_angle = gyro_sensor.angle()
        raw_color = color_sensor.color()


        # writing the values to the RTE
        Rte_Write_IOHandler_si16_Raw_distance(raw_distance)
        Rte_Write_IOHandler_si16_Raw_angle(raw_angle)
        Rte_Write_IOHandler_e_Raw_color(raw_color)
        

        previous_shoot = shoot

        await asyncio.sleep_ms(async_timer)
