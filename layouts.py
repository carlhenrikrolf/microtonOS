#! /home/pi/.venv/bin/python3

def get_row_col(key):
	row = 0
	col = key
	while col >= (6 if row % 2 == 0 else 5):
		col -= 6 if row % 2 == 0 else 5
		row += 1
	return row, col
	
def get_key(row,col):
	key = sum(6 if i % 2 == 0 else 5 for i in range(row))
	return key + col

def exquis_layout(width=3, top_note=67):
	
	assert top_note in range(60, 128)
	mapping = [[0]*6 if row % 2 == 0 else [0]*5 for row in range(0,11)]
	overlap = (10 - width) % 5
	
	if width in range(1,6):
		last_note = top_note
		for row in [10, 8, 6, 4, 2, 0]:
			for col in range(5, -1, -1):
				note = last_note - (5 - col)
				mapping[row][col] = note
			last_note = note - 5 + overlap + 1
		last_note = top_note - 6 + overlap
		for row in [9, 7, 5, 3, 1]:
			for col in range(4, -1, -1):
				note = last_note - (4 - col)
				mapping[row][col] = note
			last_note = note - 6 + overlap + 1
		output = []
		for row in mapping:
			for key in row:
				output.append(key)
		return output
						
	elif width in range(6,11):
		for row in [10, 8, 6]:
			pass
		for row in [9, 7]:
			pass
		for row in [4, 2, 0]:
			pass
		for row in [3, 1]:
			pass
			
		
	else:
		raise ValueError('width must be in range [1, 11)')
		
print(exquis_layout())
	
