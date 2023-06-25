import struct
import socket
import re

from evdev import InputDevice, ecodes
from select import select
dev = InputDevice('/dev/input/event1')

IP = "192.168.1.162"
PORT = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); # UDP

while( 1 ):
  r,w,x = select([dev],[],[])
  for event in dev.read():
    message = str(event)
    sock.sendto(bytes(message, "utf-8"),(IP,PORT))
    print(message)
