vars = [
    "ui8_Control_bits",

    "si16_Angle",
    "si16_Raw_angle",
    "b_Angle_reset",

    "f_Distance",
    "si16_Raw_distance",

    "e_Raw_color",
    "e_Color",

    "ui32_Time",
    "ui32_Last_packet_time",
    
    "si16_Motor_speed_left",
    "si16_Motor_speed_right",

    "b_Emergency_distance",
    "b_Emergency_timeout",
    "E_State",
    "b_Shoot",
]



comps = {
    "StateMachineSWC": [
        ["ui8_Control_bits", "b_Emergency_distance", "b_Emergency_timeout", "b_Shoot"],
        ["E_State", "b_Angle_reset"]
    ],
    "MotorSWC": [
        ["E_State", "si16_Angle", "ui32_Time"],
        ["si16_Motor_speed_left", "si16_Motor_speed_right"]
    ],
    "GyroSWC": [
        ["si16_Raw_angle", "b_Angle_reset"],
        ["si16_Angle", "b_Angle_reset"]
    ],
    "UltrasonicSWC": [
        ["si16_Raw_distance"],
        ["f_Distance"]
    ],
    "ColorsensorSWC": [
        ["e_Raw_color"],
        ["e_Color"]
    ],
    "EmergencySWC": [
        ["ui32_Time", "ui32_Last_packet_time", "f_Distance"],
        ["b_Emergency_distance", "b_Emergency_timeout"]
    ],
    "BazookaSWC": [
        ["E_State"],
        ["b_Shoot"]
    ],
    "ComunicationHandler": [
        ["ui32_Time", "f_Distance"],
        ["ui8_Control_bits", "ui32_Last_packet_time"]
    ],
    "IOHandler": [
        ["si16_Motor_speed_left", "si16_Motor_speed_right", "b_Shoot"],
        ["si16_Raw_distance", "si16_Raw_angle", "e_Raw_color", "b_Shoot"]
    ],
    "Stopwatch": [
        [],
        ["ui32_Time"]
    ]
}

ind = " " * 4
basepath = "./Internship_2024/"

with open(basepath + "RTE.py", "w", encoding="utf-8") as f:
    for var in vars:
        f.write(f"global {var}\n")

    f.write("\n\n")
    for comp in comps:
        f.write(f"\n\n# {comp}\n")
        functions = []
        for rv in comps[comp][0]:
            assert rv in vars
            functionName = f"Rte_Read_{comp}_{rv}"
            functions.append(functionName)
            f.write(f"def {functionName}():\n{ind}global {rv}\n{ind}return {rv}\n\n")
        for wv in comps[comp][1]:
            assert wv in vars
            functionName = f"Rte_Write_{comp}_{wv}"
            functions.append(functionName)
            f.write(f"def {functionName}(arg):\n{ind}global {wv}\n{ind}{wv} = arg\n\n")
        with open(basepath + comp + ".py", "w", encoding="utf-8") as cfile:
            cfile.write(f"from RTE import {', '.join(functions)}\n")