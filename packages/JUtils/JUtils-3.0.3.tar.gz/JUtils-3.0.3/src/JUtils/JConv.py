"""Functions for converting values"""

from math import sin, cos, sqrt, atan2, pi

def rgb2hex(rgb: tuple) -> str:
    '''
    Convert an RGB tuple to a hexadecimal string representation.

    Parameters:
    rgb (tuple): An RGB tuple with 3 integers between 0 and 255, inclusive, representing the red, green, and blue values.

    Returns:
    str: A hexadecimal string representation of the input RGB tuple, in the form '#RRGGBB'.

    Example:
    >>> rgb_to_hex((255, 0, 255))
    '#ff00ff'
    '''
    return ('#{:02x}{:02x}{:02x}').format(*rgb)

def hex2rgb(hx: str) -> tuple:
    '''
    Convert a hexadecimal string representation to an RGB tuple.

    Parameters:
    hx (str): A hexadecimal string representation of an RGB color, in the form '#RRGGBB'.

    Returns:
    tuple: An RGB tuple with 3 integers between 0 and 255, inclusive, representing the red, green, and blue values.

    Example:
    >>> hex2rgb('#ff00ff')
    (255, 0, 255)
    '''
    return tuple([int(hx[1:][i:i+2], 16) for i in (0, 2, 4)])

def hex2asc(hx: str) -> str:
    '''
    Convert a string of hexadecimal characters to a string of ASCII characters.
    
    Parameters:
        hx (str): The string of hexadecimal characters to be converted.
        
    Returns:
        str: The resulting string of ASCII characters.
    
    Example:
        >>> hex2asc('0000ff')
        '048048048048102102' #048 048 048 048 102 102
    '''
    return ''.join([str(ord(x)).zfill(3) for x in hx[1:]])

def deg2rad(deg: float) -> float:
    '''Converts an angle in degrees to radians.

    Parameters:
        deg (float): An angle in degrees.

    Returns:
        float: The equivalent angle in radians.
    '''
    return deg * pi / 180

def rad2deg(rad: float) -> float:
    '''Converts an angle in radians to degrees.

    Parameters:
        rad (float): An angle in radians.

    Returns:
        float: The equivalent angle in degrees.
    '''
    return rad * 180 / pi

def pol2cart(ang: float, r: float) -> tuple:
    '''Converts polar coordinates to Cartesian coordinates.

    Args:
        ang (float): An angle in degrees.
        r (float): The distance from the origin.

    Returns:
        tuple: A tuple of the Cartesian coordinates (x, y).
    '''
    return (r*cos(deg2rad(ang)), r*sin(deg2rad(ang)))

def cart2pol(x: float, y: float) -> tuple:
    '''Converts Cartesian coordinates to polar coordinates.

    Args:
        x (float): The x-coordinate.
        y (float): The y-coordinate.

    Returns:
        tuple: Polar coordinates (th, r), where r is the distance fromthe origin and th is the angle in degrees.
    '''
    r = sqrt(x*x + y*y)
    th = rad2deg(atan2(y, x))
    return (th, r)

def rgb2gray(rgb: tuple) -> int:
    """
    Converts an RGB color tuple to a grayscale integer value using the luminosity method.
    
    Args:
        rgb (tuple): A tuple containing 3 integers representing the RGB color values. The values
                     should be in the range of 0-255, inclusive.
                     
    Returns:
        int: The grayscale integer value representing the given RGB color tuple.
    """
    return int(0.299*rgb[0]//1 + 0.587*rgb[1]//1 + 0.114*rgb[2]//1)