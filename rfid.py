from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


def read_rfid():
    id, text = reader.read()
    return id, text


def write_rfid(text_to_write):
    reader.write(text_to_write)
