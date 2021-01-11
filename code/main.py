#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from datetime import datetime

import stepper
import rfid
import inout

REGISTERED_UIDS_FILE = '.registered_uids.txt'
LOG_FILE = 'log.txt'


def save_new_uid(uid):
    inout.append_text_line_to_file(
        LOG_FILE,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Registered new uid: ' + uid)
    inout.append_text_line_to_file(REGISTERED_UIDS_FILE, uid)
    registered_uids.append(uid)
    print('Successfully registered new uid:', uid)


def register_first_key_as_master(uid):
    stepper.turn_stepper(20, True)
    time.sleep(0.2)
    stepper.turn_stepper(20, False)
    time.sleep(0.2)
    save_new_uid(uid)
    for _ in range(2):
        stepper.turn_stepper(20, True)
        time.sleep(0.2)
        stepper.turn_stepper(20, False)
        time.sleep(0.2)


def register_new_uid():
    stepper.turn_stepper(20, True)
    time.sleep(0.2)
    stepper.turn_stepper(20, False)
    time.sleep(0.2)
    uid, _ = rfid.read_rfid()
    if uid not in registered_uids:
        save_new_uid(uid)
    else:
        print('Uid is already registered!')
    for _ in range(2):
        stepper.turn_stepper(20, True)
        time.sleep(0.2)
        stepper.turn_stepper(20, False)
        time.sleep(0.2)


if __name__ == "__main__":
    try:
        registered_uids = inout.read_lines_from_file(REGISTERED_UIDS_FILE)
        print('Registered uids:', registered_uids)
        while True:
            print('Listening to RFID module...')
            uid, text = rfid.read_rfid()
            print(uid, uid in registered_uids)
            if len(registered_uids) == 0:
                print('No uids registered yet, registering new (master) key.')
                register_first_key_as_master(uid)
            elif uid == registered_uids[0]:
                print('Master key recognized! Registering new uid...')
                register_new_uid()
            if uid in registered_uids:
                print('Unlocked!')
                inout.append_text_line_to_file(
                    LOG_FILE,
                    str(datetime.now) + ' Opened lock with uid: ' + uid)
                stepper.turn_stepper(90, True)
                time.sleep(0.5)
                for _ in range(2):
                    stepper.turn_stepper(20, False)
                    time.sleep(0.3)
                    stepper.turn_stepper(20, True)
                    time.sleep(0.3)
                stepper.turn_stepper(90, False)
            else:
                print('Unauthorized! Sorry :P')
                inout.append_text_line_to_file(
                    LOG_FILE,
                    str(datetime.now) + ' Refused to open lock with uid: ' + uid)
                for _ in range(5):
                    stepper.turn_stepper(5, True)
                    time.sleep(0.2)
                    stepper.turn_stepper(5, False)
                    time.sleep(0.2)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
