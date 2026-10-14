import socket
from time import sleep
import hexformatter
import pygame
import threading
UDP_IP1 = "192.168.1.1"
UDP_PORT1 = 7099
UDP_IP2 = "192.168.169.1"
UDP_PORT2 = 8800
RTSP_PORT = 7070
UDP_PORT3 = 52613
base_speed = 128

formatter = hexformatter.HexFormatter()
messages = formatter.format_file("messages.json")
print("starting")
print(messages)

print("UDP target IP: %s" % UDP_IP1)
print("UDP target port: %s" % UDP_PORT1)

def getCleanHex(num):
    hexNum = hex(num)[2:]
    if hexNum == "0":
        hexNum = "00"
    return hexNum

def sendMessageTCP(message, ip, port):
    sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_STREAM) # UDP
    sock.connect((ip, port))
    sock.sendall(message)
    response = sock.recv(1024)
    print(response)

def sendMessageUDP(message, ip, port, recv=True):
    sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
    sock.sendto(message, (ip, port))
    sock.close()

class Drone():
    def __init__(self, start_speed):
        self.throttle = start_speed
        self.rotation = start_speed
        self.roll = start_speed
        self.pitch = start_speed
        self.reg_speed = start_speed
        self.base_i = 50
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.start = True

    def doAction(self, msg):
        sendMessageUDP(messages[msg], UDP_IP1, UDP_PORT1)
        print(msg)

    def launch(self):
        i = 0
        while (i < self.base_i + 50):
            i += 1
            sleep(0.05)
            if i < self.base_i:
                self.doAction("standby")
            elif i < self.base_i + 40:
                self.doAction("activate")
            else:
                self.doAction("fly")

    def sendSpeed(self):
        speed_str = f"03 66 {getCleanHex(self.roll)} {getCleanHex(self.pitch)} {getCleanHex(self.throttle)} {getCleanHex(self.rotation)} 00 {getCleanHex(self.reg_speed)} 99"
        speed_bytes = bytes.fromhex(speed_str)
        sendMessageUDP(speed_bytes, UDP_IP1, UDP_PORT1)

    def stop(self, emergency=False):
        self.running = False
        i = 0
        while i < 50:
            i += 1
            if emergency:
                self.doAction('emergency_stop')
            else:
                self.doAction('soft_stop')
            sleep(0.01)

    def adjustSpeed(self, speed, keys, keypos, keyneg):
        if keys[keypos] and not speed == 255: #because of thread
            speed += 1
        elif keys[keyneg] and not speed == 0:
            speed -= 1
        return speed

    def controls(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                self.stop(emergency=True)
            elif keys[pygame.K_BACKQUOTE]:
                self.stop()
            elif keys[pygame.K_SPACE]:
                self.start = True

            self.throttle = self.adjustSpeed(self.throttle, keys, pygame.K_UP, pygame.K_DOWN)
            self.rotation = self.adjustSpeed(self.rotation, keys, pygame.K_e, pygame.K_q)
            self.reg_speed = self.adjustSpeed(self.reg_speed, keys, pygame.K_LEFT, pygame.K_RIGHT)
            self.roll = self.adjustSpeed(self.roll, keys, pygame.K_d, pygame.K_a)
            self.pitch = self.adjustSpeed(self.pitch, keys, pygame.K_w, pygame.K_s)
            if len(keys) > 0:
                print(f"Speed: throttle:{self.throttle}, rot:{self.rotation}, roll: {self.roll}, pitch: {self.pitch}, reg_speed:{self.reg_speed}")
            
            if keys[pygame.K_LSHIFT]:
                sleep(0.03)
            else:
                sleep(0.1)

    def fly(self):
        while True:
            if self.start:
                self.launch()
                self.running = True
                self.start = False
            while self.running:
                self.sendSpeed()

    def run(self):
        flyThread = threading.Thread(target=self.fly)
        controlThread = threading.Thread(target=self.controls)
        controlThread.start()
        flyThread.start()





def main():
    drone = Drone(base_speed)
    drone.run()

main()