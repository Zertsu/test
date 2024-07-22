from RTE import Rte_Read_BazookaSWC_E_State, Rte_Write_BazookaSWC_b_Shoot
import uasyncio as asyncio

from typedefs import States


async def BazookaSWC():
    previousState = States.NONE
    while True: 
        state = Rte_Read_BazookaSWC_E_State()
        if state == States.SHOOT and previousState != States.SHOOT:
            Rte_Write_BazookaSWC_b_Shoot(1)
        previousState = state

        await asyncio.sleep_ms(50)  # Adjust sleep time later if needed
