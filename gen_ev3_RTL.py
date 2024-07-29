#!/usr/bin/python3

# This file implements automatic generation of the RTE.py file, and automatic updating 
# of the relevant software components (keeping manually written code).
# The "variables" and "components" variables describe the contents of the generated files.

# The "variables" dictionary defines the avaliable variables in the RTE.
# The key is the name of the variable and the value is the initial value of that variable.
variables = {
    "ui8_Control_bits": 0,
    "b_Control_bits_valid":  False,
    "S_face_position": (0, 0, 0),

    "si16_Angle":  0,
    "si16_Raw_angle":  0,
    "b_Angle_reset":   False,

    "f_Distance":  0,
    "S_Max_distance_and_angle": (0, 0),
    "f_avg_Distance": 0,
    "si16_Raw_distance":   0,
    "b_Distance_reset": 0,

    "e_Raw_color": None,
    "e_Color": None,

    "si16_Motor_speed_left":   0,
    "si16_Motor_speed_right":  0,
    "si16_turn_angle": 0,

    "b_Emergency_distance": False,
    "b_Emergency_timeout": False,
    "E_State": None,
    "b_Shoot": False,

    "b_guarding_mode": False,
}



# The "components" dictionary describes each software component in the following format:
# The key is the components name, its value is a list containing two lists.
# The first inner list defines the variables the software component needs to read from the RTE,
# and the second inner list defines the variables the software component needs to write to the RTE.
components = {
    "StateMachineSWC": [
        ["ui8_Control_bits", "b_Emergency_distance", "b_Emergency_timeout", "b_Shoot", "b_guarding_mode"],
        ["E_State", "b_Angle_reset", "b_guarding_mode"]
    ],
    "GuardingStateMachineSWC": [
        ["b_guarding_mode", "S_face_position", "S_Max_distance_and_angle", "f_avg_Distance", "si16_turn_angle", "f_Distance"],
        ["b_guarding_mode", "E_State", "b_Angle_reset", "b_Distance_reset", "si16_turn_angle"]
    ],
    "MotorSWC": [
        ["E_State", "si16_Angle", "si16_turn_angle"],
        ["si16_Motor_speed_left", "si16_Motor_speed_right", "si16_turn_angle"]
    ],
    "GyroSWC": [
        ["si16_Raw_angle", "b_Angle_reset"],
        ["si16_Angle", "b_Angle_reset"]
    ],
    "UltrasonicSWC": [
        ["si16_Raw_distance", "b_Distance_reset", "si16_Angle"],
        ["f_Distance", "S_Max_distance_and_angle", "f_avg_Distance"]
    ],
    "ColorsensorSWC": [
        ["e_Raw_color"],
        ["e_Color"]
    ],
    "EmergencySWC": [
        ["b_Control_bits_valid", "f_Distance"],
        ["b_Emergency_distance", "b_Emergency_timeout"]
    ],
    "BazookaSWC": [
        ["E_State"],
        ["b_Shoot"]
    ],
    "ComunicationHandler": [
        ["f_Distance"],
        ["ui8_Control_bits", "b_Control_bits_valid", "S_face_position"]
    ],
    "IOHandler": [
        ["si16_Motor_speed_left", "si16_Motor_speed_right", "b_Shoot"],
        ["si16_Raw_distance", "si16_Raw_angle", "e_Raw_color", "b_Shoot"]
    ]
}

# Import necessay modules 
import os
import re

# Configuration

# Indentation string
ind = " " * 4

# Target path where the files should be generated
basepath = "./Internship_2024/"

# Two strings that surround the autogenerated code in the software components.
# The autogenerated code gets put between these two strings in the original file,
# replacing everything in between, but leaving the resot of the file the same 
editGuards = ["# Autogenerated code, DO NOT EDIT\n", "# End of autogenerated code\n"]

with open(basepath + "RTE.py", "w", encoding="utf-8") as RTEfile:
    # Define all variables as global in the RTE
    for variable in variables:
        RTEfile.write(f"global {variable}\n")
    RTEfile.write("\n")

    # Give default values to the variables in the RTE
    for variable in variables:
        RTEfile.write(f"{variable} = {variables[variable]}\n")
    RTEfile.write("\n\n")


    for component in components:
        RTEfile.write(f"\n\n# {component}\n")
        # Generate functions for the current component
        functions = []
        for readVariables in components[component][0]:
            # Generate read functions
            assert readVariables in variables # Make sure that the variable exits
            functionName = f"Rte_Read_{component}_{readVariables}"
            functions.append(functionName)
            RTEfile.write(f"def {functionName}():\n{ind}global {readVariables}\n{ind}return {readVariables}\n\n")
        for writtenVariables in components[component][1]:
            # Generate write functions
            assert writtenVariables in variables # Make sure that the variable exits
            functionName = f"Rte_Write_{component}_{writtenVariables}"
            functions.append(functionName)
            RTEfile.write(f"def {functionName}(arg):\n{ind}global {writtenVariables}\n{ind}{writtenVariables} = arg\n\n")
        
        # Generate or update the software component file
        fileImports = f"{editGuards[0]}from RTE import {', '.join(functions)}\n{editGuards[1]}"
        currentFileName = basepath + component + ".py"
        if os.path.isfile(currentFileName):
            # The file already exists, update it
            with open(currentFileName, "r+", encoding="utf-8") as currentFile:
                fileContents = currentFile.read()
                a = re.search(f"{editGuards[0]}.*?{editGuards[1]}", fileContents, re.MULTILINE | re.DOTALL)
                assert a # Make sure that we still have the editGuards
                fileContents = fileContents[0: a.regs[0][0]] + fileImports + fileContents[a.regs[0][1]:]
                currentFile.seek(0)
                currentFile.truncate(0)
                currentFile.write(fileContents)
        else:
            # The file does not exist, create it
            with open(currentFileName, "w", encoding="utf-8") as currentFile:
                currentFile.write(fileImports)
