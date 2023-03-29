import os


def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass