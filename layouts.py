#! /home/pi/.venv/bin/python3

def exquis_layout(width=3, top_note=67):
	
	assert top_note in range(60, 128)
	mapping = [[0]*6 if row % 2 == 0 else [0]*5 for row in range(0,11)]
	overlap = (10 - width) % 5
	
	if width in range(1,6):
		last_note = top_note
		for row in range(10, -1, -1):
			if row % 2 == 0: # is even
				for col in range(5, -1, -1):
					note = last_note - (5 - col)
					mapping[row][col] = note
				last_note = note - 1 + overlap
			else:
				for col in range(4, -1, -1):
					note = last_note - (4 - col)
					mapping[row][col] = note
				last_note = note - 1 + overlap
						
	elif width in range(6,11):
		last_note = top_note
		for row in range(10, 5, -1):
			if row % 2 == 0: # is even
				for col in range(5, -1, -1):
					note = last_note - (5 - col)
					mapping[row][col] = note
				last_note = note - 5 + overlap
			else:
				for col in range(4, -1, -1):
					note = last_note - (4 - col)
					mapping[row][col] = note
				last_note = note - 6 + overlap
		last_note = top_note - 6 + 1
		for row in range(4, -1, -1):
			if row % 2 == 0: # is even
				for col in range(5, -1, -1):
					note = last_note - (5 - col)
					mapping[row][col] = note
				last_note = note - 5 + overlap
			else:
				for col in range(4, -1, -1):
					note = last_note - (4 - col)
					mapping[row][col] = note
				last_note = note - 6 + overlap
		
	else:
		raise ValueError('width must be in range [1, 11)')
		
	output = []
	for row in mapping:
		for key in row:
			output.append(key)
	return mapping
		
print(exquis_layout())
	
