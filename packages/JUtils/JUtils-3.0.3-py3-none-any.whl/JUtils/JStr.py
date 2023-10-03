"""Functions for string analysing and modification"""

from os import listdir

NL = '\n' #newline constant to keep code clean

def locBrac(string: str, brac: str, ix: int) -> int:
    '''
    Finds the index of the closing bracket that matches the opening bracket at the given index in the given string.

    Parameters:
        string (str): The input string.
        brac (str): The bracket character | Possible are ( [ { <
        ix (int): The index of the opening bracket in the input string.

    Returns:
        int: The index of the closing bracket in the input string, or -1 if no matching closing bracket was found.

    Example:
        >>> locBrac('[hello[world]]', '[', 0)
        13
        >>> locBrac('<hello<world>>', '<', 6)
        12
        >>> locBrac('{hello}world}', '{', 0)
        -1
    '''
    fil = {'(':')', '[':']', '{':'}', '<':'>'}
    if not brac in fil:
        return -1
    if not brac in string:
        return -1
    st = []
    for i, ch in enumerate(string):
        if ch == brac:
            st.append(i)
        elif ch == fil[brac]:
            st.pop()
        if st == [] and i >= ix:
            return i
    return -1

def multiCenter(s: str, l: int) -> str:
    """
    Centers the text in a string by padding spaces on either side of each line.
    
    Args:
        s (str): The input string to center.
        l (int): The desired width of the centered string.
        
    Returns:
        str: The centered string. Each line is padded with spaces on either side to center the text. If
             a line already has an odd number of characters, the extra space is added to the right
             side of the line.
    """
    return "\n".join([" "*((l-len(x))//2) + x + " "*((l-len(x))//2) for x in s.split("\n")])

def listPath(d: str) -> list[str]:
    """
    Just like os.listdir(), but with appended path.
    
    Args:
        d: The path to list.
        
    Returns:
        list: A list of paths of files and directories in the given path.
    """
    return [d + "\\" + x for x in listdir(d)]