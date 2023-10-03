"""Functions for handling console output"""

from time import sleep

def printn(*args):
    '''Prints the given arguments, with newlines before and after (works with multiple args like print)
    
    Parameters:
        *args: The arguments to print.
    '''
    print('\n'+' '.join(str(x) for x in args)+'\n')

def delayPrint(s: str, t: float=0.5):
    '''Prints the given string with a slight delay after each character.

    Parameters:
        s: A string.
    '''
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(len(s)+1):
        print(LINE_UP, end=LINE_CLEAR)
        print(s[:i])
        sleep(t)