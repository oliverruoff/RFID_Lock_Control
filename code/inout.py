def append_text_line_to_file(file_path, text):
    with open(file_path, "a") as myfile:
        myfile.write(text + "\n")


def read_lines_from_file(file_path):
    with open(file_path, "r") as myfile:
        data = [s.replace("\n", "") for s in myfile.readlines()]
        return data
