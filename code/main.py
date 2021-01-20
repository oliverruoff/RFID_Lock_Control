#!/usr/bin/env python

import RPi.GPIO as GPIO

import stepper
import rfid
import inout

REGISTERED_UIDS_FILE = '.registered_uids'
LOG_FILE = 'log.txt'


def save_new_uid(uid):
    inout.write_log_file(LOG_FILE, 'Registered new uid:', uid)
    inout.append_text_line_to_file(REGISTERED_UIDS_FILE, uid)
    registered_uids.append(uid)
    print('Successfully registered new uid:', uid)


def register_first_key_as_master(uid):
    stepper.toggle_stepper(20, 1, 0.2)
    save_new_uid(uid)
    stepper.toggle_stepper(20, 2, 0.2)


def register_new_uid():
    stepper.toggle_stepper(20, 1, 0.2)
    uid, _ = rfid.read_rfid()
    if uid not in registered_uids:
        save_new_uid(uid)
    else:
        print('Uid is already registered!')
    stepper.toggle_stepper(20, 2, 0.2)


if __name__ == "__main__":
    try:
        registered_uids = inout.read_lines_from_file(REGISTERED_UIDS_FILE)
        print('Registered uids:', registered_uids)
        while True:
            print('Listening to RFID module...')
            uid, text = rfid.read_rfid()
            print(uid, uid in registered_uids)
            # First time using the lock control -> registering master key
            if len(registered_uids) == 0:
                print('No uids registered yet, registering new (master) key.')
                register_first_key_as_master(uid)
            # Master key recognized
            elif uid == registered_uids[0]:
                print('Master key recognized! Registering new uid...')
                register_new_uid()
            # Registered key recognized
            if uid in registered_uids:
                print('Unlocked!')
                inout.write_log_file(LOG_FILE, 'Opened lock with uid:', uid)
                stepper.toggle_stepper(110, 1, 0.5)
            # Unregistered key recognized
            else:
                print('Unauthorized! Sorry :P')
                inout.write_log_file(
                    LOG_FILE, 'Refused to open lock with uid:', uid)
                stepper.toggle_stepper(5, 5, 0.2)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
