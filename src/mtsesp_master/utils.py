from midi_implementation.dualo import exquis as xq

def color_coding(number):
	digits = [xq.white, xq.lime, xq.yellow, xq.red, xq.magenta, xq.blue, xq.cyan, xq.dark]
	return [digits[number // 8], digits[number % 8]]
