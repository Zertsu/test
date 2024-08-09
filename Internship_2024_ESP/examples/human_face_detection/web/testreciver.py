import socket
import struct

udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp.bind(("0.0.0.0", 15002))
while True:
    data, addr = udp.recvfrom(1024)
    print(data)
    if data[0] == 0:
        udp.sendto(b"\1\0", addr)
    if data[0] == 4:
        print(len(data))
        f = struct.unpack("<bHHHHHHHHHHHHHHHHH" , data)
        print(f"Frame: {f[2]}, {f[3]}")
        print(f"Box: {f[4]}, {f[5]}, {f[6]}, {f[7]}")
        print(f"Nose: {f[8]}, {f[9]}")
        print(f"Eyes: {f[10]}, {f[11]}, {f[12]}, {f[13]}")
        print(f"Mouth: {f[14]}, {f[15]}, {f[16]}, {f[17]}")
