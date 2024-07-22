from RTE import Rte_Read_MotorSWC_E_State, Rte_Read_MotorSWC_si16_Angle, Rte_Read_MotorSWC_ui32_Time, Rte_Write_MotorSWC_si16_Motor_speed_left, Rte_Write_MotorSWC_si16_Motor_speed_right
from typedefs import States

async def MotorSWC():
    previousState = NONE
    timesChanged = 0  # counter for the above situation
    while True: 
        state = Rte_Read_MotorSWC_E_State()
        # angle = Rte_Read_MotorSWC_si16_Angle()   # we might not use this later
        # time - probably won't use it later
        # speeds are in deg/s
        if state == SHOOT or state == IDLE or state == NONE:
            L_motor_speed = 0   # in these cases do nothing, come to a full stop
            R_motor_speed = 0
            
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)


        if state == GO_FORWARD and previousState == GO_BACKWARD:

            L_motor_speed = 0   # changing from backward to forward, so it needs to reset to 0
            R_motor_speed = 0
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
            
            # have to wait for 0.5 seconds before proceeding!!
            timesChanged++
            if timesChanged == 10:
                previousState = state
                L_motor_speed = 100   # random speed I made up to be default speed
                R_motor_speed = 100
                Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
                Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
                timesChanged = 0


            

        if state == GO_BACKWARD and previousState == GO_FORWARD:
            L_motor_speed = 0   # changing from backward to forward, so it needs to reset to 0
            R_motor_speed = 0
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
            
            # have to wait for 0.5 seconds before proceeding!!

            timesChanged++
            if timesChanged == 10:
                previousState = state
                L_motor_speed = -100   # random speed I made up to be default speed
                R_motor_speed = -100
                Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
                Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
                timesChanged = 0

            

        
        # left and right

        if state == TURN_LEFT and previousState == TURN_RIGHT:
            L_motor_speed = 100   # random speed I made up to be default speed
            R_motor_speed = 100
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)
            L_motor_speed = 100   
            R_motor_speed = -100
            Rte_Write_MotorSWC_si16_Motor_speed_left(L_motor_speed)
            Rte_Write_MotorSWC_si16_Motor_speed_right(R_motor_speed)

        if state == TURN_RIGHT and previousState == TURN_LEFT:
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