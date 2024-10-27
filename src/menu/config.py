"""
    col 0: name of engine. i.e. 'to <engine>'
    col 1: number of programs per bank

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
	['pianoteq', (6,4,6,2)],
	['tuneBfree', (6,6,6)],
	['surge_xt', (4,4,4)],
]

drivers = [
	['reface_cp', (0)],
]
