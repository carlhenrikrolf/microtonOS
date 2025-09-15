import numpy as np


class Standard:
    def lower(self, config):
        root_note = config["root"]["note"]
        root_hertz = config["root"]["Hertz"]
        frequency = np.full(shape=128, fill_value=root_hertz)
        for i in range(128):
            frequency[i] *= 2 ** ((i - root_note) / 12)
        return frequency

    def upper(self, config):
        frequency = self.lower(config)
        return frequency


standard = Standard()

test = {
    "name": "test",
    "root": {"note": 69, "Hertz": 440.0},
    "cents": 78.00,
    "Halberstadt": [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14],
}  # to be removed later


class EqualTempered:
    def lower(self, config):
        root_note = config["root"]["note"]
        root_hertz = config["root"]["Hertz"]
        cents = config["cents"]
        halberstadt = config["Halberstadt"]
        mapping = np.array(halberstadt, dtype=int)
        for _ in range(10):  # slightly overshoots 128
            tmp = mapping[-1] + np.array(halberstadt[1:])
            mapping = np.concatenate([mapping, tmp])
        mapping -= mapping[root_note]
        frequency = np.full(shape=128, fill_value=root_hertz)
        for i in range(128):
            frequency[i] *= 2 ** (mapping[i] * cents / 1200.0)
        return frequency

    def upper(self, config):
        cents = config["cents"]
        frequency = self.lower(config)
        frequency *= 2 ** (cents / 1200.0)
        return frequency


equal_tempered = EqualTempered()
