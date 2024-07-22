from RTE import Rte_Read_MotorSWC_E_State, Rte_Read_MotorSWC_si16_Angle, Rte_Read_MotorSWC_ui32_Time, Rte_Write_MotorSWC_si16_Motor_speed_left, Rte_Write_MotorSWC_si16_Motor_speed_right
import uasyncio as asyncio
from typedefs import States

async def MotorSWC():
    previousState = States.NONE
    timesChanged = 0  # counter for the above situation
    while True: 
        state = Rte_Read_MotorSWC_E_State()
        # angle = Rte_Read_MotorSWC_si16_Angle()   # we might not use this later
        # time - probably won't use it later
        # speeds are in deg/s
        if state == States.SHOOT or state == States.IDLE or state == States.NONE:
            L_motor_speed = 0   # in these cases do nothing, come to a full stop
            R_motor_speed = 0
            
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)


        if state == States.GO_FORWARD and previousState == States.GO_BACKWARD:

            L_motor_speed = 0   # changing from backward to forward, so it needs to reset to 0
            R_motor_speed = 0
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
            
            # have to wait for 0.5 seconds before proceeding!!
            timesChanged += 1
            if timesChanged == 10:
                previousState = state
                L_motor_speed = 100   # random speed I made up to be default speed
                R_motor_speed = 100
                Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
                Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
                timesChanged = 0


            

        if state == States.GO_BACKWARD and previousState == States.GO_FORWARD:
            L_motor_speed = 0   # changing from backward to forward, so it needs to reset to 0
            R_motor_speed = 0
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
            
            # have to wait for 0.5 seconds before proceeding!!

            timesChanged += 1
            if timesChanged == 10:
                previousState = state
                L_motor_speed = -100   # random speed I made up to be default speed
                R_motor_speed = -100
                Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
                Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
                timesChanged = 0

            

        
        # left and right

        if state == States.TURN_LEFT and previousState == States.TURN_RIGHT:
            L_motor_speed = 100   # random speed I made up to be default speed
            R_motor_speed = 100
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
            L_motor_speed = 100   
            R_motor_speed = -100
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)

        if state == States.TURN_RIGHT and previousState == States.TURN_LEFT:
            L_motor_speed = 100   # random speed I made up to be default speed
            R_motor_speed = 100
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
            L_motor_speed = -100
            R_motor_speed = 100
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)


        previousState = state

        await asyncio.sleep_ms(50)  # Adjust sleep time later if needed
