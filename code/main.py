#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from datetime import datetime

import stepper
import rfid
import inout

REGISTERED_UIDS_FILE = '.registered_uids.txt'
LOG_FILE = 'log.txt'


def register_new_uid():
    for _ in range(2):
        stepper.turn_stepper(20, True)
        time.sleep(0.2)
        stepper.turn_stepper(20, False)
        time.sleep(0.2)
        id, _ = rfid.read_rfid()
        if id not in registered_uids:
            inout.append_text_line_to_file(
                LOG_FILE,
                str(datetime.now) + ' Registered new id: ' + id)
            inout.append_text_line_to_file(REGISTERED_UIDS_FILE, id)
            registered_uids.append(id)
        for _ in range(3):
            stepper.turn_stepper(20, True)
            time.sleep(0.2)
            stepper.turn_stepper(20, False)
            time.sleep(0.2)


if __name__ == "__main__":
    try:
        registered_uids = inout.read_lines_from_file(REGISTERED_UIDS_FILE)
        while True:
            id, text = rfid.read_rfid()
            print(id, id in registered_uids)
            if len(registered_uids) == 0 or id == registered_uids[0]:
                print('Master key recognized!')
                register_new_uid()
            if id in registered_uids:
                print('Unlocked!')
                inout.append_text_line_to_file(
                    LOG_FILE,
                    str(datetime.now) + ' Opened lock with id: ' + id)
                stepper.turn_stepper(90, True)
                time.sleep(0.5)
                for _ in range(2):
                    stepper.turn_stepper(10, False)
                    time.sleep(0.5)
                    stepper.turn_stepper(10, True)
                    time.sleep(0.5)
                stepper.turn_stepper(90, False)
            else:
                print('Unauthorized! Sorry :P')
                inout.append_text_line_to_file(
                    LOG_FILE,
                    str(datetime.now) + ' Refused to open lock with id: ' + id)
                for _ in range(5):
                    stepper.turn_stepper(5, True)
                    time.sleep(0.2)
                    stepper.turn_stepper(5, False)
                    time.sleep(0.2)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
