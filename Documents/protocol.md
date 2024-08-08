# UDP Communication Protocol Between ESP32 and EV3 Lego Robot

This document outlines the communication protocol used for exchanging data between an ESP32 microcontroller and an EV3 Lego robot via UDP packets. Each packet is identified by a unique packet ID (the first byte), which determines the structure and purpose of the rest of the packet's data.

## Packet Structure

### General Structure
- **Byte 0**: Packet ID (1 byte)
- **Byte 1-n**: Data (varies depending on Packet ID)

### Packet ID Definitions

#### **00 - Ping**
- **Direction**: Two-way (ESP32 ↔ EV3)
- **Description**: This packet is used to check the connection between devices. The receiving device should respond with a PONG packet.
- **Data**: 
  - **Byte 1**: A single byte that gets echoed back in the PONG packet.
  
#### **01 - Pong**
- **Direction**: Two-way (ESP32 ↔ EV3)
- **Description**: This is the response to the PING packet. It confirms that the receiving device is connected and active.
- **Data**: 
  - **Byte 1**: The same byte received in the PING packet.

#### **02 - Controls**
- **Direction**: ESP32 to EV3
- **Description**: This packet contains the states of the controls from the ESP32's web interface. These states control various functions of the robot.
- **Data**: 
  - **Byte 1**: Control states encoded in 1 byte.
    - **b0**: Acceleration requested (1 bit)
    - **b1**: Brake requested (1 bit)
    - **b2**: Left turn requested (1 bit)
    - **b3**: Right turn requested (1 bit)
    - **b4**: Bazooka fire trigger (1 bit)
    - **b5**: Reserved
    - **b6**: Guarding mode (1 bit)
    - **b7**: Reserved

#### **03 - Distance**
- **Direction**: EV3 to ESP32
- **Description**: This packet sends the measured distance from the EV3 robot's ultrasonic sensor to the ESP32.
- **Data**: 
  - **Bytes 1-4**: The measured distance as a float (4 bytes).

#### **04 - Face Position**
- **Direction**: ESP32 to EV3
- **Description**: This packet communicates the position of a recognized faces, which used by the robot for tracking.
- **Data**: 
  - **Bytes 1-2**: Face type (16-bit unsigned integer)
    - **0**: No recognized faces
    - **1**: Foe recognized
    - **2**: Friend recognized
  - **Bytes 3-4**: Frame width (16-bit unsigned integer)
  - **Bytes 5-6**: Frame height (16-bit unsigned integer)
  - **Bytes 7-8**: Box X position (16-bit unsigned integer)
  - **Bytes 9-10**: Box Y position (16-bit unsigned integer)
  - **Bytes 11-12**: Box width (16-bit unsigned integer)
  - **Bytes 13-14**: Box height (16-bit unsigned integer)
  - **Bytes 15-16**: Nose X position (16-bit unsigned integer)
  - **Bytes 17-18**: Nose Y position (16-bit unsigned integer)
  - **Bytes 19-20**: Left eye X position (16-bit unsigned integer)
  - **Bytes 21-22**: Left eye Y position (16-bit unsigned integer)
  - **Bytes 23-24**: Right eye X position (16-bit unsigned integer)
  - **Bytes 25-26**: Right eye Y position (16-bit unsigned integer)
  - **Bytes 27-28**: Left side of mouth X position (16-bit unsigned integer)
  - **Bytes 29-30**: Left side of mouth Y position (16-bit unsigned integer)
  - **Bytes 31-32**: Right side of mouth X position (16-bit unsigned integer)
  - **Bytes 33-34**: Right side of mouth Y position (16-bit unsigned integer)

#### **05 - Guarding Mode State**
- **Direction**: EV3 to ESP32
- **Description**: This packet informs the ESP32 when the robot enters or leaves guarding mode.
- **Data**: 
  - **Byte 1**: Guarding mode state (1 byte Boolean value)
    - **0**: Guarding mode off
    - **1**: Guarding mode on
