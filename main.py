import socket
from time import sleep
import asyncio
import hexformatter
UDP_IP1 = "192.168.1.1"
UDP_PORT1 = 7099
UDP_IP2 = "192.168.169.1"
UDP_PORT2 = 8800
RTSP_PORT = 7070
UDP_PORT3 = 52613

formatter = hexformatter.HexFormatter()
messages = formatter.format_file("messages.json")
print("starting")
print(messages)

print("UDP target IP: %s" % UDP_IP1)
print("UDP target port: %s" % UDP_PORT1)

async def sendMessageTCP(message, ip, port):
    sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_STREAM) # UDP
    sock.connect((ip, port))
    sock.sendall(message)
    response = sock.recv(1024)
    print(response)

async def sendMessageUDP(message, ip, port, recv=True):
    loop = asyncio.get_running_loop()
    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock.sendto(message, (ip, port))
    response = ""
    try:
        if recv:
            response, _ = await asyncio.wait_for(loop.sock_recvfrom(sock, 1024), timeout=.2)
    except TimeoutError:
        pass
    print(response)
    print(f"sent to {port}")
    sock.close()


async def main():
    i = 0
    while (True):
        i += 1
        await sendMessageUDP(messages['activation1'], UDP_IP1, UDP_PORT1)
        await sendMessageUDP(messages['start2'], UDP_IP2, UDP_PORT2, False)
        if i == 50:
            await sendMessageUDP(messages['flight'], UDP_IP1, UDP_PORT1)
            await sendMessageUDP(messages['flight'], UDP_IP1, UDP_PORT1)
            await sendMessageUDP(messages['flight'], UDP_IP1, UDP_PORT1)
            print("BIGH CHUNGUS HELLO I'M SUPPOSED TO BE FLYING!!!")

asyncio.run(main())
