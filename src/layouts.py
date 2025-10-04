import numpy as np
from midi_implementation.midi1 import percussion as perc
from midi_implementation.intuitive_instruments import exquis2_1_0 as xq

red = np.array([1, 0, 0])
magenta = np.array([1, 0, 1])


def hexagonal(
    height,
    width,
    up,
    right,
    bottom_crop=False,
    top_right=69,
    bottom_right=None,
    bottom_left=None,
    top_left=None,
):
    layout = np.zeros([height, width], int)
    for row in range(height):
        for col in range(width):
            term = right * ((height - row + int(bottom_crop)) // 2)
            layout[row, col] = up * (height - row) + term + right * col
    if top_left is not None:
        diff = top_left - layout[0, 0]
    elif bottom_left is not None:
        diff = bottom_left - layout[-1, 0]
    elif bottom_right is not None:
        diff = bottom_right - layout[-1, -1]
    else:
        diff = top_right - layout[0, -1]
    layout += diff
    return layout


def rectangular(
    height,
    width,
    up,
    right,
    bottom_crop=None,
    top_right=69,
    bottom_right=None,
    bottom_left=None,
    top_left=None,
):
    layout = np.zeros([height, width], int)
    for row in range(height):
        for col in range(width):
            layout[row, col] = up * (height - row) + right * col
    if top_left is not None:
        diff = top_left - layout[0, 0]
    elif bottom_left is not None:
        diff = bottom_left - layout[-1, 0]
    elif bottom_right is not None:
        diff = bottom_right - layout[-1, -1]
    else:
        diff = top_right - layout[0, -1]
    layout += diff
    return layout


def dash(height, width):
    """
    Used for splitting the layout lengthwise.
    Produces a list of coordinates forming a straight line.
    """
    separator = []
    for col in range(width):
        separator.append((round(height / 2) - 1, col))
    return separator


def backslash(height, width):
    separator = []
    separator.append((round(height / 2) - 1, round(width / 2)))
    while True:
        x = separator[-1][1]  # up
        y = separator[-1][0] - 1
        if y not in range(height):
            break
        separator.append((y, x))
        x = separator[-1][1] + 1  # right
        if x not in range(width):
            break
        separator.append((y, x))
        x = separator[-1][1] + 1  # right
        if x not in range(width):
            break
        separator.append((y, x))
        x = separator[-1][1] + 1  # up right
        y = separator[-1][0] - 1
        if x not in range(width) or y not in range(height):
            break
        separator.append((y, x))
    while True:
        x = separator[0][1] - 1  # down left
        y = separator[0][0] + 1
        if x not in range(width) or y not in range(height):
            break
        separator.insert(0, (y, x))
        x = separator[0][1] - 1  # left
        if x not in range(width):
            break
        separator.insert(0, (y, x))
        x = separator[0][1] - 1  # left
        if x not in range(width):
            break
        separator.insert(0, (y, x))
        y = separator[0][0] + 1
        if x not in range(width):
            break
        separator.insert(0, (y, x))
    flipped_separator = [(y, width - 1 - x) for (y, x) in separator]
    return flipped_separator


def slash(height, width):
    separator = backslash(height, width)
    mid = round(height / 2) - 1
    n = len(separator)
    inverted = []
    for i in range(n):
        x = separator[i][1]
        y = mid + (mid - separator[i][0])
        inverted.append((y, x))
    return inverted


def endpoints(separator):  # potential add-on. add overlaps
    xmin = min([i[1] for i in separator])
    xmax = max([i[1] for i in separator])
    ymax = max([i[0] for i in separator])
    ymin = min([i[0] for i in separator])
    lefts = []
    rights = []
    for i in separator:
        if i[1] == xmin:
            lefts.append(i)
        if i[1] == xmax:
            rights.append(i)
    left = lefts[0]
    for i in lefts:
        if min(abs(i[0] - ymax), abs(i[0] - ymin)) > min(
            abs(left[0] - ymax), abs(left[0] - ymin)
        ):
            left = i
    right = rights[0]
    for i in rights:
        if min(abs(i[0] - ymax), abs(i[0] - ymin)) > min(
            abs(right[0] - ymax), abs(right[0] - ymin)
        ):
            right = i
    return left, right


def split(height, width, up, right, grid, separation, kind, top_right=69, overlap=1):
    """
    Used to create a split layout.
    grid is either rectangular or square from above
    The separator can be a dash, a slash, or a backslash.
    The kind is either 'parallel', meaning that
    going past the left side on the lower takes you to right side of the higher.
    Or, the kind is 'sequential', meaning that
    going up the upper right corner on lower takes you to the lower left corner on higher.
    """
    layout = grid(height, width, up, right, top_right=top_right)
    separator = separation(height, width)
    left_end, right_end = endpoints(separator)
    if kind == "parallel":
        bottom_height = height - right_end[0] - 1
        bottom = grid(bottom_height, width, up, right, top_right=layout[0, 0 + overlap])
    elif kind == "sequential":
        bottom_height = height - right_end[0]
        bottom = grid(
            bottom_height,
            width,
            up,
            right,
            top_right=layout[left_end[0], left_end[1] + overlap],
        )
    else:
        raise Warning(
            "kind must be either 'parallel' or 'sequential'. (If both, 'parallel takes precedence.)"
        )
    mid_height = height - bottom_height + 1
    overlap_crop = False if bottom_height % 2 > 0 else True
    mid = grid(
        mid_height,
        width,
        up,
        right,
        bottom_crop=overlap_crop,
        bottom_right=bottom[0, -1],
    )
    lower = np.concatenate([mid[:-1, :], bottom])
    for y, x in separator:
        for i in range(y + 1, height):
            layout[i, x] = lower[i, x]
    for i in separator:
        layout[i] = -1
    return layout


def clean(layout):
    clean_layout = layout.tolist()
    for i, row in enumerate(clean_layout):
        for j, note in enumerate(row):
            if note not in range(0, 128):
                clean_layout[i][j] = -1
    return clean_layout


def crop(layout):
    n = len(layout)
    for i, row in enumerate(layout):
        if (n - i) % 2 == 0:
            row.pop(-1)
    return layout


class Exquis:
    def __init__(self):
        pass

    def translate(self):
        pass

    def flip(self):
        pass

    def dilate(self):
        pass


class HarmonicTable:
    pass


def f3(d):
    if d % 3 > 0:
        out = round(d / 3)
    else:
        out = 0
        for i in range(1, int(d / 3) + 1):
            if i > out and i % 2 > 0:
                out = i
    return out


class WickiHayden:
    pass


class Janko:
    pass


class Isomorphic:
    def __init__(self):
        pass

    def reinitialize(self):
        pass

    def kind(self, id=None):
        pass

    def dilate(self, id=None):
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
