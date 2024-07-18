from RTE import Rte_Read_IOHandler_si16_Motor_speed_left, Rte_Read_IOHandler_si16_Motor_speed_right, Rte_Read_IOHandler_b_Shoot, Rte_Write_IOHandler_si16_Raw_distance, Rte_Write_IOHandler_si16_Raw_angle, Rte_Write_IOHandler_e_Raw_color, Rte_Write_IOHandler_b_Shoot

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)

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

async def IOHandler():

    #initializing the previos_shoot, shoot_state 
    previous_shoot = 0
    shoot_state = 0

    while True: 

        # reading values from the RTE    
        motor_speed_left = Rte_Read_IOHandler_si16_Motor_speed_left()
        motor_speed_right = Rte_Read_IOHandler_si16_Motor_speed_right()
        shoot = Rte_Read_IOHandler_b_Shoot()
        

        # telling the bazooka to shoot
        if shoot == 1 and previous_shoot = 0:
            bazooka.reset_angle()
            bazooka.run_angle(1080, 1000, then=Stop.HOLD, wait=False)
            shoot = 0
            shoot_state = 1

        # checking if the shoot was completed
        if shoot_state == 1 and bazooka.angle()<1002 and bazooka.angle()>998:
            shoot_state = 0
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

        await asyncio.sleep_ms(50)
