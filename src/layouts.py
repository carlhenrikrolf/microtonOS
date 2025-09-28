import numpy as np
from midi_implementation.midi1 import percussion as perc
from midi_implementation.intuitive_instruments import exquis2_1_0 as xq
from utils import load_config

config = {"general_settings": load_config(__file__, "../config/general_settings.toml")}
red = np.array(config["general_settings"]["palette"]["red"])
magenta = np.array(config["general_settings"]["palette"]["magenta"])


class TwelveTone:
    pass


class EqualTempered:
    pass


class Isomorphic:
    def __init__(self):
        pass

    def reinitialize(self):
        pass

    def kind(self, id=None):
        pass

    def dilation(self, id=None):
        pass

    def manual(self, id=None):
        pass

    def root(self, id=None):
        pass

    def flip(self, lr, ud):
        pass

    def translate(self, steps):
        pass


class Drums:
    def __init__(self, high, low, device, ghostnote=127, color0=red, color1=magenta):
        self.device = device
        high_inner, high_outer = self.high_to_notes(high)
        low_inner, low_outer = self.low_to_notes(low)
        if self.device == "Exquis":
            notes = self.exquis(
                high_inner, high_outer, low_inner, low_inner, low_outer, ghostnote
            )
            self.notes = xq.linearize(notes)
            black = np.array([0.0, 0.0, 0.0])
            colors = self.exquis(black, color0, black, color1, color0, black)
            self.colors = xq.linearize(colors)
        else:
            raise ValueError("Not (yet) implemented for this device")

    def high_to_notes(self, high):
        match high:
            case "drumkit":
                return [perc.acoustic_snare, perc.side_stick]
            case "toms":
                return [perc.high_tom] * 2
            case "cymbals":
                return [perc.pedal_hihat] * 2
            case "bongó":
                return [perc.high_bongo] * 2
            case "congas":
                return [perc.open_high_conga, perc.mute_high_conga]
            case "timbales":
                return [perc.high_timbale] * 2
            case "agôgo":
                return [perc.high_agogo] * 2
            case "shakers":
                return [perc.maracas] * 2
            case "güiro":
                return [perc.short_guiro] * 2
            case "woodblock":
                return [perc.high_woodblock] * 2
            case "triangle":
                return [perc.mute_triangle] * 2
            case _:
                raise ValueError("Not a valid percussion name")

    def low_to_notes(self, low):
        match low:
            case "drumkit":
                return [perc.acoustic_bass_drum] * 2
            case "toms":
                return [perc.low_tom] * 2
            case "cymbals":
                return [perc.ride_bell, perc.ride_cymbal_1]
            case "bongó":
                return [perc.low_bongo] * 2
            case "congas":
                return [perc.low_conga] * 2
            case "timbales":
                return [perc.low_timbale] * 2
            case "agôgo":
                return [perc.low_agogo] * 2
            case "shakers":
                return [perc.cabasa] * 2
            case "güiro":
                return [perc.long_guiro] * 2
            case "woodblock":
                return [perc.low_woodblock] * 2
            case "triangle":
                return [perc.open_triangle] * 2
            case _:
                raise ValueError("Not a valid percussion name")

    def exquis(self, hi, ho, li, lb, lo, gn):
        result = [
            [gn, gn, gn, gn, gn, gn],
            [gn, ho, ho, gn, gn],
            [gn, ho, hi, ho, gn, gn],
            [gn, ho, ho, gn, gn],
            [gn, gn, gn, gn, gn, gn],
            [gn, gn, gn, gn, gn],
            [gn, gn, lo, lo, lo, gn],
            [gn, lo, lb, lb, lo],
            [gn, lo, lb, li, lb, lo],
            [gn, lo, lb, lb, lo],
            [gn, gn, lo, lo, lo, gn],
        ]
        return result

    def reinitialize(self, high, low, ghostnote=127):
        high_inner, high_outer = self.high_to_notes(high)
        low_inner, low_outer = self.low_to_notes(low)
        if self.device == "Exquis":
            notes = self.exquis(
                high_inner, high_outer, low_inner, low_inner, low_outer, ghostnote
            )
            self.notes = xq.linearize(notes)
        else:
            raise ValueError("Not (yet) implemented for this device")
