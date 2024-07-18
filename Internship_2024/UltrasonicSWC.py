from RTE import Rte_Read_UltrasonicSWC_si16_Raw_distance, Rte_Write_UltrasonicSWC_f_Distance


# Task to read ultrasonic sensor continuously
async def UltrasonicSWC():
    while True: 
        distance = Rte_Read_UltrasonicSWC_si16_Raw_distance()   #It will read in mm 
        # Transfer to cm based on requirement:
        distance /= 10
        Rte_Write_UltrasonicSWC_f_Distance(distance)


        await asyncio.sleep_ms(50)  # Adjust sleep time as needed

