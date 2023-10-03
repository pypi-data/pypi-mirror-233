"""Functions for array analysing and modification"""

import typing

def IterComp(a: typing.Iterable, b: typing.Iterable) -> bool | None:
    """
    Check if 2 iterables of the same length have the same elements, regardless of type.
    Args:
        a: An iterable object.
        b: An iterable object.
    Returns:
        - True if every element in `a` is equal to the corresponding element in `b`.
        - False if there is at least one pair of non-equal elements in `a` and `b`.
        - None if the length of `a` and `b` differ.
    Examples:
        >>> IterComp([1, 2, 3], [1, 2, 3])
        True
        >>> IterComp([1, 2, 3], [1, 2, 4])
        False
        >>> IterComp([1, 2, 3], [1, 2])
        None
    """
    if len(a) != len(b):
        return None
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

def segm(arr: list, n: int) -> list[list]:
    '''
    Divide a list into sublists of a specified size.
    
    Parameters:
        arr (list): The list to be divided into sublists.
        n (int): The size of each sublist.
        
    Returns:
        list: A list of sublists, where each sublist contains 'n' elements.
        
    Example:
        >>> segm([1, 1, 1, 1, 1, 1], 2)
        [[1, 1], [1, 1], [1, 1]]
    '''
    return [arr[x:x+n] for x in range(0, len(arr), n)]

def flt2d(arr: list[list]) -> list:
    '''
    Flatten a list of lists into a single list. Only for 2d lists, because the inner items should not be flattened.
    
    Parameters:
        arr (list): The list of lists to be flattened.
        
    Returns:
        list: The resulting flattened list.
        
    Example:
        >>> flt([[(), ()], [(), ()]])
        [(), (), (), (), (), ()]
    '''
    return [y for x in arr for y in x]

def overlp(l1: list, l2: list) -> bool:
    '''
    Checks if elements in l1 and l2 share any same elements

    Parameters:
        l1 (list): a list of elements
        l2 (list): a list of elements

    Returns:
        bool: if there are any overlaps between l1 and l2
    '''
    return bool(set(l1) & set(l2))

def rmap(funcs: typing.Iterable, *args):
    """
    Apply a sequence of functions to input arguments and yield the results.

    Args:
        funcs (Iterable): An iterable containing functions to be applied.
        *args: one or more arguments that will be passed to the functions.

    Yields:
        object: The result of applying each function to the input arguments.

    Example:
        >>> funcs = [lambda x, y: x * y, lambda x, y: x + y]
        >>> list(rmap(funcs, 2, 3))
        [6, 5]
    """
    for f in funcs:
        yield f() if len(args) == 0 else f(*args)
