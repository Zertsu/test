# This SWC is making the Guarding mode work, changes states and gives control to the other SWC's
# The SWC has respounds for the Searching, Attacking, Shooting and Obstycle avoidance



# Autogenerated code, DO NOT EDIT
from RTE import Rte_Read_GuardingStateMachineSWC_b_guarding_mode, Rte_Read_GuardingStateMachineSWC_S_face, Rte_Read_GuardingStateMachineSWC_S_Max_distance_and_angle, Rte_Read_GuardingStateMachineSWC_f_avg_Distance, Rte_Read_GuardingStateMachineSWC_si16_turn_angle, Rte_Read_GuardingStateMachineSWC_f_Distance, Rte_Read_GuardingStateMachineSWC_b_Angle_reset, Rte_Write_GuardingStateMachineSWC_b_guarding_mode, Rte_Write_GuardingStateMachineSWC_E_State, Rte_Write_GuardingStateMachineSWC_b_Angle_reset, Rte_Write_GuardingStateMachineSWC_b_Distance_reset, Rte_Write_GuardingStateMachineSWC_si16_turn_angle, Rte_Write_GuardingStateMachineSWC_ui16_motor_speed, Rte_Write_GuardingStateMachineSWC_b_guarding_emergency
# End of autogenerated code

import uasyncio as asyncio
from typedefs import States
from typedefs import GuardStates

# global variables we use for different functions 
# initialization for the variables
# !!!!! DO NOT DELETE ANY OF THEM BEFORE MAKING SURE IT IS NOT USED ANYMORE !!!!! ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

global async_timer
async_timer = 50 # this variable stores the time in ms that we use in asyncio.sleep

global run_time
run_time = 0 # we use it to count the Running time in obstycle avoidance mode 

global distance
distance = 0 # we store the distance we get from the ultrasonic sensor

global state
state = States.IDLE # we set the states to control the SWC's

global guard_state
guard_state = GuardStates.SEARCH # we store thecurrent state in here

global face_position
face_position = (0,0,0) # this stores the face's data

global last_turn
last_turn = TURN.RIGHT # stores tha last turn's diraction

global entry_number
entry_number = 0 # counts in what entry level we are

global right_avg
right_avg = 0 # right distance average

global right_obstycle
right_obstycle = (0,0) # stores the right max distance and angle

global left_avg
left_avg = 0 # left distance average

global left_obstycle
left_obstycle (0,0) # stores the left max distance and angle

global emergency_distance
emergency_distance = 40 # minimum distance from obsticle

global max_run_time 
max_run_time = 20000 # the time in ms we need to run

global min_distance_tomove
min_distance_tomove = 100 # minimum distance to avoid an obsticle

global left_face_margin
left_face_margin = 125 # face in left side

global right_face_margin
right_face_margin = 130 # face in right side

global min_eye_margin
min_eye_margin = 10 # minimum distance between the eyes

global max_eye_margin
max_eye_margin = 30 # maximum distance between the eyes


# end of global variables
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def obstycle():

    # global variabals
    global guard_state
    global distance
    global state
    global entry_number 
    global right_obstycle
    global right_avg
    global left_obstycle
    global left_avg
    global run_time
    global last_turn
    global emergency_distance
    global max_run_time
    global min_distance_tomove

    # local variables
    # entry_number different states
    no_obstycle = 0
    first_turn = 1
    first_turn_back = 2
    secound_turn = 3
    secound_turn_back = 4
    turning_correctly = 5
    moovement_done = 6

    # getting data from RTE to a local variable
    distance = Rte_Read_GuardingStateMachineSWC_f_Distance

    # checking in what state we are and doing things accordingly
    if distance < emergency_distance and entry_number == no_obstycle:
        guard_state = GuardStates.OBSTYCLE
        entry_number = first_turn
        state = State.IDLE
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        Rte_Write_GuardingStateMachineSWC_b_Distance_reset(True)
        Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
        Rte_Write_GuardingStateMachineSWC_si16_turn_angle(90)

    elif entry_number == first_turn and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        if angle == 0:
            right_obstycle = Rte_Read_GuardingStateMachineSWC_S_Max_distance_and_angle()
            right_avg = Rte_Read_GuardingStateMachineSWC_f_avg_Distance()
            entry_number = first_turn_back
            Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
            Rte_Write_GuardingStateMachineSWC_si16_turn_angle(-90)

    elif entry_number == first_turn_back and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        if angle == 0:
            entry_number = secound_turn
            Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
            Rte_Write_GuardingStateMachineSWC_b_Distance_reset(True)
            Rte_Write_GuardingStateMachineSWC_si16_turn_angle(-90)

    elif entry_number == secound_turn and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        if angle == 0:
            left_obstycle = Rte_Read_GuardingStateMachineSWC_S_Max_distance_and_angle()
            left_avg = Rte_Read_GuardingStateMachineSWC_f_avg_Distance
            entry_number = secound_turn_back
            Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
            Rte_Write_GuardingStateMachineSWC_si16_turn_angle(90)

    elif entry_number == secound_turn_back and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        if angle == 0:
            entry_number = turning_correctly
            if right_avg >= left_avg and right_obstycle[0] >= min_distance_tomove:
                Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
                Rte_Write_GuardingStateMachineSWC_si16_turn_angle(right_obstycle[1])
                last_turn = TURN.RIGHT
            elif right_avg <= left_avg and left_obstycle[0] >= min_distance_tomove:
                Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
                Rte_Write_GuardingStateMachineSWC_si16_turn_angle(left_obstycle[1]-360)
                last_turn = TURN.LEFT
            else:
                Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
                Rte_Write_GuardingStateMachineSWC_si16_turn_angle(180)

    elif entry_number == turning_correctly and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        if angle == 0:
            if distance < emergency_distance and entry_number == turning_correctly:
                entry_number = 0
                run_time = 0
            else:
                state = States.GO_FORWARD
                Rte_Write_GuardingStateMachineSWC_E_State(state)
                run_time = run_time + async_timer
                if run_time == max_run_time:
                    entry_number == moovement_done

    elif entry_number == moovement_done and guard_state == GuardStates.OBSTYCLE:
        guard_state = GuardStates.SEARCH
        run_time = 0
        entry_number = 0
    else: 
        guard_state = GuardStates.SEARCH
        run_time = 0
        entry_number = 0
        continue    


def shooting():

    # global variabals
    global face_position
    global state

    # local variables 
    enemy = 1
    friend = 2

    # checking what we need to do with the face we see
    if face_position[0] == enemy:
        # say something
        state = States.SHOOT
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        Rte_Write_GuardingStateMachineSWC_b_guarding_mode(False)
        continue

    elif face_position[0] == friend:
        # say something
        Rte_Write_GuardingStateMachineSWC_b_guarding_mode(False)
        continue



def attacking():

    # global variabals
    global face_position
    global left_face_margin
    global right_face_margin
    global min_eye_margin
    global max_eye_margin

    # getting data from RTE to a global variable
    face_position = Rte_Read_GuardingStateMachineSWC_S_face_position

    # checking if the face we see is in middle or not and turning accordingly
    if face_position[1] > left_face_margin and face_position[1] < right_face_margin:

        # checking if we are close enough to shoot
        if face_position[2] > min_eye_margin and face_position[2]< max_eye_margin:
            state = GO_FORWARD
            Rte_Write_GuardingStateMachineSWC_E_State(state)
            continue

        # changeing state if we are ready
        else:
            guard_state = SHOOTING
            continue

    elif face_position[1] < left_face_margin
        state = TURN_LEFT
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        continue

    elif face_position[1] > right_face_margin
        state = TURN_RIGHT
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        continue

def searching():

    # global variabals
    global guard_state
    global face_position
    global last_turn

    # local variables
    no_face = 0

    # getting data from RTE to a global variable
    face_position = Rte_Read_GuardingStateMachineSWC_S_face_position

    # checking if we see a face
    if face_position[0] == no_face:
        # turning opposite to the last turn
        if last_turn == TURN.RIGHT:
            state = TURN_LEFT
            Rte_Write_GuardingStateMachineSWC_E_State(state)
            continue
        elif last_turn == TURN.LEFT:
            state = TURN_RIGHT
            Rte_Write_GuardingStateMachineSWC_E_State(state)
            continue
    # changeing state if we see a face
    else:
        guard_state = GuardStates.ATTACKING
        continue



async def guard_state_machine():

    # global variabals
    global async_timer
    global guard_state

    while True: 

        # getting data from RTE to a local variable
        guard_mode = Rte_Read_GuardingStateMachineSWC_b_guarding_mode

        # checking in what state we are and calling the functions accordingly
        if guard_mode:
            if guard_state == GuardStates.OBSTYCLE:
                obstycle()
            elif guard_state == GuardStates.SEARCH:
                searching()
            elif guard_state == GuardStates.ATTACKING:
                attacking()
            elif guard_state == GuardStates.SHOOTING:
                shooting()
            obstycle()

        await asyncio.sleep_ms(async_timer)  # Adjust sleep time later if needed
