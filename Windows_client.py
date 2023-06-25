import socket
import re
import struct
from pynput.mouse import Button, Controller
import numpy as np

MAX_DGRAM = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 50000))

mouse = Controller()

class mouse_event():
    timestamp = 0.
    code = 0
    type = 0
    val = 0
    def __init__(self, stamp,c,t,v):
        self.timestamp = stamp
        self.code = c
        self.type = t
        self.val = v
    def __print__(self):
        print(str(self.timestamp)+ "," + str(self.code) + "," + str(self.type) + "," + str(self.val))

def create_mouse_event(data):
    s = np.float64(data[0].replace("event at ",""))
    c = np.int32(data[1].replace("code ","").replace(" ",""))
    t = np.int32(data[2].replace("type ","").replace(" ",""))
    v = np.int32(data[3].replace("val ","").replace(" ",""))
    event = mouse_event(s,c,t,v)
    return event
message,address = sock.recvfrom(MAX_DGRAM)
data = message.decode().split(',')
old_event = create_mouse_event(data)
while(1):
    message,address = sock.recvfrom(MAX_DGRAM)
    data = message.decode().split(',')
    event = create_mouse_event(data)
    #event.__print__()
    check = event.timestamp - old_event.timestamp
    old_event = event

    match event.code:
        case 0:
            if event.type == 2:
            #print("X AXIS MOVE")
                mouse.move(int(event.val),0)   
        case 1:
            #print("Y AXIS MOVE")
            if event.type == 2:
                mouse.move(0,int(event.val))
        case 272:
            if(event.val == 1):
                mouse.press(Button.left)
                print("LEFT BUTTON PRESSED")
            if(event.val == 0):
                mouse.release(Button.left)
                print("LEFT BUTTON RELEASED")
        case 273:
            if(event.val == 1):
                mouse.press(Button.right)
                print("RIGHT BUTTON PRESSED")
            if(event.val == 0):
                mouse.release(Button.right)
                print("RIGHT BUTTON RELEASED")
        case 274:
            if(event.val == 1):
                mouse.press(Button.middle)
                print("MIDDLE BUTTON PRESSED")
            if(event.val == 0):
                mouse.release(Button.middle)
                print("MIDDLE BUTTON RELEASED")
        case 275:
            if(event.val == 1):
                mouse.press(Button.x1)
                print("BACK BUTTON PRESSED")
            if(event.val == 0):
                mouse.release(Button.x1)
                print("BACK BUTTON RELEASED")
        case 276:
            if(event.val == 1):
                mouse.press(Button.x2)
                print("FORWARD BUTTON PRESSED")
            if(event.val == 0):
                mouse.release(Button.x2)
                print("FORWARD BUTTON RELEASED")        
        case 8:
            mouse.scroll(0,event.val)
            print("SCROLL EVENT")
        case _:
            #event.__print__()
            pass

