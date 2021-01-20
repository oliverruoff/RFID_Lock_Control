from datetime import datetime


def append_text_line_to_file(file_path, text):
    with open(file_path, "a") as myfile:
        myfile.write(text + "\n")


def read_lines_from_file(file_path):
    with open(file_path, "r") as myfile:
        data = [s.replace("\n", "") for s in myfile.readlines()]
        return data


def write_log_file(log_file_path, text, uid):
    text_to_write = ' '.join(
        [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text, uid])
    append_text_line_to_file(log_file_path, text_to_write)
