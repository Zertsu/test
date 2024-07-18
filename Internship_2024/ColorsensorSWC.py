from RTE import Rte_Read_ColorsensorSWC_e_Raw_color, Rte_Write_ColorsensorSWC_e_Color
#for unit test:
from RTE import Rte_Write_IOHandler_e_Raw_color

from collections import Counter
from enum import Enum
from pybricks.parameters import Color



# Task to read color sensor continuously
async def ColorsensorSWC():
    buffer_size = 10
    color_buffer = []    #This will store 10 colors each time, analyzing and returning the most common one
    while True: 
        while len(color_buffer) < buffer_size:
            color = Rte_Read_ColorsensorSWC_e_Raw_color()
            color_buffer.append(color)


        if len(color_buffer) == buffer_size:
            # Counting occurrences of each color in buffer:
            color_counts = Counter(color_buffer)

            # Finding the most common color:
            most_common_color, _ = color_counts.most_common(1)[0]

            Rte_Write_ColorsensorSWC_e_Color(most_common_color)

            color_buffer.pop(0)  # Removing oldest element


        

        await asyncio.sleep_ms(50)  # Adjust sleep time later if needed


async def ColorsensorSWC_UNIT_TEST():
    while True: 
        # there's no I/O Handler yet, so I'll take a function from there that writes the raw color to RTE
        Rte_Write_IOHandler_e_Raw_color(Color.RED)
        

        await asyncio.sleep_ms(10)  # Adjust sleep time later if needed

