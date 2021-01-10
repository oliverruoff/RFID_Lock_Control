#!/usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8) (1,8° per step (oruoff))
STEPPER_ACTIVATE_PIN = 4


GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(STEPPER_ACTIVATE_PIN, GPIO.OUT)

GPIO.output(DIR, CW)
GPIO.output(STEPPER_ACTIVATE_PIN, GPIO.HIGH)

step_count = SPR
delay = .001

ALLOWED_RFID_ID_LIST = [455618101515, 659764798954]
PASSWORD_LIST = ['topsecretlol']

reader = SimpleMFRC522()

try:
    while True:
        id, text = reader.read()
        text = text.strip()
        print(id, id in ALLOWED_RFID_ID_LIST)
        print('>' + text + '<', text in PASSWORD_LIST)
        if id in ALLOWED_RFID_ID_LIST and text in PASSWORD_LIST:
            print('Unlocked!')
            GPIO.output(DIR, CW)
            for x in range(step_count):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP, GPIO.LOW)
                sleep(delay)
            sleep(.5)
            GPIO.output(DIR, CCW)
            for x in range(step_count):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP, GPIO.LOW)
                sleep(delay)
        else:
            print('Unauthorized! Sorry :P')
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
