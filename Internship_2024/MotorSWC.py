# This SWC is responsible for controlling the motors speed according to regulations

# Autogenerated code, DO NOT EDIT
from RTE import Rte_Read_MotorSWC_E_State, Rte_Read_MotorSWC_si16_Angle, Rte_Read_MotorSWC_si16_turn_angle, Rte_Write_MotorSWC_si16_Motor_speed_left, Rte_Write_MotorSWC_si16_Motor_speed_right, Rte_Write_MotorSWC_si16_turn_angle
# End of autogenerated code

import uasyncio as asyncio
from typedefs import States

# Configuration
runPeriod = 50
timeGuards = {
    "forward-backward": 500,
    "left-right": 100
}
motorSpeed = 100

async def MotorSWC():
    global runPeriod
    global timeGuards
    global motorSpeed

    forwardGuard = 0
    backwardGuard = 0
    leftGuard = 0
    rightGuard = 0
    while True: 
        state = Rte_Read_MotorSWC_E_State()
        angle = Rte_Read_MotorSWC_si16_Angle()

        # Write the motor speeds considering the guards
        if state == States.GO_FORWARD and forwardGuard <= 0:
            backwardGuard = timeGuards["forward-backward"]
            Rte_Write_MotorSWC_si16_Motor_speed_left(motorSpeed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(motorSpeed)
        elif state == States.GO_BACKWARD and backwardGuard <= 0:
            forwardGuard = timeGuards["forward-backward"]
            Rte_Write_MotorSWC_si16_Motor_speed_left(-motorSpeed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(-motorSpeed)
        elif state == States.TURN_LEFT and leftGuard <= 0:
            rightGuard = timeGuards["left-right"]
            Rte_Write_MotorSWC_si16_Motor_speed_left(-motorSpeed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(motorSpeed)
        elif state == States.TURN_RIGHT and rightGuard <= 0:
            leftGuard = timeGuards["left-right"]
            Rte_Write_MotorSWC_si16_Motor_speed_left(motorSpeed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(-motorSpeed)
        # turn angle state:
        elif state == States.TURN_ANGLE 
            turn_angle = Rte_Read_MotorSWC_si16_turn_angle()
            if angle > (turn_angle % 360) - 2 and angle < (turn_angle % 360) + 2:
                turn_angle = 0
                Rte_Write_MotorSWC_si16_turn_angle(turn_angle)
            
            elif turn_angle < 0:
                Rte_Write_MotorSWC_si16_Motor_speed_left(-motorSpeed)
                Rte_Write_MotorSWC_si16_Motor_speed_right(motorSpeed)
            else:
                Rte_Write_MotorSWC_si16_Motor_speed_right(-motorSpeed)
                Rte_Write_MotorSWC_si16_Motor_speed_left(motorSpeed)
            

        else:
            Rte_Write_MotorSWC_si16_Motor_speed_left(0)
            Rte_Write_MotorSWC_si16_Motor_speed_right(0)

        # Process guards
        leftGuard = max(leftGuard - runPeriod, 0)
        rightGuard = max(rightGuard - runPeriod, 0)
        forwardGuard = max(forwardGuard - runPeriod, 0)
        backwardGuard = max(backwardGuard - runPeriod, 0)

        await asyncio.sleep_ms(runPeriod)
