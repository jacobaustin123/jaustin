
import os

def read(filename):
    """Reads the data in a given file."""

    with open(filename, 'r') as f:
        return f.read()

def readlines(path):
    """Reads the lines in a given file."""

    with open(path, 'r') as f:
        return f.read().splitlines()

def listdir(path):
    """Returns a list of files in the given directory with the base path name included."""

    return [os.path.join(path, f) for f in os.listdir(path)]

def write(path, string):
    """Writes a given string to a file in append mode."""

    with open(path, 'a') as f:
        f.write(string)