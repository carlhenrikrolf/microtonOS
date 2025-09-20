# external libraries
import numpy as np

# constants
middle_c = 60


def array(np_array):
    rounded = np_array  # .round(decimals=12)
    return rounded.tolist()


# Frozen classes for each tuning system
class TwelveTone:
    def __init__(self, config):
        self.root_note = config["root"]["note"]
        self.root_hertz = config["root"]["Hertz"]
        self.cents = config["cents"]
        assert len(self.cents) == 13

    def linear(self, octave=0):
        c2c = self.cents[-1] - self.cents[0]
        new_root_hertz = self.root_hertz * 2 ** (octave * c2c / 1200.0)
        overshot_cents = np.array(self.cents)
        for _ in range(10):
            tmp = overshot_cents[-1] + np.array(self.cents[1:])
            overshot_cents = np.concatenate([overshot_cents, tmp])
        overshot_cents -= overshot_cents[self.root_note]
        frequency = np.full(shape=128, fill_value=new_root_hertz)
        for i in range(128):
            frequency[i] *= 2 ** (overshot_cents[i] / 1200.0)
        return frequency

    def lower(self):
        frequency = self.linear()
        return frequency

    def upper(self):
        frequency = self.linear()
        return frequency


class EqualTempered:
    def __init__(self, config):
        self.root_note = config["root"]["note"]
        self.root_hertz = config["root"]["Hertz"]
        self.cents = config["cents"]
        self.halberstadt = config["Halberstadt"]
        assert len(self.halberstadt) == 13

    def linear(self, octave=0):
        c2c = self.cents * (self.halberstadt[-1] - self.halberstadt[0])
        new_root_hertz = self.root_hertz * 2 ** (octave * c2c / 1200.0)
        frequency = np.full(shape=128, fill_value=new_root_hertz)
        for i in range(128):
            frequency[i] *= 2 ** ((i - self.root_note) * self.cents / 1200.0)
        return frequency

    def lower(self):
        overshot_mapping = np.array(self.halberstadt, dtype=int)
        for _ in range(10):  # slightly overshoots 128
            tmp = overshot_mapping[-1] + np.array(self.halberstadt[1:])
            overshot_mapping = np.concatenate([overshot_mapping, tmp])
        overshot_mapping -= overshot_mapping[self.root_note]
        frequency = np.full(shape=128, fill_value=self.root_hertz)
        for i in range(128):
            frequency[i] *= 2 ** (overshot_mapping[i] * self.cents / 1200.0)
        return frequency

    def upper(self):
        frequency = self.lower()
        frequency *= 2 ** (self.cents / 1200.0)
        return frequency


class FineTuned:
    pass


class Macrotonal:
    pass


# Dynamic class for the tuning parameters
class Tuning:
    def __init__(self, bank_name, config):
        self.octave = 0
        self.bank_name = bank_name
        self.pgm_name = config["name"]
        if bank_name == "twelve-tone":
            self.system = TwelveTone(config)
        elif bank_name == "equal-tempered":
            self.system = EqualTempered(config)
        elif bank_name == "finetuned":
            self.system = FineTuned(config)
        elif bank_name == "macrotonal":
            self.system = Macrotonal(config)
        else:
            raise ValueError(
                'bank_name must be "twelve-tone", "equal-tempered", "finetuned", or "macrotonal"'
            )
        self.linear = array(self.system.linear())
        self.lower = array(self.system.lower())
        self.upper = array(self.system.upper())

    def switch_octave(self, octave):
        assert octave in [-2, -1, 0, 1, 2]
        self.octave = octave
        self.linear = array(self.system.linear(octave=octave))

    def toggle_keys(self, keys, manual):
        assert self.bank_name == "finetuned"
        assert all([type(key) is int for key in keys])
        if manual == "lower":
            self.lower = array(self.system.lower(keys=keys))
        elif manual == "upper":
            self.upper = array(self.system.lower(keys=keys))
        else:
            raise ValueError('manual must be "lower" or "upper"')

    def change_key(self, key, manual):
        assert self.bank_name == "macrotonal"
        assert key in range(12)
        if manual == "lower":
            self.lower = array(self.system.lower(key=key))
        elif manual == "upper":
            self.upper = array(self.system.lower(key=key))
        else:
            raise ValueError('manual must be "lower" or "upper"')

    def set_ombak(self, ombak, manual):
        assert self.bank_name == "macrotonal"
        assert hasattr(ombak, "__round__")
        if manual == "lower":
            self.lower = array(self.system.lower(ombak=ombak))
        elif manual == "upper":
            self.upper = array(self.system.lower(ombak=ombak))
        else:
            raise ValueError('manual must be "lower" or "upper"')


# Tests to be removed
test_std = {
    "name": "12edo (standard)",
    "root": {"note": 69, "Hertz": 440.0},
    "cents": [
        0.00,
        100.00,
        200.00,
        300.00,
        400.00,
        500.00,
        600.00,
        700.00,
        800.00,
        900.00,
        1000.00,
        1100.00,
        1200.00,
    ],
}

test_phi = {
    "name": "8edPhi",
    "root": {"note": 69, "Hertz": 440.0},
    "cents": [
        0.00,
        104.14,
        208.27,
        312.41,
        416.55,
        520.68,
        624.82,
        728.95,
        833.09,
        937.23,
        1041.36,
        1145.5,
        1249.64,
    ],
}

test_rev = {
    "name": "reverse",
    "root": {"note": 69, "Hertz": 440.0},
    "cents": [
        0.00,
        -100.00,
        -200.00,
        -300.00,
        -400.00,
        -500.00,
        -600.00,
        -700.00,
        -800.00,
        -900.00,
        -1000.00,
        -1100.00,
        -1200.00,
    ],
}

test_alpha = {
    "name": "test",
    "root": {"note": 69, "Hertz": 440.0},
    "cents": 78.00,
    "Halberstadt": [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14],
}
