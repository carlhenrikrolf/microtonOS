from colour import Color

def convert(color):
    return Color(color) if type(color) is str else color

def negative(color):
    color = convert(color)
    result = Color()
    result.rgb = [1-i for i in color.rgb]
    return result
    
def set_luminance(color, coefficient, reference=None):
    color = convert(color)
    reference = convert(color if reference is None else reference)
    if 0 <= coefficient <= 1:
        luminance = coefficient * reference.luminance
        result = color
        result.luminance = luminance
    elif -1 <= coefficient:
        luminance = -coefficient
        luminance *= negative(reference).luminance
        result = negative(color)
        result.luminance = luminance
    else:
        raise ValueError("Coefficient must be within -1 and 1")
    return result