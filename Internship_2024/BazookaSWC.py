from RTE import Rte_Read_BazookaSWC_E_State, Rte_Write_BazookaSWC_b_Shoot
from typedefs import States



async def BazookaSWC():
    previousState = NONE
    while True: 
        state = Rte_Read_BazookaSWC_E_State()
        if state == SHOOT and previousState != SHOOT:
            Rte_Write_BazookaSWC_b_Shoot(1)
        previousState = state

        await asyncio.sleep_ms(50)  # Adjust sleep time later if needed

