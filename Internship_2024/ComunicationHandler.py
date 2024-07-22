from RTE import Rte_Read_ComunicationHandler_ui32_Time, Rte_Read_ComunicationHandler_f_Distance, Rte_Write_ComunicationHandler_ui8_Control_bits, Rte_Write_ComunicationHandler_ui32_Last_packet_time
import uasyncio as asyncio


import socket
import struct

# Configuration
bindAddress = ("0.0.0.0", 16002)
recieveRunPeriod = 20
sendRunPeriod = 50

# Global Variables
lastPacketSender = ("0.0.0.0", 0)
udpSocket = None

async def ComunicationHandler_Recieve():
    global bindAddress
    global recieveRunPeriod
    global lastPacketSender
    global udpSocket

    # Setup UDP socket
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.setblocking(False)
    udpSocket.bind(bindAddress)

    # Initialize local variables
    runsSinceLastPacket = 0

    while True:
        packet, recvAddress = udpSocket.recvfrom(64)
        print(packet, recvAddress)
        if packet:
            runsSinceLastPacket = 0
            lastPacketSender = recvAddress
            response = handlePacket(packet)
            if not response == None:
                udpSocket.sendto(response, recvAddress)
        else:
            runsSinceLastPacket += 1
        Rte_Write_ComunicationHandler_ui32_Last_packet_time(runsSinceLastPacket * runPeriod)
        await asyncio.sleep_ms(recieveRunPeriod)


def handlePacket(packet):
    packetType = packet[0]
    packetData = packet[0:]

    if packetType == 0:
        # Ping packet
        return packetData
    if packetType == 1:
        # Pong packet
        # do nothing
        return
    if packetType == 2:
        Rte_Write_ComunicationHandler_ui8_Control_bits(packetData[0])
        return


async def ComunicationHandler_Send():
    global lastPacketSender
    global udpSocket

    while True:
        if lastPacketSender[0] != "0.0.0.0":
            distance = Rte_Read_ComunicationHandler_f_Distance()
            packetData = struct.pack("!Bf", 3, distance)
            udpSocket.sendto(packetData, lastPacketSender)
