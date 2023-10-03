"""Color constants importable by name"""

#https://htmlcolorcodes.com/color-names/
#stripped and renamed by Jan

from random import randint

def randColor() -> tuple:
    '''Returns a random color
    
    Returns:
        tuple: A 3-tuple of integers representing the red, green, and blue components of the color.
    '''
    return (randint(0, 255), randint(0, 255), randint(0, 255))

RGB_RED              = (255, 0, 0)
RGB_RED_DARK         = (139, 0, 0)
RGB_CRIMSON          = (220, 20, 60)
RGB_SALMON           = (250, 128, 114)
RGB_SALMON_LIGHT     = (255, 160, 122)
RGB_SALMON_DARK      = (233, 150, 122)
RGB_MAROON           = (128, 0, 0)

RGB_ROSE             = (255, 105, 180)
RGB_ROSE_LIGHT       = (255, 192, 203)
RGB_ROSE_DARK        = (219, 112, 147)
RGB_PINK             = (255, 20, 147)
RGB_PINK_DARK        = (199, 21, 133)

RGB_ORANGE           = (255, 140, 0)
RGB_ORANGE_LIGHT     = (255, 165, 0)
RGB_ORANGE_DARK      = (255, 69, 0)
RGB_TOMATO           = (255, 99, 71)
RGB_CORAL            = (255, 127, 80)

RGB_YELLOW           = (255, 255, 0)
RGB_YELLOW_LIGHT     = (255, 255, 224)
RGB_GOLD             = (255, 215, 0)
RGB_MOCCASIN         = (255, 228, 181)
RGB_KHAKI            = (240, 230, 140)
RGB_KHAKI_LIGHT      = (238, 232, 170)
RGB_KHAKI_DARK       = (189, 183, 107)

RGB_PURPLE           = (128, 0, 128)
RGB_INDIGO           = (75, 0, 130)
RGB_MAGENTA          = (255, 0, 255)
RGB_MAGENTA_DARK     = (139, 0, 139)
RGB_FUCHSIA          = (255, 0, 255)
RGB_VIOLET           = (238, 130, 238)
RGB_VIOLET_DARK      = (148, 0, 211)
RGB_LAVENDER         = (230, 230, 250)
RGB_SLATEBLUE        = (106, 90, 205)
RGB_SLATEBLUE_DARK   = (72, 61, 139)

RGB_GREEN            = (0, 128, 0)
RGB_GREEN_LIGHT      = (144, 238, 144)
RGB_GREEN_DARK       = (0, 100, 0)
RGB_LIME             = (0, 255, 0)
RGB_LIMEGREEN        = (50, 205, 50)
RGB_LAWNGREEN        = (124, 252, 0)
RGB_GREENYELLOW      = (173, 255, 47)
RGB_PALEGREEN        = (152, 251, 152)
RGB_SPRINGGREEN      = (0, 255, 127)
RGB_SEAGREEN         = (46, 139, 87)
RGB_SEAGREEN_LIGHT   = (32, 178, 170)
RGB_SEAGREEN_DARK    = (143, 188, 139)
RGB_OLIVE            = (128, 128, 0)
RGB_OLIVE_DARK       = (85, 107, 47)
RGB_OLIVEDRAB        = (107, 142, 35)

RGB_BLUE             = (0, 0, 255)
RGB_BLUE_LIGHT       = (173, 216, 230)
RGB_NAVY             = (0, 0, 128)
RGB_MIDNIGHTBLUE     = (25, 25, 112)
RGB_ROYALBLUE        = (65, 105, 225)
RGB_CORNFLOWERBLUE   = (100, 149, 237)
RGB_DODGERBLUE       = (30, 144, 255)
RGB_AQUA             = (0, 255, 255)
RGB_CYAN             = (0, 255, 255)
RGB_CYAN_LIGHT       = (224, 255, 255)
RGB_CYAN_DARK        = (0, 139, 139)
RGB_TEAL             = (0, 128, 128)
RGB_TURQUOISE        = (64, 224, 208)
RGB_TURQUOISE_DARK   = (0, 206, 209)
RGB_AQUAMARINE       = (127, 255, 238)
RGB_CADETBLUE        = (95, 158, 160)
RGB_STEELBLUE        = (70, 130, 180)
RGB_STEELBLUE_LIGHT  = (176, 196, 222)
RGB_POWDERBLUE       = (176, 224, 230)
RGB_SKYBLUE          = (135, 206, 235)
RGB_SKYBLUE_LIGHT    = (135, 206, 250)
RGB_SKYBLUE_DARK     = (0, 191, 255)

RGB_BROWN            = (139, 69, 19)
RGB_BROWN_LIGHT      = (160, 82, 45)
RGB_BROWNRED         = (165, 42, 42)
RGB_CHOCOLATE        = (210, 105, 30)
RGB_PERU             = (205, 133, 63)
RGB_SANDYBROWN       = (244, 164, 96)
RGB_ROSYBROWN        = (188, 143, 143)
RGB_GOLDENBROWN      = (218, 165, 32)
RGB_GOLDENBROWN_DARK = (184, 134, 11)
RGB_TAN              = (210, 180, 140)
RGB_CORNSLIK         = (255, 248, 220)
RGB_BLANCHEDALMOND   = (255, 235, 205)
RGB_BISQUE           = (255, 228, 196)
RGB_WHEAT            = (245, 222, 179)

RGB_WHITE            = (255, 255, 255)
RGB_SNOW             = (255, 255, 250)
RGB_HONEYDEW         = (240, 255, 240)
RGB_MINTCREAM        = (245, 255, 250)
RGB_AZURE            = (240, 255, 255)
RGB_ALICEBLUE        = (240, 248, 255)
RGB_GHOSTWHITE       = (248, 248, 255)
RGB_WHITESMOKE       = (245, 245, 245)
RGB_SEASHELL         = (255, 245, 238)
RGB_BEIGE            = (245, 245, 220)
RGB_OLDLACE          = (253, 245, 230)
RGB_FLORALWHITE      = (255, 250, 240)
RGB_IVORY            = (255, 255, 240)
RGB_ANTIQUEWHITE     = (250, 245, 215)
RGB_LINEN            = (250, 240, 230)
RGB_LAVENDERBUSH     = (255, 240, 245)
RGB_MISTYROSE        = (255, 228, 225)

RGB_BLACK            = (0, 0, 0)
RGB_GRAY             = (128, 128, 128)
RGB_GRAY_LIGHT       = (211, 211, 211)
RGB_GRAY_DARK        = (169, 169, 169)
RGB_SILVER           = (192, 192, 192)
RGB_DIMGRAY          = (105, 105, 105)
RGB_SLATEGRAY        = (112, 128, 144)
RGB_SLATEGRAY_LIGHT  = (119, 136, 153)
RGB_SLATEGRAY_DARK   = (47, 79, 79)
RGB_GAINSBORO        = (220, 220, 220)



HEX_RED              = '#FF0000'
HEX_RED_DARK         = '#8B0000'
HEX_CRIMSON          = '#DC143C'
HEX_SALMON           = '#FA8072'
HEX_SALMON_LIGHT     = '#FFA07A'
HEX_SALMON_DARK      = '#E9967A'
HEX_MAROON           = '#800000'

HEX_ROSE             = '#FF69B4'
HEX_ROSE_LIGHT       = '#FFC0CB'
HEX_ROSE_DARK        = '#DB7093'
HEX_PINK             = '#FF1493'
HEX_PINK_DARK        = '#C71585'

HEX_ORANGE           = '#FF8C00'
HEX_ORANGE_LIGHT     = '#FFA500'
HEX_ORANGE_DARK      = '#FF4500'
HEX_TOMATO           = '#FF6347'
HEX_CORAL            = '#FF7F50'

HEX_YELLOW           = '#FFFF00'
HEX_YELLOW_LIGHT     = '#FFFFE0'
HEX_GOLD             = '#FFD700'
HEX_MOCCASIN         = '#FFE4B5'
HEX_KHAKI            = '#F0E68C'
HEX_KHAKI_LIGHT      = '#EEE8AA'
HEX_KHAKI_DARK       = '#BDB76B'

HEX_PURPLE           = '#800080'
HEX_INDIGO           = '#4B0082'
HEX_MAGENTA          = '#FF00FF'
HEX_MAGENTA_DARK     = '#8B008B'
HEX_FUCHSIA          = '#FF00FF'
HEX_VIOLET           = '#EE82EE'
HEX_VIOLET_DARK      = '#9400D3'
HEX_LAVENDER         = '#E6E6FA'
HEX_SLATEBLUE        = '#6A5ACD'
HEX_SLATEBLUE_DARK   = '#483D8B'

HEX_GREEN            = '#008000'
HEX_GREEN_LIGHT      = '#90EE90'
HEX_GREEN_DARK       = '#006400'
HEX_LIME             = '#00FF00'
HEX_LIMEGREEN        = '#32CD32'
HEX_LAWNGREEN        = '#7CFC00'
HEX_GREENYELLOW      = '#ADFF2F'
HEX_PALEGREEN        = '#98FB98'
HEX_SPRINGGREEN      = '#00FF7F'
HEX_SEAGREEN         = '#2E8B57'
HEX_SEAGREEN_LIGHT   = '#20B2AA'
HEX_SEAGREEN_DARK    = '#8FBC8B'
HEX_OLIVE            = '#808000'
HEX_OLIVE_DARK       = '#556B2F'
HEX_OLIVEDRAB        = '#6B8E23'

HEX_BLUE             = '#0000FF'
HEX_BLUE_LIGHT       = '#ADD8E6'
HEX_NAVY             = '#000080'
HEX_MIDNIGHTBLUE     = '#191970'
HEX_ROYALBLUE        = '#4169E1'
HEX_CORNFLOWERBLUE   = '#6495ED'
HEX_DODGERBLUE       = '#1E90FF'
HEX_AQUA             = '#00FFFF'
HEX_CYAN             = '#00FFFF'
HEX_CYAN_LIGHT       = '#E0FFFF'
HEX_CYAN_DARK        = '#008B8B'
HEX_TEAL             = '#008080'
HEX_TURQUOISE        = '#40E0D0'
HEX_TURQUOISE_DARK   = '#00CED1'
HEX_AQUAMARINE       = '#7FFFEE'
HEX_CADETBLUE        = '#5F9EA0'
HEX_STEELBLUE        = '#4682B4'
HEX_STEELBLUE_LIGHT  = '#B0C4DE'
HEX_POWDERBLUE       = '#B0E0E6'
HEX_SKYBLUE          = '#87CEEB'
HEX_SKYBLUE_LIGHT    = '#87CEFA'
HEX_SKYBLUE_DARK     = '#00BFFF'

HEX_BROWN            = '#8B4513'
HEX_BROWN_LIGHT      = '#A0522D'
HEX_BROWNRED         = '#A52A2A'
HEX_CHOCOLATE        = '#D2691E'
HEX_PERU             = '#CD853F'
HEX_SANDYBROWN       = '#F4A460'
HEX_ROSYBROWN        = '#BC8F8F'
HEX_GOLDENBROWN      = '#DAA520'
HEX_GOLDENBROWN_DARK = '#B8860B'
HEX_TAN              = '#D2B48C'
HEX_CORNSLIK         = '#FFF8DC'
HEX_BLANCHEDALMOND   = '#FFEBCD'
HEX_BISQUE           = '#FFE4C4'
HEX_WHEAT            = '#F5DEB3'

HEX_WHITE            = '#FFFFFF'
HEX_SNOW             = '#FFFFFA'
HEX_HONEYDEW         = '#F0FFF0'
HEX_MINTCREAM        = '#F5FFFA'
HEX_AZURE            = '#F0FFFF'
HEX_ALICEBLUE        = '#F0F8FF'
HEX_GHOSTWHITE       = '#F8F8FF'
HEX_WHITESMOKE       = '#F5F5F5'
HEX_SEASHELL         = '#FFF5EE'
HEX_BEIGE            = '#F5F5DC'
HEX_OLDLACE          = '#FDF5E6'
HEX_FLORALWHITE      = '#FFFAF0'
HEX_IVORY            = '#FFFFF0'
HEX_ANTIQUEWHITE     = '#FAF5D7'
HEX_LINEN            = '#FAF0E6'
HEX_LAVENDERBUSH     = '#FFF0F5'
HEX_MISTYROSE        = '#FFE4E1'

HEX_BLACK            = '#000000'
HEX_GRAY             = '#808080'
HEX_GRAY_LIGHT       = '#D3D3D3'
HEX_GRAY_DARK        = '#A9A9A9'
HEX_SILVER           = '#C0C0C0'
HEX_DIMGRAY          = '#696969'
HEX_SLATEGRAY        = '#708090'
HEX_SLATEGRAY_LIGHT  = '#778899'
HEX_SLATEGRAY_DARK   = '#2F4F4F'
HEX_GAINSBORO        = '#DCDCDC'