from colour import Color

def negative(color):
    result = Color()
    if type(color) is str:
        result = Color(color)
        return negative(result)
    else:
        result.rgb = [1-i for i in color.rgb]
        return result
    
def set_luminance(color, coefficient, reference=Color("white")):
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