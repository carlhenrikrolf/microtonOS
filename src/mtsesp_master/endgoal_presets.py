from tunings import Default, Micro, Macro, Subset, Ombak, Octave, Arbitrary
from layouts import exquis, harmonic_table, wicki_hayden, janko

tunings = [
	Macro('5edo', 5, 2, 1, [None, 0, None, 1, None, None, 2, None, 3, None, 4, None], 1, concert_a_frequency=440.0*2**(1/5)),
	Macro('7edo', 7, 2, 1, [0, None, 1, None, 2, 3, None, 4, None, 5, None, 6], 2),
	Octave('Just7', [1, None, 9/8, None, 5/4, 11/8, None, 3/2, None, 13/8, None 7/4, None], 2, unit='ratios'),
	Macro('13ed3', 13, 3, 1, [
			0, None, 1, None, 2, 3, 4, 5, None, 6, None, 7,
			8, 9, 10, None, 11, 12, None, 13, None, 14, 15, 16,
			17, None, 18, None, 19, 20, 21, 22, None, 23, 24, 25
		], 2),
	Macro('9edo', 9, 2, 1, [0, 1, None, 2, 3, 4, 5, None, 6, None, 7, 8], 2),
	Ombak('5edo+ombak', 0.0, +10.0, 5, 2, 1, [
			None, 0, None, 2, None, None, 4, None, 6, None, 8, None,
			None, 10, None, 12, None, None, 14, None, 16, None, 18, None,
			None, 1, None, 3, None, None, 5, None, 7, None, 9, None,
			None, 11, None, 13, None, None, 15, None, 17, None, 19, None
		], 2, concert_a_frequency=440.0*2**(1/5)),
	Macro('10edo', 10, 2, 1, [0, 1, 2, 3, None, 4, 5, 6, 7, 8, 9, None], 2),
	Default(),
	Octave('Pythagorean', pythagorean(), 3, unit='ratios'),
	Micro('14edo', 14, 2, 1, [0, 1, 2, 3, (4,5), 6, 7, 8, 9, 10, 11, (12,13)], 3),
	Micro('9ed3/2', 9, 3, 2, [
			0, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 14,
			16, 17, 18, 19, 21, 22, 23, 24, None, 25, None, 26
		], 3),
	Micro('17edo', 17, 2, 1, [0, (1,2), 3, 4, (5,6), 7, (8,9), 10, (11,12), 13, 14, (15,16)], 4),
	Ombak('9edo-ombak', -10.0, 0.0, 9, 2, 1, [
			0, 2, None, 4, 6, 8, 10, None, 12, None, 14, 16,
			18, 20, None, 22, 24, 26, 28, None, 30, None, 32, 34,
			1, 3, None, 5, 7, 9, 11, None, 13, None, 15, 17,
			19, 21, None, 23, 25, 27, 29, None, 31, None, 33, 35
		], 4),
	Micro('19edo', 19, 2, 1, [0, (2,1), 3, (5,4), (6,7), 8, (10,9), 11, (13,12), 14, (16,15), (17,18)], 5),
	Subset('48edo', 48, 2, 1, {0, 3, 4, 8, 12, 13, 15, 16, 20, 24, 23, 28, 31, 32, 36, 40, 41, 43, 44}, [0, (4,3), 8, (12,13), (15,16), 20, (24,23), 28, (32,31), 36, (40,41), (43,44)], 4),
	Micro('8ed4/3'), 8, 4, 3, [
			0, 2, 3, 5, 6, 8, 10, 11, 13, 15, 16, 18),
			19, 21, 22, 24, 26, 27, 29, 31, 32, 34, 37, 39)
		], 5),
	Micro('22edo', 22, 2, 1, [0, (2,1), (4,3), (5,6), (7,8), 9, (11,10), (13,12), (15,14), (17,16), (18,19), (20,21)], 5),
	Subset('53edo', 53, 2, 1, {0, 4, 5, 8, 9, 13, 14, 17, 18, 22, 26, 27, 30, 31, 35, 36, 39, 40, 44, 45, 48, 49}, [0, (4,5), (9,8), (13,14), (17,18), 22, (26,27), (31,30), (35,36), (40,39), (44,45), (48,49)], 5),
	Micro('24edo', 24, 2, 1, [(0,-1), (2,1), (4,3), (6,5), (7,8), (10,9), (12,11), (14,13), (16,15), (18,17), (20,19), (21,22)], 6),
	Micro('29edo', 29, 2, 1, [0, (2,3), 5, (7,8), (9,10), 12, (14,15), 17, (19,20), 22, (24,25), (26,27)], 7),
	Micro('31edo', 31, 2, 1, [0, (3,2), (5,6), (8,7), (10,9), 13, (16,15), (18,19), (21,20), (23, 24), (26,25), (28,27)], 8),
	Micro('34edo', 34, 2, 1, [0, (2,3), 6, (8,9), (10,11), (14,12), (17,16), (20,19), (23,22), (25,26), (27,28), (29,30), (32,31)], 8),
	Micro('36edo', 36, 2, 1, [(0,-1), (3,2), (6,5), (9,8), (11,12), (15,14), (18,17), (21,20), (24,23), (27,26), (30,29), (32,33)], 9),
	Arbitrary('Harmonic Series', range(1,129), 3, unit='ratios'),
	]
			
default_tuning_pgm = 7
			
layouts = [
	exquis,
	harmonic_table,
	wicki_hayden,
	janko,
	]
	
default_layout_pgm = 0


class Init:
	
	equave = 0
	is_left_right = False
	is_up_down = False
	transposition = 69
	transposition_range = range(69,128)
	
init = Init()
	
	
