global ui8_Control_bits
global si16_Angle
global si16_Raw_angle
global b_Angle_reset
global f_Distance
global si16_Raw_distance
global e_Raw_color
global e_Color
global ui32_Time
global ui32_Last_packet_time
global si16_Motor_speed_left
global si16_Motor_speed_right
global b_Emergency_distance
global b_Emergency_timeout
global E_State
global b_Shoot




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

def Rte_Write_StateMachineSWC_E_State(arg):
    global E_State
    E_State = arg

def Rte_Write_StateMachineSWC_b_Angle_reset(arg):
    global b_Angle_reset
    b_Angle_reset = arg



# MotorSWC
def Rte_Read_MotorSWC_E_State():
    global E_State
    return E_State

def Rte_Read_MotorSWC_si16_Angle():
    global si16_Angle
    return si16_Angle

def Rte_Read_MotorSWC_ui32_Time():
    global ui32_Time
    return ui32_Time

def Rte_Write_MotorSWC_si16_Motor_speed_left(arg):
    global si16_Motor_speed_left
    si16_Motor_speed_left = arg

def Rte_Write_MotorSWC_si16_Motor_speed_right(arg):
    global si16_Motor_speed_right
    si16_Motor_speed_right = arg



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

def Rte_Write_UltrasonicSWC_f_Distance(arg):
    global f_Distance
    f_Distance = arg



# ColorsensorSWC
def Rte_Read_ColorsensorSWC_e_Raw_color():
    global e_Raw_color
    return e_Raw_color

def Rte_Write_ColorsensorSWC_e_Color(arg):
    global e_Color
    e_Color = arg



# EmergencySWC
def Rte_Read_EmergencySWC_ui32_Time():
    global ui32_Time
    return ui32_Time

def Rte_Read_EmergencySWC_ui32_Last_packet_time():
    global ui32_Last_packet_time
    return ui32_Last_packet_time

def Rte_Read_EmergencySWC_f_Distance():
    global f_Distance
    return f_Distance

def Rte_Write_EmergencySWC_b_Emergency_distance(arg):
    global b_Emergency_distance
    b_Emergency_distance = arg

def Rte_Write_EmergencySWC_b_Emergency_timeout(arg):
    global b_Emergency_timeout
    b_Emergency_timeout = arg



# BazookaSWC
def Rte_Read_BazookaSWC_E_State():
    global E_State
    return E_State

def Rte_Write_BazookaSWC_b_Shoot(arg):
    global b_Shoot
    b_Shoot = arg



# ComunicationHandler
def Rte_Read_ComunicationHandler_ui32_Time():
    global ui32_Time
    return ui32_Time

def Rte_Read_ComunicationHandler_f_Distance():
    global f_Distance
    return f_Distance

def Rte_Write_ComunicationHandler_ui8_Control_bits(arg):
    global ui8_Control_bits
    ui8_Control_bits = arg

def Rte_Write_ComunicationHandler_ui32_Last_packet_time(arg):
    global ui32_Last_packet_time
    ui32_Last_packet_time = arg



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



# Stopwatch
def Rte_Write_Stopwatch_ui32_Time(arg):
    global ui32_Time
    ui32_Time = arg

