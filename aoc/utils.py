import time


def read_input(file_name):
    with open(file_name, 'r') as f:
        stripped_lines = (line.rstrip() for line in f.readlines())
        return [line for line in stripped_lines if line]


def timeit(func):

    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()

        print('{0} took {1} seconds.'.format(func.__name__, end_time - start_time))

    return wrapper
