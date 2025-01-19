from colour import Color

def negative(color):
    result = Color()
    if type(color) is str:
        result = Color(color)
        return negative(result)
    else:
        result.rgb = [1-i for i in color.rgb]
        return result