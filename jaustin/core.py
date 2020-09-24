import os, sys
from bdb import BdbQuit
from contextlib import contextmanager
from pdb import post_mortem
import traceback
import types
import subprocess
import logging

import jaustin
import jaustin.color

""" Command utilities """

def run(command, timeout=120):
    """Run a given shell command in a subprocess and return the result with captured stdout and stderr."""

    result = subprocess.run(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return result


def decompress(filename, timeout=120):
    """Decompress a given .rar or .zip file to the same root directory. Requires
       unrar and unzip to be installed."""

    assert os.path.isfile(filename), "File does not exist or is not a valid file."

    dirname = os.path.dirname(filename)
    _, ext = os.path.splitext(os.path.basename(filename))

    ext_dict = {  # two spaces as a hack to handle escaped filenames
        '.rar' : 'unrar  -o+  x  {filename} {dirname}',
        '.zip' : 'unzip  -o  {filename}  -d  {dirname}'
    }

    if ext not in ext_dict.keys():
        raise TypeError(f"Unable to decompress file with unknown extension {ext}.")
    
    command = ext_dict[ext].format(filename=filename, dirname=dirname)
    logging.info(f"Extracting {ext} archive (running ({command.split('  ')})")
    result = jaustin.run(command, timeout=timeout)
    logging.info(f"Extraction completed with return code {result.returncode}.")

    if result.returncode != 0:
        print("[WARNING]", result.stderr)

    return result
        

""" Examination utilities """

def help(foo):
    """Prints any documentation attached to a given method."""

    print(foo.__doc__)

def examine(obj):
    """Examines a given object's attributes and print them color-coded by type."""
    
    fields = []
    methods = []
    for entry in dir(obj):
        try:
            value = getattr(obj, entry) 
        except:
            continue
        if type(value) is types.BuiltinMethodType or type(value) is type or type(value) is types.MethodType or type(value) is types.MethodWrapperType:
            methods.append(entry)
        else:
            fields.append(entry)

    print(jaustin.color.bold("==========  Summary  ==========\n"))

    lspace = ""

    attributes = {
        'type' : obj.__class__.__name__,
        'no. methods' : len(methods),
        'no. fields' : len(fields),
        'help' : obj.__doc__,
    }

    for field, value in attributes.items():
        print(f"{lspace}{jaustin.color.green(field.ljust(15))} : {jaustin.color.cyan(value)}")

    print()

    print(f"{lspace}{jaustin.color.blue('methods:')}")
    for entry in methods:
        print("        " + jaustin.color.cyan(entry))

    print()

    print(f"{lspace}{jaustin.color.blue('fields:')}")
    for entry in fields:
        print("        " + jaustin.color.cyan(entry))

@contextmanager
def debug(do_debug=True):
    """Context manager that ddrops into the PDB post_mortem debugger on failure.

    Example:
        >>> with jaustin.debug():
        >>>     main()
    """

    try:
        yield None
    except BdbQuit:
        raise
    except KeyboardInterrupt:
        raise
    except Exception as e:
        if do_debug:
            print(''.join(traceback.format_exception(e.__class__,e,e.__traceback__)))
            print(e)
            post_mortem()
            sys.exit(1)
        else:
            raise e
    finally:
        pass