import mido


class MinilogueXD:
    # cc
    CVin1_control = 118
    CVin2_control = 119

    # values
    CVin1_value = 64
    CVin2_value = 64

    def CVin1(self, msg=None, bimodal=True, value=64, channel=0):
        """Bimodal means that 64 is the middle value."""
        if msg is None:
            self.CVin1_value = value
            if not bimodal:
                value = value // 2 + 64
            return mido.Message(
                "control_change",
                control=self.CVin1_control,
                value=value,
                channel=channel,
            )
        else:
            if msg.is_cc(self.CVin1_control):
                self.CVin1_value = msg.value
                if bimodal:
                    return self.CVin1_value
                else:
                    return 2 * self.CVin1_value - 127
            return None

    def CVin2(self, msg=None, bimodal=True, value=64, channel=0):
        """Bimodal means that 64 is the middle value."""
        if msg is None:
            self.CVin2_value = value
            if not bimodal:
                value = value // 2 + 64
            return mido.Message(
                "control_change",
                control=self.CVin2_control,
                value=value,
                channel=channel,
            )
        else:
            if msg.is_cc(self.CVin2_control):
                self.CVin2_value = msg.value
                if bimodal:
                    return self.CVin2_value
                else:
                    return 2 * self.CVin2_value - 127
            return None


minilogue_xd = MinilogueXD()
