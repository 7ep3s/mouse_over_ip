import struct
import socket
import re
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from evdev import InputDevice, ecodes
from select import select

IPs = ["192.168.1.162","10.0.0.8"];
index = 0;
IP = IPs[index];

def next_IP():
  global index
  index = index + 1;
  try:
    IP = IPs[index];
  except:
    index = 0;
    IP = IPs[index];
  print("switching to client "+IP);

def button_callback(channel):
  next_IP();
dev = InputDevice('/dev/input/event1');
PORT = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); # UDP

GPIO.setwarnings(False); # Ignore warning for now
GPIO.setmode(GPIO.BOARD); # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN); # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback); # Setup event on pin 10 rising edge

while( 1 ):
  r,w,x = select([dev],[],[]);
  
  #message = input("Press enter to quit\n\n"); # Run until someone presses enter

  for event in dev.read():
    message = str(event);
    sock.sendto(bytes(message, "utf-8"),(IP,PORT))
    print(message)
  GPIO.cleanup(); # Clean up