# This SWC is making the Guarding mode work, changes states and gives control to the other SWC's
# The SWC has respounds for the Searching, Attacking, Shooting and Obstycle avoidance



# Autogenerated code, DO NOT EDIT
from RTE import Rte_Read_GuardingStateMachineSWC_b_guarding_mode, Rte_Read_GuardingStateMachineSWC_S_face, Rte_Read_GuardingStateMachineSWC_b_Angle_reset, Rte_Read_GuardingStateMachineSWC_S_Max_distance_and_angle, Rte_Read_GuardingStateMachineSWC_f_avg_Distance, Rte_Read_GuardingStateMachineSWC_si16_turn_angle, Rte_Read_GuardingStateMachineSWC_f_Distance, Rte_Read_GuardingStateMachineSWC_si16_Angle, Rte_Write_GuardingStateMachineSWC_b_guarding_mode, Rte_Write_GuardingStateMachineSWC_E_State, Rte_Write_GuardingStateMachineSWC_b_Angle_reset, Rte_Write_GuardingStateMachineSWC_b_Distance_reset, Rte_Write_GuardingStateMachineSWC_si16_turn_angle, Rte_Write_GuardingStateMachineSWC_ui16_motor_speed, Rte_Write_GuardingStateMachineSWC_b_guarding_emergency, Rte_Write_GuardingStateMachineSWC_E_play_sound
# End of autogenerated code

import Logger
import uasyncio as asyncio
from typedefs import States
from typedefs import GuardStates
from typedefs import TURN
from typedefs import SoundFiles

# global variables we use for different functions 
# initialization for the variables
# !!!!! DO NOT DELETE ANY OF THEM BEFORE MAKING SURE IT IS NOT USED ANYMORE !!!!! ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#region globals

global log 
log = Logger.Logger("Guarding State Machine")

class SearchFlag():
    reset = 0
    half_turn = 1
    full_turn = 2

global async_timer
async_timer = 50 # this variable stores the time in ms that we use in asyncio.sleep

global search_flag 
search_flag = 0 # chacking if we are in search mode for too long

global enter_guard_mode
enter_guard_mode = False # stores if we are entering guarding mode

global run_time
run_time = 0 # we use it to count the Running time in obstycle avoidance mode 

global distance
distance = 100 # we store the distance we get from the ultrasonic sensor

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
left_obstycle = (0,0) # stores the left max distance and angle

global emergency_distance
emergency_distance = 40 # minimum distance from obsticle

global idle_time 
idle_time = 0 # time we spend in idle mode

global max_idle_time 
max_idle_time = 5000 # maximum time we spend in idle mode

global in_box_flag
in_box_flag = 0 # checking if we are in a box

global max_run_time 
max_run_time = 20000 # the time in ms we need to run

global min_distance_tomove
min_distance_tomove = 100 # minimum distance to avoid an obsticle

global left_face_margin
left_face_margin = 120 # face in left side

global right_face_margin
right_face_margin = 135 # face in right side

global first_sleep
first_sleep = 500 # first sleep waitng for softwares to get ready

global angle_delay
angle_delay = 5 # angle we have to delay for the robots width in obstycle avoidation

global stay
stay = True # if we have to wait or not

global motor_speed_slow
motor_speed_slow = 50 # slow motor speed for searching and face centering

global motor_speed_fast
motor_speed_fast = 100 # fast motot speed for obstycle avoidance

global max_eye_margin
max_eye_margin = 40 # maximum distance between the eyes

#endregion

# end of global variables
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# this Function is controlling the obsticle avoidance
def obstycle():

    # global variabals
    global guard_state
    global search_flag 
    global motor_speed_fast
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
    global stay
    global in_box_flag

    # local variables
    # entry_number different states
    no_obstycle = 0
    first_turn = 1
    first_turn_back = 2
    secound_turn = 3
    secound_turn_back = 4
    turning_correctly = 5
    moovement_done = 6

    # in_box_flag states
    not_in_box = 0
    maybe_in_box = 1

    # getting data from RTE to a local variable
    distance = Rte_Read_GuardingStateMachineSWC_f_Distance()

    # checking in what state we are and doing things accordingly
    if distance < emergency_distance and entry_number == no_obstycle:

        guard_state = GuardStates.OBSTYCLE
        log.LOGI(guard_state)
        entry_number = first_turn
        state = States.IDLE
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        Rte_Write_GuardingStateMachineSWC_b_Distance_reset(True)
        Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
        Rte_Write_GuardingStateMachineSWC_E_play_sound(SoundFiles.OBJECT)
        state = States.TURN_ANGLE
        Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_fast)
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        Rte_Write_GuardingStateMachineSWC_si16_turn_angle(90)

    elif entry_number == first_turn and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        angleReset = Rte_Read_GuardingStateMachineSWC_b_Angle_reset()
        if angle == 0 and not angleReset:
            right_obstycle = Rte_Read_GuardingStateMachineSWC_S_Max_distance_and_angle()
            right_avg = Rte_Read_GuardingStateMachineSWC_f_avg_Distance()
            entry_number = first_turn_back
            Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
            state = States.TURN_ANGLE
            Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_fast)
            Rte_Write_GuardingStateMachineSWC_E_State(state)
            Rte_Write_GuardingStateMachineSWC_si16_turn_angle(-90)


    elif entry_number == first_turn_back and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        angleReset = Rte_Read_GuardingStateMachineSWC_b_Angle_reset()
        if angle == 0 and not angleReset:
            entry_number = secound_turn
            Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
            Rte_Write_GuardingStateMachineSWC_b_Distance_reset(True)
            state = States.TURN_ANGLE
            Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_fast)
            Rte_Write_GuardingStateMachineSWC_E_State(state)

    elif entry_number == secound_turn and guard_state == GuardStates.OBSTYCLE and stay:
        angleReset = Rte_Read_GuardingStateMachineSWC_b_Angle_reset()
        if not angleReset:
            Rte_Write_GuardingStateMachineSWC_si16_turn_angle(-90)
            stay = False

    elif entry_number == secound_turn and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        if angle == 0:
            left_obstycle = Rte_Read_GuardingStateMachineSWC_S_Max_distance_and_angle()
            left_avg = Rte_Read_GuardingStateMachineSWC_f_avg_Distance()
            entry_number = secound_turn_back
            Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
            state = States.TURN_ANGLE
            Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_fast)
            Rte_Write_GuardingStateMachineSWC_E_State(state)
            Rte_Write_GuardingStateMachineSWC_si16_turn_angle(90)

    elif entry_number == secound_turn_back and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        if angle == 0:
            entry_number = turning_correctly
            if right_avg >= left_avg and right_obstycle[0] >= min_distance_tomove:
                Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
                state = States.TURN_ANGLE
                Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_fast)
                Rte_Write_GuardingStateMachineSWC_E_State(state)
                Rte_Write_GuardingStateMachineSWC_si16_turn_angle(right_obstycle[1]+angle_delay)
                last_turn = TURN.RIGHT

            elif right_avg <= left_avg and left_obstycle[0] >= min_distance_tomove:
                Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
                state = States.TURN_ANGLE
                Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_fast)
                Rte_Write_GuardingStateMachineSWC_E_State(state)
                Rte_Write_GuardingStateMachineSWC_si16_turn_angle(left_obstycle[1]-360-angle_delay)
                last_turn = TURN.LEFT

            else:
                Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
                state = States.TURN_ANGLE
                Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_fast)
                Rte_Write_GuardingStateMachineSWC_E_State(state)
                Rte_Write_GuardingStateMachineSWC_si16_turn_angle(180)
                if in_box_flag == not_in_box:
                    in_box_flag = maybe_in_box
                elif in_box_flag == maybe_in_box:
                    state = States.IDLE
                    Rte_Write_GuardingStateMachineSWC_E_State(state)
                    Rte_Write_GuardingStateMachineSWC_b_guarding_emergency(True)
                    guard_state = GuardStates.SEARCH
                    log.LOGI(guard_state)
                    search_flag = SearchFlag.reset
                    in_box_flag = not_in_box
                    Rte_Write_GuardingStateMachineSWC_E_play_sound(SoundFiles.CRYING)


    elif entry_number == turning_correctly and guard_state == GuardStates.OBSTYCLE:

        # getting data from RTE to a local variable
        angle = Rte_Read_GuardingStateMachineSWC_si16_turn_angle()
        if angle == 0:
            if distance < emergency_distance and entry_number == turning_correctly:
                entry_number = no_obstycle
                Rte_Write_GuardingStateMachineSWC_E_play_sound(SoundFiles.OBJECT)
                run_time = 0
                stay = True
            else:
                state = States.GO_FORWARD
                Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_fast)
                Rte_Write_GuardingStateMachineSWC_E_State(state)
                in_box_flag = not_in_box
                run_time = run_time + async_timer

                if run_time == max_run_time:
                    run_time = 0
                    entry_number = moovement_done

    elif entry_number == moovement_done and guard_state == GuardStates.OBSTYCLE:
        guard_state = GuardStates.SEARCH
        log.LOGI(guard_state)
        search_flag = SearchFlag.reset
        run_time = 0
        entry_number = no_obstycle
        stay = True
    else: 
        guard_state = GuardStates.SEARCH
        run_time = 0
        entry_number = no_obstycle
        stay = True

# this function is making the shooting
def shooting():

    # global variabals
    global face_position
    global state
    global guard_state

    # local variables 
    enemy = 1
    friend = 2

    # checking what we need to do with the face we see
    if face_position[0] == enemy:
        # say something
        state = States.SHOOT
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        Rte_Write_GuardingStateMachineSWC_E_play_sound(SoundFiles.GAMEOVER)
        Rte_Write_GuardingStateMachineSWC_b_guarding_mode(False)
        state = States.IDLE
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        guard_state = GuardStates.SEARCH
        log.LOGI(guard_state)
        search_flag = SearchFlag.reset
        
    elif face_position[0] == friend:
        Rte_Write_GuardingStateMachineSWC_E_play_sound(SoundFiles.HI)
        Rte_Write_GuardingStateMachineSWC_b_guarding_mode(False)
        state = States.IDLE
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        guard_state = GuardStates.SEARCH
        log.LOGI(guard_state)
        search_flag = SearchFlag.reset

# this function centers the face and closes the gap to 50 cm 
def attacking():

    # global variabals
    global async_timer
    global search_flag 
    global face_position
    global left_face_margin
    global motor_speed_slow
    global right_face_margin
    global max_eye_margin
    global guard_state
    global idle_time
    global max_idle_time

    # local variables 
    enemy = 1

    # getting data from RTE to a global variable
    face_position = Rte_Read_GuardingStateMachineSWC_S_face()

    # checking if the face we see is in middle or not and turning accordingly
    if face_position[1] > left_face_margin and face_position[1] < right_face_margin:

        # checking if we are close enough to shoot
        if face_position[2] < max_eye_margin and face_position[0] == enemy:
            state = States.GO_FORWARD
            Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_slow)
            Rte_Write_GuardingStateMachineSWC_E_State(state)
            
        # changeing state if we are ready
        else:
            guard_state = GuardStates.SHOOTING
            log.LOGI(guard_state)

        idle_time = 0
    
    elif face_position[0] == 0:
        state = States.IDLE
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        idle_time = idle_time + async_timer
        if idle_time == max_idle_time:
            guard_state = GuardStates.SEARCH
            log.LOGI(guard_state)
            search_flag = SearchFlag.reset

    elif face_position[1] < left_face_margin:
        state = States.TURN_RIGHT
        Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_slow)
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        idle_time = 0
        
    elif face_position[1] > right_face_margin:
        state = States.TURN_LEFT
        Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_slow)
        Rte_Write_GuardingStateMachineSWC_E_State(state)
        idle_time = 0

# this function is searching for face     
def searching():

    # global variabals
    global guard_state
    global search_flag 
    global face_position
    global last_turn
    global motor_speed_slow

    # local variables
    no_face = 0
    
    # getting data from RTE to a global variable
    face_position = Rte_Read_GuardingStateMachineSWC_S_face()

    # checking if we see a face
    if face_position[0] == no_face:
        # turning opposite to the last turn
        if last_turn == TURN.RIGHT:
            state = States.TURN_LEFT
            Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_slow)
            Rte_Write_GuardingStateMachineSWC_E_State(state)
        elif last_turn == TURN.LEFT:
            state = States.TURN_RIGHT
            Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(motor_speed_slow)
            Rte_Write_GuardingStateMachineSWC_E_State(state)
    # changeing state if we see a face
    else:
        guard_state = GuardStates.ATTACKING
        log.LOGI(guard_state)
    
    angle_delay = 2

    if search_flag == SearchFlag.reset:
        Rte_Write_GuardingStateMachineSWC_b_Angle_reset(True)
        Rte_Write_GuardingStateMachineSWC_E_play_sound(SoundFiles.SEARCHING)
        search_flag = SearchFlag.half_turn
    elif search_flag == SearchFlag.half_turn:
        angle = Rte_Read_GuardingStateMachineSWC_si16_Angle()
        if angle < 180 + angle_delay and angle > 180 - angle_delay:
            search_flag = SearchFlag.full_turn
    elif search_flag == SearchFlag.full_turn:
        angle = Rte_Read_GuardingStateMachineSWC_si16_Angle()
        if angle < 0 + angle_delay or angle > 360 - angle_delay:
            Rte_Write_GuardingStateMachineSWC_E_play_sound(SoundFiles.CRYING)
            state = States.IDLE
            Rte_Write_GuardingStateMachineSWC_E_State(state)
            Rte_Write_GuardingStateMachineSWC_b_guarding_mode(False)
            guard_state = GuardStates.SEARCH
            log.LOGI(guard_state)
            search_flag = SearchFlag.reset
            
# this function checks if we are in guarding mode and also calls the other function in every state      
async def guard_state_machine():

    # global variabals
    global async_timer
    global enter_guard_mode
    global guard_state
    global search_flag 
    await asyncio.sleep_ms(first_sleep)  # Adjust sleep time later if needed

    log.LOGI("Starting Gaurding State Machine")
    while True: 

        # getting data from RTE to a local variable
        guard_mode = Rte_Read_GuardingStateMachineSWC_b_guarding_mode()
        if guard_mode != enter_guard_mode and guard_mode:
            enter_guard_mode = not enter_guard_mode
            guard_state = GuardStates.SEARCH
            log.LOGI(guard_state)
            search_flag = SearchFlag.reset
        elif guard_mode != enter_guard_mode and not guard_mode:
            enter_guard_mode = not enter_guard_mode
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
    log.LOGF("Exited loop")
