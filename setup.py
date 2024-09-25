from setuptools import setup, find_packages

setup(
        name='microtonOS',
        version='1.0',
        description='making a xenharmonic synth from a Raspberry Pi',
        packages=[*find_packages(where='src'), 'midi_implementation'],
        package_dir={"" : "src", "midi_implementation" : "midi_implementation"}, 
    )
