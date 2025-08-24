import mido
from colour import Color

manufacturer_id = [0x00, 0x21, 0x7E]


class Exquis2_1_0:
    """Exquis firmware 2.1.0.
    I Haven't tested it.
    I realised that although the slider can be controlled,
    only 12 note scales can be set,
    whereas in the older version (1.2.0),
    the entire 61 note range can be set."""

    prefix = [*manufacturer_id, 0x7F]

    setup_developer_mode = 0x00

    # Below requires develoment mode to be active
    scale_list = 0x01
    color_palette = 0x02
    refresh = 0x03
    led_color = 0x04
    tempo = 0x05
    root_note = 0x06
    scale_number = 0x07
    custom_scale = 0x08
    snapshot = 0x09

    # Below can be added to setup developer mode
    pad_mode = 0x01
    encoder_mode = 0x02
    slider_mode = 0x04
    up_down_mode = 0x08
    settings_sound_mode = 0x10
    misc_mode = 0x20
    all_mode = (
        pad_mode
        + encoder_mode
        + slider_mode
        + up_down_mode
        + settings_sound_mode
        + misc_mode
    )

    # LED/control IDs
    pad = [i for i in range(0, 61)]
    slider = [i for i in range(80, 86)]  # same name
    slider_on = 90  # ??
    slider_off = 127  # ??
    settings = 100
    sound = 101
    record = 102
    loop = 103
    clips = 104
    play = 105
    down = 106
    up = 107
    left = 108
    right = 109
    encoder_knob = [i for i in range(110, 114)]
    encoder_button = [i for i in range(114, 118)]

    # LED FX
    led_fx = [None] * 7
    led_fx[0] = no_fx = 0x00
    led_fx[1] = pulse2black = 0x3F  # synced to tempo
    led_fx[2] = pulse2white = 0x7F  # same
    led_fx[3] = pulse2red = 0x3E
    led_fx[4] = pulse2green = 0x7E
    led_fx[5] = alpha_channel = lambda x: round(0x3D * x)
    led_fx[6] = blend2white = lambda x: 0x40 + round((0x70 - 0x40) * x)

    def developer_mode(
        self,
        action,
        pads=True,
        encoders=True,
        slider=True,
        up=True,
        down=True,
        settings=True,
        sound=True,
        misc=True,
    ):
        """Enter or exit developer mode."""
        assert action in ["enter", "exit"]
        mode = 0
        if action == "enter":
            if pads:
                mode += self.pad_mode
            if encoders:
                mode += self.encoder_mode
            if slider:
                mode += self.slider_mode
            if up or down:
                mode += self.up_down_mode
            if settings or sound:
                mode += self.settings_sound_mode
            if misc:
                mode += self.misc_mode
        data = [*self.prefix, self.setup_developer_mode, mode]
        msg = mido.Message("sysex", data=data)
        return msg

    def use_scales(self, number):
        """Specify the number of scales to be selectable in the setting menu."""
        if number in range(0, 256):
            data = [*self.prefix, self.scale_list, number // 128, number % 128]
        else:
            data = [*self.prefix, self.scale_list]
        msg = mido.Message("sysex", data=data)
        return msg

    def get_color_palette(self, msg=None, index=None):
        """Request the entire color palette or a specific index. Analyse response.
        The color palette is used for setting colors with midi cc messages."""
        assert index in range(0, 128)
        data = [*self.prefix, self.color_palette]
        prefix_len = len(data)
        if msg is None:
            if index is None:
                return mido.Message("sysex", data=data)
            else:
                data.append(index)
                return mido.Message("sysex", data=data)
        elif msg.type == "sysex" and msg.data[:prefix_len] == data:
            entire_palette = len(msg.data) == prefix_len + 128 * 3
            single_color = len(msg.data) == prefix_len + 3
            if entire_palette:
                palette = [] * 128
                for n, i in enumerate(range(prefix_len, prefix_len + 3 * 128, 3)):
                    color = Color()
                    color.rgb = [j / 128.0 for j in msg.data[i : i + 3]]
                    palette[n] = color
            elif single_color:
                palette = Color()
                palette.rgb = [j / 128.0 for j in msg.data[prefix_len:]]
            else:
                return None
            return palette
        else:
            return None

    def set_color_palette(self, colors, start_index=0):
        """Set the color palette by supplying a list of colors.
        The inital index is assumed to be 0 unless specified otherwise.The color palette is used for setting colors with midi cc messages."""
        assert start_index in range(0, 128)
        assert len(colors) <= 128 - start_index
        data = [*self.prefix, self.color_palette, start_index]
        for color in colors:
            if type(color) is tuple:
                r, g, b = color
            elif type(color) is Color:
                r, g, b = color.rgb
            data.append(round(r * 127))
            data.append(round(g * 127))
            data.append(round(b * 127))
        return mido.Message("sysex", data=data)

    def get_refresh(self, msg=None):
        """Request a refresh of LEDs.
        Receive a request with infomration whether the settings menu was just entered or what page of the settings menu has been left."""
        data = [*self.prefix, self.refresh]
        if msg is None:
            return mido.Message("sysex", data=data)
        elif msg.type == "sysex" and msg.data[: len(data)] == data:
            settings_page = msg.data[len(data)]
            if settings_page == 0x7F:
                return "enter"
            return settings_page
        else:
            return None

    def set_led_colors(self, colors, fx=None, start_index=0):
        assert start_index in range(0, 128)
        assert len(colors) <= 128 - start_index
        if fx is None:
            fx = [self.no_fx] * len(colors)
        assert len(colors) == len(fx)
        data = [*self.prefix, self.led_color, start_index]
        for color, fx in zip(colors, fx):
            if type(color) is tuple:
                r, g, b = color
            elif type(color) is Color:
                r, g, b = color.rgb
            data.append(round(r * 127))
            data.append(round(g * 127))
            data.append(round(b * 127))
            data.append(fx)
        return mido.Message("sysex", data=data)

    def get_tempo(self, msg=None):
        data = [*self.prefix, self.tempo]
        if msg is None:
            return mido.Message("sysex", data=data)
        elif msg.type == "sysex" and msg.data[: len(data)] == tuple(data):
            msb = msg.data[len(data)]
            lsb = msg.data[len(data) + 1]
            bpm = msb * 128 + lsb
            return bpm
        else:
            return None

    def set_tempo(self, bpm):
        if bpm < 20:
            bpm = 20
        elif bpm > 240:
            bpm = 240
        else:
            bpm = round(bpm)
        msb = bpm // 128
        lsb = bpm % 128
        data = [*self.prefix, self.tempo, msb, lsb]
        return mido.Message("sysex", data=data)

    def get_root_note(self, msg=None):
        """C=0, C#=1, ..., B=11"""
        data = [*self.prefix, self.root_note]
        if msg is None:
            return mido.Message("sysex", data=data)
        elif msg.type == "sysex" and msg.data[: len(data)] == data:
            root_note = msg.data[len(data)]
            return root_note
        else:
            return None

    def set_root_note(self, note):
        """C=0, C#=1, ..., B=11"""
        assert note in range(0, 12)
        data = [*self.prefix, self.root_note, note]
        return mido.Message("sysex", data=data)

    def get_scale_number(self, msg=None):
        """Sent by Exquis every time a scale is changed in the settings menu."""
        data = [*self.prefix, self.scale_number]
        if msg is None:
            return mido.Message("sysex", data=data)
        elif msg.type == "sysex" and msg.data[: len(data)] == data:
            scale_number = msg.data[len(data)]
            return scale_number
        else:
            return None

    def set_scale_number(self, number):
        assert number in range(0, 128)
        data = [*self.prefix, self.scale_number, number]
        return mido.Message("sysex", data=data)

    def get_custom_scale(self, msg=None):
        """Only 12 degrees"""
        data = [*self.prefix, self.custom_scale]
        if msg is None:
            return mido.Message("sysex", data=data)
        elif msg.type == "sysex" and msg.data[: len(data)] == data:
            scale = msg.data[len(data) :]
            return scale
        else:
            return None

    def set_custom_scale(self, scale):
        """Only 12 degrees"""
        assert len(scale) == 12
        data = [*self.prefix, self.custom_scale, *scale]
        return mido.Message("sysex", data=data)

    def get_snapshot(self, msg=None):
        """Get a snapshot of all the settings."""
        data = [*self.prefix, self.snapshot]
        if msg is None:
            return mido.Message("sysex", data=data)
        elif msg.type == "sysex" and msg.data[: len(data)] == data:
            snapshot = msg.data[len(data) :]
            return snapshot
        else:
            return None

    def set_snapshot(self, snapshot):
        """Set a snapshot of all the settings."""
        data = [*self.prefix, self.snapshot, *snapshot]
        return mido.Message("sysex", data=data)

    def is_pressed(self, msg, button):
        if msg.is_cc(button):
            if msg.channel == 15:
                if msg.value == 127:
                    return True
        return False

    def is_released(self, msg, button):
        if msg.is_cc(button):
            if msg.channel == 15:
                if msg.value == 0:
                    return True
        return False


exquis2_1_0 = Exquis2_1_0()
