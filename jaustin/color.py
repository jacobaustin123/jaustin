from colorama import Fore, Back, Style

def color(s,c):
    return '\001'+c+'\002'+str(s)+'\001'+Style.RESET_ALL+'\002'

""" Add colors to a string and return the string """

def green(s):
    return color(s, Fore.GREEN)
    
def red(s):
    return color(s, Fore.RED)

def pink(s):
    return color(s, Fore.MAGENTA)

def blue(s):
    return color(s, Fore.BLUE)

def cyan(s):
    return color(s, Fore.CYAN)

def yellow(s):
    return color(s, Fore.YELLOW)

def gray(s):
    return color(s,'\033[90m')


""" Add style to a string (bold, underline) """

def bold(s):
    return color(s,'\033[1m')

def underline(s):
    return color(s,'\033[4m')