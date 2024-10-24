"""
    row 0: names
    row 1: number of banks
    row 2: number of programs per bank

    programs and bankks are numbered 0,1,2,...
"""


inputs = [ # maybe add all of this as future work?
	'exquis',
	'reface_cp',
	#'line_in', # future work
	#'keystep', # future work
    #'xd', # future work
]

wrappers = [
    ['pianoteq', 'tuneBfree', 'surgeXT'],
    [4, 3, 6],
    [(6,4,6,2), (6,6,6), (4,4,4)],
]

drivers = [
    ['reface_cp'],
    [1],
    [6],
]
