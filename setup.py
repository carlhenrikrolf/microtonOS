from setuptools import setup, find_packages

setup(
        name='microtonOS',
        version='1.0',
        description='making a xenharmonic synth from a Raspberry Pi',
        packages=[*find_packages(where='src'),
		'midi_implementation',
		'modulation',
        'utils'],
        package_dir={"" : "src",
		"midi_implementation" : "lib/midi_implementation",
		"modulation" : "lib/modulation",
        "utils": "lib/utils"},
    )
