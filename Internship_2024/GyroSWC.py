from RTE import Rte_Read_GyroSWC_si16_Raw_angle, Rte_Read_GyroSWC_b_Angle_reset, Rte_Write_GyroSWC_si16_Angle, Rte_Write_GyroSWC_b_Angle_reset

# Task to read gyroscopic sensor continuously
async def GyroSWC():
    reset_angle = 0 #The angle that it starts counting from
    while True: 
        gyro_sensor_value = Rte_Read_GyroSWC_si16_Raw_angle()

        angle_reset_bit = Rte_Read_GyroSWC_b_Angle_reset()
        if angle_reset_bit == 1:  #The bit that we get from RTE telling us we need to reset
            Rte_Write_GyroSWC_b_Angle_reset(0)    #Once we're done, we set it back to 0
            reset_angle = gyro_sensor_value  #The "new 0" becomes the current angle from gyro
        
        gyro_sensor_value -= reset_angle
        gyro_sensor_value %= 360  #Making sure the angle is in the 0-360 interval

        Rte_Write_GyroSWC_si16_Angle(gyro_sensor_value)


        await asyncio.sleep_ms(50)  # Adjust sleep time later if needed
