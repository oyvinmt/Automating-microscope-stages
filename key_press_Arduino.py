# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 08:07:00 2021

@author: Øyvind Taraldsen

This script allows the control of stepper motors via an Arduino by using the keyboard.

The serial communication functions are taken from the excelent tutorial found on
https://forum.arduino.cc/t/serial-input-basics-updated/382007
"""
from pynput import keyboard
import warnings
import pygame
import serial
import serial.tools.list_ports

pygame.init()
def waitForArduino():
    # wait until the Arduino sends 'Arduino Ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded
    global startMarker, endMarker
    
    msg = ""
    while msg.find("Arduino is ready") == -1:
        while ser.inWaiting() == 0:
            pass
        msg = recvFromArduino()
        print (msg) # python3 requires parenthesis
        print ()

def recvFromArduino():
    global startMarker, endMarker
    ck = ""
    x = "z" # any value that is not an end- or startMarker
    byteCount = -1 # to allow for the fact that the last increment will be one too many
    
    # wait for the start character
    while  ord(x) != startMarker: 
        x = ser.read()
    
    # save data until the end marker is found
    while ord(x) != endMarker:
        if ord(x) != startMarker:
            ck = ck + x.decode("utf-8") # change for Python3
            byteCount += 1
        x = ser.read()
    
    return(ck)

    
def sendToArduino(sendStr):
    ser.write(sendStr.encode('utf-8')) # change for Python3
    
# NOTE the user must ensure that the serial port and baudrate are correct
#serPort = "COM4"
baudRate = 57600

### detects and sets correct port
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description  # may need tweaking to match new arduinos
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

ser = serial.Serial(arduino_ports[0], baudRate)

"""
The following line can be used to set port manualy in case of issues.
"""
#ser = serial.Serial(serPort, baudRate)

startMarker = 60
endMarker = 62
waitForArduino()

"""
This uses the pygame module to run a "game" that takes inputs from the keyboard and sends
instructions to the Arduino based on those. Changing the keys in the event-loop allows 
one to change the keybindings.
"""
clock = pygame.time.Clock()
display = pygame.display.set_mode((100,100))
pygame.key.set_repeat()
while True :
    clock.tick(200)
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    diag = False
    for event in events:
        if event.type == pygame.KEYDOWN:
            
            if keys[pygame.K_KP6]:
                if keys[pygame.K_KP8]:
                    sendToArduino("e")
                elif keys[pygame.K_KP2]:
                    sendToArduino("z")
                else:
                    sendToArduino("d")
            if keys[pygame.K_KP4]:
                if keys[pygame.K_KP8]:
                    sendToArduino('q')
                elif keys[pygame.K_KP2]:
                    sendToArduino('z')
                else:
                    sendToArduino('a')
            if keys[pygame.K_KP8]:
                if keys[pygame.K_KP6]:
                    sendToArduino('e')
                elif keys[pygame.K_KP4]:
                    sendToArduino('q')
                else:
                    sendToArduino('w')
            if keys[pygame.K_KP2]:
                if keys[pygame.K_KP4]:
                    sendToArduino('z')
                elif keys[pygame.K_KP6]:
                    sendToArduino('c')
                else:
                    sendToArduino('s')
                    
            elif keys[pygame.K_KP_PLUS]:
                sendToArduino('r')
            elif keys[pygame.K_KP_MINUS]:
                sendToArduino('f')

            elif keys[pygame.K_KP3]:
                sendToArduino('o')
            elif keys[pygame.K_KP9]:
                sendToArduino('l')
                
            elif keys[pygame.K_KP0]:
                sendToArduino('3')
            elif keys[pygame.K_KP1]:
                sendToArduino('1')
            elif keys[pygame.K_KP7]:
                sendToArduino('2')
        if event.type == pygame.KEYUP:
            sendToArduino(' ')
            
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        break
    pygame.display.update()
    pygame.event.pump()