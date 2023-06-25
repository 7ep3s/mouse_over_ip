import struct
import socket
import re
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from evdev import InputDevice, ecodes
from select import select

IPs = ["192.168.1.162","10.0.0.8"];
index = 0;
IP = IPs[index];

class Computer():
  ip = "0.0.0.0"
  name = "none"
  res = (0,0)
  def __init__(self,i,n,r):
    self.ip = i
    self.name = n
    self.res = r
    
    
computers = list()
computers.append(Computer("192.168.1.162","tepes-pc",(5360,1440)))
computers.append(Computer("10.0.0.8","tepes-mac",(3456,2234)))

def next_computer():
  global index
  index = index + 1;
  try:
    IP = computers[index].ip;
  except:
    index = 0;
    IP = computers[index].ip;
  print("switching to client "+IP);

def button_callback(channel):
  next_computer();
dev = InputDevice('/dev/input/event1');
PORT = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); # UDP

GPIO.setwarnings(False); # Ignore warning for now
GPIO.setmode(GPIO.BOARD); # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN); # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.FALLING,callback=button_callback); # Setup event on pin 10 rising edge

while( 1 ):
  r,w,x = select([dev],[],[]);
  
  #message = input("Press enter to quit\n\n"); # Run until someone presses enter

  for event in dev.read():
    message = str(event);
    sock.sendto(bytes(message, "utf-8"),(computers[index].ip,PORT))
    print(message)
    print(computers[index].ip)

GPIO.cleanup(); # Clean up