from RTE import Rte_Read_EmergencySWC_ui32_Time, Rte_Read_EmergencySWC_ui32_Last_packet_time, Rte_Read_EmergencySWC_f_Distance, Rte_Write_EmergencySWC_b_Emergency_distance, Rte_Write_EmergencySWC_b_Emergency_timeout


async def EmergencySWC():
    while True: 
        # time = Rte_Read_EmergencySWC_ui32_Time()    # we will probably remove stopwatch, so time as well
        lastPacketTime = Rte_Read_EmergencySWC_ui32_Last_packet_time()  # tells us how many seconds have passed since receiving the last packet
        distance = Rte_Read_EmergencySWC_f_Distance()

        if distance < 10:    # this is already in cm, right?
            Rte_Write_EmergencySWC_b_Emergency_distance(1)
        
        if lastPacketTime > 30:               #ms   # if last packet time is more than half a second, enter timeout emergency mode
            Rte_Write_EmergencySWC_b_Emergency_timeout(1)

        await asyncio.sleep_ms(50)  # Adjust sleep time later if needed
