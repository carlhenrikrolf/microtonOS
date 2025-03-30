from colour import Color
import numpy as np


# Lib
#####

tone_to_int = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]

is_white_key = [
    True,
    False,
    True,
    False,
    True,
    True,
    False,
    True,
    False,
    True,
    False,
    True,
]

ch = {"master": {0}}
ch["isomorphic"] = {*range(0, 12)}
ch["mpe"] = {*range(0, 13)}
ch["halberstadt"] = {12, 13}
ch["multituning"] = {13, 14}
ch["manual2"] = {14, 15}

def concat(terms, middle_note, note_range, cumulative):
    terms = np.array(terms) if len(np.array(terms).shape) == 1 else np.array([terms])
    span = max(note_range) - min(note_range) + 1
    middle = middle_note - min(note_range)
    arr = np.zeros(span)
    if cumulative:
        for i, note in enumerate(range(middle + 1, span)):
            arr[note] += terms[i % len(terms)]
            arr[note] += terms[-1] * (i // len(terms))
        for i, note in enumerate(range(middle, -1, -1), start=0):
            arr[note] += terms[(-i - 1) % len(terms)]
            arr[note] -= terms[-1] * ((i // len(terms)) + 1)
    else:
        for i, note in enumerate(range(middle + 1, span)):
            term = terms[i % len(terms)]
            arr[note] += arr[note - 1] + term
        for i, note in enumerate(range(middle - 1, -1, -1), start=1):
            term = terms[-i % len(terms)]
            arr[note] += arr[note + 1] - term
    return arr


def convert(steps, unit, root_note, root_frequency, middle_note, note_range, cumulative):
    result = np.array(steps)
    if unit == "ratios":
        result = 1200 * np.log2(result)
    result = concat(result, middle_note, note_range, cumulative)
    if unit == "Hertz":
        result -= result[root_note]
        result += root_frequency
    else:
        result = 2 ** (result / 1200)
        result /= result[root_note]
        result *= root_frequency
    return result


def ombakify(pengumbang, pengisep, half):
    pengumbang = 0.0 if pengumbang is None else float(pengumbang)
    pengisep = 0.0 if pengisep is None else float(pengisep)
    full = []
    for frequency in half:
        full.append(frequency - pengumbang)
        full.append(frequency + pengisep)
    full = np.array(full)
    return full


# Templates
###########


class Default:
    """
        With preset parameters, the Default class corresponds to 12edo. The paramters are defined as follows:
        - name: A string for identifying the tuning. Does not affect sound. For MTS, it needs to be ascii and at most 16 characters long. Anything else will be ignored.
        - steps: A floating point number corresponding to the step size. Can also be set to a list of floating point numbers for steps of uneven sizes. After the last step the first step is repeated.
        - unit: "ratios", "cents", or "Hertz". Specifies the unit of the step size(s).
        - cumulative: Only relevant if step sizes are unequal. True by default, which means that step sizes relate to the last pitch. If set to False, step sizes relate to the initial item of the list of steps.
        - root_note: A MIDI note number. If steps are of uneven sizes, this is the midi note number from which the counting is started. 69 by default, i.e. concert A = A above middle C.
        - root_frequency: Frequency of the root note in Hertz. 440.0 Hz by default.
        - pengumbang: Only applicable to the Ombak child class. Each note is duplicated and pengumbang is the number of Hertz by which even MIDI notes are lowered.
        - pengisep: Only applicable to the Ombak child class. Each note is duplicated and pengisep is the number of Hertz by which odd MIDI notes are raised.
        - halberstadt: The mapping between keys in the Halberstadt layout and steps. [0,1,...,11,12] by default. The last key is the first key of the next repetition, so if there are 13 items, the repetitions coincide with the 7+5 keys repetitions of the Halberstadt layout.
            - If an entry is None, the corresponding keys are muted.
            - If an entry is a tuple, e.g. (a,b,c), the default mapping is a. Pressing the footswitch changes it to b and releasing it changes it back to a. Pressing the corresponding keyswitch changes it to b, pressing again to c, and pressing one more time back to a.
        - boundary_tone: "c", "c#", ..., "a#", or "b". Corresponds to the first element in halberstadt. "c" by default.
        - stretch: None by default. Changing the octave in the tuning function shifts the frequency by the amount corresponding to one period of the halberstadt mapping. If a floating point number is specified it represents the stretch in cents while changing the octave. 0 means pure octaves. Negative numbers means compressed octaves. Counted from the root note.
        - dilation: suggested dilation for isomorphic layouts. preferably set to an approximation of 1 whole + 1 half tone (minor third). Does not affect the sound.
    """
    white_keys = "red"
    black_keys = "black"

    non_keys = "white"

    def __init__(
        self,
        name="12edo",
        steps=2 ** (1 / 12),
        unit="ratios",
        cumulative=True,
        root_note=69,
        root_frequency=440.0,
        pengumbang=None,
        pengisep=None,
        halberstadt=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        boundary_tone="c",
        stretch=None,
        dilation=3,
        **kwargs,
    ):
        self.name = name if type(name) is str else "Unnamed"
        self.steps = steps
        assert unit in ["ratios", "cents", "Hertz"]
        self.unit = unit
        self.cumulative = cumulative
        self.root_note = root_note
        self.root_frequency = root_frequency
        self.pengumbang = pengumbang
        self.pengisep = pengisep
        self.halberstadt = halberstadt
        self.boundary_tone = boundary_tone
        self.stretch = stretch
        self.dilation = dilation

        self.octave = 0
        self.keys_per_octave = len(self.halberstadt) - 1
        self.switches = [0] * self.keys_per_octave
        self.is_switch = [
            True if hasattr(degree, "__len__") else False for degree in self.halberstadt
        ]
        self.init_halberstadt = [
            degree[0] if self.is_switch[i] else degree
            for i, degree in enumerate(self.halberstadt)
        ]
        self.degrees_per_octave = self.init_halberstadt[-1] - self.init_halberstadt[0]
        self.middle_key = 60 + tone_to_int.index(self.boundary_tone)
        self.root_degree = self.init_halberstadt[self.root_note - self.middle_key]
        self.middle_note = self.root_note - self.root_degree
        self.pedal = None
        self.is_ignored = [False] * 128
        self.backup = [[set() for _ in range(16)] for _ in range(128)]
        self.is_micro = max(self.halberstadt) - min(self.halberstadt) > 12
        self.is_macro = max(self.halberstadt) - min(self.halberstadt) < 12

    def remap(self, note):
        pass

    def get_colors(self):
        pass

    def get_frequencies(self):
        pass

    def tuning(self, mts, equave=None):
        pass

    def ignore(self, note_msg):
        pass

    def thru(self, old_msg, outport, msg, highlight=None):
        pass

    def halberstadtify(self, outport, msg, manual=None, highlight=None):
        pass

    def manual2(self):
        pass

    def reset(self):
        pass

    def keyswitches(self, outport, msg, manual=1, highlight=None):
        pass

    def footswitch(self, msg):
        pass


class EDO(Default):
    white_keys = "red"
    black_keys = "darkorange"

    def halberstadtify():
        pass

    def manual2(self):
        pass

    def keyswitches(self):
        pass

    def footswitch(self):
        pass


class Octaveless(EDO):
    white_keys = "red"
    black_keys = "magenta"


class EqualHertz(EDO):
    white_keys = "blue"
    black_keys = "magenta"


class Ombak(Default):
    white_keys = "blue"
    black_keys = "green"

    def get_frequencies(self):
        floor = int(self.root_note / 2)
        if self.stretch is None:
            root_note = self.root_note - self.octave * self.degrees_per_octave
            root_note -= floor
            result = convert(self.steps, self.unit, root_note, self.root_frequency, 2 * floor, range(floor, floor + 64), self.cumulative)
        else: # test this statement
            base = 2 ** ((1200 + self.stretch) / 1200)
            root_frequency = self.root_frequency * base ** self.octave
            result = convert(self.steps, self.unit, self.root_note, root_frequency, 2 * floor, range(floor, floor + 64, self.cumulative))
        result = ombakify(self.pengumbang, self.pengisep, result)
        for i, frequency in enumerate(result):
            if frequency <= 0:
                result[i] = 440.0
                self.is_ignored[i] = True
            else:
                self.is_ignored[i] = False
        return result.tolist()
    
    def halberstadtify(self, outport, msg, highlight=None):
        if hasattr(msg, "note"):
            isomorphic_note = self.remap(msg.note)
            if not self.ignore(isomorphic_note):
                channel = ch["halberstadt"].difference(ch["multituning"])
                # additionally, add other kind of channel
                note_msg = msg.copy(note=isomorphic_note, channel=int(*channel))
                self.thru(msg, outport, note_msg, highlight=highlight)
                if self.pedal is True:
                    note_msg2 = msg.copy(note=isomorphic_note - 1)
                    self.thru(msg, outport, note_msg2, highlight=highlight)
        else:
            outport.send(msg)
    
    def manual2ify(self, outport, msg, highlight=None):
        if hasattr(msg, "note"):
            isomorphic_note = ...
        else:
            outport.send(msg)

    def footswitch(self):
        pass


class Uneven(EDO):
    white_keys = "yellow"
    black_keys = "green"

    def get_colors(self):
        pass

    def manual2(self):
        pass
