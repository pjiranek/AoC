def read_input(file_name):
    with open(file_name, 'r') as f:
        stripped_lines = (line.strip() for line in f.readlines())
        return [line for line in stripped_lines if line]
