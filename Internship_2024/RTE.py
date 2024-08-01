global ui8_Control_bits
global b_Control_bits_valid
global S_face
global S_face_position
global si16_Angle
global si16_Raw_angle
global b_Angle_reset
global f_Distance
global S_Max_distance_and_angle
global f_avg_Distance
global si16_Raw_distance
global b_Distance_reset
global e_Raw_color
global e_Color
global si16_Motor_speed_left
global si16_Motor_speed_right
global si16_turn_angle
global ui16_motor_speed
global b_Emergency_distance
global b_Emergency_timeout
global E_State
global b_Shoot
global b_guarding_mode
global b_guarding_emergency
global E_play_sound

ui8_Control_bits = 0
b_Control_bits_valid = False
S_face = (0, 0, 0)
S_face_position = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
si16_Angle = 0
si16_Raw_angle = 0
b_Angle_reset = False
f_Distance = 0
S_Max_distance_and_angle = (0, 0)
f_avg_Distance = 0
si16_Raw_distance = 0
b_Distance_reset = 0
e_Raw_color = None
e_Color = None
si16_Motor_speed_left = 0
si16_Motor_speed_right = 0
si16_turn_angle = 0
ui16_motor_speed = 100
b_Emergency_distance = False
b_Emergency_timeout = False
E_State = None
b_Shoot = False
b_guarding_mode = False
b_guarding_emergency = False
E_play_sound = 0




# FaceProcessorSWC
def Rte_Read_FaceProcessorSWC_S_face_position():
    global S_face_position
    return S_face_position

def Rte_Write_FaceProcessorSWC_S_face(arg):
    global S_face
    S_face = arg



# StateMachineSWC
def Rte_Read_StateMachineSWC_ui8_Control_bits():
    global ui8_Control_bits
    return ui8_Control_bits

def Rte_Read_StateMachineSWC_b_Emergency_distance():
    global b_Emergency_distance
    return b_Emergency_distance

def Rte_Read_StateMachineSWC_b_Emergency_timeout():
    global b_Emergency_timeout
    return b_Emergency_timeout

def Rte_Read_StateMachineSWC_b_Shoot():
    global b_Shoot
    return b_Shoot

def Rte_Read_StateMachineSWC_b_guarding_mode():
    global b_guarding_mode
    return b_guarding_mode

def Rte_Write_StateMachineSWC_E_State(arg):
    global E_State
    E_State = arg

def Rte_Write_StateMachineSWC_b_Angle_reset(arg):
    global b_Angle_reset
    b_Angle_reset = arg

def Rte_Write_StateMachineSWC_b_guarding_mode(arg):
    global b_guarding_mode
    b_guarding_mode = arg

def Rte_Write_StateMachineSWC_ui16_motor_speed(arg):
    global ui16_motor_speed
    ui16_motor_speed = arg



# GuardingStateMachineSWC
def Rte_Read_GuardingStateMachineSWC_b_guarding_mode():
    global b_guarding_mode
    return b_guarding_mode

def Rte_Read_GuardingStateMachineSWC_S_face():
    global S_face
    return S_face

def Rte_Read_GuardingStateMachineSWC_b_Angle_reset():
    global b_Angle_reset
    return b_Angle_reset

def Rte_Read_GuardingStateMachineSWC_S_Max_distance_and_angle():
    global S_Max_distance_and_angle
    return S_Max_distance_and_angle

def Rte_Read_GuardingStateMachineSWC_f_avg_Distance():
    global f_avg_Distance
    return f_avg_Distance

def Rte_Read_GuardingStateMachineSWC_si16_turn_angle():
    global si16_turn_angle
    return si16_turn_angle

def Rte_Read_GuardingStateMachineSWC_f_Distance():
    global f_Distance
    return f_Distance

def Rte_Write_GuardingStateMachineSWC_b_guarding_mode(arg):
    global b_guarding_mode
    b_guarding_mode = arg

def Rte_Write_GuardingStateMachineSWC_E_State(arg):
    global E_State
    E_State = arg

def Rte_Write_GuardingStateMachineSWC_b_Angle_reset(arg):
    global b_Angle_reset
    b_Angle_reset = arg

def Rte_Write_GuardingStateMachineSWC_b_Distance_reset(arg):
    global b_Distance_reset
    b_Distance_reset = arg

def Rte_Write_GuardingStateMachineSWC_si16_turn_angle(arg):
    global si16_turn_angle
    si16_turn_angle = arg

def Rte_Write_GuardingStateMachineSWC_ui16_motor_speed(arg):
    global ui16_motor_speed
    ui16_motor_speed = arg

def Rte_Write_GuardingStateMachineSWC_b_guarding_emergency(arg):
    global b_guarding_emergency
    b_guarding_emergency = arg

def Rte_Write_GuardingStateMachineSWC_si16_Angle(arg):
    global si16_Angle
    si16_Angle = arg

def Rte_Write_GuardingStateMachineSWC_E_play_sound(arg):
    global E_play_sound
    E_play_sound = arg



# MotorSWC
def Rte_Read_MotorSWC_E_State():
    global E_State
    return E_State

def Rte_Read_MotorSWC_si16_Angle():
    global si16_Angle
    return si16_Angle

def Rte_Read_MotorSWC_si16_turn_angle():
    global si16_turn_angle
    return si16_turn_angle

def Rte_Read_MotorSWC_ui16_motor_speed():
    global ui16_motor_speed
    return ui16_motor_speed

def Rte_Write_MotorSWC_si16_Motor_speed_left(arg):
    global si16_Motor_speed_left
    si16_Motor_speed_left = arg

def Rte_Write_MotorSWC_si16_Motor_speed_right(arg):
    global si16_Motor_speed_right
    si16_Motor_speed_right = arg

def Rte_Write_MotorSWC_si16_turn_angle(arg):
    global si16_turn_angle
    si16_turn_angle = arg



# GyroSWC
def Rte_Read_GyroSWC_si16_Raw_angle():
    global si16_Raw_angle
    return si16_Raw_angle

def Rte_Read_GyroSWC_b_Angle_reset():
    global b_Angle_reset
    return b_Angle_reset

def Rte_Write_GyroSWC_si16_Angle(arg):
    global si16_Angle
    si16_Angle = arg

def Rte_Write_GyroSWC_b_Angle_reset(arg):
    global b_Angle_reset
    b_Angle_reset = arg



# UltrasonicSWC
def Rte_Read_UltrasonicSWC_si16_Raw_distance():
    global si16_Raw_distance
    return si16_Raw_distance

def Rte_Read_UltrasonicSWC_b_Distance_reset():
    global b_Distance_reset
    return b_Distance_reset

def Rte_Read_UltrasonicSWC_si16_Angle():
    global si16_Angle
    return si16_Angle

def Rte_Write_UltrasonicSWC_f_Distance(arg):
    global f_Distance
    f_Distance = arg

def Rte_Write_UltrasonicSWC_b_Distance_reset(arg):
    global b_Distance_reset
    b_Distance_reset = arg

def Rte_Write_UltrasonicSWC_S_Max_distance_and_angle(arg):
    global S_Max_distance_and_angle
    S_Max_distance_and_angle = arg

def Rte_Write_UltrasonicSWC_f_avg_Distance(arg):
    global f_avg_Distance
    f_avg_Distance = arg



# ColorsensorSWC
def Rte_Read_ColorsensorSWC_e_Raw_color():
    global e_Raw_color
    return e_Raw_color

def Rte_Write_ColorsensorSWC_e_Color(arg):
    global e_Color
    e_Color = arg



# EmergencySWC
def Rte_Read_EmergencySWC_b_Control_bits_valid():
    global b_Control_bits_valid
    return b_Control_bits_valid

def Rte_Read_EmergencySWC_f_Distance():
    global f_Distance
    return f_Distance

def Rte_Read_EmergencySWC_b_guarding_emergency():
    global b_guarding_emergency
    return b_guarding_emergency

def Rte_Write_EmergencySWC_b_Emergency_distance(arg):
    global b_Emergency_distance
    b_Emergency_distance = arg

def Rte_Write_EmergencySWC_b_Emergency_timeout(arg):
    global b_Emergency_timeout
    b_Emergency_timeout = arg

def Rte_Write_EmergencySWC_b_guarding_emergency(arg):
    global b_guarding_emergency
    b_guarding_emergency = arg

def Rte_Write_EmergencySWC_b_guarding_mode(arg):
    global b_guarding_mode
    b_guarding_mode = arg



# BazookaSWC
def Rte_Read_BazookaSWC_E_State():
    global E_State
    return E_State

def Rte_Write_BazookaSWC_b_Shoot(arg):
    global b_Shoot
    b_Shoot = arg



# ComunicationHandler
def Rte_Read_ComunicationHandler_f_Distance():
    global f_Distance
    return f_Distance

def Rte_Write_ComunicationHandler_ui8_Control_bits(arg):
    global ui8_Control_bits
    ui8_Control_bits = arg

def Rte_Write_ComunicationHandler_b_Control_bits_valid(arg):
    global b_Control_bits_valid
    b_Control_bits_valid = arg

def Rte_Write_ComunicationHandler_S_face_position(arg):
    global S_face_position
    S_face_position = arg



# IOHandler
def Rte_Read_IOHandler_si16_Motor_speed_left():
    global si16_Motor_speed_left
    return si16_Motor_speed_left

def Rte_Read_IOHandler_si16_Motor_speed_right():
    global si16_Motor_speed_right
    return si16_Motor_speed_right

def Rte_Read_IOHandler_b_Shoot():
    global b_Shoot
    return b_Shoot

def Rte_Read_IOHandler_E_play_sound():
    global E_play_sound
    return E_play_sound

def Rte_Write_IOHandler_si16_Raw_distance(arg):
    global si16_Raw_distance
    si16_Raw_distance = arg

def Rte_Write_IOHandler_si16_Raw_angle(arg):
    global si16_Raw_angle
    si16_Raw_angle = arg

def Rte_Write_IOHandler_e_Raw_color(arg):
    global e_Raw_color
    e_Raw_color = arg

def Rte_Write_IOHandler_b_Shoot(arg):
    global b_Shoot
    b_Shoot = arg

def Rte_Write_IOHandler_E_play_sound(arg):
    global E_play_sound
    E_play_sound = arg

