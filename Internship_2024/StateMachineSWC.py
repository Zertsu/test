# Autogenerated code, DO NOT EDIT
from RTE import Rte_Read_StateMachineSWC_ui8_Control_bits, Rte_Read_StateMachineSWC_b_Emergency_distance, Rte_Read_StateMachineSWC_b_Emergency_timeout, Rte_Read_StateMachineSWC_b_Shoot, Rte_Write_StateMachineSWC_E_State, Rte_Write_StateMachineSWC_b_Angle_reset
# End of autogenerated code

import uasyncio as asyncio
from typedefs import States

# Initialize states
lastState = States.NONE
state = States.IDLE
nextState = States.IDLE


def check_first_entry():
    return state != lastState


def checkTranitionNeeded_Idle():
    global nextState
    # In case of comunication timeout, don't change out of IDLE
    timeoutEmergency = Rte_Read_StateMachineSWC_b_Emergency_timeout()
    if timeoutEmergency:
        return False
    
    # If we're not in timout we can go backwards
    controlBits = Rte_Read_StateMachineSWC_ui8_Control_bits()
    if controlBits & 1 << 1:
        nextState = States.GO_BACKWARD
        return True

    # To do anything else we have to not be in a distance emergency
    distanceEmergency = Rte_Read_StateMachineSWC_b_Emergency_distance()
    if distanceEmergency:
        return False

    # Change state acording to the control bits
    if controlBits & 1 << 0:
        nextState = States.GO_FORWARD
        return True
    if controlBits & 1 << 2:
        nextState = States.TURN_LEFT
        return True
    if controlBits & 1 << 3:
        nextState = States.TURN_RIGHT
        return True
    if controlBits & 1 << 4:
        nextState = States.SHOOT
        return True
    return False

 
previousShootBit = True
shootBit = True
def checkTranitionNeeded_Shoot():
    global previousShootBit
    global shootBit
    global nextState
    previousShootBit = shootBit

    # Go back to IDLE state when the shoot bit transitions to False
    shootBit = Rte_Read_StateMachineSWC_b_Shoot()
    if previousShootBit and not shootBit:
        nextState = States.IDLE
        return True
    return False


def checkTranitionNeeded_Mooving(mask):
    global nextState
    controlBits = Rte_Read_StateMachineSWC_ui8_Control_bits()
    emergency_distance = Rte_Read_StateMachineSWC_b_Emergency_distance()
    emergency_timeout = Rte_Read_StateMachineSWC_b_Emergency_timeout()
    
    # In case of an emergency go back to IDLE state
    if emergency_timeout:
        nextState = States.IDLE
        return True
    if emergency_distance and not (controlBits & 1 << 1):
        nextState = States.IDLE
        return True

    # When the desired bit becomes false in the controlBits go back to IDLE
    if not (controlBits & mask):
        nextState = States.IDLE
        return True
    return False

async def state_machine():
    global state
    global lastState
    global nextState
    nextState = state
    while True:
        if state == States.IDLE:
            if(check_first_entry() == True):
                pass # Do nothing
            else:
                if(checkTranitionNeeded_Idle() == True):
                    pass # Do nothing
                else :
                    pass # Do nothing
        
        elif state == States.GO_FORWARD:
            checkTranitionNeeded_Mooving(1 << 0)
        elif state == States.GO_BACKWARD:
            checkTranitionNeeded_Mooving(1 << 1)
        elif state == States.TURN_LEFT:
            if(check_first_entry() == True):
                Rte_Write_StateMachineSWC_b_Angle_reset(False)
            checkTranitionNeeded_Mooving(1 << 2)
        elif state == States.TURN_RIGHT:
            if(check_first_entry() == True):
                Rte_Write_StateMachineSWC_b_Angle_reset(False)
            checkTranitionNeeded_Mooving(1 << 3)
        elif state == States.SHOOT:
            if(check_first_entry() == True):
                pass # Do nothing
            else:
                if(checkTranitionNeeded_Shoot() == True):
                    pass # Do nothing
                else :
                    pass # Do nothing

        lastState = state
        state = nextState

        Rte_Write_StateMachineSWC_E_State(state)
        await asyncio.sleep_ms(50)  # Adjust sleep time as needed
