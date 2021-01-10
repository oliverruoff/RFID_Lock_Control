#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

import rfid
import stepper
import io

REGISTERED_RFID_UIDS = [455618101515, 659764798954]

try:
    while True:
        id, text = rfid.read_rfid()
        print(id, id in REGISTERED_RFID_UIDS)
        if id in REGISTERED_RFID_UIDS:
            print('Unlocked!')
            stepper.turn_stepper(85, True)
            time.sleep(0.5)
            stepper.turn_stepper(85, False)
        else:
            print('Unauthorized! Sorry :P')
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
