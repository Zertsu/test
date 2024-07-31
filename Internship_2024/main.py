#!/usr/bin/env pybricks-micropython
import uasyncio as asyncio

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# SWC imports
import GuardingStateMachineSWC
import StateMachineSWC
import MotorSWC
import GyroSWC
import UltrasonicSWC
import ColorsensorSWC
import EmergencySWC
import BazookaSWC

# Handlers
import ComunicationHandler
import IOHandler


def main():
    loop = asyncio.get_event_loop()
    
    # Handler tasks
    loop.create_task(IOHandler.IOHandler())
    loop.create_task(ComunicationHandler.ComunicationHandler_Recieve())
    loop.create_task(ComunicationHandler.ComunicationHandler_Send())

    # SWCs
    # loop.create_task(StateMachineSWC.state_machine())
    loop.create_task(GuardingStateMachineSWC.guard_state_machine())
    loop.create_task(MotorSWC.MotorSWC())
    loop.create_task(GyroSWC.GyroSWC())
    loop.create_task(UltrasonicSWC.UltrasonicSWC())
    loop.create_task(ColorsensorSWC.ColorsensorSWC())
    loop.create_task(EmergencySWC.EmergencySWC())
    loop.create_task(BazookaSWC.BazookaSWC())
    
    
    loop.run_forever()

# Run the event loop
main()
