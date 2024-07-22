from RTE import Rte_Read_StateMachineSWC_ui8_Control_bits, Rte_Read_StateMachineSWC_b_Emergency_distance, Rte_Read_StateMachineSWC_b_Emergency_timeout, Rte_Read_StateMachineSWC_b_Shoot, Rte_Write_StateMachineSWC_E_State, Rte_Write_StateMachineSWC_b_Angle_reset



import uasyncio as asyncio

from typedefs import States


lastState = States.NONE
state = States.IDLE
nextState = States.IDLE

def check_first_entry():
    return state != lastState


def checkTranitionNeeded_Idle():
    global nextState
    timeoutEmergency = Rte_Read_StateMachineSWC_b_Emergency_timeout()
    if timeoutEmergency:
        return False
    
    controlBits = Rte_Read_StateMachineSWC_ui8_Control_bits()
    if controlBits & 1 << 1:
        nextState = States.GO_BACKWARD
        return True

    distanceEmergency = Rte_Read_StateMachineSWC_b_Emergency_distance()
    if distanceEmergency:
        return False


    if controlBits & 1 << 0:
        nextState = States.GO_FORWARD
        return True
    if controlBits & 1 << 2:
        nextState = States.TURN_LEFT
    if controlBits & 1 << 3:
        nextState = States.TURN_RIGHT
    if controlBits & 1 << 4:
        nextState = States.SHOOT

 
previousShootBit = True
shootBit = True
def checkTranitionNeeded_Shoot():
    global previousShootBit
    global shootBit
    global nextState
    previousShootBit = shootBit
    shootBit = Rte_Read_StateMachineSWC_b_Shoot()
    if previousShootBit and not shootBit:
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
            pass # Do nothing
        elif state == States.GO_BACKWARD:
            pass # Do nothing
        elif state == States.TURN_LEFT:
            if(check_first_entry() == True):
                Rte_Write_StateMachineSWC_b_Angle_reset(False)
        elif state == States.TURN_RIGHT:
            if(check_first_entry() == True):
                Rte_Write_StateMachineSWC_b_Angle_reset(False)
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
